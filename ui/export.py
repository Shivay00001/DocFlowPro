"""
Export Panel - FIXED FOR ALL USERS
Critical fix: Properly uses user_id to filter exports
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import os
import re


class ExportPanel(ttk.Frame):
    """Export panel with proper user data isolation - FIXED"""
    
    def __init__(self, parent, engine, user_id):
        """
        Initialize export panel
        CRITICAL: Stores user_id for proper data filtering
        """
        super().__init__(parent)
        self.frame = self  # For panel switching compatibility
        self.engine = engine
        self.user_id = user_id  # CRITICAL FIX: Store user ID
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create export panel widgets"""
        # Title
        title_frame = ttk.Frame(self)
        title_frame.pack(fill='x', padx=20, pady=(20, 10))
        
        title_label = ttk.Label(
            title_frame,
            text="Export Data",
            font=('Helvetica', 16, 'bold')
        )
        title_label.pack(side='left')
        
        # Main content frame
        content_frame = ttk.Frame(self)
        content_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Export options
        options_frame = ttk.LabelFrame(content_frame, text="Export Options", padding=15)
        options_frame.pack(fill='x', pady=(0, 15))
        
        # Export type
        ttk.Label(options_frame, text="Export Type:", font=('Helvetica', 10, 'bold')).grid(
            row=0, column=0, sticky='w', pady=(0, 10)
        )
        
        self.export_type_var = tk.StringVar(value="documents")
        
        ttk.Radiobutton(
            options_frame,
            text="Documents",
            variable=self.export_type_var,
            value="documents"
        ).grid(row=1, column=0, sticky='w', padx=20)
        
        ttk.Radiobutton(
            options_frame,
            text="Invoices",
            variable=self.export_type_var,
            value="invoices"
        ).grid(row=2, column=0, sticky='w', padx=20)
        
        ttk.Radiobutton(
            options_frame,
            text="Complete Data",
            variable=self.export_type_var,
            value="complete"
        ).grid(row=3, column=0, sticky='w', padx=20)
        
        # Format selection
        ttk.Label(options_frame, text="Format:", font=('Helvetica', 10, 'bold')).grid(
            row=0, column=1, sticky='w', pady=(0, 10), padx=(30, 0)
        )
        
        self.format_var = tk.StringVar(value="pdf")
        
        ttk.Radiobutton(
            options_frame,
            text="PDF",
            variable=self.format_var,
            value="pdf"
        ).grid(row=1, column=1, sticky='w', padx=(50, 0))
        
        excel_radio = ttk.Radiobutton(
            options_frame,
            text="Excel (Paid Plans)",
            variable=self.format_var,
            value="excel"
        )
        excel_radio.grid(row=2, column=1, sticky='w', padx=(50, 0))
        
        # Export buttons
        buttons_frame = ttk.Frame(content_frame)
        buttons_frame.pack(fill='x', pady=10)
        
        export_btn = ttk.Button(
            buttons_frame,
            text="Export Data",
            command=self._export_data,
            style='Accent.TButton'
        )
        export_btn.pack(side='left', padx=5)
        
        preview_btn = ttk.Button(
            buttons_frame,
            text="Preview Data",
            command=self._preview_data
        )
        preview_btn.pack(side='left', padx=5)
        
        # Status label
        self.status_label = ttk.Label(
            content_frame,
            text="",
            font=('Helvetica', 9),
            foreground='#666'
        )
        self.status_label.pack(pady=10)
        
        # Statistics frame
        stats_frame = ttk.LabelFrame(content_frame, text="Export Statistics", padding=15)
        stats_frame.pack(fill='both', expand=True, pady=(15, 0))
        
        self.stats_text = tk.Text(
            stats_frame,
            height=10,
            width=60,
            wrap='word',
            font=('Courier', 9)
        )
        self.stats_text.pack(fill='both', expand=True)
        
        # Load initial statistics
        self._load_statistics()
    
    def _load_statistics(self):
        """Load and display export statistics for current user"""
        self.stats_text.delete('1.0', 'end')
        
        try:
            # Get user statistics - FIXED: Uses self.user_id
            stats = self.engine.get_my_statistics()
            
            stats_text = f"""
Export Statistics for Your Account
{'='*50}

Documents:     {stats.get('total_documents', 0)}
Invoices:      {stats.get('total_invoices', 0)}
Total Revenue: ₹{stats.get('total_revenue', 0):.2f}

Last Updated:  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            """
            
            self.stats_text.insert('1.0', stats_text.strip())
            
        except Exception as e:
            self.stats_text.insert('1.0', f"Error loading statistics: {str(e)}")
    
    def _preview_data(self):
        """Preview data to be exported"""
        export_type = self.export_type_var.get()
        
        try:
            # CRITICAL FIX: Get data for current user only
            if export_type == "documents":
                data = self.engine.get_my_documents()
                data_type = "Documents"
            elif export_type == "invoices":
                data = self.engine.get_my_invoices()
                data_type = "Invoices"
            else:  # complete
                data_export = self.engine.export_my_data()
                docs = data_export.get('documents', [])
                invs = data_export.get('invoices', [])
                
                preview_msg = f"""
Complete Data Preview:
=====================

Documents: {len(docs)}
Invoices:  {len(invs)}

This will export all your data in the selected format.
                """
                messagebox.showinfo("Preview", preview_msg.strip())
                return
            
            if not data:
                messagebox.showinfo(
                    "No Data",
                    f"You have no {data_type.lower()} to export.\n\n"
                    f"Create some {data_type.lower()} first, then try exporting again."
                )
                return
            
            # Show preview
            preview_msg = f"{data_type} to export: {len(data)}\n\n"
            preview_msg += "Click 'Export Data' to save to file."
            
            messagebox.showinfo("Preview", preview_msg)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to preview data: {str(e)}")
    
    
    
    def _export_data(self):
        """Export data - STANDALONE WORKING VERSION"""
        export_type = self.export_type_var.get()
        format_type = self.format_var.get()
        
        try:
            # Get user's data
            data = self.engine.export_my_data()
            
            if not data:
                messagebox.showerror("Error", "Failed to retrieve data")
                return
            
            # Prepare data based on type
            if export_type == "documents":
                items = data.get('documents', [])
                title = "Documents Export"
            elif export_type == "invoices":
                items = data.get('invoices', [])
                title = "Invoices Export"
            else:  # complete
                items = data
                title = "Complete Data Export"
            
            # Check if data exists
            if export_type != "complete" and not items:
                messagebox.showinfo("No Data", f"No {export_type} to export")
                return
            
            # Ask save location
            ext = "pdf" if format_type == "pdf" else "xlsx"
            file_path = filedialog.asksaveasfilename(
                defaultextension=f".{ext}",
                initialfile=f"{export_type}_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{ext}",
                filetypes=[(f"{format_type.upper()} files", f"*.{ext}")]
            )
            
            if not file_path:
                return
            
            self.status_label.config(text="Exporting...")
            self.update()
            
            # Export
            if format_type == "pdf":
                success = self._do_pdf_export(export_type, items, file_path, title)
            else:
                success = self._do_excel_export(export_type, items, file_path, title)
            
            if success:
                self.status_label.config(text=f"✓ Exported: {file_path}")
                messagebox.showinfo("Success", f"Exported successfully!\n\n{file_path}")
            else:
                self.status_label.config(text="✗ Export failed")
                messagebox.showerror("Error", "Export failed")
                
        except Exception as e:
            self.status_label.config(text="✗ Error")
            messagebox.showerror("Error", f"Export error:\n{str(e)}")
    
    def _do_pdf_export(self, export_type, items, file_path, title):
        """Direct PDF export using reportlab - SHOWS EXTRACTED DATA"""
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.lib import colors
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            
            doc = SimpleDocTemplate(file_path, pagesize=A4)
            elements = []
            styles = getSampleStyleSheet()
            
            # Title
            elements.append(Paragraph(f"<b>{title}</b>", styles['Title']))
            elements.append(Spacer(1, 20))
            elements.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles['Normal']))
            elements.append(Spacer(1, 20))
            
            if export_type == "documents":
                # Documents table with EXTRACTED INVOICE DATA
                data = [['ID', 'Title', 'Type', 'Extracted Data', 'Created']]
                # Auto-extraction support
                try:
                    from utils.data_extractor import UniversalDataExtractor
                    extractor = UniversalDataExtractor()
                    has_extractor = True
                except:
                    has_extractor = False
                
                for item in items[:100]:
                    # Get extracted data preview (invoice details, OCR text)
                    description = str(item.get('description', ''))
                    ocr_text = str(item.get('ocr_text', ''))
                    extracted = description or ocr_text
                    
                    # AUTO-EXTRACT if missing and file exists
                    if not extracted.strip() and has_extractor:
                        file_path = item.get('file_path', '')
                        if file_path and os.path.exists(file_path):
                            try:
                                auto_data = extractor.extract_from_file(file_path)
                                if auto_data and 'error' not in auto_data:
                                    parts = []
                                    if auto_data.get('invoice_number'): parts.append(f"Inv#{auto_data['invoice_number']}")
                                    if auto_data.get('client_name'): parts.append(f"Client:{auto_data['client_name']}")
                                    if auto_data.get('total_amount'): parts.append(f"Rs.{auto_data['total_amount']}")
                                    extracted = ' | '.join(parts) if parts else '[Auto-extracted: No data]'
                            except:
                                pass
                    
                    # Show first 80 chars of extracted data
                    extracted_preview = extracted[:80] + '...' if len(extracted) > 80 else extracted
                    if not extracted_preview.strip():
                        extracted_preview = '(No data)'
                    
                    title_text = str(item.get('title', ''))[:35]
                    file_type = str(item.get('file_type', 'N/A'))
                    created = str(item.get('created_at', ''))[:10]
                    
                    data.append([
                        str(item.get('id', '')),
                        title_text,
                        file_type,
                        extracted_preview,  # SHOW EXTRACTED DATA!
                        created
                    ])
                
                t = Table(data, colWidths=[25, 120, 40, 250, 60])
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a237e')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 9),
                    ('FONTSIZE', (0, 1), (-1, -1), 7),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP')
                ]))
                elements.append(t)
                
                # Summary
                elements.append(Spacer(1, 20))
                summary_text = f"<b>Total Documents:</b> {len(items)}"
                elements.append(Paragraph(summary_text, styles['Normal']))
                
            elif export_type == "invoices":
                # Invoices table with ALL EXTRACTED DATA
                data = [['Invoice #', 'Client', 'Date', 'Subtotal', 'Tax', 'Total', 'Status']]
                
                total_amount = 0
                total_tax = 0
                
                for item in items[:100]:
                    inv_num = str(item.get('invoice_number', 'N/A'))
                    client = str(item.get('client_name', 'N/A'))[:25]
                    date = str(item.get('invoice_date', 'N/A'))[:10]
                    subtotal = item.get('subtotal', 0)
                    tax = item.get('tax_amount', 0)
                    total = item.get('total_amount', 0)
                    status = str(item.get('status', 'pending')).upper()
                    
                    total_amount += total
                    total_tax += tax
                    
                    data.append([
                        inv_num,
                        client,
                        date,
                        f"₹{subtotal:,.2f}",
                        f"₹{tax:,.2f}",
                        f"₹{total:,.2f}",
                        status
                    ])
                
                # Add totals row
                data.append([
                    '', '', 'TOTAL:', 
                    '', 
                    f"₹{total_tax:,.2f}",
                    f"₹{total_amount:,.2f}",
                    ''
                ])
                
                t = Table(data, colWidths=[70, 120, 60, 70, 70, 80, 60])
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a237e')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('ALIGN', (3, 0), (-1, -1), 'RIGHT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 9),
                    ('FONTSIZE', (0, 1), (-1, -1), 8),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
                    ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
                    ('LINEABOVE', (0, -1), (-1, -1), 2, colors.black)
                ]))
                elements.append(t)
                
                # Summary statistics
                elements.append(Spacer(1, 20))
                summary = f"""
                <b>Summary Statistics:</b><br/>
                Total Invoices: {len(items)}<br/>
                Total Revenue: ₹{total_amount:,.2f}<br/>
                Total Tax Collected: ₹{total_tax:,.2f}<br/>
                """
                elements.append(Paragraph(summary, styles['Normal']))
            
            doc.build(elements)
            return True
            
        except Exception as e:
            print(f"PDF export error: {e}")
            return False
    
    def _do_excel_export(self, export_type, items, file_path, title):
        """Direct Excel export using openpyxl"""
        try:
            from openpyxl import Workbook
            from openpyxl.styles import Font, PatternFill
            
            wb = Workbook()
            ws = wb.active
            ws.title = export_type.capitalize()
            
            if export_type == "documents":
                # ONLY EXTRACTED DATA - No metadata
                headers = ['Document', 'Invoice Number', 'Client Name', 'Amount', 'Date', 'Full Extracted Text']
                ws.append(headers)
                
                for cell in ws[1]:
                    cell.font = Font(bold=True, color="FFFFFF")
                    cell.fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
                
                # Auto-extraction support
                try:
                    from utils.data_extractor import UniversalDataExtractor
                    extractor = UniversalDataExtractor()
                    has_extractor = True
                except:
                    has_extractor = False
                
                for item in items:
                    # Get extracted data from database
                    description = item.get('description', '') or ''
                    ocr_text = item.get('ocr_text', '') or ''
                    
                    # Parse extracted fields
                    invoice_num = ''
                    client_name = ''
                    amount = ''
                    inv_date = ''
                    
                    # Extract from description
                    if 'Invoice:' in description:
                        parts = description.split(',')
                        for part in parts:
                            part = part.strip()
                            if part.startswith('Invoice:'):
                                invoice_num = part.replace('Invoice:', '').strip()
                            elif part.startswith('Client:'):
                                client_name = part.replace('Client:', '').strip()
                            elif part.startswith('Amount:'):
                                amount = part.replace('Amount:', '').strip()
                            elif part.startswith('Date:'):
                                inv_date = part.replace('Date:', '').strip()
                    
                    # If no data, try auto-extract
                    if not invoice_num and has_extractor:
                        file_path = item.get('file_path', '')
                        if file_path and os.path.exists(file_path):
                            try:
                                auto_data = extractor.extract_from_file(file_path)
                                if auto_data and 'error' not in auto_data:
                                    invoice_num = auto_data.get('invoice_number', '')
                                    client_name = auto_data.get('client_name', '')
                                    amount = f"Rs.{auto_data.get('total_amount', '')}" if auto_data.get('total_amount') else ''
                                    inv_date = auto_data.get('invoice_date', '')
                                    ocr_text = auto_data.get('raw_text', '')[:500]
                            except:
                                pass
                    
                    ws.append([
                        item.get('title', ''),
                        invoice_num,
                        client_name,
                        amount,
                        inv_date,
                        ocr_text[:300] if ocr_text else ''
                    ])
                
                # Set column widths
                ws.column_dimensions['A'].width = 25
                ws.column_dimensions['B'].width = 15
                ws.column_dimensions['C'].width = 20
                ws.column_dimensions['D'].width = 15
                ws.column_dimensions['E'].width = 12
                ws.column_dimensions['F'].width = 50
                    
            elif export_type == "invoices":
                headers = ['Invoice #', 'Client', 'Date', 'Amount', 'Status']
                ws.append(headers)
                
                for cell in ws[1]:
                    cell.font = Font(bold=True)
                    cell.fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
                
                for item in items:
                    ws.append([
                        item.get('invoice_number', ''),
                        item.get('client_name', ''),
                        str(item.get('invoice_date', ''))[:10],
                        item.get('total_amount', 0),
                        item.get('status', '')
                    ])
            
            wb.save(file_path)
            return True
            
        except Exception as e:
            print(f"Excel export error: {e}")
    def refresh(self):
        """Refresh panel"""
        self._load_statistics()
    
    def _export_to_pdf(self, data, filename):
        """Export data to PDF"""
        try:
            from reportlab.lib.pagesizes import letter, A4
            from reportlab.lib import colors
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            
            # Ask where to save
            file_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf")],
                initialfile=f"{filename}.pdf"
            )
            
            if not file_path:
                return
            
            # Create PDF
            doc = SimpleDocTemplate(file_path, pagesize=A4)
            elements = []
            styles = getSampleStyleSheet()
            
            # Title
            title = Paragraph(f"<b>DocFlow Pro - Data Export</b>", styles['Title'])
            elements.append(title)
            elements.append(Spacer(1, 20))
            
            # Export info
            info = Paragraph(f"Exported on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal'])
            elements.append(info)
            elements.append(Spacer(1, 20))
            
            # Documents
            if 'documents' in data and data['documents']:
                doc_title = Paragraph("<b>Documents</b>", styles['Heading2'])
                elements.append(doc_title)
                elements.append(Spacer(1, 10))
                
                # Auto-extraction support
                try:
                    from utils.data_extractor import UniversalDataExtractor
                    extractor = UniversalDataExtractor()
                    has_extractor = True
                except:
                    has_extractor = False
                
                doc_data = [['ID', 'Title', 'Type', 'Extracted Data', 'Created']]
                for doc in data['documents'][:50]:  # Limit to 50
                    # Get extracted data or auto-extract
                    extracted = doc.get('description', '') or doc.get('ocr_text', '')
                    
                    # AUTO-EXTRACT if missing
                    if not extracted.strip() and has_extractor:
                        file_path = doc.get('file_path', '')
                        if file_path and os.path.exists(file_path):
                            try:
                                auto_data = extractor.extract_from_file(file_path)
                                if auto_data and 'error' not in auto_data:
                                    parts = []
                                    if auto_data.get('invoice_number'): parts.append(f"Inv#{auto_data['invoice_number']}")
                                    if auto_data.get('client_name'): parts.append(f"Client:{auto_data['client_name']}")
                                    if auto_data.get('total_amount'): parts.append(f"Rs.{auto_data['total_amount']}")
                                    extracted = ' | '.join(parts) if parts else '(No invoice data)'
                            except:
                                pass
                    
                    extracted_preview = extracted[:80] + '...' if len(extracted) > 80 else extracted
                    if not extracted_preview.strip():
                        extracted_preview = '(No data)'
                    
                    doc_data.append([
                        str(doc.get('id', '')),
                        str(doc.get('title', ''))[:35],
                        str(doc.get('file_type', 'N/A')),
                        extracted_preview,  # EXTRACTED DATA!
                        str(doc.get('created_at', ''))[:10]
                    ])
                
                table = Table(doc_data)
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                elements.append(table)
                elements.append(Spacer(1, 20))
            
            # Invoices
            if 'invoices' in data and data['invoices']:
                inv_title = Paragraph("<b>Invoices</b>", styles['Heading2'])
                elements.append(inv_title)
                elements.append(Spacer(1, 10))
                
                inv_data = [['Invoice #', 'Client', 'Date', 'Amount']]
                for inv in data['invoices'][:50]:  # Limit to 50
                    inv_data.append([
                        str(inv.get('invoice_number', '')),
                        str(inv.get('client_name', ''))[:30],
                        str(inv.get('invoice_date', ''))[:10],
                        f"₹{inv.get('total_amount', 0):,.2f}"
                    ])
                
                table = Table(inv_data)
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                elements.append(table)
            
            # Build PDF
            doc.build(elements)
            
            messagebox.showinfo(
                "Success",
                f"Data exported successfully!\n\nFile: {file_path}"
            )
            
        except Exception as e:
            messagebox.showerror("Export Failed", f"PDF export failed:\n{str(e)}")
    
    def _export_to_excel(self, data, filename):
        """Export data to Excel"""
        try:
            from openpyxl import Workbook
            from openpyxl.styles import Font, PatternFill
            
            # Ask where to save
            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx")],
                initialfile=f"{filename}.xlsx"
            )
            
            if not file_path:
                return
            
            # Create workbook
            wb = Workbook()
            
            # Documents sheet - DETAILED INVOICE FORMAT
            if 'documents' in data and data['documents']:
                ws = wb.active
                ws.title = "Documents"
                
                # Detailed Headers matching professional invoice export
                headers = [
                    'id',
                    'document_name', 
                    'invoice_number',
                    'invoice_date',
                    'vendor_name',
                    'vendor_gst',
                    'customer_name',
                    'customer_gst',
                    'taxable_amount',
                    'gst_amount',
                    'net_amount',
                    'total',
                    'status',
                    'created_at',
                    'user_id'
                ]
                ws.append(headers)
                
                # Style headers with blue background
                for cell in ws[1]:
                    cell.font = Font(bold=True, color="FFFFFF")
                    cell.fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
                
                # Auto-extraction support
                try:
                    from utils.data_extractor import UniversalDataExtractor
                    extractor = UniversalDataExtractor()
                    has_extractor = True
                except:
                    has_extractor = False
                
                # Data rows - extract ALL invoice fields
                for doc in data['documents']:
                    # Get existing extracted data
                    description = doc.get('description', '')
                    ocr_text = doc.get('ocr_text', '')
                    
                    # Initialize all fields
                    invoice_data = {
                        'invoice_number': '',
                        'invoice_date': '',
                        'vendor_name': '',
                        'vendor_gst': '',
                        'client_name': '',
                        'customer_gst': '',
                        'taxable_amount': 0,
                        'cgst': 0,
                        'sgst': 0,
                        'total_amount': 0
                    }
                    
                    # Try to extract from existing description/OCR
                    if description or ocr_text:
                        # Parse existing data for invoice fields
                        text = (description + ' ' + ocr_text).lower()
                        
                        # Extract invoice number
                        inv_match = re.search(r'invoice\s*(?:number|#|no)?:?\s*([a-z0-9\-/]+)', text, re.I)
                        if inv_match:
                            invoice_data['invoice_number'] = inv_match.group(1)
                        
                        # Extract client/customer name  
                        client_match = re.search(r'(?:client|customer):\s*([a-z0-9\s]+?)(?:\n|,|$)', text, re.I)
                        if client_match:
                            invoice_data['client_name'] = client_match.group(1).strip()
                        
                        # Extract date
                        date_match = re.search(r'date:\s*([0-9\-/]+)', text, re.I)
                        if date_match:
                            invoice_data['invoice_date'] = date_match.group(1)
                        
                        # Extract amount
                        amt_match = re.search(r'(?:total|amount).*?(?:rs\.?|₹)\s*([0-9,]+)', text, re.I)
                        if amt_match:
                            invoice_data['total_amount'] = amt_match.group(1).replace(',', '')
                    
                    # AUTO-EXTRACT if data still missing
                    if not invoice_data['invoice_number'] and has_extractor:
                        file_path = doc.get('file_path', '')
                        if file_path and os.path.exists(file_path):
                            try:
                                auto_data = extractor.extract_from_file(file_path)
                                if auto_data and 'error' not in auto_data:
                                    # Update with extracted data
                                    invoice_data['invoice_number'] = auto_data.get('invoice_number', '')
                                    invoice_data['invoice_date'] = auto_data.get('invoice_date', '')
                                    invoice_data['client_name'] = auto_data.get('client_name', '')
                                    invoice_data['vendor_name'] = auto_data.get('vendor_name', '')
                                    invoice_data['vendor_gst'] = auto_data.get('vendor_gst', '')
                                    invoice_data['customer_gst'] = auto_data.get('customer_gst', '')
                                    invoice_data['total_amount'] = auto_data.get('total_amount', 0)
                                    
                                    # Calculate GST breakdown (if total given)
                                    if invoice_data['total_amount']:
                                        try:
                                            total = float(str(invoice_data['total_amount']).replace(',', ''))
                                            # Assuming total includes 18% GST (CGST 9% + SGST 9%)
                                            taxable = total / 1.18
                                            gst_amount = total - taxable
                                            invoice_data['taxable_amount'] = round(taxable, 2)
                                            invoice_data['cgst'] = round(gst_amount / 2, 2)
                                            invoice_data['sgst'] = round(gst_amount / 2, 2)
                                        except:
                                            pass
                            except:
                                pass
                    
                    # Append row with ALL fields
                    ws.append([
                        doc.get('id', ''),
                        doc.get('title', '') or doc.get('file_path', '').split('/')[-1],  # document_name
                        invoice_data['invoice_number'] or '',
                        invoice_data['invoice_date'] or '',
                        invoice_data['vendor_name'] or '',
                        invoice_data['vendor_gst'] or '',
                        invoice_data['client_name'] or '',
                        invoice_data['customer_gst'] or '',
                        invoice_data['taxable_amount'] or 0,
                        invoice_data['cgst'] + invoice_data['sgst'] if (invoice_data['cgst'] or invoice_data['sgst']) else 0,  # gst_amount
                        invoice_data['taxable_amount'] + invoice_data['cgst'] + invoice_data['sgst'] if invoice_data['taxable_amount'] else 0,  # net_amount
                        invoice_data['total_amount'] or 0,
                        'pending',  # status - can be enhanced
                        str(doc.get('created_at', ''))[:19],  # created_at (without milliseconds)
                        doc.get('user_id', '')
                    ])
                
                # Set column widths for readability
                ws.column_dimensions['A'].width = 5   # id
                ws.column_dimensions['B'].width = 30  # document_name
                ws.column_dimensions['C'].width = 18  # invoice_number
                ws.column_dimensions['D'].width = 15  # invoice_date
                ws.column_dimensions['E'].width = 20  # vendor_name
                ws.column_dimensions['F'].width = 15  # vendor_gst
                ws.column_dimensions['G'].width = 20  # customer_name
                ws.column_dimensions['H'].width = 15  # customer_gst
                ws.column_dimensions['I'].width = 12  # taxable_amount
                ws.column_dimensions['J'].width = 12  # gst_amount
                ws.column_dimensions['K'].width = 12  # net_amount
                ws.column_dimensions['L'].width = 12  # total
                ws.column_dimensions['M'].width = 10  # status
                ws.column_dimensions['N'].width = 20  # created_at
                ws.column_dimensions['O'].width = 8   # user_id
            
            # Invoices sheet - DETAILED FORMAT (same as documents)
            if 'invoices' in data and data['invoices']:
                if 'documents' in data and data['documents']:
                    ws = wb.create_sheet(title="Invoices")
                else:
                    ws = wb.active
                    ws.title = "Invoices"
                
                # Same 15 columns as documents
                headers = [
                    'id',
                    'invoice_name',
                    'invoice_number',
                    'invoice_date',
                    'vendor_name',
                    'vendor_gst',
                    'customer_name',
                    'customer_gst',
                    'taxable_amount',
                    'gst_amount',
                    'net_amount',
                    'total',
                    'status',
                    'created_at',
                    'user_id'
                ]
                ws.append(headers)
                
                # Style headers
                for cell in ws[1]:
                    cell.font = Font(bold=True, color="FFFFFF")
                    cell.fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
                
                # Data
                for inv in data['invoices']:
                    # Calculate totals from line items if available
                    line_items = inv.get('line_items', [])
                    
                    taxable = 0
                    if line_items:
                        taxable = sum(float(item.get('amount', 0)) for item in line_items)
                    elif inv.get('total_amount'):
                        # If no line items, reverse calculate from total
                        total = float(inv.get('total_amount', 0))
                        taxable = total / 1.18
                    
                    gst = taxable * 0.18
                    cgst = gst / 2
                    sgst = gst / 2
                    net = taxable + gst
                    
                    ws.append([
                        inv.get('id', ''),
                        inv.get('invoice_number', ''),
                        inv.get('invoice_number', ''),
                        inv.get('invoice_date', '') or inv.get('created_at', '')[:10],
                        '',  # vendor_name (can be added to invoice model)
                        inv.get('seller_gst', ''),
                        inv.get('client_name', ''),
                        inv.get('client_gst', ''),
                        round(taxable, 2),
                        round(gst, 2),
                        round(net, 2),
                        inv.get('total_amount', round(net, 2)),
                        inv.get('status', 'generated'),
                        str(inv.get('created_at', ''))[:19],
                        inv.get('user_id', '')
                    ])
                
                # Set column widths
                ws.column_dimensions['A'].width = 5
                ws.column_dimensions['B'].width = 25
                ws.column_dimensions['C'].width = 18
                ws.column_dimensions['D'].width = 15
                ws.column_dimensions['E'].width = 20
                ws.column_dimensions['F'].width = 15
                ws.column_dimensions['G'].width = 20
                ws.column_dimensions['H'].width = 15
                ws.column_dimensions['I'].width = 12
                ws.column_dimensions['J'].width = 12
                ws.column_dimensions['K'].width = 12
                ws.column_dimensions['L'].width = 12
                ws.column_dimensions['M'].width = 10
                ws.column_dimensions['N'].width = 20
                ws.column_dimensions['O'].width = 8
            
                if 'documents' not in data or not data['documents']:
                    ws = wb.active
                    ws.title = "Invoices"
                else:
                    ws = wb.create_sheet("Invoices")
                
                # Headers
                headers = ['Invoice Number', 'Client Name', 'Date', 'Amount', 'Status']
                ws.append(headers)
                
                # Style headers
                for cell in ws[1]:
                    cell.font = Font(bold=True)
                    cell.fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
                
                # Data
                for inv in data['invoices']:
                    ws.append([
                        inv.get('invoice_number', ''),
                        inv.get('client_name', ''),
                        str(inv.get('invoice_date', ''))[:10],
                        inv.get('total_amount', 0),
                        inv.get('status', '')
                    ])
            
            # Save
            wb.save(file_path)
            
            messagebox.showinfo(
                "Success",
                f"Data exported successfully!\n\nFile: {file_path}"
            )
            
        except Exception as e:
            messagebox.showerror("Export Failed", f"Excel export failed:\n{str(e)}")
    
    def _schedule_export(self):
        """Schedule automatic exports"""
        messagebox.showinfo(
            "Scheduled Exports",
            "Scheduled export feature:\n\n"
            "• Daily exports at specified time\n"
            "• Weekly/Monthly reports\n"
            "• Auto-backup to cloud\n\n"
            "Feature: Coming in next update"
        )
    
    def refresh(self):
        """Refresh export panel"""
        pass
