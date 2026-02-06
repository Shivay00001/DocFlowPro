"""Extract data from all documents - NO UNICODE"""
import sqlite3
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils.data_extractor import UniversalDataExtractor

conn = sqlite3.connect('docflow.db')
cursor = conn.cursor()
cursor.execute("SELECT id, file_path, title FROM documents WHERE user_id = 1")
docs = cursor.fetchall()
print(f"Found {len(docs)} documents")

extractor = UniversalDataExtractor()
for doc_id, file_path, title in docs:
    try:
        print(f"Processing ID {doc_id}: {title[:30]}")
        if not file_path or not os.path.exists(file_path):
            print(f"  File not found")
            continue
        data = extractor.extract_from_file(file_path)
        if 'error' in data:
            print(f"  Error: {data['error'][:50]}")
            continue
        parts = []
        if data.get('invoice_number'): parts.append(f"Invoice: {data['invoice_number']}")
        if data.get('client_name'): parts.append(f"Client: {data['client_name']}")
        if data.get('total_amount'): parts.append(f"Amount: Rs.{data['total_amount']}")
        description = ', '.join(parts) if parts else 'Data extracted'
        ocr_text = data.get('raw_text', '')[:500]
        cursor.execute("UPDATE documents SET description = ?, ocr_text = ? WHERE id = ?", 
                      (description, ocr_text, doc_id))
        print(f"  DONE: {description[:50]}")
    except Exception as e:
        print(f"  Error: {str(e)[:50]}")

conn.commit()
conn.close()
print("\nExtraction complete! Restart app now.")
