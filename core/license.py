"""
License Management and Validation
With VERY LIMITED free tier
"""

from datetime import datetime
from typing import Optional, Dict


# PLAN FEATURES - Free tier is VERY LIMITED
PLAN_FEATURES = {
    'free': {
        'max_documents': 10,         # ⚠️ Very limited
        'max_invoices': 5,           # ⚠️ Very limited
        'max_exports_per_month': 3,  # ⚠️ Very limited
        'pdf_export': True,          # Basic PDF only
        'excel_export': False,       # ❌ Excel is PAID
        'gst_invoice': False,        # ❌ GST is PAID
        'ai_features': False,        # ❌ No AI
        'analytics': False,          # ❌ No analytics
        'auto_backup': False,        # ❌ No backup
        'priority_support': False,
        'api_access': False,
        'bulk_upload': False,        # ❌ No bulk
        'ocr_limit': 5,              # ⚠️ Only 5 OCR
        'premium_categories': False, # ❌ Free categories only
        'name': 'Free Trial',
        'price': 0,
        'description': 'Limited trial - upgrade to unlock'
    },
    'starter': {
        'max_documents': 100,
        'max_invoices': 50,
        'max_exports_per_month': 50,
        'pdf_export': True,
        'excel_export': True,        # ✅
        'gst_invoice': True,         # ✅
        'ai_features': True,
        'analytics': True,
        'auto_backup': True,
        'priority_support': False,
        'api_access': False,
        'bulk_upload': True,
        'ocr_limit': 100,
        'premium_categories': True,  # ✅
        'name': 'Starter',
        'price': 2999,
        'description': 'Perfect for small businesses'
    },
    'professional': {
        'max_documents': 500,
        'max_invoices': 200,
        'max_exports_per_month': 200,
        'pdf_export': True,
        'excel_export': True,
        'gst_invoice': True,
        'ai_features': True,
        'analytics': True,
        'auto_backup': True,
        'priority_support': True,
        'api_access': True,
        'bulk_upload': True,
        'ocr_limit': 500,
        'premium_categories': True,
        'name': 'Professional',
        'price': 4999,
        'description': 'For growing businesses'
    },
    'lifetime': {
        'max_documents': 999999,
        'max_invoices': 999999,
        'max_exports_per_month': 999999,
        'pdf_export': True,
        'excel_export': True,
        'gst_invoice': True,
        'ai_features': True,
        'analytics': True,
        'auto_backup': True,
        'priority_support': True,
        'api_access': True,
        'bulk_upload': True,
        'ocr_limit': 999999,
        'premium_categories': True,
        'name': 'Lifetime Access',
        'price': 9999,
        'description': 'Pay once, use forever'
    }
}


class LicenseManager:
    """Manages software licensing and validation"""
    
    # Pricing plans (for backward compatibility)
    PLANS = {
        'free': {
            'name': 'Free Trial',
            'price': 0,
            'currency': 'INR',
            'description': 'Limited trial - 10 docs, 5 invoices'
        },
        'starter': {
            'name': 'Starter Plan',
            'price': 2999,
            'currency': 'INR',
            'description': '₹2,999 - Full features for small business'
        },
        'professional': {
            'name': 'Professional Plan',
            'price': 4999,
            'currency': 'INR',
            'description': '₹4,999 - Advanced features + support'
        },
        'lifetime': {
            'name': 'Lifetime Access',
            'price': 9999,
            'currency': 'INR',
            'description': '₹9,999 one-time - All features forever'
        }
    }
    
    def __init__(self, db_manager):
        """Initialize license manager"""
        self.db = db_manager
    
    def get_user_plan(self, user_id: int) -> str:
        """Get current plan for user"""
        license_info = self.db.get_user_license(user_id)
        if not license_info:
            return 'free'
        
        return license_info.get('plan_type', 'free')
    
    def validate_license(self, user_id: int) -> Dict:
        """Validate user license and return status"""
        plan_type = self.get_user_plan(user_id)
        limits = self.get_plan_limits(plan_type)
        
        return {
            'valid': True,
            'plan_type': plan_type,
            'plan_name': limits['name'],
            'status': 'active',
            'limits': limits
        }
    
    def get_plan_limits(self, plan: str) -> Dict:
        """Get limits for a specific plan"""
        return PLAN_FEATURES.get(plan, PLAN_FEATURES['free'])
    
    def can_create_document(self, user_id: int) -> tuple:
        """Check if user can create more documents"""
        plan = self.get_user_plan(user_id)
        limits = self.get_plan_limits(plan)
        
        current_count = len(self.db.get_user_documents(user_id))
        max_allowed = limits['max_documents']
        
        if current_count >= max_allowed:
            return False, f"Document limit reached ({max_allowed} max). Upgrade to add more!"
        
        return True, "OK"
    
    def can_create_invoice(self, user_id: int) -> tuple:
        """Check if user can create more invoices"""
        plan = self.get_user_plan(user_id)
        limits = self.get_plan_limits(plan)
        
        current_count = len(self.db.get_user_invoices(user_id))
        max_allowed = limits['max_invoices']
        
        if current_count >= max_allowed:
            return False, f"Invoice limit reached ({max_allowed} max). Upgrade to add more!"
        
        return True, "OK"
    
    def can_export_to_excel(self, user_id: int) -> tuple:
        """Check if user can export to Excel"""
        plan = self.get_user_plan(user_id)
        limits = self.get_plan_limits(plan)
        
        if not limits['excel_export']:
            return False, "Excel export is a Premium feature. Upgrade to Starter (₹2,999) or higher!"
        
        return True, "OK"
    
    def can_create_gst_invoice(self, user_id: int) -> tuple:
        """Check if user can create GST invoices"""
        plan = self.get_user_plan(user_id)
        limits = self.get_plan_limits(plan)
        
        if not limits['gst_invoice']:
            return False, "GST invoices are Premium. Upgrade to Starter (₹2,999) or higher!"
        
        return True, "OK"
    
    def can_use_premium_category(self, user_id: int) -> tuple:
        """Check if user can use premium categories"""
        plan = self.get_user_plan(user_id)
        limits = self.get_plan_limits(plan)
        
        if not limits['premium_categories']:
            return False, "Premium categories require Starter plan (₹2,999) or higher!"
        
        return True, "OK"
