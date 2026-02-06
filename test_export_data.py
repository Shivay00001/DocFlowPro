"""
QUICK FIX TEST - Verify Export Shows Extracted Data
"""

# Test the export module directly
import sys
import os

# Add parent directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.database import DatabaseManager

# Initialize database
db = DatabaseManager('docflow.db')

# Get documents
docs = db.get_user_documents(1)  # User ID 1

print("=" * 60)
print("DOCUMENTS IN DATABASE:")
print("=" * 60)

for doc in docs:
    print(f"\nID: {doc['id']}")
    print(f"Title: {doc.get('title', 'N/A')}")
    print(f"Type: {doc.get('file_type', 'N/A')}")
    print(f"Description: {doc.get('description', '(empty)')[:100]}")
    print(f"OCR Text: {doc.get('ocr_text', '(empty)')[:100]}")
    print("-" * 60)

print("\n" + "=" * 60)
print(f"TOTAL: {len(docs)} documents")
print("=" * 60)

# Check what export would show
print("\nEXPORT PREVIEW:")
print("=" * 60)

for doc in docs:
    extracted = doc.get('description', '') or doc.get('ocr_text', '')
    preview = extracted[:80] + '...' if len(extracted) > 80 else extracted
    if not preview.strip():
        preview = "(No data)"
    
    print(f"ID {doc['id']}: {preview}")

print("\n✓ This is what SHOULD appear in export 'Extracted Data' column")
