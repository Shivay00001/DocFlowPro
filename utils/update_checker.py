"""
Update Checker - Check for application updates
"""

import requests
import json
from core.logger import get_logger

logger = get_logger('app')


class UpdateChecker:
    """Check for application updates"""
    
    # Current version
    CURRENT_VERSION = "2.1.0"
    
    # Update check URL (configure this with your actual API)
    VERSION_URL = "https://api.example.com/docflowpro/version.json"
    
    # Fallback local version file for testing
    LOCAL_VERSION_FILE = "version_check.json"
    
    @staticmethod
    def check_for_updates(use_local=False):
        """
        Check if updates are available
        Returns: dict with update info
        """
        try:
            if use_local:
                # Use local file for testing
                return UpdateChecker._check_local()
            
            # Check online
            response = requests.get(UpdateChecker.VERSION_URL, timeout=5)
            data = response.json()
            
            return UpdateChecker._process_version_data(data)
            
        except requests.RequestException as e:
            logger.warning(f"Update check failed (network): {e}")
            return {
                'update_available': False,
                'error': 'Network error',
                'current_version': UpdateChecker.CURRENT_VERSION
            }
        except Exception as e:
            logger.error(f"Update check failed: {e}")
            return {
                'update_available': False,
                'error': str(e),
                'current_version': UpdateChecker.CURRENT_VERSION
            }
    
    @staticmethod
    def _check_local():
        """Check using local version file (for testing)"""
        try:
            with open(UpdateChecker.LOCAL_VERSION_FILE, 'r') as f:
                data = json.load(f)
            return UpdateChecker._process_version_data(data)
        except FileNotFoundError:
            logger.info("No local version file found")
            return {'update_available': False, 'current_version': UpdateChecker.CURRENT_VERSION}
        except Exception as e:
            logger.error(f"Local version check failed: {e}")
            return {'update_available': False, 'error': str(e)}
    
    @staticmethod
    def _process_version_data(data):
        """Process version data and determine if update needed"""
        latest_version = data.get('version', UpdateChecker.CURRENT_VERSION)
        
        update_available = UpdateChecker.is_newer_version(latest_version)
        
        result = {
            'update_available': update_available,
            'current_version': UpdateChecker.CURRENT_VERSION,
            'latest_version': latest_version
        }
        
        if update_available:
            result.update({
                'download_url': data.get('download_url', ''),
                'changelog': data.get('changelog', 'No changelog available'),
                'release_date': data.get('release_date', ''),
                'critical': data.get('critical', False)
            })
            
            logger.info(f"Update available: {latest_version}")
        
        return result
    
    @staticmethod
    def is_newer_version(latest_version):
        """Compare version strings (semantic versioning)"""
        try:
            current = tuple(map(int, UpdateChecker.CURRENT_VERSION.split('.')))
            latest = tuple(map(int, latest_version.split('.')))
            return latest > current
        except Exception as e:
            logger.warning(f"Version comparison failed: {e}")
            return False
    
    @staticmethod
    def create_test_version_file(version="2.2.0", has_update=True):
        """Create test version file (for development)"""
        data = {
            'version': version if has_update else UpdateChecker.CURRENT_VERSION,
            'download_url': 'https://example.com/DocFlowPro_v2.2.0.exe',
            'changelog': 'Bug fixes and performance improvements',
            'release_date': '2025-12-20',
            'critical': False
        }
        
        with open(UpdateChecker.LOCAL_VERSION_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"Test version file created: {version}")
