"""
Script to Extract Data from All Documents
Run this to populate extracted data in database
"""

import sqlite3
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.data_extractor import UniversalDataExtractor

def extract_all_documents():
    """Extract data from all documents in database"""
    
    conn = sqlite3.connect('docflow.db')
    cursor = conn.cursor()
    
    # Get all documents with empty description/ocr_text
    cursor.execute("""
        SELECT id, file_path, title 
        FROM documents 
        WHERE user_id = 1
        AND (description IS NULL OR description = '' OR ocr_text IS NULL OR ocr_text = '')
    """)
    
    docs = cursor.fetchall()
    
    if not docs:
        print("✓ All documents already have extracted data!")
        conn.close()
        return
    
    print(f"Found {len(docs)} documents needing extraction...")
    
    extractor = UniversalDataExtractor()
    success_count = 0
    
    for doc_id, file_path, title in docs:
        try:
            print(f"\nProcessing: {title} (ID: {doc_id})")
            
            if not file_path or not os.path.exists(file_path):
                print(f"  ✗ File not found: {file_path}")
                continue
            
            # Extract data
            data = extractor.extract_from_file(file_path)
            
            if 'error' in data:
                print(f"  ✗ Extraction error: {data['error']}")
                continue
            
            # Format description
            parts = []
            if data.get('invoice_number'):
                parts.append(f"Invoice: {data['invoice_number']}")
            if data.get('client_name'):
                parts.append(f"Client: {data['client_name']}")
            if data.get('total_amount'):
                parts.append(f"Amount: Rs.{data['total_amount']}")
            if data.get('invoice_date'):
                parts.append(f"Date: {data['invoice_date']}")
            
            description = ', '.join(parts) if parts else 'Extracted data'
            ocr_text = data.get('raw_text', '')[:500]  # First 500 chars
            
            # Update database
            cursor.execute("""
                UPDATE documents
                SET description = ?, ocr_text = ?
                WHERE id = ?
            """, (description, ocr_text, doc_id))
            
            print(f"  ✓ Extracted: {description}")
            success_count += 1
            
        except Exception as e:
            print(f"  ✗ Error: {e}")
    
    # Commit all changes
    conn.commit()
    conn.close()
    
    print(f"\n{'='*60}")
    print(f"✅ Complete! Extracted data from {success_count}/{len(docs)} documents")
    print(f"{'='*60}")
    print("\nNow:")
    print("1. Restart DocFlowPro application")
    print("2. Go to Export → Documents → Excel")
    print("3. See 'Extracted Data' column filled!")

if __name__ == "__main__":
    extract_all_documents()
