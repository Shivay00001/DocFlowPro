"""
Invoices Panel for DocFlow Pro
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
import json


class InvoicesPanel(ttk.Frame):
    """Invoices management panel"""
    
    def __init__(self, parent, engine, user_id):
        super().__init__(parent)
        self.frame = self  # For panel switching compatibility
        self.engine = engine
        self.user_id = user_id
        
        self._create_widgets()
        self._load_invoices()
    
    def _create_widgets(self):
        """Create panel widgets"""
        # Title and toolbar
        toolbar = ttk.Frame(self)
        toolbar.pack(fill='x', padx=20, pady=(20, 10))
        
        ttk.Button(
            toolbar,
            text="➕ Create Invoice",
            command=self._create_invoice
        ).pack(side='left', padx=(0, 5))
        
        ttk.Button(
            toolbar,
            text="✏️ Edit",
            command=self._edit_invoice
        ).pack(side='left', padx=5)
        
        ttk.Button(
            toolbar,
            text="🗑️ Delete",
            command=self._delete_invoice
        ).pack(side='left', padx=5)
        
        ttk.Button(
            toolbar,
            text="📤 Share Invoice",
            command=self._share_invoice
        ).pack(side='left', padx=5)
        
        ttk.Button(
            toolbar,
            text="🔄 Refresh",
            command=self.refresh
        ).pack(side='right', padx=5)
        
        # Invoices list
        list_frame = ttk.Frame(self)
        list_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side='right', fill='y')
        
        # Treeview
        columns = ('Invoice #', 'Client', 'Date', 'Amount', 'Status')
        self.tree = ttk.Treeview(
            list_frame,
            columns=columns,
            show='tree headings',
            yscrollcommand=scrollbar.set
        )
        
        scrollbar.config(command=self.tree.yview)
        
        # Column headers
        self.tree.heading('#0', text='ID')
        self.tree.heading('Invoice #', text='Invoice #')
        self.tree.heading('Client', text='Client')
        self.tree.heading('Date', text='Date')
        self.tree.heading('Amount', text='Amount')
        self.tree.heading('Status', text='Status')
        
        # Column widths
        self.tree.column('#0', width=50)
        self.tree.column('Invoice #', width=150)
        self.tree.column('Client', width=250)
        self.tree.column('Date', width=120)
        self.tree.column('Amount', width=120)
        self.tree.column('Status', width=100)
        
        self.tree.pack(fill='both', expand=True)
        
        # Bind double-click
        self.tree.bind('<Double-1>', self._view_invoice)
    
    def _load_invoices(self):
        """Load user's invoices"""
        # Clear existing
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            invoices = self.engine.get_my_invoices()
            
            for inv in invoices:
                self.tree.insert(
                    '',
                    'end',
                    text=str(inv.get('id', '')),
                    values=(
                        inv.get('invoice_number', ''),
                        inv.get('client_name', ''),
                        inv.get('invoice_date', ''),
                        f"₹{inv.get('total_amount', 0):.2f}",
                        inv.get('status', 'pending').upper()
                    ),
                    tags=(inv.get('id'),)
                )
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load invoices: {str(e)}")
    
    def _create_invoice(self):
        """Create a new invoice"""
        dialog = tk.Toplevel(self)
        dialog.title("Create Invoice")
        dialog.geometry("500x600")
        dialog.transient(self)
        dialog.grab_set()
        
        # Invoice number
        ttk.Label(dialog, text="Invoice Number:").pack(pady=(20, 5), padx=20, anchor='w')
        inv_number_entry = ttk.Entry(dialog, width=50)
        inv_number_entry.pack(padx=20)
        inv_number_entry.insert(0, f"INV-{datetime.now().strftime('%Y%m%d-%H%M%S')}")
        
        # Client name
        ttk.Label(dialog, text="Client Name:").pack(pady=(10, 5), padx=20, anchor='w')
        client_entry = ttk.Entry(dialog, width=50)
        client_entry.pack(padx=20)
        
        # Client email
        ttk.Label(dialog, text="Client Email (optional):").pack(pady=(10, 5), padx=20, anchor='w')
        email_entry = ttk.Entry(dialog, width=50)
        email_entry.pack(padx=20)
        
        # Invoice date
        ttk.Label(dialog, text="Invoice Date:").pack(pady=(10, 5), padx=20, anchor='w')
        date_entry = ttk.Entry(dialog, width=50)
        date_entry.pack(padx=20)
        date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        
        # Tax rate
        ttk.Label(dialog, text="Tax Rate (%):").pack(pady=(10, 5), padx=20, anchor='w')
        tax_entry = ttk.Entry(dialog, width=50)
        tax_entry.pack(padx=20)
        tax_entry.insert(0, "18")
        
        # Items (simplified)
        ttk.Label(dialog, text="Item Description:").pack(pady=(10, 5), padx=20, anchor='w')
        item_desc_entry = ttk.Entry(dialog, width=50)
        item_desc_entry.pack(padx=20)
        
        ttk.Label(dialog, text="Quantity:").pack(pady=(10, 5), padx=20, anchor='w')
        qty_entry = ttk.Entry(dialog, width=50)
        qty_entry.pack(padx=20)
        qty_entry.insert(0, "1")
        
        ttk.Label(dialog, text="Rate (₹):").pack(pady=(10, 5), padx=20, anchor='w')
        rate_entry = ttk.Entry(dialog, width=50)
        rate_entry.pack(padx=20)
        rate_entry.insert(0, "1000")
        
        def save():
            try:
                # Validate
                inv_number = inv_number_entry.get().strip()
                client_name = client_entry.get().strip()
                
                if not inv_number or not client_name:
                    messagebox.showerror("Error", "Invoice number and client name are required")
                    return
                
                # Create items list
                items = [{
                    'description': item_desc_entry.get() or 'Service/Product',
                    'quantity': float(qty_entry.get() or 1),
                    'rate': float(rate_entry.get() or 0)
                }]
                
                # Create invoice
                success, result = self.engine.create_invoice(
                    invoice_number=inv_number,
                    client_name=client_name,
                    invoice_date=date_entry.get(),
                    items=items,
                    client_email=email_entry.get(),
                    tax_rate=float(tax_entry.get() or 0)
                )
                
                if success:
                    messagebox.showinfo("Success", "Invoice created successfully!")
                    dialog.destroy()
                    self._load_invoices()
                else:
                    messagebox.showerror("Error", result)
                    
            except ValueError as e:
                messagebox.showerror("Error", "Please enter valid numbers for quantity, rate, and tax")
        
        ttk.Button(dialog, text="Create Invoice", command=save).pack(pady=20)
    
    def _view_invoice(self, event):
        """View invoice details"""
        selection = self.tree.selection()
        if not selection:
            return
        
        item = self.tree.item(selection[0])
        inv_id = int(item['text'])
        
        
        # Get full invoice data
        invoices = self.engine.get_my_invoices()
        invoice = next((inv for inv in invoices if inv['id'] == inv_id), None)
        
        if not invoice:
            messagebox.showerror("Error", "Invoice not found")
            return
        
        # Build detailed message
        details = [
            f"Invoice Number: {invoice.get('invoice_number', 'N/A')}",
            f"Client: {invoice.get('client_name', 'N/A')}",
            f"Date: {invoice.get('invoice_date', 'N/A')}",
            f"Amount: ₹{invoice.get('total_amount', 0):,.2f}",
            f"Status: {invoice.get('status', 'Generated').upper()}",
        ]
        
        if invoice.get('client_gst'):
            details.append(f"Client GST: {invoice['client_gst']}")
        
        # Add line items if available
        line_items = invoice.get('line_items', [])  
        if line_items:
            details.append("\n━━━ LINE ITEMS ━━━")
            for idx, item in enumerate(line_items, 1):
                desc = item.get('description', 'Item')
                qty = item.get('quantity', 1)
                rate = item.get('rate', 0)
                amt = item.get('amount', 0)
                details.append(f"{idx}. {desc}")
                details.append(f"   Qty: {qty} × ₹{rate:,.2f} = ₹{amt:,.2f}")
        
        details.append("\n💡 Use 'Share Invoice' to export as PDF")
        
        messagebox.showinfo(
            f"Invoice #{invoice.get('invoice_number', inv_id)}",
            "\n".join(details)
        )

    
    def _edit_invoice(self):
        """Edit selected invoice"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select an invoice to edit")
            return
        
        item = self.tree.item(selection[0])
        inv_id = int(item['text'])
        
        # Create edit dialog
        dialog = tk.Toplevel(self)
        dialog.title("Edit Invoice")
        dialog.geometry("400x300")
        dialog.transient(self)
        dialog.grab_set()
        
        # Get current invoice data
        values = item['values']
        current_client = values[1]
        current_status = values[4].lower()
        
        ttk.Label(dialog, text="Client Name:").pack(pady=(20, 5), padx=20, anchor='w')
        client_entry = ttk.Entry(dialog, width=50)
        client_entry.pack(padx=20)
        client_entry.insert(0, current_client)
        
        ttk.Label(dialog, text="Status:").pack(pady=(10, 5), padx=20, anchor='w')
        status_var = tk.StringVar(value=current_status)
        status_frame = ttk.Frame(dialog)
        status_frame.pack(padx=20, anchor='w')
        
        ttk.Radiobutton(status_frame, text="Pending", variable=status_var, value="pending").pack(side='left', padx=5)
        ttk.Radiobutton(status_frame, text="Paid", variable=status_var, value="paid").pack(side='left', padx=5)
        ttk.Radiobutton(status_frame, text="Cancelled", variable=status_var, value="cancelled").pack(side='left', padx=5)
        
        ttk.Label(dialog, text="Notes:").pack(pady=(10, 5), padx=20, anchor='w')
        notes_entry = tk.Text(dialog, width=50, height=5)
        notes_entry.pack(padx=20)
        
        def save_changes():
            client = client_entry.get().strip()
            if not client:
                messagebox.showerror("Error", "Client name is required")
                return
            
            success = self.engine.update_invoice(
                inv_id,
                client_name=client,
                status=status_var.get(),
                notes=notes_entry.get('1.0', 'end').strip()
            )
            
            if success:
                messagebox.showinfo("Success", "Invoice updated successfully!")
                dialog.destroy()
                self._load_invoices()
            else:
                messagebox.showerror("Error", "Failed to update invoice")
        
        ttk.Button(dialog, text="Save Changes", command=save_changes).pack(pady=20)
    
    def _delete_invoice(self):
        """Delete selected invoice"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select an invoice to delete")
            return
        
        item = self.tree.item(selection[0])
        inv_id = int(item['text'])
        inv_number = item['values'][0]
        
        # Confirm deletion
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete this invoice?\n\nInvoice #: {inv_number}\n\nThis action cannot be undone!"
        )
        
        if not confirm:
            return
        
        success = self.engine.delete_invoice(inv_id)
        
        if success:
            messagebox.showinfo("Success", "Invoice deleted successfully!")
            self._load_invoices()
        else:
            messagebox.showerror("Error", "Failed to delete invoice")
    
    def _share_invoice(self):
        """Share selected invoice"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select an invoice to share")
            return
        
        # Get invoice data - ID is in the text column
        item = self.tree.item(selection[0])
        invoice_id = int(item['text'])  # Fixed: use text, not values[0]
        
        invoice = self.engine.get_invoice_by_id(invoice_id)
        if not invoice:
            messagebox.showerror("Error", "Invoice not found")
            return
        
        # Share options dialog
        dialog = tk.Toplevel(self)
        dialog.title("Share Invoice")
        dialog.geometry("400x250")
        dialog.transient(self)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - 200
        y = (dialog.winfo_screenheight() // 2) - 125
        dialog.geometry(f"400x250+{x}+{y}")
        
        tk.Label(
            dialog,
            text=f"📄 Share Invoice #{invoice.get('invoice_number')}",
            font=('Segoe UI', 14, 'bold')
        ).pack(pady=20)
        
        tk.Label(
            dialog,
            text=f"Client: {invoice.get('client_name')}\nAmount: ₹{invoice.get('total_amount', 0):,.2f}",
            font=('Segoe UI', 10)
        ).pack(pady=10)
        
        btn_frame = tk.Frame(dialog)
        btn_frame.pack(pady=20)
        
        def save_pdf():
            """Save invoice as PDF"""
            try:
                from tkinter import filedialog
                from utils.pdf_generator import PDFGenerator
                
                filename = filedialog.asksaveasfilename(
                    defaultextension=".pdf",
                    initialfile=f"Invoice_{invoice.get('invoice_number')}.pdf",
                    filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
                )
                
                if filename:
                    generator = PDFGenerator()
                    generator.generate_invoice(invoice, filename)
                    messagebox.showinfo("Success", f"Invoice saved:\n{filename}")
                    dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save PDF:\n{str(e)}")
        
        def send_email():
            """Open email client with invoice"""
            try:
                import webbrowser
                client_email = invoice.get('client_email', '')
                subject = f"Invoice #{invoice.get('invoice_number')}"
                body = f"Dear {invoice.get('client_name')},\n\nPlease find attached invoice #{invoice.get('invoice_number')} for ₹{invoice.get('total_amount', 0):,.2f}.\n\nThank you!"
                
                mailto = f"mailto:{client_email}?subject={subject}&body={body}"
                webbrowser.open(mailto)
                
                messagebox.showinfo("Info", "Email client opened. Please attach the PDF manually.")
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open email:\n{str(e)}")
        
        def send_whatsapp():
            """Send via WhatsApp"""
            try:
                import webbrowser
                phone = invoice.get('client_phone', '')
                message = f"Invoice #{invoice.get('invoice_number')} for ₹{invoice.get('total_amount', 0):,.2f}. Thank you!"
                
                # WhatsApp Web URL
                url = f"https://wa.me/{phone}?text={message}"
                webbrowser.open(url)
                
                messagebox.showinfo("Info", "WhatsApp opened. Please send the message.")
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open WhatsApp:\n{str(e)}")
        
        tk.Button(
            btn_frame,
            text="💾 Save as PDF",
            command=save_pdf,
            font=('Segoe UI', 10),
            bg='#2196f3',
            fg='white',
            padx=15,
            pady=8,
            cursor='hand2',
            relief='flat'
        ).pack(side='left', padx=5)
        
        tk.Button(
            btn_frame,
            text="📧 Email",
            command=send_email,
            font=('Segoe UI', 10),
            bg='#4caf50',
            fg='white',
            padx=15,
            pady=8,
            cursor='hand2',
            relief='flat'
        ).pack(side='left', padx=5)
        
        tk.Button(
            btn_frame,
            text="💬 WhatsApp",
            command=send_whatsapp,
            font=('Segoe UI', 10),
            bg='#25d366',
            fg='white',
            padx=15,
            pady=8,
            cursor='hand2',
            relief='flat'
        ).pack(side='left', padx=5)
        
        tk.Button(
            dialog,
            text="Cancel",
            command=dialog.destroy,
            font=('Segoe UI', 10),
            padx=20,
            pady=5
        ).pack(pady=(10, 0))
    
    def refresh(self):
        """Refresh invoices list"""
        self._load_invoices()
