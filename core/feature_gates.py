"""
Feature Gates - Access control based on user plans
"""

from typing import Dict, List


class FeatureGates:
    """Manages feature access based on user subscription plans"""
    
    # Feature definitions - Aligned with pricing
    FEATURES = {
        'free': {
            'max_documents': 50,
            'max_invoices': 20,
            'ocr_enabled': True,
            'export_pdf': True,
            'export_excel': False,
            'bulk_operations': False,
            'analytics': False,
            'custom_templates': False,
            'api_access': False,
        },
        'starter': {
            'max_documents': 100,
            'max_invoices': 50,
            'ocr_enabled': True,
            'export_pdf': True,
            'export_excel': False,
            'bulk_operations': False,
            'analytics': True,
            'custom_templates': False,
            'api_access': False,
        },
        'professional': {
            'max_documents': 500,
            'max_invoices': 200,
            'ocr_enabled': True,
            'export_pdf': True,
            'export_excel': True,
            'bulk_operations': True,
            'analytics': True,
            'custom_templates': True,
            'api_access': False,
        },
        'lifetime': {
            'max_documents': -1,  # Unlimited
            'max_invoices': -1,   # Unlimited
            'ocr_enabled': True,
            'export_pdf': True,
            'export_excel': True,
            'bulk_operations': True,
            'analytics': True,
            'custom_templates': True,
            'api_access': True,
        }
    }
    
    @staticmethod
    def can_access_feature(plan_type: str, feature: str) -> bool:
        """Check if a plan has access to a feature"""
        plan_features = FeatureGates.FEATURES.get(plan_type, FeatureGates.FEATURES['free'])
        return plan_features.get(feature, False)
    
    @staticmethod
    def get_limit(plan_type: str, limit_type: str) -> int:
        """Get resource limit for a plan"""
        plan_features = FeatureGates.FEATURES.get(plan_type, FeatureGates.FEATURES['free'])
        return plan_features.get(limit_type, 0)
    
    @staticmethod
    def check_document_limit(plan_type: str, current_count: int) -> bool:
        """Check if user can create more documents"""
        max_docs = FeatureGates.get_limit(plan_type, 'max_documents')
        if max_docs == -1:  # Unlimited
            return True
        return current_count < max_docs
    
    @staticmethod
    def check_invoice_limit(plan_type: str, current_count: int) -> bool:
        """Check if user can create more invoices"""
        max_invoices = FeatureGates.get_limit(plan_type, 'max_invoices')
        if max_invoices == -1:  # Unlimited
            return True
        return current_count < max_invoices
    
    @staticmethod
    def get_plan_features(plan_type: str) -> Dict:
        """Get all features for a plan"""
        return FeatureGates.FEATURES.get(plan_type, FeatureGates.FEATURES['free'])
    
    @staticmethod
    def get_upgrade_message(feature: str) -> str:
        """Get upgrade message for a locked feature"""
        messages = {
            'export_excel': "Excel export is available in paid plans. Upgrade to unlock!",
            'bulk_operations': "Bulk operations require a paid plan. Upgrade now!",
            'analytics': "Advanced analytics available in paid plans. Upgrade to access!",
            'custom_templates': "Custom templates are a premium feature. Upgrade to unlock!",
            'api_access': "API access is available in lifetime plan only.",
        }
        return messages.get(feature, "This feature requires a paid plan. Please upgrade!")
