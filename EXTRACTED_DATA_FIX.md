# DocFlowPro - Quick Fix Guide

## Issue: Extracted Data Not Displaying

**Problem:** Export shows filenames, not the extracted OCR/invoice data from uploaded documents.

**Root Cause:** Data IS being extracted and saved to database (in `description` field), but:

1. Documents panel NOT showing the description/extracted data
2. Need to display OCR text, invoice details in a readable format

## Solution Deploy Guide

### Step 1: Update Documents Panel to Show Extracted Data

The data extractor ALREADY works and saves to `description` field.  
Just need Documents panel to SHOW it!

**Add column to documents list:**

```python
# In ui/documents.py, update columns:
columns = ('ID', 'Title', 'Type', 'Date', 'Extracted Data')  # ← ADD THIS

# When loading documents:
for doc in documents:
    # Show first 50 chars of extracted data
    extracted = doc.get('description', '')[:50] or 'No data'
    self.tree.insert('', 'end', values=(
        doc['id'],
        doc['title'],
        doc.get('file_type', 'Unknown'),
        doc.get('created_at', '')[:10],
        extracted  # ← SHOW THIS
    ))
```

### Step 2: View Full Extracted Data

**On double-click:**

```python
def _view_document(self):
    doc = engine.db.get_document_by_id(doc_id, user_id)
    
    details = f"""
Document: {doc['title']}

EXTRACTED DATA:
{doc.get('description', 'No data extracted')}

File: {doc.get('file_path', 'N/A')}
Type: {doc.get('file_type', 'Unknown')}
Tags: {doc.get('tags', 'None')}
OCR Text: {doc.get('ocr_text', 'None')}
    """
    
    messagebox.showinfo("Document Details", details)
```

## What's Already Working

✅ Data Extractor (`utils/data_extractor.py`) - WORKING  
✅ Database storage (`description` field) - WORKING  
✅ Export shows title, category, tags - WORKING  
✅ Enhanced upload dialog saves extracted data - WORKING  

## What Needs UI Update

❌ Documents panel showing filename instead of data  
❌ Need "Extracted Data" column  
❌ Double-click should show FULL extracted invoice details  

## Quick Test

1. Upload a document with invoice data
2. Check database:

   ```sql
   SELECT id, title, description FROM documents WHERE user_id=1;
   ```

3. You'll see extracted data IS there in description!
4. Just need to display it in UI

## Next: Enhance Document View Dialog

Show extracted data in a nice format like:

```
═══════════════════════════════
📄 DOCUMENT DETAILS
═══════════════════════════════

Invoice Number: INV-001
Client: ABC Corp
GST: 29ABCD1234F1Z5
Amount: ₹15,000
Date: 2025-12-16

OCR Text:
[Raw text extracted from image/PDF]

File: invoice_abc.pdf
Uploaded: 2025-12-19
```

This gives professional view of extracted data!
