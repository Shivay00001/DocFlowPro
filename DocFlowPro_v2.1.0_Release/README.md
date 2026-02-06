# DocFlow Pro - Enterprise Document Management System

**Version 2.1.0 Enterprise Edition**  
**Copyright © 2025. All Rights Reserved.**

---

## 🚀 What's New in v2.1.0 Enterprise

**Major Enterprise Enhancements:**

- ✅ Session Management - 30-minute auto-logout for security
- ✅ Automatic Database Backup - Daily backups with 7-day retention
- ✅ Input Validation Layer - Comprehensive data validation
- ✅ File Security - Magic number verification, size limits
- ✅ Pagination System - Handle 1000+ records efficiently
- ✅ Auto-Update Checker - Stay current with latest version
- ✅ Business Rules Engine - Plan enforcement and limits
- ✅ Error Recovery - Auto-retry and database recovery
- ✅ Performance Monitoring - Track operation metrics

---

## Overview

DocFlow Pro is a comprehensive enterprise document management and invoicing system with advanced features including OCR, ML-powered analytics, GST/ITR compliance, and payment processing.

## Features

✨ **Core Features:**

- Document management with OCR text extraction
- Professional invoice generation
- PDF and Excel export capabilities
- User data isolation and security
- Production-grade logging

📊 **Advanced Analytics:**

- ML-powered data cleaning
- Sales predictions and forecasting
- Anomaly detection
- Business intelligence dashboard
- Regulatory compliance helpers (GST, TDS, ITR)

🤖 **AI Integration:**

- AI Data Factory for automation
- Support for OpenAI, Claude, and Gemini APIs
- Smart expense categorization
- Data quality scoring

💳 **Payment Integration:**

- Razorpay payment gateway
- Multiple plan tiers (Free, Starter, Professional, Lifetime)
- Secure license management

---

## 🏢 Enterprise Features (v2.1.0)

**Security & Reliability:**

- **Session Management** - Auto-logout after 30 minutes of inactivity
- **Auto-Backup System** - Daily database backups, 7-day retention
- **Input Validation** - Comprehensive data validation across all forms

**Performance & Scalability:**

- **File Security** - Magic number verification, file type validation
- **Pagination** - Efficient handling of large datasets (1000+ records)
- **Update Checker** - Automatic update notifications

**Advanced Systems:**

- **Business Rules** - Enforce plan limits and business logic
- **Error Recovery** - Auto-retry mechanisms, database recovery
- **Performance Monitoring** - Real-time operation tracking

---

## System Requirements

**Operating System:**

- Windows 10/11 (64-bit)

**Hardware:**

- Minimum 4GB RAM (8GB recommended)
- 500MB free disk space
- Internet connection (for payment processing and AI features)

**Software Dependencies:**

- Python 3.8+ OR standalone .exe (no Python required)
- Tesseract OCR (for image text extraction) - Optional

---

## Installation

### Option 1: Standalone Executable (Recommended)

1. Download `DocFlowPro.exe`
2. Run the executable
3. Follow the setup wizard
4. **IMPORTANT:** Save the admin password shown on first launch!

### Option 2: From Source

```bash
# Install dependencies
pip install -r requirements.txt

# Run application
python main.py
```

---

## First Time Setup

### 1.Administrator Password

On first launch, a **secure random password** is generated for the admin account.

**CRITICAL:** The password is saved to `ADMIN_PASSWORD.txt` - **SAVE IT IMMEDIATELY!**

```
Username: admin
Password: [saved in ADMIN_PASSWORD.txt]
```

### 2. API Keys (For Payment Features)

Set environment variables for Razorpay integration:

**Windows PowerShell:**

```powershell
$env:RAZORPAY_KEY_ID = "your_key_here"
$env:RAZORPAY_KEY_SECRET = "your_secret_here"
```

**Windows CMD:**

```cmd
setx RAZORPAY_KEY_ID "your_key_here"
setx RAZORPAY_KEY_SECRET "your_secret_here"
```

### 3. OCR Setup (Optional)

For image text extraction, install Tesseract OCR:

1. Download from: <https://github.com/UB-Mannheim/tesseract/wiki>
2. Install to: `C:\Program Files\Tesseract-OCR`
3. See `OCR_SETUP.md` for details

---

## Quick Start

1. **Launch Application**
   - Double-click "DocFlowPro.exe" OR run `python main.py`

2. **Login**
   - Username: `admin`
   - Password: [from ADMIN_PASSWORD.txt]

3. **Create Invoice**
   - Click "Invoices" → "Create Invoice"
   - Fill in details
   - Click "Save"

4. **Upload Document**
   - Click "Documents" → "Add Document"
   - Select file (PDF, Excel, Image, etc.)
   - System automatically extracts data

5. **Export Data**
   - Click "Export" → Choose format (PDF/Excel)
   - Select documents/invoices
   - Click "Export"

---

## Pricing Plans

| Plan | Price | Features |
|------|-------|----------|
| **Free** | ₹0 | 20 docs/month, Basic OCR, PDF export |
| **Monthly** | ₹299/month | Full features, Excel export, Priority support |
| **Lifetime** | ₹2,999 | One-time payment, All features forever |

Upgrade within the application: **Settings** → **Upgrade Plan**

---

## Security Features

✅ Secure random password generation  
✅ User data isolation (each user sees only their data)  
✅ Production logging for audit trails  
✅ Payment gateway integration with encryption  
✅ Environment variable support for API keys  

---

## Support

📧 **Email:** <support@yourcompany.com>  
📚 **Documentation:** See `DEPLOYMENT.md` for detailed guides  
🐛 **Bug Reports:** Include `logs/errors.log` with your report  

**Log Files Location:**

- Application logs: `logs/docflow.log`
- Error logs: `logs/errors.log`
- Payment logs: `logs/payments.log`

---

## Troubleshooting

### Application Won't Start

- Check `logs/errors.log` for details
- Ensure all dependencies installed
- Try running as Administrator

### OCR Not Working

- Install Tesseract OCR (see OCR_SETUP.md)
- Verify installation: `tesseract --version`

### Payment Gateway Errors

- Ensure environment variables are set
- Check internet connection
- Verify Razorpay account is active

### "File Not Found" Errors

- Ensure running from correct directory
- Check file permissions

---

## Legal

This software is licensed under proprietary terms. See `LICENSE.txt` for full details.

**Disclaimer:** This software is provided "AS IS" without warranties. Users are responsible
for compliance with tax and data protection regulations in their jurisdiction.

---

## Version History

**v2.1.0 Enterprise** (2025-12-19)

- ✅ Session management with auto-timeout
- ✅ Automatic database backup system
- ✅ Comprehensive input validation
- ✅ File security with magic number verification
- ✅ Pagination for large datasets
- ✅ Auto-update checker
- ✅ Business rules engine
- ✅ Error recovery mechanisms
- ✅ Performance monitoring system

**v2.0** (2025-12-19)

- Production-ready release
- Enhanced security (random password generation)
- Improved error handling
- Comprehensive logging
- Fixed critical bugs
- Added deployment documentation

---

## Credits

Powered by:

- Razorpay for payment processing
- Tesseract for OCR
- Python ecosystem libraries

---

**DocFlow Pro** - Professional Document Management Made Simple

Copyright © 2025. All Rights Reserved.
