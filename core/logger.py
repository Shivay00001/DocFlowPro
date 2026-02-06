"""
Production Logging System for DocFlow Pro
Centralized logging with rotation and proper formatting
"""

import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime


class ProductionLogger:
    """Centralized logging system for production"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ProductionLogger, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        self._initialized = True
        self.log_dir = "logs"
        
        # Create logs directory if it doesn't exist
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        
        # Setup loggers
        self._setup_loggers()
    
    def _setup_loggers(self):
        """Setup different log handlers"""
        
        # Main application logger
        self.app_logger = logging.getLogger('DocFlowPro')
        self.app_logger.setLevel(logging.DEBUG)
        
        # Error logger (errors only)
        self.error_logger = logging.getLogger('DocFlowPro.Error')
        self.error_logger.setLevel(logging.ERROR)
        
        # Payment logger (financial transactions)
        self.payment_logger = logging.getLogger('DocFlowPro.Payment')
        self.payment_logger.setLevel(logging.INFO)
        
        # Create formatters
        detailed_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        simple_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Main app log file (10MB, keep 5 backups)
        app_handler = RotatingFileHandler(
            os.path.join(self.log_dir, 'docflow.log'),
            maxBytes=10*1024*1024,  # 10 MB
            backupCount=5,
            encoding='utf-8'
        )
        app_handler.setLevel(logging.DEBUG)
        app_handler.setFormatter(detailed_formatter)
        self.app_logger.addHandler(app_handler)
        
        # Error log file (5MB, keep 3 backups)
        error_handler = RotatingFileHandler(
            os.path.join(self.log_dir, 'errors.log'),
            maxBytes=5*1024*1024,  # 5 MB
            backupCount=3,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(detailed_formatter)
        self.error_logger.addHandler(error_handler)
        
        # Payment log file (critical for financial records)
        payment_handler = RotatingFileHandler(
            os.path.join(self.log_dir, 'payments.log'),
            maxBytes=5*1024*1024,  # 5 MB
            backupCount=10,  # Keep more backups for financial records
            encoding='utf-8'
        )
        payment_handler.setLevel(logging.INFO)
        payment_handler.setFormatter(detailed_formatter)
        self.payment_logger.addHandler(payment_handler)
        
        # Console handler (for development)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(simple_formatter)
        self.app_logger.addHandler(console_handler)
    
    def get_logger(self, name='app'):
        """Get appropriate logger"""
        if name == 'error':
            return self.error_logger
        elif name == 'payment':
            return self.payment_logger
        else:
            return self.app_logger
    
    def log_startup(self):
        """Log application startup"""
        self.app_logger.info("="*60)
        self.app_logger.info("DocFlow Pro Application Starting")
        self.app_logger.info(f"Timestamp: {datetime.now()}")
        self.app_logger.info("="*60)
    
    def log_shutdown(self):
        """Log application shutdown"""
        self.app_logger.info("="*60)
        self.app_logger.info("DocFlow Pro Application Shutting Down")
        self.app_logger.info(f"Timestamp: {datetime.now()}")
        self.app_logger.info("="*60)
    
    def log_error(self, error, context=""):
        """Log an error with context"""
        import traceback
        self.error_logger.error(f"Error: {error}")
        if context:
            self.error_logger.error(f"Context: {context}")
        self.error_logger.error(f"Traceback:\n{traceback.format_exc()}")
    
    def log_payment(self, action, details):
        """Log payment transaction"""
        self.payment_logger.info(f"PAYMENT: {action}")
        self.payment_logger.info(f"Details: {details}")


# Global logger instance
logger_instance = ProductionLogger()

def get_logger(name='app'):
    """Convenience function to get logger"""
    return logger_instance.get_logger(name)
