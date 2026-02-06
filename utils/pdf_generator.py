"""
PDF Generator for DocFlow Pro
Generates PDF reports, invoices, and document exports
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from datetime import datetime
from typing import List, Dict
import os


class PDFGenerator:
    """Generate professional PDF documents"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a237e'),
            spaceAfter=30,
            alignment=TA_CENTER
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#283593'),
            spaceAfter=12,
        ))
        
        self.styles.add(ParagraphStyle(
            name='RightAlign',
            parent=self.styles['Normal'],
            alignment=TA_RIGHT,
        ))
    
    def generate_invoice_pdf(self, invoice_data: Dict, filename: str) -> bool:
        """Generate PROFESSIONAL invoice PDF"""
        try:
            doc = SimpleDocTemplate(filename, pagesize=A4, 
                                  topMargin=0.5*inch, bottomMargin=0.5*inch)
            story = []
            
            # Company Header (Blue bar)
            header_data = [[
                Paragraph("<b>DocFlow Pro</b><br/><font size=8>Professional Invoice Management</font>", 
                         self.styles['CustomTitle'])
            ]]
            header_table = Table(header_data, colWidths=[7*inch])
            header_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#1a237e')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, -1), 15),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
            ]))
            story.append(header_table)
            story.append(Spacer(1, 0.3*inch))
            
            # Invoice Title
            title = Paragraph("<b>INVOICE</b>", self.styles['CustomTitle'])
            story.append(title)
            story.append(Spacer(1, 0.2*inch))
            
            # Invoice Details (2 column layout)
            invoice_info_left = [
                ['<b>Invoice Number:</b>', invoice_data.get('invoice_number', 'N/A')],
                ['<b>Invoice Date:</b>', invoice_data.get('invoice_date', 'N/A')],
                ['<b>Due Date:</b>', invoice_data.get('due_date', 'N/A')],
            ]
            
            invoice_info_right = [
                ['<b>Status:</b>', f"<font color='green'><b>{invoice_data.get('status', 'PENDING').upper()}</b></font>"],
                ['<b>Payment Terms:</b>', 'Net 30 Days'],
                ['<b>Currency:</b>', 'INR (₹)'],
            ]
            
            # Create two-column layout
            left_table = Table(invoice_info_left, colWidths=[1.5*inch, 2*inch])
            left_table.setStyle(TableStyle([
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#1a237e')),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]))
            
            right_table = Table(invoice_info_right, colWidths=[1.5*inch, 2*inch])
            right_table.setStyle(TableStyle([
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#1a237e')),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]))
            
            combined_info = Table([[left_table, right_table]], colWidths=[3.5*inch, 3.5*inch])
            story.append(combined_info)
            story.append(Spacer(1, 0.3*inch))
            
            # Bill To Section
            bill_to_heading = Paragraph("<b>BILL TO:</b>", self.styles['CustomHeading'])
            story.append(bill_to_heading)
            story.append(Spacer(1, 0.1*inch))
            
            client_info = f"""
            <b>{invoice_data.get('client_name', 'N/A')}</b><br/>
            {invoice_data.get('client_email', '')}<br/>
            {invoice_data.get('client_address', '')}
            """
            client_para = Paragraph(client_info, self.styles['Normal'])
            story.append(client_para)
            story.append(Spacer(1, 0.3*inch))
            
            # Items Table
            items = invoice_data.get('items', [])
            if isinstance(items, str):
                import json
                items = json.loads(items)
            
            items_data = [['#', 'Description', 'Quantity', 'Rate (₹)', 'Amount (₹)']]
            
            for idx, item in enumerate(items, 1):
                desc = item.get('description', '')
                qty = item.get('quantity', 0)
                rate = item.get('rate', 0)
                amount = qty * rate
                items_data.append([
                    str(idx),
                    desc,
                    str(qty),
                    f"{rate:,.2f}",
                    f"{amount:,.2f}"
                ])
            
            items_table = Table(items_data, colWidths=[0.5*inch, 3.5*inch, 1*inch, 1.5*inch, 1.5*inch])
            items_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a237e')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (0, -1), 'CENTER'),
                ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                ('ALIGN', (2, 0), (-1, -1), 'RIGHT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('TOPPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
            ]))
            
            story.append(items_table)
            story.append(Spacer(1, 0.3*inch))
            
            # Totals Section (Right-aligned)
            subtotal = invoice_data.get('subtotal', 0)
            tax_rate = invoice_data.get('tax_rate', 0)
            tax_amount = invoice_data.get('tax_amount', 0)
            total = invoice_data.get('total_amount', 0)
            
            totals_data = [
                ['Subtotal:', f"₹ {subtotal:,.2f}"],
                [f'Tax ({tax_rate}% GST):', f"₹ {tax_amount:,.2f}"],
                ['<b>Total Amount:</b>', f"<b>₹ {total:,.2f}</b>"],
            ]
            
            totals_table = Table(totals_data, colWidths=[5*inch, 2*inch])
            totals_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
                ('FONTSIZE', (0, 0), (-1, -2), 10),
                ('FONTSIZE', (0, -1), (-1, -1), 12),
                ('TEXTCOLOR', (0, -1), (-1, -1), colors.HexColor('#1a237e')),
                ('LINEABOVE', (1, -1), (-1, -1), 2, colors.HexColor('#1a237e')),
                ('TOPPADDING', (0, -1), (-1, -1), 10),
                ('BOTTOMPADDING', (0, -1), (-1, -1), 10),
            ]))
            
            story.append(totals_table)
            story.append(Spacer(1, 0.4*inch))
            
            # Notes
            if invoice_data.get('notes'):
                notes_heading = Paragraph("<b>Notes:</b>", self.styles['CustomHeading'])
                story.append(notes_heading)
                notes = Paragraph(invoice_data['notes'], self.styles['Normal'])
                story.append(notes)
                story.append(Spacer(1, 0.3*inch))
            
            # Footer
            footer_text = """
            <para align=center>
            <font size=8 color='#666666'>
            Thank you for your business!<br/>
            For queries, contact: support@docflowpro.com | +91-XXXXXXXXXX
            </font>
            </para>
            """
            footer = Paragraph(footer_text, self.styles['Normal'])
            story.append(Spacer(1, 0.3*inch))
            story.append(footer)
            
            # Build PDF
            doc.build(story)
            return True
            
        except Exception as e:
            print(f"Error generating invoice PDF: {e}")
            return False
    
    def generate_documents_export_pdf(self, documents: List[Dict], filename: str) -> bool:
        """Generate PDF export of documents list"""
        try:
            doc = SimpleDocTemplate(filename, pagesize=A4)
            story = []
            
            # Title
            title = Paragraph("Documents Export", self.styles['CustomTitle'])
            story.append(title)
            
            export_date = Paragraph(f"Exported on: {datetime.now().strftime('%Y-%m-%d %H:%M')}", 
                                   self.styles['RightAlign'])
            story.append(export_date)
            story.append(Spacer(1, 0.3*inch))
            
            # Summary
            summary_text = f"Total Documents: {len(documents)}"
            summary = Paragraph(summary_text, self.styles['CustomHeading'])
            story.append(summary)
            story.append(Spacer(1, 0.2*inch))
            
            # Documents table
            table_data = [['#', 'Title', 'Category', 'Created Date']]
            
            for idx, doc in enumerate(documents, 1):
                title_text = doc.get('title', 'Untitled')[:50]  # Truncate long titles
                category = doc.get('category', 'N/A')
                created = doc.get('created_at', 'N/A')
                if created and len(created) > 10:
                    created = created[:10]  # Show only date
                
                table_data.append([str(idx), title_text, category, created])
            
            docs_table = Table(table_data, colWidths=[0.5*inch, 3.5*inch, 1.5*inch, 1.5*inch])
            docs_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a237e')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
            ]))
            
            story.append(docs_table)
            
            # Build PDF
            doc.build(story)
            return True
            
        except Exception as e:
            print(f"Error generating documents export PDF: {e}")
            return False
    
    def generate_invoices_export_pdf(self, invoices: List[Dict], filename: str) -> bool:
        """Generate PDF export of invoices list"""
        try:
            doc = SimpleDocTemplate(filename, pagesize=A4)
            story = []
            
            # Title
            title = Paragraph("Invoices Export", self.styles['CustomTitle'])
            story.append(title)
            
            export_date = Paragraph(f"Exported on: {datetime.now().strftime('%Y-%m-%d %H:%M')}", 
                                   self.styles['RightAlign'])
            story.append(export_date)
            story.append(Spacer(1, 0.3*inch))
            
            # Summary
            total_amount = sum(inv.get('total_amount', 0) for inv in invoices)
            summary_text = f"Total Invoices: {len(invoices)} | Total Amount: ₹{total_amount:.2f}"
            summary = Paragraph(summary_text, self.styles['CustomHeading'])
            story.append(summary)
            story.append(Spacer(1, 0.2*inch))
            
            # Invoices table
            table_data = [['Invoice #', 'Client', 'Date', 'Amount', 'Status']]
            
            for inv in invoices:
                inv_num = inv.get('invoice_number', 'N/A')
                client = inv.get('client_name', 'N/A')[:30]
                date = inv.get('invoice_date', 'N/A')
                amount = f"₹{inv.get('total_amount', 0):.2f}"
                status = inv.get('status', 'pending').upper()
                
                table_data.append([inv_num, client, date, amount, status])
            
            inv_table = Table(table_data, colWidths=[1.2*inch, 2.5*inch, 1.2*inch, 1.2*inch, 1*inch])
            inv_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a237e')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (3, 0), (3, -1), 'RIGHT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
            ]))
            
            story.append(inv_table)
            
            # Build PDF
            doc.build(story)
            return True
            
        except Exception as e:
            print(f"Error generating invoices export PDF: {e}")
            return False
    
    def generate_invoice(self, invoice_data: Dict, filename: str) -> bool:
        """Alias for generate_invoice_pdf for compatibility"""
        return self.generate_invoice_pdf(invoice_data, filename)
