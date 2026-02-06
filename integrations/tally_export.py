"""
Tally Integration - Export invoices to Tally XML format
"""

from typing import List, Dict
from datetime import datetime
import xml.etree.ElementTree as ET


class TallyExporter:
    """Export invoices to Tally-compatible XML format"""
    
    def __init__(self):
        self.company_name = "DocFlow Pro Company"
    
    def export_invoices_to_xml(self, invoices: List[Dict], output_file: str) -> bool:
        """
        Export invoices to Tally XML
        Returns: True if successful
        """
        try:
            # Create XML structure
            envelope = ET.Element('ENVELOPE')
            
            header = ET.SubElement(envelope, 'HEADER')
            ET.SubElement(header, 'TALLYREQUEST').text = 'Import Data'
            
            body = ET.SubElement(envelope, 'BODY')
            import_data = ET.SubElement(body, 'IMPORTDATA')
            request_desc = ET.SubElement(import_data, 'REQUESTDESC')
            ET.SubElement(request_desc, 'REPORTNAME').text = 'Vouchers'
            
            request_data = ET.SubElement(import_data, 'REQUESTDATA')
            
            # Add each invoice as voucher
            for invoice in invoices:
                self._add_voucher(request_data, invoice)
            
            # Write to file
            tree = ET.ElementTree(envelope)
            tree.write(output_file, encoding='utf-8', xml_declaration=True)
            
            return True
            
        except Exception as e:
            print(f"Tally export error: {e}")
            return False
    
    def _add_voucher(self, parent, invoice: Dict):
        """Add invoice as Tally voucher"""
        voucher = ET.SubElement(parent, 'TALLYMESSAGE', xmlns='TallyData')
        
        # Voucher details
        voucher_elem = ET.SubElement(voucher, 'VOUCHER', REMOTEID='', VCHKEY='', VCHTYPE='Sales')
        
        # Invoice date
        date_str = invoice.get('invoice_date', datetime.now().strftime('%Y%m%d'))
        ET.SubElement(voucher_elem, 'DATE').text = date_str
        
        # Invoice number
        ET.SubElement(voucher_elem, 'VOUCHERNUMBER').text = invoice.get('invoice_number', 'INV-000')
        
        # Party name (client)
        ET.SubElement(voucher_elem, 'PARTYLEDGERNAME').text = invoice.get('client_name', 'Unknown')
        
        # Amount
        amount = invoice.get('total_amount', 0)
        ET.SubElement(voucher_elem, 'AMOUNT').text = str(amount)
        
        # Ledger entries
        ledger_entries = ET.SubElement(voucher_elem, 'ALLLEDGERENTRIES.LIST')
        
        # Debit entry (Customer)
        debit_entry = ET.SubElement(ledger_entries, 'LEDGERNAME')
        debit_entry.text = invoice.get('client_name', 'Unknown')
        ET.SubElement(ledger_entries, 'ISDEEMEDPOSITIVE').text = 'Yes'
        ET.SubElement(ledger_entries, 'AMOUNT').text = str(amount)
        
        # Credit entry (Sales)
        credit_entries = ET.SubElement(voucher_elem, 'ALLLEDGERENTRIES.LIST')
        credit_ledger = ET.SubElement(credit_entries, 'LEDGERNAME')
        credit_ledger.text = 'Sales'
        ET.SubElement(credit_entries, 'ISDEEMEDPOSITIVE').text = 'No'
        ET.SubElement(credit_entries, 'AMOUNT').text = str(-amount)
    
    def export_gst_data(self, invoices: List[Dict], output_file: str) -> bool:
        """Export GST data for Tally"""
        try:
            envelope = ET.Element('ENVELOPE')
            
            # Similar structure but with GST fields
            # Implementation simplified for now
            
            tree = ET.ElementTree(envelope)
            tree.write(output_file, encoding='utf-8', xml_declaration=True)
            
            return True
        except:
            return False


class TallyValidator:
    """Validate data before Tally export"""
    
    @staticmethod
    def validate_invoice(invoice: Dict) -> Dict:
        """
        Validate if invoice can be exported to Tally
        Returns: {'valid': bool, 'errors': list}
        """
        errors = []
        
        # Required fields
        if not invoice.get('invoice_number'):
            errors.append("Missing invoice number")
        
        if not invoice.get('client_name'):
            errors.append("Missing client name")
        
        if not invoice.get('total_amount') or invoice.get('total_amount') <= 0:
            errors.append("Invalid amount")
        
        if not invoice.get('invoice_date'):
            errors.append("Missing invoice date")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors
        }
    
    @staticmethod
    def validate_batch(invoices: List[Dict]) -> Dict:
        """Validate batch of invoices"""
        valid_count = 0
        invalid_invoices = []
        
        for idx, invoice in enumerate(invoices):
            result = TallyValidator.validate_invoice(invoice)
            if result['valid']:
                valid_count += 1
            else:
                invalid_invoices.append({
                    'index': idx,
                    'invoice_number': invoice.get('invoice_number', 'N/A'),
                    'errors': result['errors']
                })
        
        return {
            'total': len(invoices),
            'valid': valid_count,
            'invalid': len(invalid_invoices),
            'invalid_list': invalid_invoices
        }
