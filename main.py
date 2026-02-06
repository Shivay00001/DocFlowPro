"""
DocFlow Pro - Main Entry Point
Enterprise Document Management System
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.database import DatabaseManager
from core.engine import DocFlowEngine
from core.license import LicenseManager
from core.feature_gates import FeatureGates
from ui.login_window import LoginWindow
from ui.main_window import MainWindow
from core.logger import ProductionLogger, get_logger  # PRODUCTION: Added logging


def main():
    """Main application entry point"""
    logger = None
    
    try:
        # Initialize production logging
        logger_sys = ProductionLogger()
        logger = get_logger('app')
        logger_sys.log_startup()
        
        print("Starting DocFlow Pro...")
        logger.info("Initializing DocFlow Pro")
        
        # Initialize database
        db = DatabaseManager("docflow.db")
        print("[OK] Database initialized")
        logger.info("Database initialized successfully")
        
        # Initialize backup manager and create startup backup
        from utils.backup_manager import initialize_backup_manager
        from config.backup_config import AUTO_BACKUP_ON_START
        
        backup_manager = initialize_backup_manager("docflow.db")
        
        if AUTO_BACKUP_ON_START:
            backup_path = backup_manager.create_backup()
            if backup_path:
                print(f"[OK] Database backup created")
                logger.info(f"Startup backup created")
        
        # Start auto-backup thread
        backup_manager.start_auto_backup()
        logger.info("Backup manager initialized")
        
        # Initialize license manager
        license_manager = LicenseManager(db)
        print("[OK] License manager initialized")
        logger.info("License manager initialized")
        
        # Initialize engine
        engine = DocFlowEngine(db, license_manager, FeatureGates)
        print("[OK] Engine initialized")
        logger.info("Engine initialized")
        
        # Get or create default user (BYPASS LOGIN)
        cursor = db.connection.cursor()
        cursor.execute("SELECT id FROM users LIMIT 1")
        user = cursor.fetchone()
        
        if user:
            user_id = user[0]
            print(f"[OK] Using existing user: ID={user_id}")
            logger.info(f"Using existing user: ID={user_id}")
        else:
            # Create default admin user with SECURE random password
            import hashlib
            import secrets
            import string
            from datetime import datetime
            
            # Generate secure random password (16 characters)
            alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
            random_password = ''.join(secrets.choice(alphabet) for _ in range(16))
            
            user_data = {
                'username': 'admin',
                'password_hash': hashlib.sha256(random_password.encode()).hexdigest(),
                'full_name': 'Administrator',
                'email': 'admin@docflowpro.com',
                'role': 'admin',
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            user_id = db.create_user(
                user_data['username'],
                user_data['password_hash'],
                user_data['email'],
                user_data['full_name']
            )
            
            # SECURITY: Save password to secure file (one-time only)
            with open('ADMIN_PASSWORD.txt', 'w') as f:
                f.write(f"Admin Password (SAVE THIS): {random_password}\n")
                f.write(f"Username: admin\n")
                f.write(f"Created: {datetime.now()}\n")
                f.write("\nWARNING: Delete this file after saving password securely!\n")
            
            print(f"[OK] Created admin user (ID={user_id})")
            print(f"[!] Password saved to ADMIN_PASSWORD.txt - SAVE IT NOW!")
            logger.info(f"Created default admin user: ID={user_id}")
        
        # Initialize session manager
        from core.session_manager import get_session_manager
        session_manager = get_session_manager()
        
        # Get username for session
        user_data = db.get_user_by_id(user_id)
        username = user_data.get('username', 'admin') if user_data else 'admin'
        
        # Start session
        session_manager.start_session(user_id, username)
        logger.info("Session manager initialized")
        
        # Launch main application directly
        print("Launching main application...")
        logger.info("Launching main window")
        app = MainWindow(engine, user_id)
        app.run()
        
        print("Application closed")
        logger.info("Application closed normally")
        
        if logger:
            ProductionLogger().log_shutdown()
        
    except ImportError as e:
        error_msg = f"Missing dependency: {e}\nPlease install required packages:\npip install -r requirements.txt"
        print(f"\n[ERROR] {error_msg}")
        if logger:
            logger.error(f"Import error: {e}")
        
        try:
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror(
                "Dependency Error",
                f"{error_msg}\n\nPlease run:\npip install -r requirements.txt"
            )
        except:
            input("\nPress Enter to exit...")
    
    except Exception as e:
        error_msg = f"Application error: {e}"
        print(f"\n[ERROR] {error_msg}")
        
        if logger:
            ProductionLogger().log_error(e, "Main application startup")
        
        import traceback
        traceback.print_exc()
        
        try:
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror(
                "Application Error",
                f"DocFlow Pro encountered an error:\n\n{e}\n\nPlease check logs/errors.log for details."
            )
        except:
            pass
        
        input("\nPress Enter to exit...")



if __name__ == "__main__":
    main()
