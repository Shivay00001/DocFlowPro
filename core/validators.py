"""
Input Validators - Comprehensive validation rules
"""

import re
from datetime import datetime
from core.logger import get_logger

logger = get_logger('app')


class ValidationError(Exception):
    """Custom validation error"""
    pass


class Validator:
    """Comprehensive input validation"""
    
    @staticmethod
    def validate_invoice_number(invoice_num):
        """Validate invoice number format"""
        if not invoice_num:
            raise ValidationError("Invoice number is required")
        
        invoice_num = str(invoice_num).strip()
        
        if len(invoice_num) > 50:
            raise ValidationError("Invoice number too long (max 50 characters)")
        
        if len(invoice_num) < 3:
            raise ValidationError("Invoice number too short (min 3 characters)")
        
        # Check format (letters, numbers, hyphens, underscores only)
        if not re.match(r'^[A-Z0-9_-]+$', invoice_num.upper()):
            raise ValidationError("Invoice number can only contain letters, numbers, hyphens, and underscores")
        
        return invoice_num.upper()
    
    @staticmethod
    def validate_amount(amount):
        """Validate monetary amount"""
        try:
            amount = float(amount)
        except (ValueError, TypeError):
            raise ValidationError("Amount must be a valid number")
        
        if amount < 0:
            raise ValidationError("Amount cannot be negative")
        
        if amount == 0:
            raise ValidationError("Amount must be greater than zero")
        
        if amount > 100000000:  # 10 crore limit
            raise ValidationError("Amount exceeds maximum limit (₹10,00,00,000)")
        
        return round(amount, 2)
    
    @staticmethod
    def validate_email(email):
        """Validate email format"""
        if not email:
            return None  # Optional field
        
        email = email.strip()
        
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            raise ValidationError("Invalid email format")
        
        if len(email) > 255:
            raise ValidationError("Email too long")
        
        return email.lower()
    
    @staticmethod
    def validate_phone(phone):
        """Validate phone number (10 digits)"""
        if not phone:
            return None  # Optional
        
        # Remove spaces, hyphens, parentheses
        phone = re.sub(r'[\s\-\(\)]', '', str(phone))
        
        # Check if 10 digits
        if not re.match(r'^\d{10}$', phone):
            raise ValidationError("Phone must be 10 digits")
        
        return phone
    
    @staticmethod
    def validate_date(date_str, allow_future=True):
        """Validate date format"""
        if not date_str:
            raise ValidationError("Date is required")
        
        try:
            date_obj = datetime.strptime(str(date_str), '%Y-%m-%d')
            
            if not allow_future and date_obj > datetime.now():
                raise ValidationError("Date cannot be in the future")
            
            return date_obj.strftime('%Y-%m-%d')
            
        except ValueError:
            raise ValidationError("Invalid date format (use YYYY-MM-DD)")
    
    @staticmethod
    def validate_text(text, field_name="Field", min_length=1, max_length=255, required=True):
        """Validate text field"""
        if not text:
            if required:
                raise ValidationError(f"{field_name} is required")
            return None
        
        text = str(text).strip()
        
        if len(text) < min_length:
            raise ValidationError(f"{field_name} must be at least {min_length} characters")
        
        if len(text) > max_length:
            raise ValidationError(f"{field_name} too long (max {max_length} characters)")
        
        return text
    
    @staticmethod
    def validate_invoice_items(items):
        """Validate invoice line items"""
        if not items or len(items) == 0:
            raise ValidationError("Invoice must have at least one item")
        
        validated_items = []
        
        for i, item in enumerate(items):
            item_num = i + 1
            
            # Validate description
            if not item.get('description'):
                raise ValidationError(f"Item {item_num}: Description required")
            
            # Validate quantity
            try:
                qty = float(item.get('quantity', 0))
                if qty <= 0:
                    raise ValidationError(f"Item {item_num}: Quantity must be greater than zero")
            except (ValueError, TypeError):
                raise ValidationError(f"Item {item_num}: Invalid quantity")
            
            # Validate price
            try:
                price = float(item.get('price', 0))
                if price < 0:
                    raise ValidationError(f"Item {item_num}: Price cannot be negative")
            except (ValueError, TypeError):
                raise ValidationError(f"Item {item_num}: Invalid price")
            
            validated_items.append({
                'description': str(item['description']).strip(),
                'quantity': qty,
                'price': round(price, 2),
                'total': round(qty * price, 2)
            })
        
        return validated_items
    
    @staticmethod
    def validate_client_name(name):
        """Validate client/customer name"""
        return Validator.validate_text(name, "Client name", min_length=2, max_length=100)
    
    @staticmethod
    def validate_positive_integer(value, field_name="Value"):
        """Validate positive integer"""
        try:
            value = int(value)
            if value < 0:
                raise ValidationError(f"{field_name} must be positive")
            return value
        except (ValueError, TypeError):
            raise ValidationError(f"{field_name} must be a valid number")
