"""
Simple Working Main Window - No Fancy Gradients
"""

import tkinter as tk
from tkinter import ttk, messagebox
from ui.dashboard import DashboardPanel
from ui.documents import DocumentsPanel
from ui.invoices import InvoicesPanel
from ui.export import ExportPanel
from ui.ai_factory import AIDataFactoryPanel
from ui.business_intelligence import BusinessIntelligencePanel
from ui.data_cleaning import DataCleaningPanel
from ui.ai_settings import AISettingsPanel
from ui.regulatory_helper import RegulatoryHelperPanel
from ui.support import SupportPanel
from core.session_manager import get_session_manager
from config.session_config import CHECK_INTERVAL_SECONDS


class MainWindow:
    """Simple working main window"""
    
    def __init__(self, engine, user_id):
        self.engine = engine
        self.user_id = user_id
        self.engine.set_current_user(user_id)
        
        # Get session manager
        self.session_manager = get_session_manager()
        self.session_timeout_job = None
        
        self.window = tk.Tk()
        self.window.withdraw()  # Hide main window initially
        self.window.title("DocFlow Pro")
        self.window.geometry("1200x800")
        self.window.protocol("WM_DELETE_WINDOW", self._on_closing)
        
        # Bind activity tracking
        self.window.bind("<Key>", self._track_activity)
        self.window.bind("<Button>", self._track_activity)
        
        self._setup_window()
        self._create_ui()
        
        # Show dashboard by default
        self.show_panel('dashboard')
    
    def _setup_window(self):
        """Setup main window"""
        
        # Center window
        self.window.update_idletasks()
        width = 1400
        height = 800
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
        
        self.window.configure(bg='#f5f7fa')
    
    def _create_ui(self):
        """Create simple UI"""
        # Header
        header = tk.Frame(self.window, bg='#1a237e', height=60)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="🏭 DocFlow Pro v2.0 - AI Data Factory",
            font=('Segoe UI', 18, 'bold'),
            bg='#1a237e',
            fg='white'
        ).pack(side='left', padx=20, pady=15)
        
        # Get user info
        license_info = self.engine.get_my_license_info()
        plan_name = license_info.get('plan_name', 'Free Plan')
        
        tk.Label(
            header,
            text=f"Plan: {plan_name}",
            font=('Segoe UI', 10),
            bg='#1a237e',
            fg='white'
        ).pack(side='right', padx=20)
        
        # Main container
        main_container = tk.Frame(self.window, bg='#f5f7fa')
        main_container.pack(fill='both', expand=True)
        
        # Sidebar
        sidebar = tk.Frame(main_container, width=200, bg='white', relief='solid', borderwidth=1)
        sidebar.pack(side='left', fill='y')
        sidebar.pack_propagate(False)
        
        tk.Label(
            sidebar,
            text="Navigation",
            font=('Segoe UI', 12, 'bold'),
            bg='white',
            fg='#333'
        ).pack(pady=15)
        
        # Navigation buttons
        nav_area = tk.Frame(sidebar, bg='white')
        nav_area.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.nav_buttons = {}
        
        buttons = [
            ('📊', 'Dashboard', 'dashboard'),
            ('📄', 'Documents', 'documents'),
            ('🧾', 'Invoices', 'invoices'),
            ('📤', 'Export', 'export'),
            ('🏭', 'AI Factory', 'ai_factory'),
            ('📈', 'BI Analytics', 'bi'),
            ('🧹', 'Data Cleaning', 'cleaning'),
            ('🤖', 'AI Settings', 'ai_settings'),
            ('📚', 'Compliance', 'regulatory'),
            ('💬', 'Support', 'support'),
            ('⚙️', 'Settings', 'settings'),
        ]
        
        for icon, text, panel_id in buttons:
            btn = tk.Button(
                nav_area,
                text=f"{icon} {text}",
                font=('Segoe UI', 10),
                bg='white',
                fg='#333',
                activebackground='#e3f2fd',
                relief='flat',
                cursor='hand2',
                anchor='w',
                padx=10,
                pady=10,
                command=lambda p=panel_id: self.show_panel(p)
            )
            btn.pack(fill='x', pady=2)
            self.nav_buttons[panel_id] = btn
        
        # Content area
        self.content_frame = tk.Frame(main_container, bg='#f5f7fa')
        self.content_frame.pack(side='right', fill='both', expand=True)
        
        # Initialize all panels
        self.panels = {
            'dashboard': DashboardPanel(self.content_frame, self.engine, self.user_id),
            'documents': DocumentsPanel(self.content_frame, self.engine, self.user_id),
            'invoices': InvoicesPanel(self.content_frame, self.engine, self.user_id),
            'export': ExportPanel(self.content_frame, self.engine, self.user_id),
            'ai_factory': AIDataFactoryPanel(self.content_frame, self.engine, self.user_id),
            'bi': BusinessIntelligencePanel(self.content_frame, self.engine, self.user_id),
            'cleaning': DataCleaningPanel(self.content_frame, self.engine, self.user_id),
            'ai_settings': AISettingsPanel(self.content_frame, self.engine, self.user_id),
            'regulatory': RegulatoryHelperPanel(self.content_frame, self.engine, self.user_id),
            'support': SupportPanel(self.content_frame, self.engine, self.user_id),
        }
        
        # Settings panel
        self.panels['settings'] = self._create_settings_panel()
    
    def _create_settings_panel(self):
        """Create simple settings panel"""
        panel = tk.Frame(self.content_frame, bg='#f5f7fa')
        
        # Header
        header = tk.Frame(panel, bg='white', height=80)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="⚙️ Settings",
            font=('Segoe UI', 20, 'bold'),
            bg='white',
            fg='#333'
        ).pack(side='left', padx=20, pady=20)
        
        # Content
        content_frame = tk.Frame(panel, bg='#f5f7fa')
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # License info card
        license_card = tk.Frame(content_frame, bg='white', relief='solid', borderwidth=1)
        license_card.pack(fill='x', pady=(0, 15))
        
        tk.Label(
            license_card,
            text="💳 License Information",
            font=('Segoe UI', 14, 'bold'),
            bg='white',
            fg='#333'
        ).pack(anchor='w', padx=15, pady=(15, 10))
        
        license_info = self.engine.get_my_license_info()
        
        info_frame = tk.Frame(license_card, bg='white')
        info_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        tk.Label(
            info_frame,
            text=f"Plan: {license_info.get('plan_name', 'Free Plan')}",
            font=('Segoe UI', 11),
            bg='white',
            fg='#333'
        ).pack(anchor='w', pady=3)
        
        tk.Label(
            info_frame,
            text=f"Status: {license_info.get('status', 'active').upper()}",
            font=('Segoe UI', 11),
            bg='white',
            fg='#27ae60'
        ).pack(anchor='w', pady=3)
        
        # About card
        about_card = tk.Frame(content_frame, bg='white', relief='solid', borderwidth=1)
        about_card.pack(fill='x')
        
        tk.Label(
            about_card,
            text="ℹ️ About DocFlow Pro",
            font=('Segoe UI', 14, 'bold'),
            bg='white',
            fg='#333'
        ).pack(anchor='w', padx=15, pady=(15, 10))
        
        about_text = """DocFlow Pro v2.0 - AI Data Factory
Enterprise Document Management + Business Intelligence

✨ Core Features:
• Document & Invoice Management
• ML-Powered Analytics  
• Sales Predictions & Forecasting
• Anomaly Detection
• Data Cleaning Engine
• GST/TDS Compliance Helper
• AI Integration (OpenAI/Claude/Gemini)
• Support System
• Payment Integration"""
        
        tk.Label(
            about_card,
            text=about_text,
            font=('Segoe UI', 10),
            bg='white',
            fg='#666',
            justify='left'
        ).pack(anchor='w', padx=15, pady=(0, 15))
        
        return panel
    
    def show_panel(self, panel_id):
        """Show a specific panel"""
        # Hide all panels
        for panel in self.panels.values():
            if hasattr(panel, 'frame'):
                panel.frame.pack_forget()
            elif hasattr(panel, 'pack_forget'):
                panel.pack_forget()
        
        # Show requested panel
        if panel_id in self.panels:
            panel = self.panels[panel_id]
            if hasattr(panel, 'frame'):
                panel.frame.pack(fill='both', expand=True, padx=20, pady=20)
            else:
                panel.pack(fill='both', expand=True, padx=20, pady=20)
        else:
            # Default to dashboard
            if hasattr(self.panels['dashboard'], 'frame'):
                self.panels['dashboard'].frame.pack(fill='both', expand=True, padx=20, pady=20)
    
    def _track_activity(self, event=None):
        """Track user activity for session timeout"""
        if self.session_manager.is_session_active():
            self.session_manager.refresh_activity()
    
    def _check_session_timeout(self):
        """Check if session has timed out"""
        timed_out, warning, remaining = self.session_manager.check_timeout()
        
        if timed_out:
            # Session timed out - logout
            self._handle_session_timeout()
            return  # Don't reschedule
        
        if warning and remaining > 0:
            # Show warning
            self._show_timeout_warning(remaining)
        
        # Schedule next check
        self.session_timeout_job = self.window.after(
            CHECK_INTERVAL_SECONDS * 1000, 
            self._check_session_timeout
        )
    
    def _show_timeout_warning(self, remaining_seconds):
        """Show timeout warning dialog"""
        minutes = remaining_seconds // 60
        seconds = remaining_seconds % 60
        
        result = messagebox.askquestion(
            "Session Timeout Warning",
            f"Your session will expire in {minutes}m {seconds}s due to inactivity.\n\n"
            "Click Yes to continue working, or No to logout now.",
            icon='warning'
        )
        
        if result == 'yes':
            self.session_manager.extend_session()
        else:
            self._handle_session_timeout()
    
    def _handle_session_timeout(self):
        """Handle session timeout - logout user"""
        self.session_manager.end_session()
        
        messagebox.showinfo(
            "Session Expired",
            "Your session has expired due to inactivity.\n"
            "The application will now close for security."
        )
        
        self.window.quit()
        self.window.destroy()
    
    def _on_closing(self):
        """Handle window close"""
        if self.session_timeout_job:
            self.window.after_cancel(self.session_timeout_job)
        
        self.session_manager.end_session()
        self.window.quit()
        self.window.destroy()
    
    def run(self):
        """Start the main event loop"""
        self.window.deiconify()  # Show window
        
        # Start session timeout checker
        self._check_session_timeout()
        
        self.window.mainloop()
