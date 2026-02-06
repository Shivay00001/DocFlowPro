"""
Backup Manager - Automatic database backup and recovery
"""

import os
import shutil
import glob
import threading
import time
from datetime import datetime
from config.backup_config import (
    BACKUP_DIR,
    MAX_BACKUPS,
    AUTO_BACKUP_INTERVAL_HOURS,
    ENABLE_AUTO_BACKUP
)
from core.logger import get_logger

logger = get_logger('app')


class BackupManager:
    """Manages database backups and recovery"""
    
    def __init__(self, db_path, backup_dir=BACKUP_DIR):
        self.db_path = db_path
        self.backup_dir = backup_dir
        self.max_backups = MAX_BACKUPS
        self.auto_backup_thread = None
        
        # Create backup directory if it doesn't exist
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
            logger.info(f"Created backup directory: {self.backup_dir}")
    
    def create_backup(self, backup_name=None):
        """
        Create a database backup
        Returns: backup file path or None if failed
        """
        try:
            # Generate backup filename
            if not backup_name:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                backup_name = f'docflow_backup_{timestamp}.db'
            
            backup_path = os.path.join(self.backup_dir, backup_name)
            
            # Create backup
            shutil.copy2(self.db_path, backup_path)
            
            file_size = os.path.getsize(backup_path)
            logger.info(f"Backup created: {backup_name} ({file_size} bytes)")
            
            # Cleanup old backups
            self.cleanup_old_backups()
            
            return backup_path
            
        except Exception as e:
            logger.error(f"Backup creation failed: {e}", exc_info=True)
            return None
    
    def cleanup_old_backups(self):
        """Remove old backups, keeping only MAX_BACKUPS most recent"""
        try:
            # Get all backup files sorted by modification time
            backups = glob.glob(os.path.join(self.backup_dir, 'docflow_backup_*.db'))
            backups.sort(key=os.path.getmtime, reverse=True)
            
            # Remove excess backups
            removed_count = 0
            for old_backup in backups[self.max_backups:]:
                try:
                    os.remove(old_backup)
                    removed_count += 1
                    logger.info(f"Removed old backup: {os.path.basename(old_backup)}")
                except Exception as e:
                    logger.warning(f"Failed to remove backup {old_backup}: {e}")
            
            if removed_count > 0:
                logger.info(f"Cleaned up {removed_count} old backups")
                
        except Exception as e:
            logger.error(f"Backup cleanup failed: {e}")
    
    def list_backups(self):
        """
        List all available backups
        Returns: List of (filename, filepath, size, date) tuples
        """
        backups = []
        
        try:
            backup_files = glob.glob(os.path.join(self.backup_dir, 'docflow_backup_*.db'))
            
            for filepath in backup_files:
                filename = os.path.basename(filepath)
                size = os.path.getsize(filepath)
                mtime = os.path.getmtime(filepath)
                date = datetime.fromtimestamp(mtime)
                
                backups.append({
                    'filename': filename,
                    'filepath': filepath,
                    'size': size,
                    'date': date,
                    'date_str': date.strftime('%Y-%m-%d %H:%M:%S')
                })
            
            # Sort by date, newest first
            backups.sort(key=lambda x: x['date'], reverse=True)
            
        except Exception as e:
            logger.error(f"Failed to list backups: {e}")
        
        return backups
    
    def restore_from_backup(self, backup_filename):
        """
        Restore database from a backup
        Returns: True if successful, False otherwise
        """
        try:
            backup_path = os.path.join(self.backup_dir, backup_filename)
            
            if not os.path.exists(backup_path):
                logger.error(f"Backup file not found: {backup_filename}")
                return False
            
            # Create a safety backup of current database before restoring
            safety_backup = f'pre_restore_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db'
            safety_path = self.create_backup(safety_backup)
            
            if safety_path:
                logger.info(f"Created safety backup: {safety_backup}")
            
            # Restore from backup
            shutil.copy2(backup_path, self.db_path)
            
            logger.info(f"Database restored from backup: {backup_filename}")
            return True
            
        except Exception as e:
            logger.error(f"Restore failed: {e}", exc_info=True)
            return False
    
    def start_auto_backup(self):
        """Start automatic backup in background thread"""
        if not ENABLE_AUTO_BACKUP:
            logger.info("Auto-backup is disabled")
            return
        
        if self.auto_backup_thread and self.auto_backup_thread.is_alive():
            logger.warning("Auto-backup thread already running")
            return
        
        def backup_loop():
            logger.info(f"Auto-backup started (interval: {AUTO_BACKUP_INTERVAL_HOURS}h)")
            
            while True:
                try:
                    # Wait for interval
                    time.sleep(AUTO_BACKUP_INTERVAL_HOURS * 3600)
                    
                    # Create backup
                    backup_path = self.create_backup()
                    
                    if backup_path:
                        logger.info("Auto-backup completed successfully")
                    else:
                        logger.warning("Auto-backup failed")
                        
                except Exception as e:
                    logger.error(f"Auto-backup error: {e}", exc_info=True)
        
        self.auto_backup_thread = threading.Thread(target=backup_loop, daemon=True)
        self.auto_backup_thread.start()
    
    def get_backup_stats(self):
        """Get backup statistics"""
        backups = self.list_backups()
        
        if not backups:
            return {
                'count': 0,
                'total_size': 0,
                'latest': None,
                'oldest': None
            }
        
        total_size = sum(b['size'] for b in backups)
        
        return {
            'count': len(backups),
            'total_size': total_size,
            'total_size_mb': total_size / (1024 * 1024),
            'latest': backups[0] if backups else None,
            'oldest': backups[-1] if backups else None,
            'backups': backups
        }


# Global backup manager instance (will be initialized with db_path)
_backup_manager = None

def initialize_backup_manager(db_path):
    """Initialize global backup manager"""
    global _backup_manager
    _backup_manager = BackupManager(db_path)
    return _backup_manager

def get_backup_manager():
    """Get global backup manager instance"""
    return _backup_manager
