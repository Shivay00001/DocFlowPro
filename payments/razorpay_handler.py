"""
Razorpay Payment Integration
Handles subscriptions and plan upgrades
"""

import razorpay
import json
import os
from datetime import datetime, timedelta


class RazorpayPaymentHandler:
    """Handle Razorpay payments for plan upgrades"""
    
    # Live API Credentials - MUST be set via environment variables
    # SECURITY: NEVER hardcode API keys in production!
    RAZORPAY_KEY_ID = os.environ.get('RAZORPAY_KEY_ID')
    RAZORPAY_KEY_SECRET = os.environ.get('RAZORPAY_KEY_SECRET')
    
    if not RAZORPAY_KEY_ID or not RAZORPAY_KEY_SECRET:
        raise ValueError(
            "CRITICAL ERROR: Razorpay API credentials not found!\n"
            "You MUST set environment variables:\n"
            "  RAZORPAY_KEY_ID\n"
            "  RAZORPAY_KEY_SECRET\n\n"
            "See DEPLOYMENT.md for setup instructions."
        )
    
    # Plan pricing (in paise - 1 INR = 100 paise)
    PLANS = {
        'starter': {
            'name': 'Starter Plan',
            'price': 500000,  # ₹5,000
            'duration_days': 30,
            'features': [
                'Unlimited documents',
                'Data cleaning',
                'Tally integration',
                'Excel/PDF export'
            ]
        },
        'professional': {
            'name': 'Professional Plan',
            'price': 1000000,  # ₹10,000
            'duration_days': 30,
            'features': [
                'All Starter features',
                'ML predictions',
                'BI analytics',
                'Anomaly detection',
                'WhatsApp integration',
                'AI API (limited)'
            ]
        },
        'enterprise': {
            'name': 'Enterprise Plan',
            'price': 2500000,  # ₹25,000
            'duration_days': 30,
            'features': [
                'All Professional features',
                'AI Data Factory (full)',
                'Unlimited AI usage',
                'Custom ML models',
                'Priority support'
            ]
        },
        'lifetime': {
            'name': 'Lifetime License',
            'price': 9999900,  # ₹99,999
            'duration_days': 36500,  # 100 years
            'features': [
                'All Enterprise features',
                'Lifetime access',
                'Free updates forever',
                'VIP support'
            ]
        }
    }
    
    def __init__(self):
        """Initialize Razorpay client"""
        self.client = razorpay.Client(auth=(self.RAZORPAY_KEY_ID, self.RAZORPAY_KEY_SECRET))
    
    def create_payment_order(self, plan_id: str, user_email: str, user_name: str) -> dict:
        """
        Create a Razorpay payment order
        Returns: {'order_id', 'amount', 'currency'}
        """
        if plan_id not in self.PLANS:
            raise ValueError(f"Invalid plan: {plan_id}")
        
        plan = self.PLANS[plan_id]
        
        # Create order
        order_data = {
            'amount': plan['price'],
            'currency': 'INR',
            'receipt': f"receipt_{plan_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'notes': {
                'plan_id': plan_id,
                'plan_name': plan['name'],
                'user_email': user_email,
                'user_name': user_name
            }
        }
        
        try:
            order = self.client.order.create(data=order_data)
            return {
                'success': True,
                'order_id': order['id'],
                'amount': order['amount'],
                'currency': order['currency'],
                'plan_name': plan['name']
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def verify_payment(self, razorpay_order_id: str, razorpay_payment_id: str, 
                      razorpay_signature: str) -> bool:
        """Verify payment signature"""
        try:
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            }
            
            self.client.utility.verify_payment_signature(params_dict)
            return True
        except:
            return False
    
    def get_payment_details(self, payment_id: str) -> dict:
        """Get payment details"""
        try:
            payment = self.client.payment.fetch(payment_id)
            return {
                'success': True,
                'payment': payment
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_plan_info(self, plan_id: str) -> dict:
        """Get plan information"""
        if plan_id not in self.PLANS:
            return None
        
        plan = self.PLANS[plan_id].copy()
        plan['price_inr'] = plan['price'] / 100
        return plan
    
    def calculate_expiry_date(self, plan_id: str, start_date=None) -> str:
        """Calculate plan expiry date"""
        if plan_id not in self.PLANS:
            return None
        
        if start_date is None:
            start_date = datetime.now()
        
        duration = self.PLANS[plan_id]['duration_days']
        expiry = start_date + timedelta(days=duration)
        
        return expiry.strftime('%Y-%m-%d')
    
    @staticmethod
    def format_price(amount_paise: int) -> str:
        """Format price in rupees"""
        return f"₹{amount_paise / 100:,.0f}"


class PaymentRecordManager:
    """Manage payment records locally"""
    
    PAYMENT_FILE = "payments.json"
    
    @staticmethod
    def save_payment_record(payment_data: dict):
        """Save payment record"""
        records = PaymentRecordManager.load_payment_records()
        records.append(payment_data)
        
        with open(PaymentRecordManager.PAYMENT_FILE, 'w') as f:
            json.dump(records, f, indent=2)
    
    @staticmethod
    def load_payment_records() -> list:
        """Load all payment records"""
        if not os.path.exists(PaymentRecordManager.PAYMENT_FILE):
            return []
        
        try:
            with open(PaymentRecordManager.PAYMENT_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    
    @staticmethod
    def get_user_payments(user_id: int) -> list:
        """Get payments for a specific user"""
        all_payments = PaymentRecordManager.load_payment_records()
        return [p for p in all_payments if p.get('user_id') == user_id]
