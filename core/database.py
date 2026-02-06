"""
Database Manager for DocFlow Pro
Handles all database operations with user isolation
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import json


class DatabaseManager:
    """Manages SQLite database with user data isolation"""
    
    def __init__(self, db_path: str = "docflow.db"):
        """Initialize database connection"""
        self.db_path = db_path
        self.connection = None
        self.cursor = None
        self._connect()
        self._create_tables()
    
    def _connect(self):
        """Establish database connection"""
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
    
    def _create_tables(self):
        """Create all required tables"""
        
        # Users table - Single user per machine
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                email TEXT,
                full_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                is_active INTEGER DEFAULT 1
            )
        """)
        
        # License info table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS license_info (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                plan_type TEXT DEFAULT 'free',
                plan_status TEXT DEFAULT 'active',
                payment_id TEXT,
                subscription_start TIMESTAMP,
                subscription_end TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        
        # Documents table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                file_path TEXT,
                file_type TEXT,
                file_size INTEGER,
                ocr_text TEXT,
                tags TEXT,
                category TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        
        # Invoices table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS invoices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                invoice_number TEXT UNIQUE NOT NULL,
                client_name TEXT NOT NULL,
                client_email TEXT,
                client_address TEXT,
                invoice_date DATE NOT NULL,
                due_date DATE,
                items TEXT NOT NULL,
                subtotal REAL NOT NULL,
                tax_rate REAL DEFAULT 0,
                tax_amount REAL DEFAULT 0,
                total_amount REAL NOT NULL,
                status TEXT DEFAULT 'pending',
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        
        # Audit logs table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                action TEXT NOT NULL,
                entity_type TEXT,
                entity_id INTEGER,
                details TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        
        self.connection.commit()
    
    # ==================== USER MANAGEMENT ====================
    
    def create_user(self, username: str, password_hash: str, email: str = "", full_name: str = "") -> int:
        """Create a new user"""
        try:
            self.cursor.execute("""
                INSERT INTO users (username, password_hash, email, full_name)
                VALUES (?, ?, ?, ?)
            """, (username, password_hash, email, full_name))
            self.connection.commit()
            
            user_id = self.cursor.lastrowid
            
            # Create default free license
            self.cursor.execute("""
                INSERT INTO license_info (user_id, plan_type, plan_status)
                VALUES (?, 'free', 'active')
            """, (user_id,))
            self.connection.commit()
            
            return user_id
        except sqlite3.IntegrityError:
            return -1
    
    def get_user_by_username(self, username: str) -> Optional[Dict]:
        """Get user by username"""
        self.cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = self.cursor.fetchone()
        return dict(row) if row else None
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """Get user by ID"""
        self.cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = self.cursor.fetchone()
        return dict(row) if row else None
    
    def update_last_login(self, user_id: int):
        """Update user's last login timestamp"""
        self.cursor.execute("""
            UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?
        """, (user_id,))
        self.connection.commit()
    
    def get_user_count(self) -> int:
        """Get total number of users"""
        self.cursor.execute("SELECT COUNT(*) FROM users")
        return self.cursor.fetchone()[0]
    
    # ==================== LICENSE MANAGEMENT ====================
    
    def get_user_license(self, user_id: int) -> Optional[Dict]:
        """Get user's license information"""
        self.cursor.execute("""
            SELECT * FROM license_info WHERE user_id = ? ORDER BY id DESC LIMIT 1
        """, (user_id,))
        row = self.cursor.fetchone()
        return dict(row) if row else None
    
    def update_user_plan(self, user_id: int, plan_type: str, payment_id: str = None):
        """Update user's plan"""
        subscription_start = datetime.now()
        
        # Calculate subscription end based on plan
        if plan_type == "lifetime":
            subscription_end = datetime(2099, 12, 31)
        elif plan_type == "monthly":
            # Add 30 days
            from datetime import timedelta
            subscription_end = subscription_start + timedelta(days=30)
        else:
            subscription_end = None
        
        self.cursor.execute("""
            UPDATE license_info 
            SET plan_type = ?, payment_id = ?, subscription_start = ?, subscription_end = ?
            WHERE user_id = ?
        """, (plan_type, payment_id, subscription_start, subscription_end, user_id))
        self.connection.commit()
    
    # ==================== DOCUMENT MANAGEMENT ====================
    
    def create_document(self, user_id: int, title: str, description: str = "", 
                       file_path: str = "", file_type: str = "", file_size: int = 0,
                       ocr_text: str = "", tags: str = "", category: str = "") -> int:
        """Create a new document for a specific user"""
        self.cursor.execute("""
            INSERT INTO documents (user_id, title, description, file_path, file_type, 
                                  file_size, ocr_text, tags, category)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (user_id, title, description, file_path, file_type, file_size, ocr_text, tags, category))
        self.connection.commit()
        
        doc_id = self.cursor.lastrowid
        self._log_action(user_id, "create_document", "document", doc_id, f"Created document: {title}")
        return doc_id
    
    def get_user_documents(self, user_id: int, limit: int = None) -> List[Dict]:
        """Get all documents for a specific user - CRITICAL for export fix"""
        query = "SELECT * FROM documents WHERE user_id = ? ORDER BY created_at DESC"
        if limit:
            query += f" LIMIT {limit}"
        
        self.cursor.execute(query, (user_id,))
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]
    
    def get_document_by_id(self, doc_id: int, user_id: int) -> Optional[Dict]:
        """Get a specific document (with user verification)"""
        self.cursor.execute("""
            SELECT * FROM documents WHERE id = ? AND user_id = ?
        """, (doc_id, user_id))
        row = self.cursor.fetchone()
        return dict(row) if row else None
    
    def update_document(self, doc_id: int, user_id: int, **kwargs) -> bool:
        """Update a document (with user verification)"""
        allowed_fields = ['title', 'description', 'ocr_text', 'tags', 'category']
        updates = {k: v for k, v in kwargs.items() if k in allowed_fields}
        
        if not updates:
            return False
        
        updates['updated_at'] = datetime.now()
        
        set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
        values = list(updates.values()) + [doc_id, user_id]
        
        self.cursor.execute(f"""
            UPDATE documents SET {set_clause} WHERE id = ? AND user_id = ?
        """, values)
        self.connection.commit()
        
        self._log_action(user_id, "update_document", "document", doc_id, f"Updated document")
        return True
    
    def delete_document(self, doc_id: int, user_id: int) -> bool:
        """Delete a document (with user verification)"""
        self.cursor.execute("DELETE FROM documents WHERE id = ? AND user_id = ?", (doc_id, user_id))
        self.connection.commit()
        
        self._log_action(user_id, "delete_document", "document", doc_id, f"Deleted document")
        return self.cursor.rowcount > 0
    
    def search_documents(self, user_id: int, query: str) -> List[Dict]:
        """Search documents for a specific user"""
        search_pattern = f"%{query}%"
        self.cursor.execute("""
            SELECT * FROM documents 
            WHERE user_id = ? AND (
                title LIKE ? OR 
                description LIKE ? OR 
                ocr_text LIKE ? OR 
                tags LIKE ?
            )
            ORDER BY created_at DESC
        """, (user_id, search_pattern, search_pattern, search_pattern, search_pattern))
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]
    
    def get_user_document_count(self, user_id: int) -> int:
        """Get total document count for a user"""
        self.cursor.execute("SELECT COUNT(*) FROM documents WHERE user_id = ?", (user_id,))
        return self.cursor.fetchone()[0]
    
    # ==================== INVOICE MANAGEMENT ====================
    
    def create_invoice(self, user_id: int, invoice_number: str, client_name: str,
                      invoice_date: str, items: List[Dict], **kwargs) -> int:
        """Create a new invoice for a specific user"""
        
        # Calculate totals
        subtotal = sum(item['quantity'] * item['rate'] for item in items)
        tax_rate = kwargs.get('tax_rate', 0)
        tax_amount = subtotal * (tax_rate / 100)
        total_amount = subtotal + tax_amount
        
        items_json = json.dumps(items)
        
        self.cursor.execute("""
            INSERT INTO invoices (user_id, invoice_number, client_name, client_email, 
                                 client_address, invoice_date, due_date, items, 
                                 subtotal, tax_rate, tax_amount, total_amount, status, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (user_id, invoice_number, client_name, kwargs.get('client_email', ''),
              kwargs.get('client_address', ''), invoice_date, kwargs.get('due_date', ''),
              items_json, subtotal, tax_rate, tax_amount, total_amount, 
              kwargs.get('status', 'pending'), kwargs.get('notes', '')))
        
        self.connection.commit()
        
        invoice_id = self.cursor.lastrowid
        self._log_action(user_id, "create_invoice", "invoice", invoice_id, 
                        f"Created invoice: {invoice_number}")
        return invoice_id
    
    def get_user_invoices(self, user_id: int, limit: int = None) -> List[Dict]:
        """Get all invoices for a specific user - CRITICAL for export fix"""
        query = "SELECT * FROM invoices WHERE user_id = ? ORDER BY invoice_date DESC"
        if limit:
            query += f" LIMIT {limit}"
        
        self.cursor.execute(query, (user_id,))
        rows = self.cursor.fetchall()
        
        # Parse items JSON
        invoices = []
        for row in rows:
            invoice = dict(row)
            invoice['items'] = json.loads(invoice['items'])
            invoices.append(invoice)
        
        return invoices
    
    def get_invoice_by_id(self, invoice_id: int, user_id: int) -> Optional[Dict]:
        """Get a specific invoice (with user verification)"""
        self.cursor.execute("""
            SELECT * FROM invoices WHERE id = ? AND user_id = ?
        """, (invoice_id, user_id))
        row = self.cursor.fetchone()
        
        if row:
            invoice = dict(row)
            invoice['items'] = json.loads(invoice['items'])
            return invoice
        return None
    
    def update_invoice(self, invoice_id: int, user_id: int, **kwargs) -> bool:
        """Update an invoice (with user verification)"""
        allowed_fields = ['client_name', 'client_email', 'client_address', 
                         'invoice_date', 'due_date', 'status', 'notes']
        updates = {k: v for k, v in kwargs.items() if k in allowed_fields}
        
        if not updates:
            return False
        
        updates['updated_at'] = datetime.now()
        
        set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
        values = list(updates.values()) + [invoice_id, user_id]
        
        self.cursor.execute(f"""
            UPDATE invoices SET {set_clause} WHERE id = ? AND user_id = ?
        """, values)
        self.connection.commit()
        
        self._log_action(user_id, "update_invoice", "invoice", invoice_id, "Updated invoice")
        return True
    
    def delete_invoice(self, invoice_id: int, user_id: int) -> bool:
        """Delete an invoice (with user verification)"""
        self.cursor.execute("DELETE FROM invoices WHERE id = ? AND user_id = ?", 
                          (invoice_id, user_id))
        self.connection.commit()
        
        self._log_action(user_id, "delete_invoice", "invoice", invoice_id, "Deleted invoice")
        return self.cursor.rowcount > 0
    
    def get_user_invoice_count(self, user_id: int) -> int:
        """Get total invoice count for a user"""
        self.cursor.execute("SELECT COUNT(*) FROM invoices WHERE user_id = ?", (user_id,))
        return self.cursor.fetchone()[0]
    
    def get_user_invoice_total(self, user_id: int) -> float:
        """Get total invoice amount for a user"""
        self.cursor.execute("""
            SELECT COALESCE(SUM(total_amount), 0) FROM invoices WHERE user_id = ?
        """, (user_id,))
        return self.cursor.fetchone()[0]
    
    # ==================== EXPORT FUNCTIONALITY - FIXED ====================
    
    def export_user_data(self, user_id: int) -> Dict:
        """
        Export all data for a specific user
        CRITICAL FIX: Ensures only current user's data is exported
        """
        return {
            'user_info': self.get_user_by_id(user_id),
            'documents': self.get_user_documents(user_id),
            'invoices': self.get_user_invoices(user_id),
            'license': self.get_user_license(user_id),
            'statistics': {
                'total_documents': self.get_user_document_count(user_id),
                'total_invoices': self.get_user_invoice_count(user_id),
                'total_invoice_amount': self.get_user_invoice_total(user_id)
            }
        }
    
    # ==================== AUDIT LOGGING ====================
    
    def _log_action(self, user_id: int, action: str, entity_type: str = None, 
                   entity_id: int = None, details: str = ""):
        """Log user actions"""
        self.cursor.execute("""
            INSERT INTO audit_logs (user_id, action, entity_type, entity_id, details)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, action, entity_type, entity_id, details))
        self.connection.commit()
    
    def get_user_activity(self, user_id: int, limit: int = 50) -> List[Dict]:
        """Get recent activity for a user"""
        self.cursor.execute("""
            SELECT * FROM audit_logs WHERE user_id = ? ORDER BY created_at DESC LIMIT ?
        """, (user_id, limit))
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]
    
    # ==================== ANALYTICS ====================
    
    def get_user_statistics(self, user_id: int) -> Dict:
        """Get user statistics for dashboard"""
        return {
            'total_documents': self.get_user_document_count(user_id),
            'total_invoices': self.get_user_invoice_count(user_id),
            'total_revenue': self.get_user_invoice_total(user_id),
            'recent_documents': self.get_user_documents(user_id, limit=5),
            'recent_invoices': self.get_user_invoices(user_id, limit=5),
            'recent_activity': self.get_user_activity(user_id, limit=10)
        }
    
    # ==================== CLEANUP ====================
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
    
    def __del__(self):
        """Destructor to ensure connection is closed"""
        self.close()
