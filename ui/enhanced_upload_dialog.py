"""
Enhanced Document Upload Dialog with Auto-Extraction
"""

def create_enhanced_upload_dialog(self, file_path):
    """
    Enhanced upload dialog with invoice fields and auto-extraction
    To be added to DocumentsPanel class
    """
    dialog = tk.Toplevel(self)
    dialog.title("Review and Edit Extracted Data")
    dialog.geometry("750x750")
    dialog.transient(self)
    dialog.grab_set()
    
    # Center dialog
    dialog.update_idletasks()
    x = (dialog.winfo_screenwidth() // 2) - 375
    y = (dialog.winfo_screenheight() // 2) - 375
    dialog.geometry(f"750x750+{x}+{y}")
    
    # Header
    header = tk.Frame(dialog, bg='#f0f0f0', height=80)
    header.pack(fill='x')
    header.pack_propagate(False)
    
    tk.Label(
        header,
        text="Review and Edit Extracted Data",
        font=('Segoe UI', 18, 'bold'),
        bg='#f0f0f0',
        fg='#333'
    ).pack(pady=25)
    
    # Auto-extract data first
    extracted_data = {}
    try:
        from utils.data_extractor import UniversalDataExtractor
        extractor = UniversalDataExtractor()
        extracted_data = extractor.extract_from_file(file_path)
    except:
        pass
    
    # Scrollable form area
    canvas = tk.Canvas(dialog, bg='white')
    scrollbar = tk.Scrollbar(dialog, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg='white')
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Form fields
    form_frame = tk.Frame(scrollable_frame, bg='white')
    form_frame.pack(fill='both', expand=True, padx=40, pady=30)
    
    entries = {}
    
    # Define all fields with labels and extracted data keys
    fields = [
        ("Invoice Number", "invoice_number", extracted_data.get('invoice_number', '')),
        ("Invoice Date", "invoice_date", extracted_data.get('invoice_date', datetime.now().strftime('%Y-%m-%d'))),
        ("Vendor Name", "vendor_name", extracted_data.get('client_name', '')),
        ("Vendor GST", "vendor_gst", extracted_data.get('client_gst', '')),
        ("Vendor PAN", "vendor_pan", extracted_data.get('client_pan', '')),
        ("Customer GST", "customer_gst", ''),
        ("Taxable Amount", "taxable_amount", str(extracted_data.get('subtotal', 0))),
        ("Total Amount", "total_amount", str(extracted_data.get('total_amount', 0))),
    ]
    
    for label_text, field_key, default_value in fields:
        # Label
        label = tk.Label(
            form_frame,
            text=label_text,
            font=('Segoe UI', 10),
            bg='white',
            fg='#333'
        )
        label.pack(anchor='w', pady=(10, 5))
        
        # Entry
        entry = tk.Entry(
            form_frame,
            font=('Segoe UI', 11),
            relief='solid',
            borderwidth=1
        )
        entry.pack(fill='x', ipady=8, pady=(0, 5))
        entry.insert(0, default_value)
        
        entries[field_key] = entry
    
    # Pack canvas and scrollbar
    canvas.pack(side="left", fill="both", expand=True, padx=(20, 0), pady=(0, 20))
    scrollbar.pack(side="right", fill="y", pady=(0, 20))
    
    # Save button at bottom
    save_btn = tk.Button(
        dialog,
        text="Save",
        font=('Segoe UI', 12),
        bg='#4CAF50',
        fg='white',
        relief='flat',
        cursor='hand2',
        padx=40,
        pady=10,
        command=lambda: self._save_enhanced_document(entries, file_path, dialog)
    )
    save_btn.pack(pady=20)

def _save_enhanced_document(self, entries, file_path, dialog):
    """Save document with extracted invoice data"""
    try:
        # Extract all values
        data = {key: entry.get().strip() for key, entry in entries.items()}
        
        # Create document title
        title = f"{data.get('invoice_number', 'DOC')} - {data.get('vendor_name', 'Vendor')}"
        
        # Create document
        success, result = self.engine.create_document(
            title=title,
            file_path=file_path,
            category='Invoice',
            tags=f"{data.get('invoice_date', '')}, GST: {data.get('vendor_gst', '')}",
            description=f"""
Invoice Details:
Number: {data['invoice_number']}
Date: {data['invoice_date']}
Vendor: {data['vendor_name']}
Vendor GST: {data['vendor_gst']}
Vendor PAN: {data['vendor_pan']}
Customer GST: {data['customer_gst']}
Taxable: ₹{data['taxable_amount']}
Total: ₹{data['total_amount']}
            """.strip()
        )
        
        if success:
            # Also create invoice if data is complete
            if data.get('invoice_number') and data.get('vendor_name') and data.get('total_amount'):
                try:
                    items = [{
                        'description': 'Service/Product',
                        'quantity': 1,
                        'rate': float(data.get('taxable_amount', 0) or 0)
                    }]
                    
                    self.engine.create_invoice(
                        invoice_number=data['invoice_number'],
                        client_name=data['vendor_name'],
                        invoice_date=data['invoice_date'],
                        items=items,
                        client_gst=data.get('vendor_gst', ''),
                        client_pan=data.get('vendor_pan', ''),
                        tax_rate=18.0
                    )
                except:
                    pass  # Invoice creation is optional
            
            messagebox.showinfo("Success", "Document and invoice data saved successfully!")
            dialog.destroy()
            self.refresh()
        else:
            messagebox.showerror("Error", result)
            
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save:\n{str(e)}")
