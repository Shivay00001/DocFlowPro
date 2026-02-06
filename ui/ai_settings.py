"""
AI Settings Panel
Configure AI API keys and integrations
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json


class AISettingsPanel(ttk.Frame):
    """AI API configuration and settings"""
    
    def __init__(self, parent, engine, user_id):
        super().__init__(parent)
        self.frame = self  # For panel switching compatibility
        self.engine = engine
        self.user_id = user_id
        
        self._create_widgets()
        self._load_settings()
    
    def _create_widgets(self):
        """Create AI settings interface"""
        # Title
        title_frame = ttk.Frame(self)
        title_frame.pack(fill='x', padx=20, pady=(20, 10))
        
        ttk.Label(
            title_frame,
            text="⚙️ AI Settings",
            font=('Helvetica', 16, 'bold')
        ).pack(side='left')
        
        ttk.Label(
            title_frame,
            text="Configure external AI API integrations",
            font=('Helvetica', 9),
            foreground='#666'
        ).pack(side='left', padx=(10, 0))
        
        # Content
        content = ttk.Frame(self)
        content.pack(fill='both', expand=True, padx=20, pady=10)
        
        # AI Provider selection
        provider_frame = ttk.LabelFrame(content, text="🤖 AI Provider", padding=15)
        provider_frame.pack(fill='x', pady=(0, 15))
        
        ttk.Label(provider_frame, text="Select AI Provider:", font=('Helvetica', 10, 'bold')).pack(anchor='w', pady=(0, 5))
        
        self.provider_var = tk.StringVar(value="none")
        
        providers = [
            ("OpenAI (GPT-3.5, GPT-4)", "openai"),
            ("Anthropic (Claude)", "anthropic"),
            ("Google (Gemini)", "google"),
            ("None (Disabled)", "none")
        ]
        
        for text, value in providers:
            ttk.Radiobutton(
                provider_frame,
                text=text,
                variable=self.provider_var,
                value=value
            ).pack(anchor='w', pady=2)
        
        # API Key entry
        key_frame = ttk.LabelFrame(content, text="🔑 API Configuration", padding=15)
        key_frame.pack(fill='x', pady=(0, 15))
        
        ttk.Label(key_frame, text="API Key:").grid(row=0, column=0, sticky='w', pady=5)
        self.api_key_entry = ttk.Entry(key_frame, width=50, show='*')
        self.api_key_entry.grid(row=0, column=1, sticky='ew', padx=(10, 0), pady=5)
        
        ttk.Button(
            key_frame,
            text="👁️ Show",
            command=self._toggle_key_visibility,
            width=8
        ).grid(row=0, column=2, padx=(5, 0))
        
        key_frame.columnconfigure(1, weight=1)
        
        # Save button
        ttk.Button(
            key_frame,
            text="💾 Save Settings",
            command=self._save_settings
        ).grid(row=1, column=0, columnspan=3, pady=(10, 0))
        
        # Usage tracking
        usage_frame = ttk.LabelFrame(content, text="📊 API Usage", padding=15)
        usage_frame.pack(fill='x', pady=(0, 15))
        
        self.usage_label = ttk.Label(
            usage_frame,
            text="No API usage yet",
            font=('Helvetica', 10)
        )
        self.usage_label.pack(anchor='w')
        
        # Test connection
        test_frame = ttk.LabelFrame(content, text="🔧 Test Connection", padding=15)
        test_frame.pack(fill='x')
        
        ttk.Button(
            test_frame,
            text="🧪 Test API Connection",
            command=self._test_connection
        ).pack()
        
        self.test_result_label = ttk.Label(test_frame, text="", foreground='#666')
        self.test_result_label.pack(pady=(10, 0))
    
    def _load_settings(self):
        """Load saved AI settings"""
        try:
            from integrations.ai_apis import AIAPIManager
            
            ai_manager = AIAPIManager()
            config = ai_manager.get_current_config()
            
            if config.get('enabled'):
                self.provider_var.set(config.get('provider', 'none'))
                # Don't show actual API key for security
                if config.get('api_key_masked'):
                    self.api_key_entry.insert(0, config['api_key_masked'])
                    self.usage_label.config(
                        text=f"✓ AI enabled: {config.get('provider', 'Unknown').upper()}"
                    )
        except:
            pass
    
    def _save_settings(self):
        """Save AI settings"""
        provider = self.provider_var.get()
        api_key = self.api_key_entry.get().strip()
        
        if provider == "none":
            messagebox.showinfo("Info", "AI integration disabled")
            return
        
        if not api_key or api_key.startswith('*'):
            messagebox.showwarning("Missing Key", "Please enter a valid API key")
            return
        
        try:
            from integrations.ai_apis import AIAPIManager
            
            ai_manager = AIAPIManager()
            success = ai_manager.set_api_key(provider, api_key)
            
            if success:
                messagebox.showinfo(
                    "Success",
                    f"✓ AI settings saved!\n\nProvider: {provider.upper()}\n\n"
                    "You can now use AI features in the app."
                )
                self.usage_label.config(text=f"✓ AI enabled: {provider.upper()}")
            else:
                messagebox.showerror("Error", "Failed to save settings")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {str(e)}")
    
    def _toggle_key_visibility(self):
        """Toggle API key visibility"""
        if self.api_key_entry.cget('show') == '*':
            self.api_key_entry.config(show='')
        else:
            self.api_key_entry.config(show='*')
    
    def _test_connection(self):
        """Test API connection"""
        self.test_result_label.config(text="Testing connection...")
        self.update()
        
        try:
            from integrations.ai_apis import AIAPIManager
            
            ai_manager = AIAPIManager()
            result = ai_manager.test_connection()
            
            if result.get('success'):
                self.test_result_label.config(
                    text="✓ Connection successful!",
                    foreground='green'
                )
                messagebox.showinfo("Success", "AI API connection working!")
            else:
                self.test_result_label.config(
                    text=f"✗ {result.get('error', 'Connection failed')}",
                    foreground='red'
                )
                messagebox.showerror("Error", result.get('error', 'Connection failed'))
                
        except Exception as e:
            self.test_result_label.config(text=f"✗ Error: {str(e)}", foreground='red')
            messagebox.showerror("Error", f"Test failed: {str(e)}")
    
    def refresh(self):
        """Refresh settings"""
        self._load_settings()
