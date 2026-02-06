"""
Modern Login & Registration Window
Clear, beautiful, and user-friendly authentication
"""

import tkinter as tk
from tkinter import ttk, messagebox
import hashlib
from datetime import datetime
from ui.theme import COLORS, FONTS, SPACING, RADIUS
from ui.modern_components import GradientFrame, ModernButton


class LoginWindow:
    """Modern login window with gradient design"""
    
    def __init__(self, db_manager):
        self.db = db_manager
        self.user_id = None
        
        self.window = tk.Tk()
        self._setup_window()
        self._create_ui()
    
    def _setup_window(self):
        """Setup login window"""
        self.window.title("DocFlow Pro - Login")
        self.window.geometry("500x650")
        self.window.resizable(False, False)
        
        # Center window
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - 250
        y = (self.window.winfo_screenheight() // 2) - 325
        self.window.geometry(f"500x650+{x}+{y}")
        
        # Set background
        self.window.configure(bg=COLORS['background'])
    
    def _create_ui(self):
        """Create modern login UI"""
        # Header with gradient
        header = GradientFrame(
            self.window,
            width=500,
            height=120,
            color1=COLORS['gradient_start'],
            color2=COLORS['gradient_end']
        )
        header.pack(fill='x')
        
        # Logo and title in header
        logo_container = tk.Frame(header, bg=COLORS['gradient_start'])
        logo_container.place(relx=0.5, rely=0.5, anchor='center')
        
        tk.Label(
            logo_container,
            text="🏭",
            font=('Segoe UI', 48),
            bg=COLORS['gradient_start'],
            fg='white'
        ).pack()
        
        tk.Label(
            logo_container,
            text="DocFlow Pro",
            font=('Segoe UI', 20, 'bold'),
            bg=COLORS['gradient_start'],
            fg='white'
        ).pack()
        
        tk.Label(
            logo_container,
            text="AI Data Factory v2.0",
            font=('Segoe UI', 10),
            bg=COLORS['gradient_start'],
            fg='white'
        ).pack()
        
        # Main content area
        content = tk.Frame(self.window, bg=COLORS['background'])
        content.pack(fill='both', expand=True, padx=40, pady=30)
        
        # Check if first time setup
        cursor = self.db.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        
        if user_count == 0:
            self._create_first_time_setup(content)
        else:
            self._create_login_form(content)
    
    def _create_first_time_setup(self, parent):
        """Create first-time setup form"""
        # Welcome message
        welcome_frame = tk.Frame(parent, bg=COLORS['surface'], relief='flat')
        welcome_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(
            welcome_frame,
            text="👋 Welcome to DocFlow Pro!",
            font=('Segoe UI', 18, 'bold'),
            bg=COLORS['surface'],
            fg=COLORS['text_primary']
        ).pack(pady=(20, 10))
        
        tk.Label(
            welcome_frame,
            text="Let's create your admin account",
            font=('Segoe UI', 11),
            bg=COLORS['surface'],
            fg=COLORS['text_secondary']
        ).pack(pady=(0, 20))
        
        # Registration form
        form_frame = tk.Frame(parent, bg=COLORS['surface'], relief='flat')
        form_frame.pack(fill='both', expand=True)
        
        # Form title
        tk.Label(
            form_frame,
            text="Create Admin Account",
            font=('Segoe UI', 14, 'bold'),
            bg=COLORS['surface'],
            fg=COLORS['text_primary']
        ).pack(pady=(20, 20))
        
        # Full Name
        self._create_form_field(
            form_frame,
            "👤 Full Name",
            "Enter your full name"
        )
        self.fullname_entry = self.entry_widget
        
        # Username
        self._create_form_field(
            form_frame,
            "✨ Username",
            "Choose a username"
        )
        self.username_entry = self.entry_widget
        
        # Email
        self._create_form_field(
            form_frame,
            "📧 Email",
            "your.email@example.com"
        )
        self.email_entry = self.entry_widget
        
        # Password
        self._create_form_field(
            form_frame,
            "🔒 Password",
            "Create a strong password",
            show='●'
        )
        self.password_entry = self.entry_widget
        
        # Confirm Password
        self._create_form_field(
            form_frame,
            "✅ Confirm Password",
            "Re-enter your password",
            show='●'
        )
        self.confirm_password_entry = self.entry_widget
        
        # Register button
        btn_frame = tk.Frame(form_frame, bg=COLORS['surface'])
        btn_frame.pack(pady=(20, 20))
        
        register_btn = tk.Button(
            btn_frame,
            text="🚀 Create Account",
            font=('Segoe UI', 12, 'bold'),
            bg=COLORS['accent'],
            fg='white',
            activebackground=COLORS['accent_light'],
            activeforeground='white',
            relief='flat',
            cursor='hand2',
            padx=30,
            pady=12,
            command=self._register_user
        )
        register_btn.pack()
        
        # Bind enter key
        self.window.bind('<Return>', lambda e: self._register_user())
    
    def _create_login_form(self, parent):
        """Create login form"""
        # Title
        title_frame = tk.Frame(parent, bg=COLORS['surface'], relief='flat')
        title_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(
            title_frame,
            text="🔐 Sign In",
            font=('Segoe UI', 18, 'bold'),
            bg=COLORS['surface'],
            fg=COLORS['text_primary']
        ).pack(pady=(20, 10))
        
        tk.Label(
            title_frame,
            text="Welcome back! Please sign in to continue",
            font=('Segoe UI', 10),
            bg=COLORS['surface'],
            fg=COLORS['text_secondary']
        ).pack(pady=(0, 20))
        
        # Login form
        form_frame = tk.Frame(parent, bg=COLORS['surface'], relief='flat')
        form_frame.pack(fill='both', expand=True)
        
        # Username
        self._create_form_field(
            form_frame,
            "👤 Username",
            "Enter your username"
        )
        self.username_entry = self.entry_widget
        
        # Password
        self._create_form_field(
            form_frame,
            "🔒 Password",
            "Enter your password",
            show='●'
        )
        self.password_entry = self.entry_widget
        
        # Login button
        btn_frame = tk.Frame(form_frame, bg=COLORS['surface'])
        btn_frame.pack(pady=(30, 20))
        
        login_btn = tk.Button(
            btn_frame,
            text="✨ Sign In",
            font=('Segoe UI', 12, 'bold'),
            bg=COLORS['primary'],
            fg='white',
            activebackground=COLORS['primary_light'],
            activeforeground='white',
            relief='flat',
            cursor='hand2',
            padx=40,
            pady=12,
            command=self._login_user
        )
        login_btn.pack()
        
        # Info text
        info_frame = tk.Frame(form_frame, bg=COLORS['surface'])
        info_frame.pack(pady=(20, 20))
        
        tk.Label(
            info_frame,
            text="💡 Tip: DocFlow Pro uses single-user mode",
            font=('Segoe UI', 9),
            bg=COLORS['surface'],
            fg=COLORS['text_hint']
        ).pack()
        
        # Bind enter key
        self.window.bind('<Return>', lambda e: self._login_user())
    
    def _create_form_field(self, parent, label, placeholder, show=None):
        """Create a modern form field"""
        field_frame = tk.Frame(parent, bg=COLORS['surface'])
        field_frame.pack(fill='x', padx=30, pady=8)
        
        # Label
        tk.Label(
            field_frame,
            text=label,
            font=('Segoe UI', 10, 'bold'),
            bg=COLORS['surface'],
            fg=COLORS['text_primary'],
            anchor='w'
        ).pack(fill='x', pady=(0, 5))
        
        # Entry with modern styling
        entry = tk.Entry(
            field_frame,
            font=('Segoe UI', 11),
            bg='white',
            fg=COLORS['text_primary'],
            relief='solid',
            borderwidth=1,
            highlightthickness=2,
            highlightbackground=COLORS['border'],
            highlightcolor=COLORS['accent'],
            show=show
        )
        entry.pack(fill='x', ipady=8)
        entry.insert(0, placeholder)
        entry.config(fg=COLORS['text_hint'])
        
        # Focus events for placeholder
        def on_focus_in(event):
            if entry.get() == placeholder:
                entry.delete(0, 'end')
                entry.config(fg=COLORS['text_primary'])
        
        def on_focus_out(event):
            if not entry.get():
                entry.insert(0, placeholder)
                entry.config(fg=COLORS['text_hint'])
        
        entry.bind('<FocusIn>', on_focus_in)
        entry.bind('<FocusOut>', on_focus_out)
        
        # Store reference
        self.entry_widget = entry
    
    def _get_entry_value(self, entry, placeholder):
        """Get entry value or empty string if placeholder"""
        value = entry.get()
        return '' if value == placeholder else value
    
    def _register_user(self):
        """Register new user"""
        # Get values
        fullname = self._get_entry_value(self.fullname_entry, "Enter your full name")
        username = self._get_entry_value(self.username_entry, "Choose a username")
        email = self._get_entry_value(self.email_entry, "your.email@example.com")
        password = self._get_entry_value(self.password_entry, "Create a strong password")
        confirm = self._get_entry_value(self.confirm_password_entry, "Re-enter your password")
        
        # Validate
        if not all([fullname, username, email, password]):
            messagebox.showerror(
                "Missing Information",
                "Please fill in all fields"
            )
            return
        
        if password != confirm:
            messagebox.showerror(
                "Password Mismatch",
                "Passwords do not match"
            )
            return
        
        if len(password) < 6:
            messagebox.showwarning(
                "Weak Password",
                "Password should be at least 6 characters long"
            )
            return
        
        # Hash password
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        # Create user
        user_data = {
            'username': username,
            'password_hash': password_hash,
            'full_name': fullname,
            'email': email,
            'role': 'admin',
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        try:
            self.user_id = self.db.create_user(
                user_data['username'],
                user_data['password_hash'],
                user_data['email'],
                user_data['full_name']
            )
            
            messagebox.showinfo(
                "Success! 🎉",
                f"Welcome to DocFlow Pro, {fullname}!\n\n"
                "Your admin account has been created.\n"
                "Click OK to start using the app."
            )
            
            self.window.destroy()
            
        except Exception as e:
            messagebox.showerror(
                "Registration Failed",
                f"Could not create account:\n{str(e)}"
            )
    
    def _login_user(self):
        """Login existing user"""
        username = self._get_entry_value(self.username_entry, "Enter your username")
        password = self._get_entry_value(self.password_entry, "Enter your password")
        
        if not username or not password:
            messagebox.showerror(
                "Missing Information",
                "Please enter both username and password"
            )
            return
        
        # Hash password
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        # Authenticate
        user = self.db.authenticate_user(username, password_hash)
        
        if user:
            self.user_id = user['id']
            
            messagebox.showinfo(
                "Welcome Back! 👋",
                f"Hello, {user.get('full_name', username)}!\n\n"
                "Loading your workspace..."
            )
            
            # Update last login
            self.db.update_user_last_login(self.user_id)
            
            self.window.destroy()
        else:
            messagebox.showerror(
                "Login Failed",
                "Invalid username or password.\n\n"
                "Please check your credentials and try again."
            )
    
    def run(self):
        """Start login window"""
        self.window.mainloop()
        return self.user_id
