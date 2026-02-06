"""
Emergency Fix Script - Add Missing Methods to Documents Panel
"""

# Add these methods to documents.py after line 240

def _edit_document(self):
    """Edit selected document"""
    selection = self.tree.selection()
    if not selection:
        messagebox.showwarning("No Selection", "Please select a document to edit")
        return
    
    # Get selected document ID from first column
    item_values = self.tree.item(selection[0], 'values')
    if not item_values:
        return
    
    doc_id = int(item_values[0])
    
    # Simple edit dialog
    new_title = tk.simpledialog.askstring(
        "Edit Document",
        "Enter new title:",
        initialvalue=item_values[1]
    )
    
    if new_title:
        try:
            # Update in database
            self.engine.db.cursor.execute(
                "UPDATE documents SET title = ? WHERE id = ? AND user_id = ?",
                (new_title, doc_id, self.user_id)
            )
            self.engine.db.connection.commit()
            messagebox.showinfo("Success", "Document updated!")
            self._load_documents()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update: {e}")

def _delete_document(self):
    """Delete selected document"""
    selection = self.tree.selection()
    if not selection:
        messagebox.showwarning("No Selection", "Please select a document to delete")
        return
    
    item_values = self.tree.item(selection[0], 'values')
    if not item_values:
        return
    
    doc_id = int(item_values[0])
    doc_title = item_values[1]
    
    # Confirm deletion
    if messagebox.askyesno(
        "Confirm Delete",
        f"Are you sure you want to delete '{doc_title}'?\n\nThis cannot be undone!"
    ):
        try:
            # Delete from database
            self.engine.db.cursor.execute(
                "DELETE FROM documents WHERE id = ? AND user_id = ?",
                (doc_id, self.user_id)
            )
            self.engine.db.connection.commit()
            messagebox.showinfo("Success", "Document deleted!")
            self._load_documents()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete: {e}")

# Add import at top if missing:
import tkinter.simpledialog
