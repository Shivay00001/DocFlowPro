"""
Professional GST Invoice Generator - Matching Industry Standard
Generates GST-compliant tax invoices like visionquantech format
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from datetime import datetime
from typing import List, Dict
import json


class GSTInvoiceGenerator:
    """Generate professional GST-compliant invoices"""
    
    def __init__(self, company_name="DocFlow Pro", company_gst="29ABCDE1234F1Z5"):
        self.company_name = company_name
        self.company_gst = company_gst
        self.styles = getSampleStyleSheet()
        self._setup_styles()
    
    def _setup_styles(self):
        """Setup custom styles"""
        self.styles.add(ParagraphStyle(
            name='CompanyName',
            fontSize=20,
            textColor=colors.HexColor('#2563eb'),  # Blue
            spaceAfter=10,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='InvoiceTitle',
            fontSize=18,
            textColor=colors.black,
            spaceAfter=20,
            spaceBefore=10,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionHeading',
            fontSize=12,
            fontName='Helvetica-Bold',
            spaceAfter=8,
            italics=True
        ))
    
    def generate_gst_invoice(self, invoice_data: Dict, filename: str) -> bool:
        """
        Generate GST-compliant invoice matching visionquantech format
        
        invoice_data structure:
        {
            'invoice_number': '78889',
            'invoice_date': '2025-12-16',
            'company_gst': 'mbzpk3060j',  # Seller GST
            'client_name': 'shivam kumar',
            'client_address': 'noida',
            'client_gst': 'mbzpk6789k',
            'items': [
                {'description': 'Service/Product', 'quantity': 1, 'rate': 7800.00}
            ],
            'cgst_rate': 9.0,  # CGST %
            'sgst_rate': 9.0,  # SGST %
        }
        """
        try:
            doc = SimpleDocTemplate(filename, pagesize=A4,
                                  topMargin=0.75*inch, bottomMargin=0.75*inch,
                                  leftMargin=0.75*inch, rightMargin=0.75*inch)
            story = []
            
            # Parse items if string
            items = invoice_data.get('items', [])
            if isinstance(items, str):
                items = json.loads(items)
            
            # Company Name Header (Blue)
            company = Paragraph(f"<b>{self.company_name}</b>", self.styles['CompanyName'])
            story.append(company)
            story.append(Spacer(1, 0.2*inch))
            
            # TAX INVOICE Title
            title = Paragraph("<b>TAX INVOICE</b>", self.styles['InvoiceTitle'])
            story.append(title)
            story.append(Spacer(1, 0.3*inch))
            
            # Invoice Details (Left aligned)
            invoice_details = [
                [f"<b>Invoice No:</b>", invoice_data.get('invoice_number', 'N/A')],
                [f"<b>Date:</b>", invoice_data.get('invoice_date', datetime.now().strftime('%Y-%m-%d'))],
                [f"<b>GST No:</b>", invoice_data.get('company_gst', self.company_gst)]
            ]
            
            details_table = Table(invoice_details, colWidths=[1.5*inch, 3*inch])
            details_table.setStyle(TableStyle([
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))
            
            story.append(details_table)
            story.append(Spacer(1, 0.3*inch))
            
            # Bill To Section
            bill_to = Paragraph("<b><i>Bill To:</i></b>", self.styles['SectionHeading'])
            story.append(bill_to)
            
            client_name = invoice_data.get('client_name', 'N/A')
            client_address = invoice_data.get('client_address', '')
            client_gst = invoice_data.get('client_gst', '')
            
            client_info_text = f"""
            <font size=11>
            {client_name}<br/>
            {client_address}<br/>
            GST: {client_gst}
            </font>
            """
            client_info = Paragraph(client_info_text, self.styles['Normal'])
            story.append(client_info)
            story.append(Spacer(1, 0.3*inch))
            
            # Items Table (Blue header like visionquantech)
            table_data = [['#', 'Description', 'Qty', 'Rate', 'Amount']]
            
            subtotal = 0
            for idx, item in enumerate(items, 1):
                desc = item.get('description', 'Service/Product')
                qty = float(item.get('quantity', 1))
                rate = float(item.get('rate', 0))
                amount = qty * rate
                subtotal += amount
                
                table_data.append([
                    str(idx),
                    desc,
                    str(int(qty)) if qty == int(qty) else f"{qty:.2f}",
                    f"₹{rate:,.2f}",
                    f"₹{amount:,.2f}"
                ])
            
            items_table = Table(table_data, colWidths=[0.5*inch, 3*inch, 0.8*inch, 1.3*inch, 1.3*inch])
            items_table.setStyle(TableStyle([
                # Header row - Blue background
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('ALIGN', (0, 0), (0, -1), 'CENTER'),  # # column
                ('ALIGN', (1, 0), (1, -1), 'LEFT'),    # Description
                ('ALIGN', (2, 0), (-1, -1), 'RIGHT'),  # Numbers
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                # Data rows
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('TOPPADDING', (0, 1), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
            ]))
            
            story.append(items_table)
            story.append(Spacer(1, 0.3*inch))
            
            # Tax Calculations (Right aligned)
            cgst_rate = float(invoice_data.get('cgst_rate', 9.0))
            sgst_rate = float(invoice_data.get('sgst_rate', 9.0))
            
            cgst_amount = subtotal * (cgst_rate / 100)
            sgst_amount = subtotal * (sgst_rate / 100)
            total_amount = subtotal + cgst_amount + sgst_amount
            
            # Totals table
            totals_data = [
                ['<b>Taxable Amount:</b>', f"₹{subtotal:,.2f}"],
                [f'<b>CGST @ {cgst_rate}%:</b>', f"₹{cgst_amount:,.2f}"],
                [f'<b>SGST @ {sgst_rate}%:</b>', f"₹{sgst_amount:,.2f}"],
                ['', ''],  # Separator
                ['<b>Total Amount:</b>', f"<b>₹{total_amount:,.2f}</b>"]
            ]
            
            totals_table = Table(totals_data, colWidths=[4.5*inch, 2.5*inch])
            totals_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
                ('FONTSIZE', (0, 0), (-1, -2), 11),
                ('FONTSIZE', (0, -1), (-1, -1), 13),
                ('LINEABOVE', (1, -2), (-1, -2), 2, colors.black),
                ('TOPPADDING', (0, -1), (-1, -1), 12),
                ('BOTTOMPADDING', (0, -1), (-1, -1), 12),
            ]))
            
            story.append(totals_table)
            story.append(Spacer(1, 0.5*inch))
            
            # Terms & Conditions (if provided)
            if invoice_data.get('notes') or invoice_data.get('terms'):
                notes = invoice_data.get('notes') or invoice_data.get('terms')
                terms_heading = Paragraph("<b>Terms & Conditions:</b>", self.styles['SectionHeading'])
                story.append(terms_heading)
                terms_para = Paragraph(f"<font size=9>{notes}</font>", self.styles['Normal'])
                story.append(terms_para)
                story.append(Spacer(1, 0.3*inch))
            
            # Footer
            footer_text = """
            <para align=center>
            <font size=8 color='#666666'>
            <b>Thank you for your business!</b><br/>
            This is a computer-generated invoice and does not require a signature.<br/>
            For queries: support@docflowpro.com | +91-XXXXXXXXXX
            </font>
            </para>
            """
            footer = Paragraph(footer_text, self.styles['Normal'])
            story.append(Spacer(1, 0.3*inch))
            story.append(footer)
            
            # Build PDF
            doc.build(story)
            
            print(f"✓ GST Invoice generated: {filename}")
            print(f"  Taxable Amount: ₹{subtotal:,.2f}")
            print(f"  CGST ({cgst_rate}%): ₹{cgst_amount:,.2f}")
            print(f"  SGST ({sgst_rate}%): ₹{sgst_amount:,.2f}")
            print(f"  Total: ₹{total_amount:,.2f}")
            
            return True
            
        except Exception as e:
            print(f"✗ Error generating GST invoice: {e}")
            import traceback
            traceback.print_exc()
            return False


# Helper function for easy usage
def generate_gst_invoice(invoice_data: Dict, filename: str, 
                        company_name="DocFlow Pro", 
                        company_gst="29ABCDE1234F1Z5") -> bool:
    """
    Quick helper to generate GST invoice
    
    Example:
        invoice = {
            'invoice_number': 'INV-001',
            'invoice_date': '2025-12-19',
            'client_name': 'ABC Corporation',
            'client_address': 'Mumbai, Maharashtra',
            'client_gst': '27ABCDE1234F1Z5',
            'items': [
                {'description': 'Professional Services', 'quantity': 1, 'rate': 10000}
            ],
            'cgst_rate': 9.0,
            'sgst_rate': 9.0
        }
        generate_gst_invoice(invoice, 'invoice.pdf')
    """
    generator = GSTInvoiceGenerator(company_name, company_gst)
    return generator.generate_gst_invoice(invoice_data, filename)


if __name__ == "__main__":
    # Test invoice generation
    test_invoice = {
        'invoice_number': '78889',
        'invoice_date': '2025-12-16',
        'company_gst': 'mbzpk3060j',
        'client_name': 'shivam kumar',
        'client_address': 'noida',
        'client_gst': 'mbzpk6789k',
        'items': [
            {'description': 'Service/Product', 'quantity': 1, 'rate': 7800.00}
        ],
        'cgst_rate': 9.0,
        'sgst_rate': 9.0,
        'notes': 'Payment due within 30 days'
    }
    
    generate_gst_invoice(test_invoice, 'test_gst_invoice.pdf',
                        company_name='visionquantech',
                        company_gst='mbzpk3060j')
