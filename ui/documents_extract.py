    
    def _extract_data_from_file(self):
        """Extract data from uploaded file"""
        from tkinter import filedialog
        from utils.data_extractor import UniversalDataExtractor, SmartDocumentParser
        
        # Select file
        file_path = filedialog.askopenfilename(
            title="Select File to Extract Data",
            filetypes=[
                ("All Supported", "*.pdf;*.xlsx;*.xls;*.csv;*.txt;*.jpg;*.png"),
                ("PDF files", "*.pdf"),
                ("Excel files", "*.xlsx;*.xls"),
                ("CSV files", "*.csv"),
                ("Text files", "*.txt"),
                ("Images", "*.jpg;*.jpeg;*.png;*.bmp"),
                ("All files", "*.*")
            ]
        )
        
        if not file_path:
            return
        
        # Show processing message
        processing_dialog = tk.Toplevel(self)
        processing_dialog.title("Extracting Data")
        processing_dialog.geometry("400x150")
        processing_dialog.transient(self)
        
        tk.Label(
            processing_dialog,
            text="🔄 Extracting data from file...",
            font=('Segoe UI', 12)
        ).pack(pady=30)
        
        tk.Label(
            processing_dialog,
            text=os.path.basename(file_path),
            font=('Segoe UI', 10),
            fg='#666'
        ).pack()
        
        processing_dialog.update()
        
        try:
            # Extract data
            extractor = UniversalDataExtractor()
            extracted_data = extractor.extract_from_file(file_path)
            
            processing_dialog.destroy()
            
            if 'error' in extracted_data:
                messagebox.showerror("Extraction Error", extracted_data['error'])
                return
            
            # Show extracted data
            self._show_extracted_data(extracted_data, file_path)
            
        except Exception as e:
            processing_dialog.destroy()
            messagebox.showerror("Error", f"Data extraction failed:\n{str(e)}")
    
    def _show_extracted_data(self, data, file_path):
        """Show extracted data and allow editing"""
        dialog = tk.Toplevel(self)
        dialog.title("Extracted Data")
        dialog.geometry("600x700")
        dialog.transient(self)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - 300
        y = (dialog.winfo_screenheight() // 2) - 350
        dialog.geometry(f"600x700+{x}+{y}")
        
        # Header
        tk.Label(
            dialog,
            text="✅ Data Extracted Successfully!",
            font=('Segoe UI', 16, 'bold'),
            fg='#4caf50'
        ).pack(pady=15)
        
        tk.Label(
            dialog,
            text="Review and edit the extracted data below",
            font=('Segoe UI', 10),
            fg='#666'
        ).pack()
        
        # Form
        form_frame = tk.Frame(dialog)
        form_frame.pack(fill='both', expand=True, padx=30, pady=20)
        
        # Invoice number
        tk.Label(form_frame, text="Invoice/Document Number:", font=('Segoe UI', 10, 'bold')).pack(anchor='w', pady=(0, 5))
        inv_entry = tk.Entry(form_frame, width=50, font=('Segoe UI', 10))
        inv_entry.insert(0, data.get('invoice_number', ''))
        inv_entry.pack(fill='x', pady=(0, 10))
        
        # Client name
        tk.Label(form_frame, text="Client Name:", font=('Segoe UI', 10, 'bold')).pack(anchor='w', pady=(0, 5))
        client_entry = tk.Entry(form_frame, width=50, font=('Segoe UI', 10))
        client_entry.insert(0, data.get('client_name', ''))
        client_entry.pack(fill='x', pady=(0, 10))
        
        # Date
        tk.Label(form_frame, text="Date:", font=('Segoe UI', 10, 'bold')).pack(anchor='w', pady=(0, 5))
        date_entry = tk.Entry(form_frame, width=50, font=('Segoe UI', 10))
        date_entry.insert(0, data.get('invoice_date', datetime.now().strftime('%Y-%m-%d')))
        date_entry.pack(fill='x', pady=(0, 10))
        
        # Amount
        tk.Label(form_frame, text="Total Amount (₹):", font=('Segoe UI', 10, 'bold')).pack(anchor='w', pady=(0, 5))
        amount_entry = tk.Entry(form_frame, width=50, font=('Segoe UI', 10))
        amount_entry.insert(0, str(data.get('total_amount', 0)))
        amount_entry.pack(fill='x', pady=(0, 10))
        
        # Items (if extracted)
        if data.get('items'):
            tk.Label(form_frame, text="Extracted Items:", font=('Segoe UI', 10, 'bold')).pack(anchor='w', pady=(10, 5))
            items_text = tk.Text(form_frame, height=8, width=50, font=('Courier', 9))
            items_text.pack(fill='both', expand=True, pady=(0, 10))
            
            for item in data.get('items', [])[:10]:  # Show first 10 items
                items_text.insert('end', f"• {item.get('description', 'Item')}: ₹{item.get('amount', 0)}\n")
        
        # Buttons
        btn_frame = tk.Frame(dialog)
        btn_frame.pack(pady=20)
        
        def create_invoice():
            """Create invoice from extracted data"""
            try:
                # Prepare items
                items = data.get('items', [])
                if not items:
                    # Create single item from total
                    items = [{
                        'description': 'Service/Product',
                        'quantity': 1,
                        'rate': float(amount_entry.get() or 0)
                    }]
                
                # Create invoice
                success, result = self.engine.create_invoice(
                    invoice_number=inv_entry.get() or f"EXT-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    client_name=client_entry.get() or 'Extracted Client',
                    invoice_date=date_entry.get(),
                    items=items,
                    tax_rate=18.0
                )
                
                if success:
                    messagebox.showinfo("Success", "Invoice created successfully from extracted data!")
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", result)
                    
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create invoice:\n{str(e)}")
        
        def create_document():
            """Create document from extracted data"""
            try:
                title = f"{inv_entry.get()} - {client_entry.get()}"
                
                success, doc_id = self.engine.create_document(
                    title=title,
                    file_path=file_path
                )
                
                if success:
                    messagebox.showinfo("Success", "Document created successfully!")
                    dialog.destroy()
                    self.refresh()
                else:
                    messagebox.showerror("Error", "Failed to create document")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create document:\n{str(e)}")
        
        tk.Button(
            btn_frame,
            text="📝 Create Invoice",
            font=('Segoe UI', 11),
            bg='#2196f3',
            fg='white',
            relief='flat',
            cursor='hand2',
            padx=20,
            pady=8,
            command=create_invoice
        ).pack(side='left', padx=5)
        
        tk.Button(
            btn_frame,
            text="📄 Save as Document",
            font=('Segoe UI', 11),
            bg='#4caf50',
            fg='white',
            relief='flat',
            cursor='hand2',
            padx=20,
            pady=8,
            command=create_document
        ).pack(side='left', padx=5)
        
        tk.Button(
            btn_frame,
            text="Cancel",
            font=('Segoe UI', 11),
            padx=20,
            pady=8,
            command=dialog.destroy
        ).pack(side='left', padx=5)
