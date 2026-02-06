"""
Feature Categorization - Free vs Paid
"""

# FREE Features (Available to all users)
FREE_FEATURES = {
    'max_documents': 20,           # 20 documents/month
    'max_invoices': 10,            # 10 invoices/month
    'basic_ocr': True,             # PDF, Excel, CSV only
    'pdf_export': True,            # PDF exports only
    'dashboard': True,
    'basic_analytics': True,
    'support': 'email',            # Email support only
    'users': 1,                     # Single user
}

# STARTER Plan Features
STARTER_FEATURES = {
    'max_documents': 100,
    'max_invoices': 50,
    'basic_ocr': True,
    'advanced_ocr': False,         # No image OCR
    'pdf_export': True,
    'excel_export': False,         # No Excel export
    'gst_filing': True,
    'itr_workflow': False,
    'ai_factory': False,
    'bi_analytics': True,
    'data_cleaning': True,
    'support': 'email',
    'users': 1,
}

# PROFESSIONAL Plan Features (Recommended)
PROFESSIONAL_FEATURES = {
    'max_documents': 500,
    'max_invoices': 200,
    'basic_ocr': True,
    'advanced_ocr': True,          # Full OCR with images
    'pdf_export': True,
    'excel_export': True,          # Excel exports enabled
    'gst_filing': True,
    'itr_workflow': True,          # ITR filing workflow
    'ai_factory': True,            # AI features
    'bi_analytics': True,
    'data_cleaning': True,
    'invoice_sharing': True,       # WhatsApp, Email
    'support': 'priority',         # Priority email support
    'users': 3,
}

# ENTERPRISE Plan Features
ENTERPRISE_FEATURES = {
    'max_documents': -1,           # Unlimited
    'max_invoices': -1,            # Unlimited
    'basic_ocr': True,
    'advanced_ocr': True,
    'pdf_export': True,
    'excel_export': True,
    'gst_filing': True,
    'itr_workflow': True,
    'ai_factory': True,
    'bi_analytics': True,
    'data_cleaning': True,
    'invoice_sharing': True,
    'api_access': True,            # API access
    'whitelabel': True,            # White-label option
    'custom_integrations': True,
    'support': 'dedicated',        # Dedicated support
    'users': -1,                   # Unlimited users
}

# LIFETIME Plan Features (Same as Professional)
LIFETIME_FEATURES = PROFESSIONAL_FEATURES.copy()
LIFETIME_FEATURES['lifetime_updates'] = True

# Feature descriptions for UI
FEATURE_DESCRIPTIONS = {
    'max_documents': 'Documents per month',
    'max_invoices': 'Invoices per month',
    'basic_ocr': 'PDF, Excel, CSV OCR',
    'advanced_ocr': 'Image OCR (JPG, PNG)',
    'pdf_export': 'PDF Export',
    'excel_export': 'Excel Export',
    'gst_filing': 'GST Filing Assistant',
    'itr_workflow': 'ITR Filing Workflow',
    'ai_factory': 'AI Automation',
    'bi_analytics': 'Business Intelligence',
    'data_cleaning': 'Data Cleaning Tools',
    'invoice_sharing': 'Share via WhatsApp/Email',
    'api_access': 'API Access',
    'whitelabel': 'White-label Option',
    'support': 'Support Level',
    'users': 'Number of Users',
}

def get_plan_features(plan_type):
    """Get features for a plan type"""
    plans = {
        'free': FREE_FEATURES,
        'starter': STARTER_FEATURES,
        'professional': PROFESSIONAL_FEATURES,
        'enterprise': ENTERPRISE_FEATURES,
        'lifetime': LIFETIME_FEATURES,
    }
    return plans.get(plan_type.lower(), FREE_FEATURES)

def check_feature_access(plan_type, feature_name):
    """Check if a plan has access to a feature"""
    features = get_plan_features(plan_type)
    return features.get(feature_name, False)
