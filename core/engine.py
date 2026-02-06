"""
Core Engine - Business Logic Layer
"""

import os
import hashlib
from typing import List, Dict, Optional
from datetime import datetime


class DocFlowEngine:
    """Core business logic engine for DocFlow Pro"""
    
    def __init__(self, db_manager, license_manager, feature_gates):
        """Initialize engine with dependencies"""
        self.db = db_manager
        self.license = license_manager
        self.features = feature_gates
        self.current_user_id = None
    
    def set_current_user(self, user_id: int):
        """Set the current logged-in user"""
        self.current_user_id = user_id
    
    # ==================== USER OPERATIONS ====================
    
    def register_user(self, username: str, password: str, email: str = "", full_name: str = "") -> tuple:
        """Register a new user (single user system)"""
        # Check if user already exists
        if self.db.get_user_count() > 0:
            return False, "User already exists. This is a single-user system."
        
        # Hash password
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        # Create user
        user_id = self.db.create_user(username, password_hash, email, full_name)
        
        if user_id > 0:
            return True, user_id
        else:
            return False, "Failed to create user"
    
    def login_user(self, username: str, password: str) -> tuple:
        """Login user and return user_id"""
        user = self.db.get_user_by_username(username)
        
        if not user:
            return False, "User not found"
        
        # Verify password
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        if user['password_hash'] != password_hash:
            return False, "Invalid password"
        
        # Update last login
        self.db.update_last_login(user['id'])
        self.current_user_id = user['id']
        
        return True, user['id']
    
    def get_or_create_default_user(self) -> int:
        """Get existing user or create default admin user"""
        cursor = self.db.connection.cursor()
        cursor.execute("SELECT id FROM users LIMIT 1")
        user = cursor.fetchone()
        
        if user:
            return user[0]
        else:
            # No user exists - this should not happen in production
            # Application should be initialized with secure password
            import hashlib
            import secrets
            import string
            alphabet = string.ascii_letters + string.digits + "!@#$%^"
            random_pwd = ''.join(secrets.choice(alphabet) for _ in range(16))
            password_hash = hashlib.sha256(random_pwd.encode()).hexdigest()
            user_id = self.db.create_user("admin", password_hash, "admin@docflow.com", "Administrator")
            return user_id
    
    # ==================== DOCUMENT OPERATIONS ====================
    
    def create_document(self, title: str, file_path: str = "", **kwargs) -> tuple:
        """Create a new document"""
        if not self.current_user_id:
            return False, "No user logged in"
        
        # Check document limit
        plan_type = self.license.get_user_plan(self.current_user_id)
        current_count = self.db.get_user_document_count(self.current_user_id)
        
        if not self.features.check_document_limit(plan_type, current_count):
            max_docs = self.features.get_limit(plan_type, 'max_documents')
            return False, f"Document limit reached ({max_docs}). Please upgrade your plan."
        
        # Get file info if provided
        file_size = 0
        file_type = ""
        if file_path and os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            file_type = os.path.splitext(file_path)[1]
        
        doc_id = self.db.create_document(
            self.current_user_id, title, 
            file_path=file_path, 
            file_size=file_size, 
            file_type=file_type,
            **kwargs
        )
        
        return True, doc_id
    
    def get_my_documents(self, limit: int = None) -> List[Dict]:
        """Get current user's documents"""
        if not self.current_user_id:
            return []
        return self.db.get_user_documents(self.current_user_id, limit)
    
    def search_my_documents(self, query: str) -> List[Dict]:
        """Search current user's documents"""
        if not self.current_user_id:
            return []
        return self.db.search_documents(self.current_user_id, query)
    
    def update_document(self, doc_id: int, **kwargs) -> bool:
        """Update a document"""
        if not self.current_user_id:
            return False
        return self.db.update_document(doc_id, self.current_user_id, **kwargs)
    
    def delete_document(self, doc_id: int) -> bool:
        """Delete a document"""
        if not self.current_user_id:
            return False
        return self.db.delete_document(doc_id, self.current_user_id)
    
    # ==================== INVOICE OPERATIONS ====================
    
    def create_invoice(self, invoice_number: str, client_name: str, 
                      invoice_date: str, items: List[Dict], **kwargs) -> tuple:
        """Create a new invoice"""
        if not self.current_user_id:
            return False, "No user logged in"
        
        # Check invoice limit
        plan_type = self.license.get_user_plan(self.current_user_id)
        current_count = self.db.get_user_invoice_count(self.current_user_id)
        
        if not self.features.check_invoice_limit(plan_type, current_count):
            max_invoices = self.features.get_limit(plan_type, 'max_invoices')
            return False, f"Invoice limit reached ({max_invoices}). Please upgrade your plan."
        
        invoice_id = self.db.create_invoice(
            self.current_user_id, invoice_number, client_name, 
            invoice_date, items, **kwargs
        )
        
        return True, invoice_id
    
    def get_my_invoices(self, limit: int = None) -> List[Dict]:
        """Get current user's invoices"""
        if not self.current_user_id:
            return []
        return self.db.get_user_invoices(self.current_user_id, limit)
    
    def get_invoice_by_id(self, invoice_id: int) -> Optional[Dict]:
        """Get single invoice by ID for the current user"""
        if not self.current_user_id:
            return None
        try:
            # Fetch all invoices for the current user and then filter
            # This might be inefficient for many invoices, but ensures user ownership check
            invoices = self.db.get_user_invoices(self.current_user_id)
            for inv in invoices:
                if inv.get('id') == invoice_id:
                    return inv
            return None
        except Exception:
            # Log the exception for debugging in a real application
            return None
    
    def update_invoice(self, invoice_id: int, **kwargs) -> bool:
        """Update an invoice"""
        if not self.current_user_id:
            return False
        return self.db.update_invoice(invoice_id, self.current_user_id, **kwargs)
    
    def delete_invoice(self, invoice_id: int) -> bool:
        """Delete an invoice"""
        if not self.current_user_id:
            return False
        return self.db.delete_invoice(invoice_id, self.current_user_id)
    
    # ==================== STATISTICS ====================
    
    def get_my_statistics(self) -> Dict:
        """Get current user's statistics"""
        if not self.current_user_id:
            return {}
        return self.db.get_user_statistics(self.current_user_id)
    
    # ==================== EXPORT - FIXED ====================
    
    def export_my_data(self) -> Dict:
        """
        Export current user's complete data
        CRITICAL FIX: Uses current_user_id for proper filtering
        """
        if not self.current_user_id:
            return {'error': 'No user logged in'}
        
        return self.db.export_user_data(self.current_user_id)
    
    def check_export_permission(self, export_type: str = 'pdf') -> tuple:
        """Check if user can perform export"""
        if not self.current_user_id:
            return False, "No user logged in"
        
        plan_type = self.license.get_user_plan(self.current_user_id)
        
        if export_type == 'excel':
            if not self.features.can_access_feature(plan_type, 'export_excel'):
                return False, self.features.get_upgrade_message('export_excel')
        
        return True, "Export allowed"
    
    # ==================== LICENSE OPERATIONS ====================
    
    def get_my_license_info(self) -> Dict:
        """Get current user's license information"""
        if not self.current_user_id:
            return {}
        return self.license.validate_license(self.current_user_id)
    
    def upgrade_my_plan(self, plan_type: str, payment_id: str = None) -> bool:
        """Upgrade current user's plan"""
        if not self.current_user_id:
            return False
        return self.license.upgrade_plan(self.current_user_id, plan_type, payment_id)
