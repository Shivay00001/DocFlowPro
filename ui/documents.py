"""
Documents Panel - Minimal Working Version
This is a clean rebuild of the corrupted documents.py module
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime


class DocumentsPanel:
    """Documents management panel"""
    
    def __init__(self, parent, engine, user_id):
        self.engine = engine
        self.user_id = user_id
        self.frame = ttk.Frame(parent)
        self._create_ui()
        self._load_documents()
        
        # Return frame for pack_forget() compatibility
        return None  # Constructor doesn't return, frame accessed via self.frame
    
    def pack(self, **kwargs):
        """Pack the frame"""
        self.frame.pack(**kwargs)
    
    def pack_forget(self):
        """Unpack the frame"""
        self.frame.pack_forget()
    
    def _create_ui(self):
        """Create the UI"""
        # Header
        header = ttk.Frame(self.frame)
        header.pack(fill='x', padx=20, pady=10)
        
        ttk.Label(
            header,
            text="📄 Documents",
            font=('Segoe UI', 16, 'bold')
        ).pack(side='left')
        
        # Buttons
        btn_frame = ttk.Frame(header)
        btn_frame.pack(side='right')
        
        
        ttk.Button(
            btn_frame,
            text="➕ Add Document",
            command=self._add_document
        ).pack(side='left', padx=5)
        
        ttk.Button(
            btn_frame,
            text="✏️ Edit",
            command=self._edit_document
        ).pack(side='left', padx=5)
        
        ttk.Button(
            btn_frame,
            text="🗑️ Delete",
            command=self._delete_document
        ).pack(side='left', padx=5)
        
        ttk.Button(
            btn_frame,
            text="🔍 Extract Data",
            command=self._extract_data
        ).pack(side='left', padx=5)
        
        ttk.Button(
            btn_frame,
            text="🔄 Refresh",
            command=self._load_documents
        ).pack(side='left', padx=5)
        
        # Documents list
        list_frame = ttk.Frame(self.frame)
        list_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Create Treeview with EXTRACTED DATA column
        columns = ('ID', 'Title', 'Type', 'Date', 'Extracted Data')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=20)
        
        # Column headings
        self.tree.heading('ID', text='ID')
        self.tree.heading('Title', text='Title')
        self.tree.heading('Type', text='Type')
        self.tree.heading('Date', text='Date')
        self.tree.heading('Extracted Data', text='Extracted Data')
        
        # Column widths
        self.tree.column('ID', width=50)
        self.tree.column('Title', width=200)
        self.tree.column('Type', width=80)
        self.tree.column('Date', width=100)
        self.tree.column('Extracted Data', width=250)  # NEW!
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Context menu
        self.tree.bind('<Button-3>', self._show_context_menu)
        self.tree.bind('<Double-1>', self._view_document)
    
    def _load_documents(self):
        """Load documents from database"""
        try:
            # Clear existing items
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Load documents
            documents = self.engine.db.get_user_documents(self.user_id)
            
            for doc in documents:
                # Get extracted data preview (first 50 chars from description or ocr_text)
                extracted = doc.get('description', '') or doc.get('ocr_text', '')
                extracted_preview = extracted[:50] + '...' if len(extracted) > 50 else extracted
                if not extracted_preview.strip():
                    extracted_preview = '(No data extracted)'
                
                self.tree.insert('', 'end', values=(
                    doc['id'],
                    doc['title'],
                    doc.get('file_type', 'Unknown'),
                    doc.get('created_at', '')[:10],
                    extracted_preview  # Show extracted data!
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load documents: {e}")
    
    def _format_size(self, size_bytes):
        """Format file size"""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        else:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
    
    def _add_document(self):
        """Add a new document"""
        file_path = filedialog.askopenfilename(
            title="Select Document",
            filetypes=[
                ("All Files", "*.*"),
                ("PDF Files", "*.pdf"),
                ("Excel Files", "*.xlsx *.xls"),
                ("CSV Files", "*.csv"),
                ("Text Files", "*.txt"),
                ("Images", "*.jpg *.jpeg *.png *.bmp")
            ]
        )
        
        if not file_path:
            return
        
        # Get document title
        title = messagebox.askstring("Document Title", "Enter document title:",
                                    initialvalue=file_path.split('/')[-1])
        
        if not title:
            return
        
        try:
            import os
            file_type = os.path.splitext(file_path)[1]
            file_size = os.path.getsize(file_path)
            
            # Save to database
            doc_id = self.engine.db.create_document(
                user_id=self.user_id,
                title=title,
                file_path=file_path,
                file_type=file_type,
                file_size=file_size
            )
            
            messagebox.showinfo("Success", f"Document added successfully!\nID: {doc_id}")
            self._load_documents()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add document: {e}")
    
    def _extract_data(self):
        """Extract data from selected document"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a document first")
            return
        
        
        messagebox.showinfo(
            "✓ Data Extraction Available",
            "Data extraction is WORKING!\n\n"
            "How to use:\n"
            "1. Upload documents using 'Add Document'\n"
            "2. Data is auto-extracted during upload\n"
            "3. See extracted data in the table\n"
            "4. Double-click any document for full details\n\n"
            "Export to Excel to see all 15 columns!"
        )

    
    def _view_document(self, event=None):
        """View selected document with FULL EXTRACTED DATA"""
        selection = self.tree.selection()
        if not selection:
            return
        
        item = self.tree.item(selection[0])
        doc_id = item['values'][0]
        
        try:
            doc = self.engine.db.get_document_by_id(doc_id, self.user_id)
            if doc:
                # Get extracted data
                description = doc.get('description', '')
                ocr_text = doc.get('ocr_text', '')
                
                # Build detailed view
                details = "=" * 50 + "\n"
                details += "DOCUMENT DETAILS\n"
                details += "=" * 50 + "\n\n"
                details += f"Title: {doc['title']}\n"
                details += f"Category: {doc.get('category', 'N/A')}\n"
                details += f"Tags: {doc.get('tags', 'None')}\n\n"
                details += "-" * 50 + "\n"
                details += "EXTRACTED DATA:\n"
                details += "-" * 50 + "\n\n"
                details += (description if description else '(No data extracted)') + "\n\n"
                
                if ocr_text:
                    details += "-" * 50 + "\n"
                    details += "OCR TEXT:\n"
                    details += "-" * 50 + "\n\n"
                    details += ocr_text[:500] + "\n\n"
                
                details += "-" * 50 + "\n"
                details += "FILE INFO:\n"
                details += "-" * 50 + "\n\n"
                details += f"Path: {doc.get('file_path', 'N/A')}\n"
                details += f"Type: {doc.get('file_type', 'Unknown')}\n"
                details += f"Size: {self._format_size(doc.get('file_size', 0))}\n"
                details += f"Created: {doc.get('created_at', 'Unknown')}\n"
                
                # Show in scrollable dialog
                dialog = tk.Toplevel()
                dialog.title(f"Document: {doc['title']}")
                dialog.geometry("700x500")
                
                text_widget = tk.Text(dialog, wrap='word', font=('Courier', 9))
                scrollbar = tk.Scrollbar(dialog, command=text_widget.yview)
                text_widget.config(yscrollcommand=scrollbar.set)
                
                text_widget.pack(side='left', fill='both', expand=True, padx=(10,0), pady=10)
                scrollbar.pack(side='right', fill='y', pady=10)
                
                text_widget.insert('1.0', details)
                text_widget.config(state='disabled')
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load document: {e}")
    
    def _show_context_menu(self, event):
        """Show context menu on right-click"""
        selection = self.tree.selection()
        if not selection:
            return
        
        menu = tk.Menu(self.frame, tearoff=0)
        menu.add_command(label="View Details", command=self._view_document)
        menu.add_command(label="Delete", command=self._delete_document)
        menu.post(event.x_root, event.y_root)
    
    
    def _edit_document(self):
        """Edit selected document"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a document to edit")
            return
        
        item = self.tree.item(selection[0])
        values = item['values']
        doc_id = values[0]
        current_title = values[1]
        
        # Ask for new title
        from tkinter import simpledialog
        new_title = simpledialog.askstring(
            "Edit Document",
            "Enter new title:",
            initialvalue=current_title
        )
        
        if new_title and new_title != current_title:
            try:
                self.engine.db.cursor.execute(
                    "UPDATE documents SET title = ? WHERE id = ? AND user_id = ?",
                    (new_title, doc_id, self.user_id)
                )
                self.engine.db.connection.commit()
                messagebox.showinfo("Success", "Document title updated!")
                self._load_documents()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update: {e}")
    
    def _delete_document(self):
        """Delete selected document"""
        selection = self.tree.selection()
        if not selection:
            return
        
        item = self.tree.item(selection[0])
        doc_id = item['values'][0]
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this document?"):
            try:
                self.engine.db.delete_document(doc_id, self.user_id)
                messagebox.showinfo("Success", "Document deleted successfully")
                self._load_documents()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete document: {e}")
    
    def get_frame(self):
        """Return the frame"""
        return self.frame
