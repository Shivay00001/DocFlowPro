"""
Upgrade Panel - Plan subscriptions with Razorpay
"""

import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
from payments.razorpay_handler import RazorpayPaymentHandler, PaymentRecordManager
from ui.theme import COLORS, FONTS, SPACING


class UpgradePanel(ttk.Frame):
    """Plan upgrade panel with Razorpay payment"""
    
    def __init__(self, parent, engine, user_id):
        super().__init__(parent)
        self.frame = self  # For panel switching compatibility
        self.engine = engine
        self.user_id = user_id
        self.payment_handler = RazorpayPaymentHandler()
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create upgrade panel UI"""
        # Header
        header = tk.Frame(self, bg=COLORS['surface'], height=80)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="💳 Upgrade Plan",
            font=('Segoe UI', 20, 'bold'),
            bg=COLORS['surface'],
            fg=COLORS['text_primary']
        ).pack(side='left', padx=SPACING['lg'], pady=SPACING['lg'])
        
        # Content
        content = tk.Frame(self, bg=COLORS['background'])
        content.pack(fill='both', expand=True, padx=SPACING['lg'], pady=SPACING['lg'])
        
        # Current plan info
        current_frame = tk.Frame(content, bg=COLORS['surface'], relief='flat')
        current_frame.pack(fill='x', pady=(0, SPACING['lg']))
        
        tk.Label(
            current_frame,
            text="📊 Current Plan",
            font=('Segoe UI', 14, 'bold'),
            bg=COLORS['surface'],
            fg=COLORS['text_primary']
        ).pack(anchor='w', padx=SPACING['md'], pady=(SPACING['md'], SPACING['sm']))
        
        license_info = self.engine.get_my_license_info()
        
        tk.Label(
            current_frame,
            text=f"Plan: {license_info.get('plan_name', 'Free Plan')}",
            font=('Segoe UI', 11),
            bg=COLORS['surface'],
            fg=COLORS['text_primary']
        ).pack(anchor='w', padx=SPACING['lg'], pady=2)
        
        if license_info.get('expires_at'):
            tk.Label(
                current_frame,
                text=f"Expires: {license_info['expires_at']}",
                font=('Segoe UI', 11),
                bg=COLORS['surface'],
                fg=COLORS['text_secondary']
            ).pack(anchor='w', padx=SPACING['lg'], pady=(0, SPACING['md']))
        
        # Plans grid
        plans_title = tk.Label(
            content,
            text="🚀 Choose Your Plan",
            font=('Segoe UI', 16, 'bold'),
            bg=COLORS['background'],
            fg=COLORS['text_primary']
        )
        plans_title.pack(anchor='w', pady=(0, SPACING['md']))
        
        plans_container = tk.Frame(content, bg=COLORS['background'])
        plans_container.pack(fill='both', expand=True)
        
        # Plan cards
        plans = [
            ('starter', '🌟 Starter', COLORS['info']),
            ('professional', '⭐ Professional', COLORS['accent']),
            ('enterprise', '💎 Enterprise', COLORS['primary']),
            ('lifetime', '♾️ Lifetime', COLORS['warning'])
        ]
        
        for idx, (plan_id, plan_title, color) in enumerate(plans):
            self._create_plan_card(plans_container, plan_id, plan_title, color, idx)
    
    def _create_plan_card(self, parent, plan_id, title, color, index):
        """Create a plan card"""
        card = tk.Frame(parent, bg=COLORS['surface'], relief='solid', borderwidth=1)
        card.grid(row=index//2, column=index%2, padx=SPACING['sm'], pady=SPACING['sm'], sticky='nsew')
        
        # Configure grid
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)
        parent.grid_rowconfigure(index//2, weight=1)
        
        # Header with color
        header = tk.Frame(card, bg=color, height=60)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text=title,
            font=('Segoe UI', 16, 'bold'),
            bg=color,
            fg='white'
        ).pack(expand=True)
        
        # Content
        content = tk.Frame(card, bg=COLORS['surface'])
        content.pack(fill='both', expand=True, padx=SPACING['md'], pady=SPACING['md'])
        
        # Price
        plan_info = self.payment_handler.get_plan_info(plan_id)
        price_text = self.payment_handler.format_price(plan_info['price'])
        
        if plan_id == 'lifetime':
            price_label = f"{price_text} (One-time)"
        else:
            price_label = f"{price_text}/month"
        
        tk.Label(
            content,
            text=price_label,
            font=('Segoe UI', 18, 'bold'),
            bg=COLORS['surface'],
            fg=color
        ).pack(pady=(0, SPACING['sm']))
        
        # Features
        for feature in plan_info['features'][:4]:  # Show first 4
            feature_frame = tk.Frame(content, bg=COLORS['surface'])
            feature_frame.pack(fill='x', pady=2)
            
            tk.Label(
                feature_frame,
                text="✓",
                font=('Segoe UI', 10),
                bg=COLORS['surface'],
                fg=COLORS['success']
            ).pack(side='left', padx=(0, 5))
            
            tk.Label(
                feature_frame,
                text=feature,
                font=('Segoe UI', 9),
                bg=COLORS['surface'],
                fg=COLORS['text_secondary'],
                anchor='w'
            ).pack(side='left', fill='x')
        
        # Upgrade button
        btn = tk.Button(
            content,
            text="🚀 Upgrade Now",
            font=('Segoe UI', 10, 'bold'),
            bg=color,
            fg='white',
            activebackground=color,
            activeforeground='white',
            relief='flat',
            cursor='hand2',
            padx=20,
            pady=8,
            command=lambda: self._initiate_payment(plan_id)
        )
        btn.pack(pady=(SPACING['md'], 0))
    
    def _initiate_payment(self, plan_id):
        """Initiate Razorpay payment"""
        # Get user info
        user_info = self.engine.db.get_user_by_id(self.user_id)
        user_email = user_info.get('email', '')
        user_name = user_info.get('full_name', '')
        
        if not user_email:
            messagebox.showerror(
                "Email Required",
                "Please update your email in user profile before upgrading."
            )
            return
        
        # Get plan info
        plan_info = self.payment_handler.get_plan_info(plan_id)
        
        # Confirm
        confirm = messagebox.askyesno(
            "Confirm Upgrade",
            f"Upgrade to {plan_info['name']}?\n\n"
            f"Price: {self.payment_handler.format_price(plan_info['price'])}\n\n"
            "You will be redirected to Razorpay payment gateway."
        )
        
        if not confirm:
            return
        
        # Create payment order
        result = self.payment_handler.create_payment_order(
            plan_id, user_email, user_name
        )
        
        if not result['success']:
            messagebox.showerror(
                "Payment Error",
                f"Could not create payment order:\n{result['error']}"
            )
            return
        
        # Show payment details and open Razorpay
        order_id = result['order_id']
        amount_inr = result['amount'] / 100
        
        # Payment URL (Razorpay hosted checkout)
        payment_url = self._generate_razorpay_checkout_url(
            order_id, amount_inr, user_email, user_name, plan_info['name']
        )
        
        messagebox.showinfo(
            "Payment Initiated",
            f"Order ID: {order_id}\n"
            f"Amount: ₹{amount_inr:,.0f}\n\n"
            "Opening Razorpay payment gateway...\n\n"
            "After payment, contact support with Order ID to activate your plan."
        )
        
        # Open browser
        webbrowser.open(payment_url)
        
        # Save pending order
        PaymentRecordManager.save_payment_record({
            'user_id': self.user_id,
            'order_id': order_id,
            'plan_id': plan_id,
            'amount': result['amount'],
            'status': 'pending',
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    
    def _generate_razorpay_checkout_url(self, order_id, amount, email, name, description):
        """Generate Razorpay checkout URL"""
        # Note: In production, you'd use Razorpay Checkout.js in a proper web form
        # For now, providing a payment link
        
        base_url = "https://razorpay.com/payment-button"
        # This is simplified - actual implementation would use Razorpay's hosted checkout
        
        return f"https://razorpay.com/?order_id={order_id}"
    
    def refresh(self):
        """Refresh panel"""
        pass


from datetime import datetime
