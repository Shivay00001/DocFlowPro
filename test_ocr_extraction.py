"""
Complete OCR Setup and Testing Guide for DocFlowPro
"""

# Test document extraction to Excel
import os
from utils.data_extractor import UniversalDataExtractor
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

def test_extraction_to_excel():
    """Test extracting data from documents and exporting to Excel"""
    
    print("=" * 60)
    print("DocFlowPro - Document Extraction to Excel Test")
    print("=" * 60)
    
    # Initialize extractor
    extractor = UniversalDataExtractor()
    
    # Test files (create samples if needed)
    test_files = [
        ("Sample PDF", "test_invoice.pdf"),
        ("Sample Image", "test_invoice.jpg"),
        ("Sample Excel", "test_data.xlsx")
    ]
    
    # Create Excel workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Extracted Data"
    
    # Headers
    headers = ['File Name', 'Type', 'Invoice Number', 'Client', 'Amount', 'Date', 'Extracted Text Preview']
    ws.append(headers)
    
    # Style headers
    for cell in ws[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
    
    # Process each file
    for file_desc, file_path in test_files:
        print(f"\nProcessing: {file_desc}")
        
        if not os.path.exists(file_path):
            print(f"  [SKIP] File not found: {file_path}")
            continue
        
        try:
            # Extract data
            data = extractor.extract_from_file(file_path)
            
            if 'error' in data:
                print(f"  [ERROR] {data['error']}")
                ws.append([file_path, "Error", "", "", "", "", data['error']])
            else:
                # Extract fields
                invoice_num = data.get('invoice_number', 'N/A')
                client = data.get('client_name', 'N/A')
                amount = data.get('total_amount', 0)
                date = data.get('invoice_date', 'N/A')
                text_preview = data.get('raw_text', '')[:100] if data.get('raw_text') else 'N/A'
                
                print(f"  [OK] Invoice: {invoice_num}, Client: {client}, Amount: {amount}")
                
                # Add to Excel
                ws.append([
                    file_path,
                    os.path.splitext(file_path)[1],
                    invoice_num,
                    client,
                    amount,
                    date,
                    text_preview
                ])
        
        except Exception as e:
            print(f"  [EXCEPTION] {str(e)}")
            ws.append([file_path, "Exception", "", "", "", "", str(e)])
    
    # Save Excel
    output_file = "extracted_data_test.xlsx"
    wb.save(output_file)
    
    print("\n" + "=" * 60)
    print(f"Excel file saved: {output_file}")
    print("=" * 60)
    
    return output_file

def test_ocr_setup():
    """Test if Tesseract OCR is properly set up"""
    print("\n" + "=" * 60)
    print("Testing Tesseract OCR Setup")
    print("=" * 60)
    
    try:
        import pytesseract
        from PIL import Image
        
        # Try to get Tesseract version
        try:
            version = pytesseract.get_tesseract_version()
            print(f"[OK] Tesseract version: {version}")
        except:
            print("[WARNING] Tesseract not found in PATH")
            print("  Trying common installation paths...")
            
            # Try common Windows paths
            paths = [
                r"C:\Program Files\Tesseract-OCR\tesseract.exe",
                r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
                r"C:\Users\{}\AppData\Local\Programs\Tesseract-OCR\tesseract.exe".format(os.getenv('USERNAME'))
            ]
            
            for path in paths:
                if os.path.exists(path):
                    print(f"  [FOUND] {path}")
                    pytesseract.pytesseract.tesseract_cmd = path
                    
                    # Test again
                    try:
                        version = pytesseract.get_tesseract_version()
                        print(f"  [OK] Tesseract version: {version}")
                        
                        # Update data_extractor.py with this path
                        print(f"\n  Add this to data_extractor.py:")
                        print(f"    pytesseract.pytesseract.tesseract_cmd = r'{path}'")
                        break
                    except:
                        continue
        
        print("\n[OK] pytesseract Python package: Installed")
        print("[OK] Pillow (PIL): Installed")
        
    except ImportError as e:
        print(f"[ERROR] Missing package: {e}")
        print("  Run: pip install pytesseract pillow")
    
    print("=" * 60)

if __name__ == "__main__":
    # Test OCR setup first
    test_ocr_setup()
    
    # Then test extraction to Excel
    print("\n\n")
    output = test_extraction_to_excel()
    
    print(f"\n\nTest complete! Check {output} for results.")
    print("\nNext: Upload documents in DocFlowPro and export to Excel to see extracted data!")
