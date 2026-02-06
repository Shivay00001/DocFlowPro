"""
Support Panel - Contact & Help
Integrated with Formspree for support requests
"""

import tkinter as tk
from tkinter import ttk, messagebox
import requests
from datetime import datetime
from ui.theme import COLORS, FONTS, SPACING


class SupportPanel(ttk.Frame):
    """Support and help panel with Formspree integration"""
    
    FORMSPREE_ENDPOINT = "https://formspree.io/f/mdkyoyna"
    
    def __init__(self, parent, engine, user_id):
        super().__init__(parent)
        self.frame = self  # For panel switching compatibility
        self.engine = engine
        self.user_id = user_id
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create support panel UI"""
        # Configure background
        self.configure(style='Modern.TFrame')
        
        # Header
        header = tk.Frame(self, bg=COLORS['surface'], height=80)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="💬 Support & Help",
            font=('Segoe UI', 20, 'bold'),
            bg=COLORS['surface'],
            fg=COLORS['text_primary']
        ).pack(side='left', padx=SPACING['lg'], pady=SPACING['lg'])
        
        # Content area
        content = tk.Frame(self, bg=COLORS['background'])
        content.pack(fill='both', expand=True, padx=SPACING['lg'], pady=SPACING['lg'])
        
        # Support form card
        form_card = tk.Frame(content, bg=COLORS['surface'], relief='flat')
        form_card.pack(fill='both', expand=True)
        
        # Card header
        tk.Label(
            form_card,
            text="📧 Contact Support",
            font=('Segoe UI', 16, 'bold'),
            bg=COLORS['surface'],
            fg=COLORS['text_primary']
        ).pack(anchor='w', padx=SPACING['lg'], pady=(SPACING['lg'], SPACING['sm']))
        
        tk.Label(
            form_card,
            text="Have questions or need help? Send us a message!",
            font=('Segoe UI', 10),
            bg=COLORS['surface'],
            fg=COLORS['text_secondary']
        ).pack(anchor='w', padx=SPACING['lg'], pady=(0, SPACING['lg']))
        
        # Form area
        form_area = tk.Frame(form_card, bg=COLORS['surface'])
        form_area.pack(fill='both', expand=True, padx=SPACING['lg'], pady=(0, SPACING['lg']))
        
        # Name field
        self._create_form_field(form_area, "👤 Your Name", "name_entry")
        
        # Email field
        self._create_form_field(form_area, "📧 Email Address", "email_entry")
        
        # Subject field
        self._create_form_field(form_area, "📝 Subject", "subject_entry")
        
        # Message field
        tk.Label(
            form_area,
            text="💬 Message",
            font=('Segoe UI', 11, 'bold'),
            bg=COLORS['surface'],
            fg=COLORS['text_primary']
        ).pack(anchor='w', pady=(SPACING['md'], SPACING['xs']))
        
        self.message_text = tk.Text(
            form_area,
            height=8,
            font=('Segoe UI', 10),
            bg='white',
            fg=COLORS['text_primary'],
            relief='solid',
            borderwidth=1,
            wrap='word',
            padx=10,
            pady=10
        )
        self.message_text.pack(fill='both', expand=True, pady=(0, SPACING['md']))
        
        # Buttons
        btn_frame = tk.Frame(form_card, bg=COLORS['surface'])
        btn_frame.pack(fill='x', padx=SPACING['lg'], pady=(0, SPACING['lg']))
        
        # Send button
        send_btn = tk.Button(
            btn_frame,
            text="📤 Send Message",
            font=('Segoe UI', 11, 'bold'),
            bg=COLORS['accent'],
            fg='white',
            activebackground=COLORS['accent_light'],
            activeforeground='white',
            relief='flat',
            cursor='hand2',
            padx=25,
            pady=10,
            command=self._send_support_request
        )
        send_btn.pack(side='left', padx=(0, SPACING['sm']))
        
        # Clear button
        clear_btn = tk.Button(
            btn_frame,
            text="🔄 Clear Form",
            font=('Segoe UI', 11),
            bg=COLORS['background'],
            fg=COLORS['text_primary'],
            activebackground=COLORS['border'],
            activeforeground=COLORS['text_primary'],
            relief='flat',
            cursor='hand2',
            padx=25,
            pady=10,
            command=self._clear_form
        )
        clear_btn.pack(side='left')
        
        # Status label
        self.status_label = tk.Label(
            btn_frame,
            text="",
            font=('Segoe UI', 10),
            bg=COLORS['surface'],
            fg=COLORS['text_secondary']
        )
        self.status_label.pack(side='right')
        
        # Help section
        help_section = tk.Frame(content, bg=COLORS['surface'], relief='flat')
        help_section.pack(fill='x', pady=(SPACING['md'], 0))
        
        tk.Label(
            help_section,
            text="❓ Frequently Asked Questions",
            font=('Segoe UI', 14, 'bold'),
            bg=COLORS['surface'],
            fg=COLORS['text_primary']
        ).pack(anchor='w', padx=SPACING['md'], pady=(SPACING['md'], SPACING['sm']))
        
        faqs = [
            ("How do I upgrade my plan?", "Go to Settings → View Upgrade Plans to see available options."),
            ("How does data export work?", "Navigate to Export panel, select data type, choose format (PDF/Excel), and click export."),
            ("Can I train custom ML models?", "Yes! Use AI Factory panel to train models on your business data."),
            ("Is my data secure?", "Absolutely! All data is stored locally on your machine with user-specific isolation."),
        ]
        
        faq_content = tk.Frame(help_section, bg=COLORS['surface'])
        faq_content.pack(fill='x', padx=SPACING['lg'], pady=(0, SPACING['md']))
        
        for question, answer in faqs:
            faq_item = tk.Frame(faq_content, bg=COLORS['background'], relief='flat')
            faq_item.pack(fill='x', pady=SPACING['xs'])
            
            tk.Label(
                faq_item,
                text=f"Q: {question}",
                font=('Segoe UI', 10, 'bold'),
                bg=COLORS['background'],
                fg=COLORS['text_primary'],
                anchor='w',
                wraplength=600
            ).pack(fill='x', padx=SPACING['sm'], pady=(SPACING['xs'], 0))
            
            tk.Label(
                faq_item,
                text=f"A: {answer}",
                font=('Segoe UI', 9),
                bg=COLORS['background'],
                fg=COLORS['text_secondary'],
                anchor='w',
                wraplength=600
            ).pack(fill='x', padx=SPACING['sm'], pady=(0, SPACING['xs']))
        
        # Auto-fill user info
        self._auto_fill_user_info()
    
    def _create_form_field(self, parent, label_text, entry_name):
        """Create a form input field"""
        tk.Label(
            parent,
            text=label_text,
            font=('Segoe UI', 11, 'bold'),
            bg=COLORS['surface'],
            fg=COLORS['text_primary']
        ).pack(anchor='w', pady=(SPACING['md'], SPACING['xs']))
        
        entry = tk.Entry(
            parent,
            font=('Segoe UI', 10),
            bg='white',
            fg=COLORS['text_primary'],
            relief='solid',
            borderwidth=1
        )
        entry.pack(fill='x', ipady=8, pady=(0, SPACING['sm']))
        
        setattr(self, entry_name, entry)
    
    def _auto_fill_user_info(self):
        """Auto-fill user name and email"""
        try:
            user_info = self.engine.db.get_user_by_id(self.user_id)
            if user_info:
                self.name_entry.insert(0, user_info.get('full_name', ''))
                self.email_entry.insert(0, user_info.get('email', ''))
        except:
            pass
    
    def _send_support_request(self):
        """Send support request via Formspree"""
        # Get form data
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        subject = self.subject_entry.get().strip()
        message = self.message_text.get('1.0', 'end').strip()
        
        # Validate
        if not all([name, email, subject, message]):
            messagebox.showwarning(
                "Incomplete Form",
                "Please fill in all fields before sending."
            )
            return
        
        # Prepare data
        data = {
            'name': name,
            'email': email,
            'subject': subject,
            'message': message,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'user_id': self.user_id,
            'app_version': 'DocFlow Pro v2.0'
        }
        
        # Update status
        self.status_label.config(text="Sending...", fg=COLORS['info'])
        self.update()
        
        try:
            # Send POST request to Formspree
            response = requests.post(
                self.FORMSPREE_ENDPOINT,
                data=data,
                headers={'Accept': 'application/json'},
                timeout=10
            )
            
            if response.status_code == 200:
                self.status_label.config(text="✓ Sent successfully!", fg=COLORS['success'])
                
                messagebox.showinfo(
                    "Message Sent! ✅",
                    "Thank you for contacting us!\n\n"
                    "We've received your message and will get back to you soon."
                )
                
                # Clear form
                self._clear_form(keep_user_info=True)
            else:
                raise Exception(f"Server returned status {response.status_code}")
                
        except Exception as e:
            self.status_label.config(text="✗ Failed to send", fg=COLORS['error'])
            
            messagebox.showerror(
                "Send Failed",
                f"Could not send message:\n{str(e)}\n\n"
                "Please check your internet connection and try again."
            )
    
    def _clear_form(self, keep_user_info=False):
        """Clear all form fields"""
        if not keep_user_info:
            self.name_entry.delete(0, 'end')
            self.email_entry.delete(0, 'end')
        
        self.subject_entry.delete(0, 'end')
        self.message_text.delete('1.0', 'end')
        self.status_label.config(text="")
        
        if not keep_user_info:
            self._auto_fill_user_info()
    
    def refresh(self):
        """Refresh panel"""
        pass
