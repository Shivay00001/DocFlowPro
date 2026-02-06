"""
CRITICAL FIX: Extract Data from Existing Documents
This script will scan all documents in database and extract/save their data
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.database import DatabaseManager
from utils.data_extractor import UniversalDataExtractor

def extract_all_documents():
    """Extract data from all documents and save to database"""
    
    print("=" * 70)
    print("DocFlowPro - Extract Data from Existing Documents")
    print("=" * 70)
    
    db = DatabaseManager('docflow.db')
    extractor = UniversalDataExtractor()
    
    # Get all documents for user 1
    docs = db.get_user_documents(1)
    
    print(f"\nFound {len(docs)} documents")
    print("=" * 70)
    
    extracted_count = 0
    failed_count = 0
    
    for doc in docs:
        doc_id = doc['id']
        title = doc.get('title', 'Untitled')
        file_path = doc.get('file_path', '')
        
        print(f"\n[{doc_id}] Processing: {title}")
        print(f"     Path: {file_path}")
        
        # Check if already has data
        current_desc = doc.get('description', '')
        current_ocr = doc.get('ocr_text', '')
        
        if current_desc.strip() or current_ocr.strip():
            print("     [SKIP] Already has extracted data")
            continue
        
        # Check if file exists
        if not file_path or not os.path.exists(file_path):
            print("     [ERROR] File not found")
            failed_count += 1
            continue
        
        try:
            # Extract data from file
            print("     [EXTRACTING...]", end='', flush=True)
            extracted_data = extractor.extract_from_file(file_path)
            
            if 'error' in extracted_data:
                print(f" [ERROR] {extracted_data['error']}")
                failed_count += 1
                continue
            
            # Prepare description with invoice data
            description_parts = []
            
            if extracted_data.get('invoice_number'):
                description_parts.append(f"Invoice Number: {extracted_data['invoice_number']}")
            
            if extracted_data.get('client_name'):
                description_parts.append(f"Client: {extracted_data['client_name']}")
            
            if extracted_data.get('total_amount'):
                description_parts.append(f"Total Amount: Rs.{extracted_data['total_amount']}")
            
            if extracted_data.get('invoice_date'):
                description_parts.append(f"Date: {extracted_data['invoice_date']}")
            
            description = '\n'.join(description_parts) if description_parts else ''
            ocr_text = extracted_data.get('raw_text', '')
            
            # Update database
            db.cursor.execute("""
                UPDATE documents 
                SET description = ?, ocr_text = ?
                WHERE id = ?
            """, (description, ocr_text, doc_id))
            db.connection.commit()
            
            print(" [OK]")
            if description:
                print(f"     Extracted: {description.replace(chr(10), ', ')}")
            else:
                print(f"     Extracted OCR text: {len(ocr_text)} chars")
            
            extracted_count += 1
            
        except Exception as e:
            print(f" [EXCEPTION] {str(e)}")
            failed_count += 1
    
    print("\n" + "=" * 70)
    print(f"SUMMARY:")
    print(f"  Successfully extracted: {extracted_count}")
    print(f"  Failed: {failed_count}")
    print(f"  Already had data: {len(docs) - extracted_count - failed_count}")
    print("=" * 70)
    
    if extracted_count > 0:
        print("\n[SUCCESS] Data extracted and saved to database!")
        print("Now your exports will show the invoice data!")
    else:
        print("\n[INFO] No new data extracted")

if __name__ == "__main__":
    extract_all_documents()
