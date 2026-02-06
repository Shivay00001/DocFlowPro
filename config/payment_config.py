"""
Razorpay Payment Configuration - LIVE CREDENTIALS

SECURITY WARNING:
================
API keys are currently stored in this file for development convenience.
For PRODUCTION deployment, you MUST:
1. Move credentials to environment variables
2. Never commit this file with real credentials to version control
3. Use encrypted configuration or secrets management

How to use environment variables:
- Set RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET in your environment
- The code will automatically use environment variables if available
"""

import os

# LIVE Razorpay API Credentials
# SECURITY: Load from environment first, fallback to hardcoded
RAZORPAY_KEY_ID = os.environ.get('RAZORPAY_KEY_ID', "rzp_live_RsWuyPx9Re47op")
RAZORPAY_KEY_SECRET = os.environ.get('RAZORPAY_KEY_SECRET', "HPxEZEjqVklglTrn7pOyOv8L")

# Warn if using hardcoded credentials
if 'RAZORPAY_KEY_ID' not in os.environ:
    import warnings
    warnings.warn(
        "SECURITY WARNING: Using hardcoded Razorpay credentials. "
        "Set RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET environment variables for production.",
        UserWarning
    )

# Payment Configuration
PAYMENT_MODE = "LIVE"  # LIVE or TEST
CURRENCY = "INR"

# SPECIAL: First User Testing Offer (₹1 for full access)
FIRST_USER_OFFER = {
    'enabled': True,
    'user_id': 1,  # Only for user_id = 1
    'price': 100,  # ₹1 in paisa
    'plan': 'professional',  # Gets Professional plan
    'duration': 'lifetime'   # Lifetime access
}

# Plan Pricing (in paisa - multiply by 100 for display)
PLAN_PRICES = {
    'starter': 49900,      # ₹499
    'professional': 99900,  # ₹999
    'enterprise': 499900,   # ₹4999
    'lifetime': 1499900     # ₹14999
}

# Annual Discount (17% off)
ANNUAL_DISCOUNT = 0.17

ANNUAL_PRICES = {
    'starter': 499900,      # ₹4999 (₹5988 - 17%)
    'professional': 999900,  # ₹9999 (₹11988 - 17%)
    'enterprise': 4999900    # ₹49999 (₹59988 - 17%)
}
