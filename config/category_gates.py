"""
Category-based Feature Gates
Define which categories are free vs premium
"""

# Document Categories
FREE_DOCUMENT_CATEGORIES = [
    'General',
    'Personal',
    'Receipts',
    'Tax Documents'
]

PREMIUM_DOCUMENT_CATEGORIES = [
    'Contracts',
    'Legal Documents',
    'Financial Reports',
    'Business Invoices',
    'Compliance Documents',
    'Audit Reports',
    'Bank Statements',
    'Property Documents'
]

# Invoice Categories/Types
FREE_INVOICE_TYPES = [
    'Simple Invoice',
    'Receipt',
    'Quotation'
]

PREMIUM_INVOICE_TYPES = [
    'GST Invoice',
    'Tax Invoice',
    'Proforma Invoice',
    'Credit Note',
    'Debit Note',
    'Commercial Invoice',
    'Export Invoice'
]

def get_available_categories(user_plan: str, category_type='document'):
    """
    Get available categories based on user's plan
    
    Args:
        user_plan: 'free', 'starter', 'professional', or 'lifetime'
        category_type: 'document' or 'invoice'
    
    Returns:
        List of available categories
    """
    if category_type == 'document':
        free_cats = FREE_DOCUMENT_CATEGORIES
        premium_cats = PREMIUM_DOCUMENT_CATEGORIES
    else:  # invoice
        free_cats = FREE_INVOICE_TYPES
        premium_cats = PREMIUM_INVOICE_TYPES
    
    # Free tier: only free categories
    if user_plan == 'free':
        return free_cats
    
    # All paid tiers: free + premium
    return free_cats + premium_cats

def is_category_allowed(category: str, user_plan: str, category_type='document'):
    """
    Check if user can use this category
    
    Returns:
        tuple: (allowed: bool, message: str)
    """
    available = get_available_categories(user_plan, category_type)
    
    if category in available:
        return True, "Category allowed"
    
    # Category is premium but user is free
    return False, f"'{category}' is a Premium feature. Upgrade to Starter (₹2,999) or higher to access."

def get_category_badge(category: str, category_type='document'):
    """
    Get badge text for category (FREE or PREMIUM)
    """
    if category_type == 'document':
        if category in FREE_DOCUMENT_CATEGORIES:
            return "FREE"
        return "PREMIUM"
    else:
        if category in FREE_INVOICE_TYPES:
            return "FREE"
        return "PREMIUM"

# For UI display
ALL_DOCUMENT_CATEGORIES = FREE_DOCUMENT_CATEGORIES + PREMIUM_DOCUMENT_CATEGORIES
ALL_INVOICE_TYPES = FREE_INVOICE_TYPES + PREMIUM_INVOICE_TYPES
