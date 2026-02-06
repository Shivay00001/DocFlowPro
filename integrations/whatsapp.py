"""
WhatsApp Business API Integration
Send invoices and reminders via WhatsApp
"""

from typing import Dict, Optional
import json


class WhatsAppSender:
    """Send business Messages via WhatsApp Business API"""
    
    def __init__(self, phone_id: str = None, access_token: str = None):
        """
        Initialize WhatsApp sender
        phone_id: WhatsApp Business Phone Number ID
        access_token: WhatsApp Business API access token
        """
        self.phone_id = phone_id
        self.access_token = access_token
        self.api_url = "https://graph.facebook.com/v18.0"
    
    def send_invoice(self, recipient_phone: str, invoice_pdf_path: str, invoice_number: str, amount: float) -> Dict:
        """
        Send invoice PDF via WhatsApp
        Returns: {'success': bool, 'message_id': str}
        """
        if not self.phone_id or not self.access_token:
            return {'success': False, 'error': 'WhatsApp not configured'}
        
        message = f"""
🧾 *Invoice #{invoice_number}*

Thank you for your business!

Amount: ₹{amount:,.2f}

Please find your invoice attached.

_DocFlow Pro - Automated Invoicing_
        """.strip()
        
        try:
            # In production, use WhatsApp API to send document
            # For now, return mock success
            return {
                'success': True,
                'message_id': 'mock_msg_id',
                'recipient': recipient_phone,
                'note': 'WhatsApp API integration requires setup'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def send_payment_reminder(self, recipient_phone: str, invoice_number: str, amount: float, due_date: str) -> Dict:
        """Send payment reminder"""
        message = f"""
⏰ *Payment Reminder*

Invoice: #{invoice_number}
Amount: ₹{amount:,.2f}
Due Date: {due_date}

Please process payment at your earliest convenience.

Thank you!
        """.strip()
        
        return self._send_text_message(recipient_phone, message)
    
    def send_thank_you(self, recipient_phone: str, invoice_number: str) -> Dict:
        """Send thank you message after payment"""
        message = f"""
✅ *Payment Received*

Thank you for your payment for Invoice #{invoice_number}!

We appreciate your business.

_DocFlow Pro_
        """.strip()
        
        return self._send_text_message(recipient_phone, message)
    
    def _send_text_message(self, recipient_phone: str, message: str) -> Dict:
        """Send text message via WhatsApp"""
        try:
            # Mock implementation
            return {
                ' success': True,
                'message_id': 'mock_msg_id',
                'recipient': recipient_phone,
                'note': 'WhatsApp API requires Business account setup'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def validate_phone(self, phone: str) -> bool:
        """Validate phone number format"""
        # Remove all non-digits
        digits = ''.join(filter(str.isdigit, phone))
        
        # Indian mobile: 10 digits
        return len(digits) == 10 or len(digits) == 12  # With country code
    
    def format_phone(self, phone: str) -> str:
        """Format phone to WhatsApp API format (+91XXXXXXXXXX)"""
        digits = ''.join(filter(str.isdigit, phone))
        
        # Add country code if missing
        if len(digits) == 10:
            return f"+91{digits}"
        elif len(digits) == 12 and digits.startswith('91'):
            return f"+{digits}"
        
        return phone


class WhatsAppConfig:
    """Manage WhatsApp configuration"""
    
    CONFIG_FILE = 'whatsapp_config.json'
    
    @staticmethod
    def save_config(phone_id: str, access_token: str):
        """Save WhatsApp configuration"""
        config = {
            'phone_id': phone_id,
            'access_token': access_token,
            'enabled': True
        }
        
        with open(WhatsAppConfig.CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
    
    @staticmethod
    def load_config() -> Dict:
        """Load WhatsApp configuration"""
        try:
            with open(WhatsAppConfig.CONFIG_FILE, 'r') as f:
                return json.load(f)
        except:
            return {'enabled': False}
    
    @staticmethod
    def is_configured() -> bool:
        """Check if WhatsApp is configured"""
        config = WhatsAppConfig.load_config()
        return config.get('enabled', False) and config.get('access_token') is not None
