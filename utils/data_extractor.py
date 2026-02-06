"""
Universal Data Extractor
Extract invoice and document data from any file format
"""

import os
import re
from datetime import datetime
from typing import Dict, List, Optional

# Configure Tesseract OCR path for Windows
try:
    import pytesseract
    # Set Tesseract executable path
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
except ImportError:
    pass  # pytesseract not installed


class UniversalDataExtractor:
    """Extract data from multiple file formats"""
    
    @staticmethod
    def extract_from_file(file_path: str) -> Dict:
        """
        Extract data from any supported file format
        Returns: Dictionary with extracted data
        """
        if not os.path.exists(file_path):
            return {'error': 'File not found'}
        
        file_ext = os.path.splitext(file_path)[1].lower()
        
        try:
            if file_ext == '.pdf':
                return UniversalDataExtractor._extract_from_pdf(file_path)
            elif file_ext in ['.xlsx', '.xls']:
                return UniversalDataExtractor._extract_from_excel(file_path)
            elif file_ext == '.csv':
                return UniversalDataExtractor._extract_from_csv(file_path)
            elif file_ext in ['.txt', '.doc', '.docx']:
                return UniversalDataExtractor._extract_from_text(file_path)
            elif file_ext in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.gif', '.webp']:
                return UniversalDataExtractor._extract_from_image(file_path)
            elif file_ext == '.docx':
                return UniversalDataExtractor._extract_from_docx(file_path)
            elif file_ext == '.doc':
                return UniversalDataExtractor._extract_from_doc(file_path)
            else:
                return UniversalDataExtractor._extract_generic(file_path)
        except Exception as e:
            return {'error': f'Extraction failed: {str(e)}'}
    
    @staticmethod
    def _extract_from_pdf(file_path: str) -> Dict:
        """Extract data from PDF"""
        try:
            # Try with PyPDF2 first
            import PyPDF2
            
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
            
            return UniversalDataExtractor._parse_invoice_text(text)
        except:
            # Fallback to basic text extraction
            return UniversalDataExtractor._extract_generic(file_path)
    
    @staticmethod
    def _extract_from_excel(file_path: str) -> Dict:
        """Extract data from Excel"""
        try:
            from openpyxl import load_workbook
            
            wb = load_workbook(file_path)
            ws = wb.active
            
            # Try to find invoice data
            data = {
                'invoice_number': '',
                'client_name': '',
                'date': '',
                'amount': 0,
                'items': []
            }
            
            # Scan cells for invoice data
            for row in ws.iter_rows(max_row=50, max_col=10, values_only=True):
                row_text = ' '.join([str(cell) for cell in row if cell])
                
                # Look for patterns
                if 'invoice' in row_text.lower():
                    inv_match = re.search(r'(?:invoice|inv)[\s:#-]*(\w+[-\w]*)', row_text, re.I)
                    if inv_match:
                        data['invoice_number'] = inv_match.group(1)
                
                if 'client' in row_text.lower() or 'customer' in row_text.lower():
                    data['client_name'] = row_text.split(':')[-1].strip()
                
                # Look for dates
                date_match = re.search(r'\d{1,2}[-/]\d{1,2}[-/]\d{2,4}', row_text)
                if date_match:
                    data['date'] = date_match.group()
                
                # Look for amounts
                amount_match = re.search(r'(?:total|amount)[\s:]*[₹$]?[\s]*([\d,]+\.?\d*)', row_text, re.I)
                if amount_match:
                    try:
                        data['amount'] = float(amount_match.group(1).replace(',', ''))
                    except:
                        pass
            
            return data
        except Exception as e:
            return {'error': f'Excel extraction failed: {str(e)}'}
    
    @staticmethod
    def _extract_from_csv(file_path: str) -> Dict:
        """Extract data from CSV"""
        try:
            import csv
            
            data = {
                'items': [],
                'total_amount': 0
            }
            
            with open(file_path, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    # Try to extract item data
                    item = {}
                    for key, value in row.items():
                        if 'description' in key.lower() or 'item' in key.lower():
                            item['description'] = value
                        elif 'quantity' in key.lower() or 'qty' in key.lower():
                            try:
                                item['quantity'] = float(value)
                            except:
                                pass
                        elif 'rate' in key.lower() or 'price' in key.lower():
                            try:
                                item['rate'] = float(value.replace('₹', '').replace(',', ''))
                            except:
                                pass
                    
                    if item:
                        data['items'].append(item)
            
            # Calculate total
            data['total_amount'] = sum(
                item.get('quantity', 1) * item.get('rate', 0) 
                for item in data['items']
            )
            
            return data
        except Exception as e:
            return {'error': f'CSV extraction failed: {str(e)}'}
    
    @staticmethod
    def _extract_from_text(file_path: str) -> Dict:
        """Extract data from text file"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                text = file.read()
            
            return UniversalDataExtractor._parse_invoice_text(text)
        except Exception as e:
            return {'error': f'Text extraction failed: {str(e)}'}
    
    @staticmethod
    def _extract_from_image(file_path: str) -> Dict:
        """Extract data from image using OCR"""
        try:
            # Try with pytesseract
            import pytesseract
            from PIL import Image
            
            # Configure Tesseract path for Windows
            import os
            import platform
            if platform.system() == 'Windows':
                # Try common Tesseract installation paths
                tesseract_paths = [
                    r'C:\Program Files\Tesseract-OCR\tesseract.exe',
                    r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
                    r'C:\Tesseract-OCR\tesseract.exe'
                ]
                
                for path in tesseract_paths:
                    if os.path.exists(path):
                        pytesseract.pytesseract.tesseract_cmd = path
                        break
            
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image)
            
            result = UniversalDataExtractor._parse_invoice_text(text)
            result['ocr_success'] = True
            result['extraction_method'] = 'OCR'
            return result
            
        except ImportError:
            # pytesseract not installed
            return {
                'error': 'OCR not available',
                'note': 'Install pytesseract: pip install pytesseract',
                'file_type': 'image',
                'file_name': os.path.basename(file_path),
                'ocr_success': False
            }
        except Exception as e:
            # OCR failed - provide helpful error
            error_msg = str(e)
            if 'tesseract' in error_msg.lower():
                return {
                    'error': 'Tesseract OCR not installed',
                    'note': 'Please install Tesseract-OCR from https://github.com/UB-Mannheim/tesseract/wiki',
                    'instructions': 'See OCR_SETUP.md for installation guide',
                    'file_type': 'image',
                    'file_name': os.path.basename(file_path),
                    'ocr_success': False
                }
            else:
                return {
                    'error': f'OCR extraction failed: {error_msg}',
                    'note': 'Try using a clearer image with better contrast',
                    'file_type': 'image',
                    'file_name': os.path.basename(file_path),
                    'ocr_success': False
                }
    
    @staticmethod
    def _extract_generic(file_path: str) -> Dict:
        """Generic extraction for unknown formats"""
        return {
            'file_name': os.path.basename(file_path),
            'file_size': os.path.getsize(file_path),
            'file_type': os.path.splitext(file_path)[1],
            'note': 'Auto-extraction not available for this format'
        }
    
    @staticmethod
    def _extract_from_docx(file_path: str) -> Dict:
        """Extract text from DOCX (Word) files"""
        try:
            from docx import Document
            
            doc = Document(file_path)
            text = '\n'.join([para.text for para in doc.paragraphs])
            
            # Also get text from tables
            for table in doc.tables:
                for row in table.rows:
                    for cell in row.cells:
                        text += ' ' + cell.text
            
            result = UniversalDataExtractor._parse_invoice_text(text)
            result['raw_text'] = text[:1000]
            result['extraction_method'] = 'DOCX'
            return result
            
        except ImportError:
            # python-docx not installed, try basic text extraction
            return UniversalDataExtractor._extract_from_text(file_path)
        except Exception as e:
            return {'error': f'DOCX extraction failed: {str(e)}'}
    
    @staticmethod
    def _extract_from_doc(file_path: str) -> Dict:
        """Extract text from older DOC files"""
        try:
            # Try with textract or antiword
            import subprocess
            result = subprocess.run(
                ['antiword', file_path],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                text = result.stdout
                extracted = UniversalDataExtractor._parse_invoice_text(text)
                extracted['raw_text'] = text[:1000]
                return extracted
        except:
            pass
        
        # Fallback to basic reading
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
                # Try to extract readable text
                text = content.decode('utf-8', errors='ignore')
                # Clean up binary garbage
                text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', ' ', text)
                return UniversalDataExtractor._parse_invoice_text(text)
        except Exception as e:
            return {'error': f'DOC extraction failed: {str(e)}'}
    
    @staticmethod
    def _parse_invoice_text(text: str) -> Dict:
        """Parse invoice data from text"""
        data = {
            'invoice_number': '',
            'client_name': '',
            'invoice_date': '',
            'due_date': '',
            'total_amount': 0,
            'tax_amount': 0,
            'items': []
        }
        
        # Invoice number patterns
        inv_patterns = [
            r'invoice\s*(?:number|no|#)[\s:]*([A-Z0-9-]+)',
            r'inv[\s#]*([A-Z0-9-]+)',
            r'bill\s*(?:no|number)[\s:]*([A-Z0-9-]+)'
        ]
        for pattern in inv_patterns:
            match = re.search(pattern, text, re.I)
            if match:
                data['invoice_number'] = match.group(1)
                break
        
        # Client/Customer name
        client_patterns = [
            r'(?:client|customer|bill\s*to|sold\s*to)[\s:]*\n?\s*([^\n]+)',
            r'(?:to|for)[\s:]+([A-Z][A-Za-z\s&.]+(?:Ltd|Inc|LLC|Pvt)?)'
        ]
        for pattern in client_patterns:
            match = re.search(pattern, text, re.I)
            if match:
                name = match.group(1).strip()
                if len(name) > 3 and len(name) < 100:
                    data['client_name'] = name
                    break
        
        # Dates
        date_pattern = r'(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})'
        dates = re.findall(date_pattern, text)
        if dates:
            data['invoice_date'] = dates[0]
            if len(dates) > 1:
                data['due_date'] = dates[1]
        
        # Amounts
        amount_patterns = [
            r'(?:total|grand\s*total|amount\s*due)[\s:]*[₹$]?\s*([\d,]+\.?\d*)',
            r'[₹$]\s*([\d,]+\.?\d*)\s*(?:total|payable)',
        ]
        for pattern in amount_patterns:
            match = re.search(pattern, text, re.I)
            if match:
                try:
                    data['total_amount'] = float(match.group(1).replace(',', ''))
                    break
                except:
                    pass
        
        # Tax
        tax_pattern = r'(?:tax|gst|vat)[\s:]*[₹$]?\s*([\d,]+\.?\d*)'
        tax_match = re.search(tax_pattern, text, re.I)
        if tax_match:
            try:
                data['tax_amount'] = float(tax_match.group(1).replace(',', ''))
            except:
                pass
        
        # Items (simple extraction)
        # Look for lines with item description and amounts
        lines = text.split('\n')
        for line in lines:
            # Pattern: Description ... Amount
            if re.search(r'\d+\.?\d*', line):
                amount_match = re.search(r'[₹$]?\s*([\d,]+\.?\d+)', line)
                if amount_match:
                    desc = line[:line.rfind(amount_match.group())].strip()
                    if desc and len(desc) > 3:
                        try:
                            data['items'].append({
                                'description': desc,
                                'amount': float(amount_match.group(1).replace(',', ''))
                            })
                        except:
                            pass
        
        # If no invoice number found, generate one
        if not data['invoice_number']:
            data['invoice_number'] = f"EXT-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        return data


class SmartDocumentParser:
    """Smart parsing for different document types"""
    
    @staticmethod
    def identify_document_type(data: Dict) -> str:
        """Identify what type of document this is"""
        text = str(data).lower()
        
        if 'invoice' in text or 'bill' in text:
            return 'invoice'
        elif 'quote' in text or 'proposal' in text:
            return 'quote'
        elif 'receipt' in text:
            return 'receipt'
        elif 'purchase order' in text or 'po' in text:
            return 'purchase_order'
        else:
            return 'document'
    
    @staticmethod
    def extract_key_fields(data: Dict) -> Dict:
        """Extract and validate key fields"""
        extracted = {}
        
        # Clean and validate invoice number
        if data.get('invoice_number'):
            extracted['invoice_number'] = data['invoice_number'].strip()
        
        # Clean client name
        if data.get('client_name'):
            name = data['client_name'].strip()
            # Remove common prefixes
            name = re.sub(r'^(to|for|client)[\s:]+', '', name, flags=re.I)
            extracted['client_name'] = name
        
        # Parse and format date
        if data.get('invoice_date'):
            try:
                # Try to parse date
                date_str = data['invoice_date']
                # Convert to YYYY-MM-DD format
                extracted['invoice_date'] = date_str
            except:
                extracted['invoice_date'] = datetime.now().strftime('%Y-%m-%d')
        
        # Ensure amount is float
        if data.get('total_amount'):
            try:
                extracted['total_amount'] = float(data['total_amount'])
            except:
                extracted['total_amount'] = 0
        
        return extracted
