"""
File Validator - File type and security validation
"""

import os
import re
from core.logger import get_logger

logger = get_logger('app')


class FileValidator:
    """Validate uploaded files for security and type"""
    
    # Allowed file extensions and their magic numbers (file signatures)
    ALLOWED_TYPES = {
        'pdf': {
            'extensions': ['.pdf'],
            'magic': b'%PDF',
            'max_size': 50 * 1024 * 1024  # 50MB
        },
        'excel': {
            'extensions': ['.xlsx', '.xls'],
            'magic': [b'PK\x03\x04', b'\xD0\xCF\x11\xE0'],  # xlsx, xls
            'max_size': 20 * 1024 * 1024  # 20MB
        },
        'csv': {
            'extensions': ['.csv'],
            'magic': None,  # Text file, no magic number
            'max_size': 10 * 1024 * 1024  # 10MB
        },
        'text': {
            'extensions': ['.txt'],
            'magic': None,
            'max_size': 5 * 1024 * 1024  # 5MB
        },
        'image': {
            'extensions': ['.jpg', '.jpeg', '.png', '.bmp'],
            'magic': [b'\xFF\xD8\xFF', b'\x89PNG', b'BM'],  # jpg, png, bmp
            'max_size': 10 * 1024 * 1024  # 10MB
        }
    }
    
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB global limit
    
    @staticmethod
    def validate_file(file_path):
        """
        Validate file for security and type
        Returns: dict with file info or raises ValueError
        """
        # Check file exists
        if not os.path.exists(file_path):
            raise ValueError("File not found")
        
        if not os.path.isfile(file_path):
            raise ValueError("Path is not a file")
        
        # Get file info
        file_size = os.path.getsize(file_path)
        file_name = os.path.basename(file_path)
        file_ext = os.path.splitext(file_name)[1].lower()
        
        # Check file size
        if file_size == 0:
            raise ValueError("File is empty")
        
        if file_size > FileValidator.MAX_FILE_SIZE:
            max_mb = FileValidator.MAX_FILE_SIZE / (1024 * 1024)
            raise ValueError(f"File too large (max {max_mb}MB)")
        
        # Check extension is allowed
        allowed = False
        file_type = None
        type_config = None
        
        for ftype, config in FileValidator.ALLOWED_TYPES.items():
            if file_ext in config['extensions']:
                allowed = True
                file_type = ftype
                type_config = config
                break
        
        if not allowed:
            raise ValueError(f"File type {file_ext} not supported")
        
        # Check type-specific size limit
        if file_size > type_config['max_size']:
            max_mb = type_config['max_size'] / (1024 * 1024)
            raise ValueError(f"{file_type.upper()} files limited to {max_mb}MB")
        
        # Validate magic number (file signature)
        if type_config['magic']:
            FileValidator._validate_magic_number(file_path, type_config['magic'], file_type)
        
        logger.info(f"File validated: {file_name} ({file_type}, {file_size} bytes)")
        
        return {
            'path': file_path,
            'name': file_name,
            'extension': file_ext,
            'type': file_type,
            'size': file_size,
            'size_mb': round(file_size / (1024 * 1024), 2)
        }
    
    @staticmethod
    def _validate_magic_number(file_path, expected_magic, file_type):
        """Validate file's magic number matches expected type"""
        try:
            with open(file_path, 'rb') as f:
                file_header = f.read(10)  # Read first 10 bytes
            
            # Handle single or multiple magic numbers
            magic_list = expected_magic if isinstance(expected_magic, list) else [expected_magic]
            
            valid = False
            for magic in magic_list:
                if file_header.startswith(magic):
                    valid = True
                    break
            
            if not valid:
                raise ValueError(f"File is not a valid {file_type.upper()} file (magic number mismatch)")
                
        except Exception as e:
            if "magic number" in str(e):
                raise
            raise ValueError(f"Failed to validate file: {e}")
    
    @staticmethod
    def sanitize_filename(filename):
        """
        Sanitize filename to prevent security issues
        - Remove dangerous characters
        - Prevent directory traversal
        - Limit length
        """
        # Remove path separators and dangerous characters
        filename = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '', filename)
        
        # Get just the basename (prevent directory traversal)
        filename = os.path.basename(filename)
        
        # Limit length
        if len(filename) > 255:
            name, ext = os.path.splitext(filename)
            filename = name[:250] + ext
        
        # Ensure filename isn't empty after sanitization
        if not filename or filename == '.':
            filename = 'unnamed_file.txt'
        
        return filename
    
    @staticmethod
    def get_allowed_extensions():
        """Get list of all allowed file extensions"""
        extensions = []
        for config in FileValidator.ALLOWED_TYPES.values():
            extensions.extend(config['extensions'])
        return extensions
    
    @staticmethod
    def get_allowed_types_description():
        """Get human-readable description of allowed types"""
        types_desc = []
        for ftype, config in FileValidator.ALLOWED_TYPES.items():
            exts = ', '.join(config['extensions'])
            max_mb = config['max_size'] / (1024 * 1024)
            types_desc.append(f"{ftype.upper()}: {exts} (max {max_mb}MB)")
        return '\n'.join(types_desc)
