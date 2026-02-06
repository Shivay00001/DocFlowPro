"""
Documents Panel - File Management & Upload
Completely separate from Invoices
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
from datetime import datetime


class DocumentsPanel(ttk.Frame):
    """Document management - upload, store, and extract data from files"""
    
    def __init__(self, parent, engine, user_id):
        super().__init__(parent)
        self.engine = engine
        self.user_id = user_id
        
        self._create_widgets()
        self._load_documents()
    
    def _create_widgets(self):
        """Create document management interface"""
        # Toolbar
        toolbar = ttk.Frame(self)
        toolbar.pack(fill='x', padx=20, pady=(20, 10))
        
        ttk.Button(
            toolbar,
            text="üìÅ Upload Document",
            command=self._upload_document
        ).pack(side='left', padx=(0, 5))
        
        ttk.Button(
            toolbar,
            text="üîç Extract Data & Upload",
            command=self._extract_and_upload
        ).pack(side='left', padx=5)
        
        ttk.Button(
            toolbar,
            text="üìä Client Summary",
            command=self._show_client_summary
        ).pack(side='left', padx=5)
        
        ttk.Button(
            toolbar,
            text="üíº Create ITR Invoice",
            command=self._create_itr_invoice
        ).pack(side='left', padx=5)
        
        ttk.Button(
            toolbar,
            text="‚úèÔ∏è Edit",
            command=self._edit_document
        ).pack(side='left', padx=5)
        
        ttk.Button(
            toolbar,
            text="üóëÔ∏è Delete",
            command=self._delete_document
        ).pack(side='left', padx=5)
        
        ttk.Button(
            toolbar,
            text="üîÑ Refresh",
            command=self.refresh
        ).pack(side='right')

        
        # Documents list
        list_frame = ttk.Frame(self)
        list_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side='right', fill='y')
        
        columns = ('Title', 'Category', 'File Type', 'Created Date')
        self.tree = ttk.Treeview(
            list_frame,
            columns=columns,
            show='tree headings',
            yscrollcommand=scrollbar.set
        )
        
        scrollbar.config(command=self.tree.yview)
        
        self.tree.heading('#0', text='ID')
        self.tree.heading('Title', text='Title')
        self.tree.heading('Category', text='Category')
        self.tree.heading('File Type', text='Type')
        self.tree.heading('Created Date', text='Created')
        
        self.tree.column('#0', width=50)
        self.tree.column('Title', width=350)
        self.tree.column('Category', width=120)
        self.tree.column('File Type', width=80)
        self.tree.column('Created Date', width=120)
        
        self.tree.pack(fill='both', expand=True)
    
    def _load_documents(self):
        """Load all documents"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            documents = self.engine.get_my_documents()
            
            for doc in documents:
                file_type = doc.get('file_type', 'N/A')
                self.tree.insert(
                    '',
                    'end',
                    text=str(doc.get('id', '')),
                    values=(
                        doc.get('title', 'Untitled'),
                        doc.get('category', 'General'),
                        file_type,
                        doc.get('created_at', '')[:10]
                    )
                )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load documents: {str(e)}")
    
    def _upload_document(self):
        """Simple document upload without extraction"""
        file_path = filedialog.askopenfilename(
            title="Select Document",
            filetypes=[
                ("All files", "*.*"),
                ("PDF files", "*.pdf"),
                ("Images", "*.png;*.jpg;*.jpeg"),
                ("Excel", "*.xlsx;*.xls"),
                ("Word", "*.doc;*.docx"),
            ]
        )
        
        if not file_path:
            return
        
        # Simple metadata dialog
        dialog = tk.Toplevel(self)
        dialog.title("Document Details")
        dialog.geometry("450x300")
        dialog.transient(self)
        dialog.grab_set()
        
        tk.Label(
            dialog,
            text="Document Details",
            font=('Segoe UI', 14, 'bold')
        ).pack(pady=15)
        
        form = tk.Frame(dialog)
        form.pack(fill='both', expand=True, padx=30)
        
        # Title
        tk.Label(form, text="Title:", font=('Segoe UI', 10)).pack(anchor='w', pady=(10, 5))
        title_entry = tk.Entry(form, width=50, font=('Segoe UI', 10))
        title_entry.insert(0, os.path.basename(file_path))
        title_entry.pack(fill='x')
        
        # Category
        tk.Label(form, text="Category:", font=('Segoe UI', 10)).pack(anchor='w', pady=(10, 5))
        category_var = tk.StringVar(value="Tax Invoice (Input)")
        category_combo = ttk.Combobox(
            form,
            textvariable=category_var,
            values=[
                "Tax Invoice (Input)",
                "Purchase Bills",
                "GST Returns",
                "Bank Statements",
                "Salary Slips",
                "Rent Receipts",
                "Investment Proofs",
                "TDS Certificates",
                "Other Tax Documents"
            ],
            width=48,
            state='readonly'
        )
        category_combo.pack(fill='x')
        
        # Tags
        tk.Label(form, text="Tags (comma-separated):", font=('Segoe UI', 10)).pack(anchor='w', pady=(10, 5))
        tags_entry = tk.Entry(form, width=50, font=('Segoe UI', 10))
        tags_entry.pack(fill='x')
        
        def save():
            title = title_entry.get().strip()
            if not title:
                messagebox.showerror("Error", "Title is required")
                return
            
            success, result = self.engine.create_document(
                title=title,
                file_path=file_path,
                category=category_var.get(),
                tags=tags_entry.get()
            )
            
            if success:
                messagebox.showinfo("Success", "Document uploaded successfully!")
                dialog.destroy()
                self.refresh()
            else:
                messagebox.showerror("Error", result)
        
        tk.Button(
            dialog,
            text="Save Document",
            font=('Segoe UI', 11),
            bg='#4CAF50',
            fg='white',
            relief='flat',
            cursor='hand2',
            padx=30,
            pady=10,
            command=save
        ).pack(pady=20)
    
    def _extract_and_upload(self):
        """Upload with data extraction (enhanced dialog)"""
        file_path = filedialog.askopenfilename(
            title="Select File to Extract & Upload",
            filetypes=[
                ("All Supported", "*.pdf;*.xlsx;*.xls;*.csv;*.txt;*.jpg;*.png"),
                ("PDF files", "*.pdf"),
                ("Excel files", "*.xlsx;*.xls"),
                ("Images", "*.jpg;*.jpeg;*.png"),
                ("All files", "*.*")
            ]
        )
        
        if not file_path:
            return
        
        # Show enhanced upload dialog with extraction
        self._show_enhanced_upload_dialog(file_path)
    
    def _show_enhanced_upload_dialog(self, file_path):
        """Enhanced upload with auto-extraction of invoice data"""
        dialog = tk.Toplevel(self)
        dialog.title("Review Extracted Data")
        dialog.geometry("700x750")
        dialog.transient(self)
        dialog.grab_set()
        
        # Header
        tk.Label(
            dialog,
            text="Review and Edit Extracted Data",
            font=('Segoe UI', 16, 'bold')
        ).pack(pady=15)
        
        # Auto-extract
        extracted_data = {}
        try:
            from utils.data_extractor import UniversalDataExtractor
            extractor = UniversalDataExtractor()
            extracted_data = extractor.extract_from_file(file_path)
        except:
            pass
        
        # Scrollable form
        canvas = tk.Canvas(dialog)
        scrollbar = tk.Scrollbar(dialog, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Form fields
        form = tk.Frame(scrollable_frame)
        form.pack(fill='both', expand=True, padx=30, pady=20)
        
        entries = {}
        
        fields = [
            ("Invoice Number", "invoice_number", extracted_data.get('invoice_number', '')),
            ("Invoice Date", "invoice_date", extracted_data.get('invoice_date', datetime.now().strftime('%Y-%m-%d'))),
            ("Vendor Name", "vendor_name", extracted_data.get('client_name', '')),
            ("Vendor GST", "vendor_gst", ''),
            ("Vendor PAN", "vendor_pan", ''),
            ("Customer GST", "customer_gst", ''),
            ("Taxable Amount", "taxable_amount", str(extracted_data.get('subtotal', 0))),
            ("Total Amount", "total_amount", str(extracted_data.get('total_amount', 0))),
        ]
        
        for label_text, field_key, default_value in fields:
            tk.Label(
                form,
                text=label_text,
                font=('Segoe UI', 10)
            ).pack(anchor='w', pady=(10, 5))
            
            entry = tk.Entry(form, font=('Segoe UI', 11), width=60)
            entry.pack(fill='x', pady=(0, 5))
            entry.insert(0, default_value)
            
            entries[field_key] = entry
        
        canvas.pack(side="left", fill="both", expand=True, padx=(20, 0), pady=(0, 20))
        scrollbar.pack(side="right", fill="y", pady=(0, 20))
        
        # Save button
        def save_enhanced():
            try:
                data = {k: v.get().strip() for k, v in entries.items()}
                title = f"{data['invoice_number']} - {data['vendor_name']}"
                
                # Create document
                success, _ = self.engine.create_document(
                    title=title,
                    file_path=file_path,
                    category='Invoice',
                    tags=f"{data['invoice_date']}, GST: {data['vendor_gst']}"
                )
                
                # Also create invoice if data is complete
                if success and data.get('invoice_number') and data.get('total_amount'):
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
                            tax_rate=18.0
                        )
                    except:
                        pass
                
                messagebox.showinfo("Success", "Document and invoice data saved!")
                dialog.destroy()
                self.refresh()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        tk.Button(
            dialog,
            text="Save",
            font=('Segoe UI', 12),
            bg='#4CAF50',
            fg='white',
            relief='flat',
            cursor='hand2',
            padx=40,
            pady=10,
            command=save_enhanced
        ).pack(pady=20)
    
    def _edit_document(self):
        """Edit selected document"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a document")
            return
        
        item = self.tree.item(selection[0])
        doc_id = int(item['text'])
        
        dialog = tk.Toplevel(self)
        dialog.title("Edit Document")
        dialog.geometry("400x250")
        dialog.transient(self)
        dialog.grab_set()
        
        values = item['values']
        
        tk.Label(dialog, text="Title:").pack(pady=(20, 5), padx=20, anchor='w')
        title_entry = tk.Entry(dialog, width=50)
        title_entry.pack(padx=20)
        title_entry.insert(0, values[0])
        
        tk.Label(dialog, text="Category:").pack(pady=(10, 5), padx=20, anchor='w')
        category_entry = tk.Entry(dialog, width=50)
        category_entry.pack(padx=20)
        category_entry.insert(0, values[1])
        
        def save():
            if self.engine.update_document(
                doc_id,
                title=title_entry.get(),
                category=category_entry.get()
            ):
                messagebox.showinfo("Success", "Document updated!")
                dialog.destroy()
                self.refresh()
            else:
                messagebox.showerror("Error", "Failed to update")
        
        tk.Button(dialog, text="Save Changes", command=save).pack(pady=20)
    
    def _delete_document(self):
        """Delete selected document"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a document")
            return
        
        item = self.tree.item(selection[0])
        doc_id = int(item['text'])
        
        if messagebox.askyesno("Confirm", f"Delete '{item['values'][0]}'?"):
            if self.engine.delete_document(doc_id):
                messagebox.showinfo("Success", "Document deleted!")
                self.refresh()
            else:
                messagebox.showerror("Error", "Failed to delete")
    
    def refresh(self):
        """Refresh documents list"""
        self._load_documents()
        d e f   _ s h o w _ c l i e n t _ s u m m a r y ( s e l f ) :  
                 " " " S h o w   c l i e n t - w i s e   d o c u m e n t   s u m m a r y   f o r   I T R   f i l i n g " " "  
                 t r y :  
                         d o c u m e n t s   =   s e l f . e n g i n e . g e t _ m y _ d o c u m e n t s ( )  
                          
                         i f   n o t   d o c u m e n t s :  
                                 m e s s a g e b o x . s h o w i n f o ( " N o   D a t a " ,   " N o   d o c u m e n t s   u p l o a d e d   y e t " )  
                                 r e t u r n  
                          
                         #   G r o u p   b y   c l i e n t  
                         f r o m   c o l l e c t i o n s   i m p o r t   d e f a u l t d i c t  
                         c l i e n t _ d a t a   =   d e f a u l t d i c t ( l a m b d a :   { ' c o u n t ' :   0 ,   ' d o c s ' :   [ ] ,   ' t o t a l _ a m o u n t ' :   0 } )  
                          
                         f o r   d o c   i n   d o c u m e n t s :  
                                 #   E x t r a c t   c l i e n t   n a m e   f r o m   t i t l e   o r   t a g s  
                                 t i t l e   =   d o c . g e t ( ' t i t l e ' ,   ' ' )  
                                 t a g s   =   d o c . g e t ( ' t a g s ' ,   ' ' )  
                                  
                                 #   S i m p l e   c l i e n t   e x t r a c t i o n   ( c a n   b e   i m p r o v e d )  
                                 c l i e n t   =   ' U n k n o w n   C l i e n t '  
                                 i f   ' - '   i n   t i t l e :  
                                         p a r t s   =   t i t l e . s p l i t ( ' - ' )  
                                         i f   l e n ( p a r t s )   >   1 :  
                                                 c l i e n t   =   p a r t s [ 1 ] . s t r i p ( )  
                                  
                                 c l i e n t _ d a t a [ c l i e n t ] [ ' c o u n t ' ]   + =   1  
                                 c l i e n t _ d a t a [ c l i e n t ] [ ' d o c s ' ] . a p p e n d ( d o c )  
                          
                         #   S h o w   s u m m a r y   d i a l o g  
                         d i a l o g   =   t k . T o p l e v e l ( s e l f )  
                         d i a l o g . t i t l e ( " C l i e n t - w i s e   T a x   D o c u m e n t   S u m m a r y " )  
                         d i a l o g . g e o m e t r y ( " 8 0 0 x 6 0 0 " )  
                         d i a l o g . t r a n s i e n t ( s e l f )  
                         d i a l o g . g r a b _ s e t ( )  
                          
                         t k . L a b e l (  
                                 d i a l o g ,  
                                 t e x t = "  x `  C l i e n t   S u m m a r y   -   I T R   F i l i n g " ,  
                                 f o n t = ( ' S e g o e   U I ' ,   1 6 ,   ' b o l d ' )  
                         ) . p a c k ( p a d y = 1 5 )  
                          
                         #   S u m m a r y   t a b l e  
                         t r e e _ f r a m e   =   t t k . F r a m e ( d i a l o g )  
                         t r e e _ f r a m e . p a c k ( f i l l = ' b o t h ' ,   e x p a n d = T r u e ,   p a d x = 2 0 ,   p a d y = 1 0 )  
                          
                         s c r o l l b a r   =   t t k . S c r o l l b a r ( t r e e _ f r a m e )  
                         s c r o l l b a r . p a c k ( s i d e = ' r i g h t ' ,   f i l l = ' y ' )  
                          
                         t r e e   =   t t k . T r e e v i e w (  
                                 t r e e _ f r a m e ,  
                                 c o l u m n s = ( ' C l i e n t ' ,   ' D o c u m e n t s ' ,   ' C a t e g o r i e s ' ,   ' A c t i o n ' ) ,  
                                 s h o w = ' h e a d i n g s ' ,  
                                 y s c r o l l c o m m a n d = s c r o l l b a r . s e t  
                         )  
                         s c r o l l b a r . c o n f i g ( c o m m a n d = t r e e . y v i e w )  
                          
                         t r e e . h e a d i n g ( ' C l i e n t ' ,   t e x t = ' C l i e n t   N a m e ' )  
                         t r e e . h e a d i n g ( ' D o c u m e n t s ' ,   t e x t = ' T o t a l   D o c s ' )  
                         t r e e . h e a d i n g ( ' C a t e g o r i e s ' ,   t e x t = ' C a t e g o r i e s ' )  
                         t r e e . h e a d i n g ( ' A c t i o n ' ,   t e x t = ' A c t i o n ' )  
                          
                         t r e e . c o l u m n ( ' C l i e n t ' ,   w i d t h = 2 5 0 )  
                         t r e e . c o l u m n ( ' D o c u m e n t s ' ,   w i d t h = 1 0 0 )  
                         t r e e . c o l u m n ( ' C a t e g o r i e s ' ,   w i d t h = 2 5 0 )  
                         t r e e . c o l u m n ( ' A c t i o n ' ,   w i d t h = 1 5 0 )  
                          
                         f o r   c l i e n t ,   d a t a   i n   c l i e n t _ d a t a . i t e m s ( ) :  
                                 c a t e g o r i e s   =   s e t ( d o c . g e t ( ' c a t e g o r y ' ,   ' N / A ' )   f o r   d o c   i n   d a t a [ ' d o c s ' ] )  
                                 t r e e . i n s e r t ( ' ' ,   ' e n d ' ,   v a l u e s = (  
                                         c l i e n t ,  
                                         d a t a [ ' c o u n t ' ] ,  
                                         ' ,   ' . j o i n ( l i s t ( c a t e g o r i e s ) [ : 3 ] ) ,  
                                         ' C r e a t e   I n v o i c e   ‚    '  
                                 ) )  
                          
                         t r e e . p a c k ( f i l l = ' b o t h ' ,   e x p a n d = T r u e )  
                          
                         d e f   o n _ d o u b l e _ c l i c k ( e v e n t ) :  
                                 s e l e c t i o n   =   t r e e . s e l e c t i o n ( )  
                                 i f   s e l e c t i o n :  
                                         i t e m   =   t r e e . i t e m ( s e l e c t i o n [ 0 ] )  
                                         c l i e n t _ n a m e   =   i t e m [ ' v a l u e s ' ] [ 0 ]  
                                         s e l f . _ c r e a t e _ i t r _ i n v o i c e _ f o r _ c l i e n t ( c l i e n t _ n a m e )  
                                         d i a l o g . d e s t r o y ( )  
                          
                         t r e e . b i n d ( ' < D o u b l e - 1 > ' ,   o n _ d o u b l e _ c l i c k )  
                          
                         t k . B u t t o n (  
                                 d i a l o g ,  
                                 t e x t = " C l o s e " ,  
                                 c o m m a n d = d i a l o g . d e s t r o y ,  
                                 p a d x = 2 0 ,  
                                 p a d y = 8  
                         ) . p a c k ( p a d y = 1 5 )  
                          
                 e x c e p t   E x c e p t i o n   a s   e :  
                         m e s s a g e b o x . s h o w e r r o r ( " E r r o r " ,   f " F a i l e d   t o   s h o w   s u m m a r y : \ n { s t r ( e ) } " )  
          
         d e f   _ c r e a t e _ i t r _ i n v o i c e ( s e l f ) :  
                 " " " C r e a t e   I T R   f i l i n g   i n v o i c e   f r o m   d o c u m e n t s " " "  
                 t r y :  
                         d o c u m e n t s   =   s e l f . e n g i n e . g e t _ m y _ d o c u m e n t s ( )  
                          
                         i f   n o t   d o c u m e n t s :  
                                 m e s s a g e b o x . s h o w i n f o ( " N o   D o c u m e n t s " ,   " U p l o a d   c l i e n t   d o c u m e n t s   f i r s t " )  
                                 r e t u r n  
                          
                         #   C o l l e c t   u n i q u e   c l i e n t s  
                         c l i e n t s   =   s e t ( )  
                         f o r   d o c   i n   d o c u m e n t s :  
                                 t i t l e   =   d o c . g e t ( ' t i t l e ' ,   ' ' )  
                                 i f   ' - '   i n   t i t l e :  
                                         p a r t s   =   t i t l e . s p l i t ( ' - ' )  
                                         i f   l e n ( p a r t s )   >   1 :  
                                                 c l i e n t s . a d d ( p a r t s [ 1 ] . s t r i p ( ) )  
                          
                         i f   n o t   c l i e n t s :  
                                 m e s s a g e b o x . s h o w i n f o ( " N o   C l i e n t s " ,   " N o   c l i e n t   n a m e s   f o u n d   i n   d o c u m e n t s " )  
                                 r e t u r n  
                          
                         #   S e l e c t   c l i e n t   d i a l o g  
                         d i a l o g   =   t k . T o p l e v e l ( s e l f )  
                         d i a l o g . t i t l e ( " C r e a t e   I T R   F i l i n g   I n v o i c e " )  
                         d i a l o g . g e o m e t r y ( " 5 0 0 x 4 0 0 " )  
                         d i a l o g . t r a n s i e n t ( s e l f )  
                         d i a l o g . g r a b _ s e t ( )  
                          
                         t k . L a b e l (  
                                 d i a l o g ,  
                                 t e x t = "  x º   C r e a t e   I T R   F i l i n g   I n v o i c e " ,  
                                 f o n t = ( ' S e g o e   U I ' ,   1 4 ,   ' b o l d ' )  
                         ) . p a c k ( p a d y = 1 5 )  
                          
                         f o r m   =   t k . F r a m e ( d i a l o g )  
                         f o r m . p a c k ( f i l l = ' b o t h ' ,   e x p a n d = T r u e ,   p a d x = 3 0 ,   p a d y = 1 0 )  
                          
                         #   C l i e n t   s e l e c t i o n  
                         t k . L a b e l ( f o r m ,   t e x t = " S e l e c t   C l i e n t : " ,   f o n t = ( ' S e g o e   U I ' ,   1 0 ,   ' b o l d ' ) ) . p a c k ( a n c h o r = ' w ' ,   p a d y = ( 0 ,   5 ) )  
                         c l i e n t _ v a r   =   t k . S t r i n g V a r ( )  
                         c l i e n t _ c o m b o   =   t t k . C o m b o b o x (  
                                 f o r m ,  
                                 t e x t v a r i a b l e = c l i e n t _ v a r ,  
                                 v a l u e s = s o r t e d ( l i s t ( c l i e n t s ) ) ,  
                                 w i d t h = 5 0 ,  
                                 s t a t e = ' r e a d o n l y '  
                         )  
                         c l i e n t _ c o m b o . p a c k ( f i l l = ' x ' ,   p a d y = ( 0 ,   1 5 ) )  
                          
                         #   F i l i n g   t y p e  
                         t k . L a b e l ( f o r m ,   t e x t = " F i l i n g   T y p e : " ,   f o n t = ( ' S e g o e   U I ' ,   1 0 ,   ' b o l d ' ) ) . p a c k ( a n c h o r = ' w ' ,   p a d y = ( 0 ,   5 ) )  
                         f i l i n g _ v a r   =   t k . S t r i n g V a r ( v a l u e = " I T R   F i l i n g   -   I n d i v i d u a l " )  
                         f i l i n g _ c o m b o   =   t t k . C o m b o b o x (  
                                 f o r m ,  
                                 t e x t v a r i a b l e = f i l i n g _ v a r ,  
                                 v a l u e s = [  
                                         " I T R   F i l i n g   -   I n d i v i d u a l " ,  
                                         " I T R   F i l i n g   -   B u s i n e s s " ,  
                                         " G S T   R e t u r n   F i l i n g " ,  
                                         " T D S   R e t u r n   F i l i n g " ,  
                                         " A u d i t   &   C o m p l i a n c e "  
                                 ] ,  
                                 w i d t h = 5 0 ,  
                                 s t a t e = ' r e a d o n l y '  
                         )  
                         f i l i n g _ c o m b o . p a c k ( f i l l = ' x ' ,   p a d y = ( 0 ,   1 5 ) )  
                          
                         #   A m o u n t  
                         t k . L a b e l ( f o r m ,   t e x t = " P r o f e s s i o n a l   F e e s   ( ‚  π ) : " ,   f o n t = ( ' S e g o e   U I ' ,   1 0 ,   ' b o l d ' ) ) . p a c k ( a n c h o r = ' w ' ,   p a d y = ( 0 ,   5 ) )  
                         a m o u n t _ e n t r y   =   t k . E n t r y ( f o r m ,   f o n t = ( ' S e g o e   U I ' ,   1 1 ) ,   w i d t h = 5 0 )  
                         a m o u n t _ e n t r y . i n s e r t ( 0 ,   " 2 5 0 0 " )  
                         a m o u n t _ e n t r y . p a c k ( f i l l = ' x ' ,   p a d y = ( 0 ,   1 5 ) )  
                          
                         #   P e r i o d  
                         t k . L a b e l ( f o r m ,   t e x t = " P e r i o d / F Y : " ,   f o n t = ( ' S e g o e   U I ' ,   1 0 ,   ' b o l d ' ) ) . p a c k ( a n c h o r = ' w ' ,   p a d y = ( 0 ,   5 ) )  
                         p e r i o d _ e n t r y   =   t k . E n t r y ( f o r m ,   f o n t = ( ' S e g o e   U I ' ,   1 1 ) ,   w i d t h = 5 0 )  
                         p e r i o d _ e n t r y . i n s e r t ( 0 ,   " F Y   2 0 2 4 - 2 5 " )  
                         p e r i o d _ e n t r y . p a c k ( f i l l = ' x ' )  
                          
                         d e f   c r e a t e _ i n v o i c e ( ) :  
                                 c l i e n t   =   c l i e n t _ v a r . g e t ( )  
                                 i f   n o t   c l i e n t :  
                                         m e s s a g e b o x . s h o w e r r o r ( " E r r o r " ,   " P l e a s e   s e l e c t   a   c l i e n t " )  
                                         r e t u r n  
                                  
                                 t r y :  
                                         f r o m   d a t e t i m e   i m p o r t   d a t e t i m e  
                                          
                                         i t e m s   =   [ {  
                                                 ' d e s c r i p t i o n ' :   f " { f i l i n g _ v a r . g e t ( ) }   -   { p e r i o d _ e n t r y . g e t ( ) } " ,  
                                                 ' q u a n t i t y ' :   1 ,  
                                                 ' r a t e ' :   f l o a t ( a m o u n t _ e n t r y . g e t ( ) )  
                                         } ]  
                                          
                                         s u c c e s s ,   r e s u l t   =   s e l f . e n g i n e . c r e a t e _ i n v o i c e (  
                                                 i n v o i c e _ n u m b e r = f " I T R - { d a t e t i m e . n o w ( ) . s t r f t i m e ( ' % Y % m % d % H % M % S ' ) } " ,  
                                                 c l i e n t _ n a m e = c l i e n t ,  
                                                 i n v o i c e _ d a t e = d a t e t i m e . n o w ( ) . s t r f t i m e ( ' % Y - % m - % d ' ) ,  
                                                 i t e m s = i t e m s ,  
                                                 t a x _ r a t e = 1 8 . 0  
                                         )  
                                          
                                         i f   s u c c e s s :  
                                                 m e s s a g e b o x . s h o w i n f o (  
                                                         " S u c c e s s " ,  
                                                         f " I T R   F i l i n g   i n v o i c e   c r e a t e d   f o r   { c l i e n t } ! \ n \ n "  
                                                         f " A m o u n t :   ‚  π { a m o u n t _ e n t r y . g e t ( ) } \ n "  
                                                         f " C h e c k   I n v o i c e s   p a n e l   f o r   d e t a i l s . "  
                                                 )  
                                                 d i a l o g . d e s t r o y ( )  
                                         e l s e :  
                                                 m e s s a g e b o x . s h o w e r r o r ( " E r r o r " ,   r e s u l t )  
                                                  
                                 e x c e p t   E x c e p t i o n   a s   e :  
                                         m e s s a g e b o x . s h o w e r r o r ( " E r r o r " ,   f " F a i l e d   t o   c r e a t e   i n v o i c e : \ n { s t r ( e ) } " )  
                          
                         t k . B u t t o n (  
                                 d i a l o g ,  
                                 t e x t = " C r e a t e   I n v o i c e " ,  
                                 f o n t = ( ' S e g o e   U I ' ,   1 1 ) ,  
                                 b g = ' # 4 C A F 5 0 ' ,  
                                 f g = ' w h i t e ' ,  
                                 r e l i e f = ' f l a t ' ,  
                                 c u r s o r = ' h a n d 2 ' ,  
                                 p a d x = 3 0 ,  
                                 p a d y = 1 0 ,  
                                 c o m m a n d = c r e a t e _ i n v o i c e  
                         ) . p a c k ( p a d y = 2 0 )  
                          
                 e x c e p t   E x c e p t i o n   a s   e :  
                         m e s s a g e b o x . s h o w e r r o r ( " E r r o r " ,   f " F a i l e d : \ n { s t r ( e ) } " )  
          
         d e f   _ c r e a t e _ i t r _ i n v o i c e _ f o r _ c l i e n t ( s e l f ,   c l i e n t _ n a m e ) :  
                 " " " Q u i c k   i n v o i c e   c r e a t i o n   f o r   s p e c i f i c   c l i e n t " " "  
                 t r y :  
                         f r o m   d a t e t i m e   i m p o r t   d a t e t i m e  
                          
                         i t e m s   =   [ {  
                                 ' d e s c r i p t i o n ' :   f " I T R   F i l i n g   -   F Y   2 0 2 4 - 2 5 " ,  
                                 ' q u a n t i t y ' :   1 ,  
                                 ' r a t e ' :   2 5 0 0  
                         } ]  
                          
                         s u c c e s s ,   r e s u l t   =   s e l f . e n g i n e . c r e a t e _ i n v o i c e (  
                                 i n v o i c e _ n u m b e r = f " I T R - { d a t e t i m e . n o w ( ) . s t r f t i m e ( ' % Y % m % d % H % M % S ' ) } " ,  
                                 c l i e n t _ n a m e = c l i e n t _ n a m e ,  
                                 i n v o i c e _ d a t e = d a t e t i m e . n o w ( ) . s t r f t i m e ( ' % Y - % m - % d ' ) ,  
                                 i t e m s = i t e m s ,  
                                 t a x _ r a t e = 1 8 . 0  
                         )  
                          
                         i f   s u c c e s s :  
                                 m e s s a g e b o x . s h o w i n f o (  
                                         " S u c c e s s " ,  
                                         f " I T R   F i l i n g   i n v o i c e   c r e a t e d   f o r   { c l i e n t _ n a m e } ! "  
                                 )  
                         e l s e :  
                                 m e s s a g e b o x . s h o w e r r o r ( " E r r o r " ,   r e s u l t )  
                                  
                 e x c e p t   E x c e p t i o n   a s   e :  
                         m e s s a g e b o x . s h o w e r r o r ( " E r r o r " ,   s t r ( e ) )  
 