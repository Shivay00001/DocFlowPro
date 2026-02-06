"""
Live Razorpay Payment Integration
"""

import razorpay
from tkinter import messagebox
import webbrowser
from datetime import datetime
import json

# Import configuration
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config.payment_config import (
    RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET, 
    PLAN_PRICES, ANNUAL_PRICES, PAYMENT_MODE,
    FIRST_USER_OFFER  # CRITICAL FIX: Added missing import
)


class PaymentGateway:
    """Live Razorpay Payment Gateway"""
    
    def __init__(self):
        """Initialize Razorpay with LIVE credentials"""
        self.client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
        self.mode = PAYMENT_MODE
        
    def create_order(self, plan_type, billing_cycle='monthly', user_email='', user_phone='', user_id=None):
        """Create Razorpay payment order"""
        try:
            # Check for first user special offer
            if user_id == FIRST_USER_OFFER['user_id'] and FIRST_USER_OFFER['enabled']:
                amount = FIRST_USER_OFFER['price']  # ₹1
                plan_type = FIRST_USER_OFFER['plan']  # Professional
                billing_cycle = FIRST_USER_OFFER['duration']  # Lifetime
                
                # Create special order note
                notes = {
                    'plan_type': plan_type,
                    'billing_cycle': billing_cycle,
                    'user_email': user_email,
                    'user_phone': user_phone,
                    'special_offer': 'FIRST_USER_₹1_TESTING'
                }
            else:
                # Get amount based on plan and cycle
                if billing_cycle == 'annual':
                    amount = ANNUAL_PRICES.get(plan_type, 99900)
                elif plan_type == 'lifetime':
                    amount = PLAN_PRICES.get('lifetime', 1499900)
                else:
                    amount = PLAN_PRICES.get(plan_type, 99900)
                
                notes = {
                    'plan_type': plan_type,
                    'billing_cycle': billing_cycle,
                    'user_email': user_email,
                    'user_phone': user_phone
                }
            
            # Create order
            order_data = {
                'amount': amount,  # Amount in paisa
                'currency': 'INR',
                'receipt': f'order_{plan_type}_{datetime.now().strftime("%Y%m%d%H%M%S")}',
                'notes': notes
            }
            
            order = self.client.order.create(data=order_data)
            return True, order
            
        except Exception as e:
            return False, str(e)
    
    def verify_payment(self, payment_id, order_id, signature):
        """Verify payment signature"""
        try:
            params_dict = {
                'razorpay_payment_id': payment_id,
                'razorpay_order_id': order_id,
                'razorpay_signature': signature
            }
            
            self.client.utility.verify_payment_signature(params_dict)
            return True
            
        except razorpay.errors.SignatureVerificationError:
            return False
    
    def get_payment_status(self, payment_id):
        """Get payment status"""
        try:
            payment = self.client.payment.fetch(payment_id)
            return payment.get('status', 'failed')
        except:
            return 'failed'
    
    def initiate_checkout(self, plan_type, billing_cycle, user_data, on_success_callback, user_id=None):
        """Initiate Razorpay checkout"""
        try:
            # Create order
            success, order = self.create_order(
                plan_type, 
                billing_cycle,
                user_data.get('email', ''),
                user_data.get('phone', ''),
                user_id=user_id  # Pass user ID for first user check
            )
            
            if not success:
                messagebox.showerror("Payment Error", f"Failed to create order: {order}")
                return False
            
            # Get amount for display
            amount = order['amount'] / 100  # Convert paisa to rupees
            
            # Special message for first user
            if user_id == FIRST_USER_OFFER['user_id'] and FIRST_USER_OFFER['enabled']:
                message = (
                    f"🎉 SPECIAL FIRST USER OFFER! 🎉\n\n"
                    f"Plan: Professional (Lifetime)\n"
                    f"Amount: ₹{amount:,.2f} ONLY!\n\n"
                    f"Opening payment page...\n"
                    f"After payment, you'll get full Professional access forever!"
                )
            else:
                message = (
                    f"Opening payment page in your browser...\n\n"
                    f"Plan: {plan_type.title()}\n"
                    f"Amount: ₹{amount:,.2f}\n\n"
                    f"After successful payment, your plan will be activated automatically."
                )
            
            # Razorpay checkout options
            payment_url = self._generate_payment_link(order, user_data)
            
            if payment_url:
                messagebox.showinfo("Payment Redirect", message)
                webbrowser.open(payment_url)
                return True
            else:
                messagebox.showerror("Error", "Failed to generate payment link")
                return False
                
        except Exception as e:
            messagebox.showerror("Payment Error", f"Failed to initiate payment:\n{str(e)}")
            return False
    
    def _generate_payment_link(self, order, user_data):
        """Generate payment link (simplified for desktop app)"""
        try:
            # In production, implement proper payment link generation
            # For now, return Razorpay dashboard link
            order_id = order['id']
            amount = order['amount'] / 100
            
            # You would integrate with your backend here to create a proper payment page
            # For demo, we'll return the order ID
            return f"https://razorpay.com/payment-link/{order_id}"
            
        except:
            return None


class UpgradeManager:
    """Manage plan upgrades and payments"""
    
    def __init__(self, engine):
        self.engine = engine
        self.gateway = PaymentGateway()
    
    def show_upgrade_dialog(self, current_plan='free'):
        """Show upgrade options dialog"""
        import tkinter as tk
        from tkinter import ttk
        
        dialog = tk.Toplevel()
        dialog.title("Upgrade Plan")
        dialog.geometry("900x700")
        
        # Header
        tk.Label(
            dialog,
            text="Choose Your Plan",
            font=('Segoe UI', 20, 'bold'),
            bg='#1a237e',
            fg='white',
            pady=20
        ).pack(fill='x')
        
        # Plans container
        plans_frame = tk.Frame(dialog)
        plans_frame.pack(fill='both', expand=True, padx=30, pady=30)
        
        plans = [
            {
                'name': 'Starter',
                'price_monthly': 499,
                'price_annual': 4999,
                'features': ['100 documents/month', '50 invoices/month', 'PDF Export', 'GST Filing', 'Email Support']
            },
            {
                'name': 'Professional',
                'price_monthly': 999,
                'price_annual': 9999,
                'features': ['500 documents/month', '200 invoices/month', 'Full OCR', 'Excel Export', 'ITR Workflow', 'WhatsApp Sharing', 'Priority Support'],
                'recommended': True
            },
            {
                'name': 'Lifetime',
                'price_monthly': None,
                'price_annual': 14999,
                'features': ['All Professional features', 'One-time payment', 'Lifetime updates', '5 users', 'Priority Support']
            }
        ]
        
        for idx, plan in enumerate(plans):
            self._create_plan_card(plans_frame, plan, idx)
        
        dialog.transient()
        dialog.grab_set()
    
    def _create_plan_card(self, parent, plan_data, column):
        """Create a plan card"""
        import tkinter as tk
        
        card = tk.Frame(parent, relief='raised', borderwidth=2)
        card.grid(row=0, column=column, padx=10, sticky='nsew')
        
        # Plan name
        tk.Label(
            card,
            text=plan_data['name'],
            font=('Segoe UI', 16, 'bold')
        ).pack(pady=10)
        
        # Price
        if plan_data.get('recommended'):
            tk.Label(
                card,
                text="RECOMMENDED",
                bg='#4CAF50',
                fg='white',
                font=('Segoe UI', 10, 'bold'),
                padx=10,
                pady=5
            ).pack()
        
        if plan_data['price_monthly']:
            tk.Label(
                card,
                text=f"₹{plan_data['price_monthly']}/month",
                font=('Segoe UI', 14)
            ).pack(pady=5)
        
        tk.Label(
            card,
            text=f"₹{plan_data['price_annual']}/year",
            font=('Segoe UI', 12),
            fg='#666'
        ).pack(pady=5)
        
        # Features
        features_frame = tk.Frame(card)
        features_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        for feature in plan_data['features']:
            tk.Label(
                features_frame,
                text=f"✓ {feature}",
                font=('Segoe UI', 10),
                anchor='w'
            ).pack(anchor='w', pady=3)
        
        # Upgrade button
        plan_name = plan_data['name'].lower()
        tk.Button(
            card,
            text="Upgrade Now",
            font=('Segoe UI', 12, 'bold'),
            bg='#2196F3',
            fg='white',
            relief='flat',
            cursor='hand2',
            padx=30,
            pady=10,
            command=lambda: self._initiate_payment(plan_name, 'annual')
        ).pack(pady=20)
    
    def _initiate_payment(self, plan_type, billing_cycle):
        """Initiate payment process"""
        user_data = {
            'email': 'user@example.com',  # Get from engine
            'phone': '9999999999'          # Get from user
        }
        
        success = self.gateway.initiate_checkout(
            plan_type,
            billing_cycle,
            user_data,
            on_success_callback=self._on_payment_success
        )
    
    def _on_payment_success(self, payment_data):
        """Handle successful payment"""
        # Update user's plan in database
        messagebox.showinfo("Success", "Payment successful! Your plan has been upgraded.")
