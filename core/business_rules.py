"""
Business Rules Engine - Enforce business logic validation
"""

from datetime import datetime
from core.logger import get_logger

logger = get_logger('app')


class BusinessRuleViolation(Exception):
    """Business rule validation error"""
    pass


class BusinessRules:
    """Enforce business logic rules"""
    
    @staticmethod
    def validate_invoice_creation(invoice_data, user_id, db_manager, license_manager):
        """Validate invoice creation against business rules"""
        
        # Rule 1: Check invoice limit based on plan
        from core.feature_gates import FeatureGates
        
        plan = license_manager.get_user_plan(user_id)
        features = FeatureGates.get_features(plan)
        max_invoices = features.get('max_invoices', 0)
        
        if max_invoices > 0:  # -1 means unlimited
            current_count = db_manager.get_user_invoice_count(user_id)
            if current_count >= max_invoices:
                raise BusinessRuleViolation(
                    f"Invoice limit reached ({max_invoices} for {plan} plan). "
                    "Please upgrade to create more invoices."
                )
        
        # Rule 2: Check duplicate invoice number
        invoice_number = invoice_data.get('invoice_number')
        if invoice_number:
            existing = BusinessRules._check_duplicate_invoice(invoice_number, user_id, db_manager)
            if existing:
                raise BusinessRuleViolation(
                    f"Invoice number '{invoice_number}' already exists"
                )
        
        # Rule 3: Validate invoice date not in future (unless explicitly allowed)
        invoice_date = invoice_data.get('invoice_date')
        if invoice_date:
            try:
                date_obj = datetime.strptime(invoice_date, '%Y-%m-%d')
                if date_obj > datetime.now():
                    raise BusinessRuleViolation("Invoice date cannot be in the future")
            except ValueError:
                pass  # Let validator handle this
        
        # Rule 4: Total amount must match items
        items = invoice_data.get('items', [])
        if items:
            calculated_total = sum(item.get('quantity', 0) * item.get('price', 0) for item in items)
            declared_total = invoice_data.get('total_amount', calculated_total)
            
            if abs(calculated_total - declared_total) > 0.01:  # Allow 1 paisa difference for rounding
                raise BusinessRuleViolation(
                    f"Total amount mismatch: declared ₹{declared_total:.2f}, "
                    f"calculated ₹{calculated_total:.2f}"
                )
        
        return True
    
    @staticmethod
    def validate_document_upload(user_id, db_manager, license_manager):
        """Validate document upload against limits"""
        
        from core.feature_gates import FeatureGates
        
        plan = license_manager.get_user_plan(user_id)
        features = FeatureGates.get_features(plan)
        max_documents = features.get('max_documents', 0)
        
        if max_documents > 0:  # -1 means unlimited
            current_count = db_manager.get_user_document_count(user_id)
            if current_count >= max_documents:
                raise BusinessRuleViolation(
                    f"Document limit reached ({max_documents} for {plan} plan). "
                    "Please upgrade to upload more documents."
                )
        
        return True
    
    @staticmethod
    def validate_export_operation(export_type, user_id, license_manager):
        """Validate export operation against plan permissions"""
        
        from core.feature_gates import FeatureGates
        
        plan = license_manager.get_user_plan(user_id)
        features = FeatureGates.get_features(plan)
        
        if export_type == 'excel':
            if not features.get('export_excel', False):
                raise BusinessRuleViolation(
                    f"Excel export not available in {plan} plan. "
                    "Please upgrade to Professional or Lifetime plan."
                )
        
        if export_type == 'bulk' and not features.get('bulk_operations', False):
            raise BusinessRuleViolation(
                f"Bulk operations not available in {plan} plan. "
                "Please upgrade to Professional or Lifetime plan."
            )
        
        return True
    
    @staticmethod
    def _check_duplicate_invoice(invoice_number, user_id, db_manager):
        """Check if invoice number already exists for user"""
        try:
            cursor = db_manager.connection.cursor()
            cursor.execute('''
                SELECT id FROM invoices 
                WHERE user_id = ? AND invoice_number = ?
                LIMIT 1
            ''', (user_id, invoice_number))
            
            return cursor.fetchone() is not None
        except Exception as e:
            logger.error(f"Duplicate check failed: {e}")
            return False
