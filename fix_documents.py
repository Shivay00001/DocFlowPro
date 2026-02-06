"""
Fix corrupted documents.py file by removing null bytes
"""

import os
import shutil

# Backup corrupted file
source = 'ui/documents.py'
backup = 'ui/documents.py.backup'

print(f"Creating backup: {backup}")
shutil.copy2(source, backup)

# Read corrupted file
print(f"Reading {source}...")
with open(source, 'rb') as f:
    data = f.read()

print(f"File size: {len(data)} bytes")
null_count = data.count(b'\x00')
print(f"Null bytes found: {null_count}")

if null_count > 0:
    # Remove null bytes
    cleaned = data.replace(b'\x00', b'')
    print(f"Removed {null_count} null bytes")
    
    # Write cleaned file
    with open(source, 'wb') as f:
        f.write(cleaned)
    
    print(f"✓ File cleaned and saved")
    print(f"✓ Backup saved as: {backup}")
else:
    print("No null bytes found - file is clean")

# Verify syntax
print("\nVerifying syntax...")
import py_compile
try:
    py_compile.compile(source, doraise=True)
    print("✓ Syntax check passed!")
except SyntaxError as e:
    print(f"✗ Syntax error: {e}")
