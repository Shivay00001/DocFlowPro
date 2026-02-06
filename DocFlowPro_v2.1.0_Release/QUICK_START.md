# DocFlowPro v2.1.0 Enterprise - Quick Start Guide

## 🚀 Installation & Setup (2 Minutes)

### Step 1: Extract Files

1. Extract `DocFlowPro_v2.1.0.zip` to a folder (e.g., `C:\DocFlowPro`)
2. You'll see: `DocFlowPro.exe` and documentation files

### Step 2: Install Tesseract OCR (For Image Text Extraction)

**Only if extracting text from images (PNG/JPG):**

1. Download Tesseract:
   - <https://github.com/UB-Mannheim/tesseract/wiki>
   - Get: `tesseract-ocr-w64-setup-5.x.x.exe`

2. Install:
   - Run installer
   - **Check "Add to PATH"** during installation
   - Default location: `C:\Program Files\Tesseract-OCR`

3. Verify:

   ```cmd
   tesseract --version
   ```

**Note:** Application works without Tesseract, but image text extraction won't work.

---

## 🎯 First Launch

### Double-click `DocFlowPro.exe`

**What happens:**

1. Database `docflow.db` created automatically
2. Default user created (username: `shivay`)
3. Auto-backup created
4. Main window opens

**First time:** No login needed! Application creates a default user automatically.

---

## ✨ Core Features (Ready to Use)

### 1. Upload Documents

- Click "Documents" panel
- Click "Upload Document"
- Select any file: PDF, Excel, Images, CSV, etc.
- **Auto-extraction:** Invoice data extracted from supported formats

### 2. View Documents

- Double-click any document
- See extracted invoice data:
  - Invoice Number
  - Client Name
  - Total Amount
  - OCR Text (if image)

### 3. Export to Excel/PDF

- Click "Export" panel
- Select "Documents" or "Invoices"
- Choose format: PDF or Excel
- Click "Export Data"
- **Shows extracted invoice data in "Extracted Data" column!**

### 4. Create GST Invoices

- Click "Invoices" panel
- Create new invoice
- Add line items
- Export → Professional GST invoice (CGST/SGST 9%)

---

## 📊 License Tiers

| Plan | Documents | Invoices | Features |
|------|-----------|----------|----------|
| **Free** | 50 | 20 | Basic features |
| **Starter** (₹2,999) | 100 | 50 | + AI Analytics |
| **Professional** (₹4,999) | 500 | 200 | + Excel Export, Advanced |
| **Lifetime** (₹9,999) | Unlimited | Unlimited | All features forever |

**Upgrade:** Click "Settings" → "Upgrade Plan"

---

## 🔧 Configuration (Optional)

### Enable Payment Processing

Create environment variables (for payment integration):

```cmd
setx RAZORPAY_KEY_ID "your_key_here"
setx RAZORPAY_KEY_SECRET "your_secret_here"
```

**Note:** Not required for basic use!

---

## 🎯 Quick Test (30 Seconds)

1. **Launch** `DocFlowPro.exe`
2. **Upload** any invoice image (PNG/JPG) or PDF
3. **Go to Documents** panel → See extracted data preview
4. **Go to Export** → Documents → Excel → Export
5. **Open Excel file** → See "Extracted Data" column!

**Expected Result:**

```
ID | Title | Type | Extracted Data | Created
1  | invoice.png | PNG | Invoice: 001, Client: ABC Corp, Amount: Rs.15000 | 2025-12-19
```

---

## 📁 File Structure

```
DocFlowPro/
├── DocFlowPro.exe (standalone executable)
├── docflow.db (created on first run)
├── backups/ (auto-backups, created automatically)
├── logs/ (application logs)
└── README.md (this file)
```

---

## ✅ Enterprise Features Included

1. **Auto-Backup** (every 24 hours)
2. **Session Management** (30-minute timeout)
3. **Input Validation** (prevents errors)
4. **File Security** (validates file types)
5. **Pagination** (handles large datasets)
6. **Auto-Update Check**
7. **Business Rules Engine**
8. **Error Recovery** (auto-retry)
9. **Performance Monitoring**

All features active by default!

---

## 🚨 Troubleshooting

### Executable doesn't launch

- **Windows Defender:** Allow the application
- **Antivirus:** Add to exception list
- **Run as Administrator** (right-click → Run as administrator)

### Image text extraction not working

- **Install Tesseract OCR** (see Step 2 above)
- Check path: `C:\Program Files\Tesseract-OCR\tesseract.exe`

### Export shows "(No data)"

- **Solution:** Documents uploaded BEFORE data extraction fix won't have data
- **Fix:** Re-upload documents OR run extraction script
- **Script:** Contact support for `extract_existing_data.py`

### Database errors

- **Delete** `docflow.db` file
- **Restart** application (fresh database created)

---

## 📞 Support & Updates

**Email:** <support@visionquantech.com>  
**Website:** <www.visionquantech.com>  
**Version:** 2.1.0 Enterprise  
**Build Date:** 2025-12-19  

---

## 📝 License

**Commercial Software License**  
© 2025 VisionQuantech. All rights reserved.  

See `LICENSE.txt` for complete terms.

---

## 🎉 You're Ready

**Start using DocFlowPro now:**

1. Double-click `DocFlowPro.exe`
2. Upload documents
3. Export to Excel
4. See your extracted invoice data!

**Enjoy your enterprise-grade document management system!** 🚀
