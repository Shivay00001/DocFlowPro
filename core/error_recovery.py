"""
Error Recovery - Auto-recovery and retry mechanisms
"""

import time
import functools
from core.logger import get_logger

logger = get_logger('app')


class ErrorRecovery:
    """Enhanced error recovery mechanisms"""
    
    @staticmethod
    def with_retry(max_attempts=3, delay=1, exceptions=(Exception,)):
        """
        Decorator to retry function on failure
        
        Usage:
            @ErrorRecovery.with_retry(max_attempts=3, delay=2)
            def my_function():
                ...
        """
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                last_exception = None
                
                for attempt in range(1, max_attempts + 1):
                    try:
                        return func(*args, **kwargs)
                    except exceptions as e:
                        last_exception = e
                        
                        if attempt < max_attempts:
                            logger.warning(
                                f"Attempt {attempt}/{max_attempts} failed for {func.__name__}: {e}. "
                                f"Retrying in {delay}s..."
                            )
                            time.sleep(delay)
                        else:
                            logger.error(
                                f"All {max_attempts} attempts failed for {func.__name__}: {e}"
                            )
                
                # All attempts failed
                raise last_exception
            
            return wrapper
        return decorator
    
    @staticmethod
    def safe_execute(func, default=None, log_errors=True):
        """
        Execute function safely, return default on error
        
        Usage:
            result = ErrorRecovery.safe_execute(lambda: risky_operation(), default=[])
        """
        try:
            return func()
        except Exception as e:
            if log_errors:
                logger.error(f"Safe execute failed: {e}", exc_info=True)
            return default
    
    @staticmethod
    def database_health_check(db_path):
        """Check database integrity"""
        import sqlite3
        
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Run integrity check
            cursor.execute("PRAGMA integrity_check")
            result = cursor.fetchone()
            
            conn.close()
            
            if result and result[0] == 'ok':
                logger.info("Database integrity check: OK")
                return True
            else:
                logger.error(f"Database integrity check failed: {result}")
                return False
                
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return False
    
    @staticmethod
    def attempt_database_recovery(db_path, backup_manager):
        """Attempt to recover database from backup"""
        logger.warning("Attempting database recovery...")
        
        try:
            # Get list of backups
            backups = backup_manager.list_backups()
            
            if not backups:
                logger.error("No backups available for recovery")
                return False
            
            # Try to restore from most recent backup
            latest_backup = backups[0]
            logger.info(f"Restoring from backup: {latest_backup['filename']}")
            
            success = backup_manager.restore_from_backup(latest_backup['filename'])
            
            if success:
                # Verify restored database
                if ErrorRecovery.database_health_check(db_path):
                    logger.info("Database recovered successfully")
                    return True
            
            logger.error("Database recovery failed")
            return False
            
        except Exception as e:
            logger.error(f"Recovery attempt failed: {e}", exc_info=True)
            return False
