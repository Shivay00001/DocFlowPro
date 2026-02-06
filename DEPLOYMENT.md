# DocFlow Pro - Production Deployment Guide

## Pre-Deployment Checklist

### 1. Security ✓ CRITICAL

- [ ] **API Keys Security**
  - Remove hardcoded Razorpay credentials from `config/payment_config.py`
  - Set environment variables: `RAZORPAY_KEY_ID` and `RAZORPAY_KEY_SECRET`
  - Verify credentials are not in version control
  
- [ ] **Database Security**
  - Enable database encryption if handling sensitive data
  - Set strong default admin password (not "admin123")
  - Consider implementing proper authentication flow
  
- [ ] **Code Obfuscation** (Optional)
  - If distributing source code, consider using PyArmor or similar tools
  - For compiled executables, ensure debug symbols are stripped

### 2. Dependencies ✓ REQUIRED

- [ ] **Python Packages**

  ```bash
  pip install -r requirements.txt
  ```
  
- [ ] **Tesseract OCR** (for image text extraction)
  - Download: <https://github.com/UB-Mannheim/tesseract/wiki>
  - Install to: `C:\Program Files\Tesseract-OCR`
  - Verify: `tesseract --version`
  - See [OCR_SETUP.md](OCR_SETUP.md) for detailed installation

- [ ] **System Requirements**
  - Windows 10/11 (64-bit)
  - 4GB RAM minimum, 8GB recommended
  - 500MB free disk space

### 3. Configuration ✓ IMPORTANT

- [ ] **Payment Configuration**
  - Verify Razorpay account is set to LIVE mode
  - Test payment flow with small amount (₹1) first
  - Ensure webhook URLs are configured (if using)
  
- [ ] **License Configuration**
  - Review plan pricing in `config/payment_config.py`
  - Verify pricing aligns with your business model
  - Update FIRST_USER_OFFER settings if needed
  
- [ ] **Feature Gates**
  - Review feature access levels in `core/feature_gates.py`
  - Ensure free plan limitations are appropriate
  - Test that paid features are properly gated

### 4. Testing ✓ MANDATORY

- [ ] **Functional Testing**

  ```bash
  # Run verification script
  python verify_all.py
  
  # Test core functionality
  python test_core.py
  
  # Launch application
  python main.py
  ```
  
- [ ] **Feature Testing**
  - [ ] Create document
  - [ ] Create invoice
  - [ ] OCR image extraction
  - [ ] Data cleaning
  - [ ] Export to PDF
  - [ ] Export toExcel
  - [ ] Payment upgrade flow (test mode first!)
  
- [ ] **Error Handling**
  - [ ] Test without Tesseract installed
  - [ ] Test with corrupted database
  - [ ] Test with missing dependencies
  - [ ] Verify error messages are user-friendly

### 5. Build Executable ✓ DISTRIBUTION

- [ ] **PyInstaller Build**

  ```bash
  # Clean previous builds
  rmdir /s /q build dist
  
  # Build executable
  pyinstaller docflowpro.spec
  
  # Test the executable
  .\dist\DocFlowPro\DocFlowPro.exe
  ```
  
- [ ] **Bundle Requirements**
  - [ ] Logo and icon files included
  - [ ] Database schema initialized
  - [ ] Default configuration files
  - [ ] OCR language data (if bundling Tesseract)
  
- [ ] **File Structure Verification**

  ```
  dist/DocFlowPro/
  ├── DocFlowPro.exe
  ├── logo.png
  ├── docflow.db (empty or with defaults)
  ├── README.txt
  └── ... (other dependencies)
  ```

### 6. Documentation ✓ USER SUPPORT

- [ ] **User Documentation**
  - [ ] Installation guide
  - [ ] Quick start tutorial
  - [ ] Feature walkthrough
  - [ ] Troubleshooting guide
  - [ ] FAQ
  
- [ ] **Technical Documentation**
  - [ ] System architecture
  - [ ] Database schema
  - [ ] API documentation (if applicable)
  - [ ] Deployment guide (this file)

### 7. Distribution ✓ DELIVERY

- [ ] **Package Contents**
  - [ ] Executable (or installer)
  - [ ] README file
  - [ ] LICENSE file
  - [ ] User manual (PDF)
  - [ ] Installation instructions
  
- [ ] **Installer Creation** (Optional but recommended)
  - Consider creating MSI installer with Inno Setup or NSIS
  - Include auto-update mechanism
  - Bundle dependencies (Tesseract OCR)
  
- [ ] **Distribution Channels**
  - [ ] Company website download
  - [ ] Email delivery to customers
  - [ ] Cloud storage links
  - [ ] License key delivery system

### 8. Post-Deployment ✓ SUPPORT

- [ ] **Monitoring**
  - Set up log file monitoring
  - Check `logs/errors.log` regularly
  - Monitor payment logs for issues
  
- [ ] **Customer Support**
  - [ ] Support email configured
  - [ ] Response templates prepared
  - [ ] Known issues documented
  - [ ] Update/patch delivery mechanism
  
- [ ] **Backup & Recovery**
  - Document database backup procedures
  - Provide data export/import tools
  - Document disaster recovery process

## Security Best Practices

### Environment Variables Setup

**Windows PowerShell:**

```powershell
# Set for current session
$env:RAZORPAY_KEY_ID = "your_key_here"
$env:RAZORPAY_KEY_SECRET = "your_secret_here"

# Set permanently (System-wide)
[System.Environment]::SetEnvironmentVariable('RAZORPAY_KEY_ID', 'your_key_here', 'Machine')
[System.Environment]::SetEnvironmentVariable('RAZORPAY_KEY_SECRET', 'your_secret_here', 'Machine')
```

**Windows CMD:**

```cmd
setx RAZORPAY_KEY_ID "your_key_here"
setx RAZORPAY_KEY_SECRET "your_secret_here"
```

### Production Hardening

1. **Disable Debug Mode**
   - Remove all `print()` debug statements
   - Disable verbose logging in production

2. **Error Messages**
   - Never expose internal paths or code to users
   - Log detailed errors, show generic messages to users
   - Implemented in `main.py` with production logger

3. **Database**
   - Regular backups
   - Transaction logging
   - Data validation on all inputs

## Common Issues & Solutions

### Issue: Payment Gateway Not Working

**Symptoms:** Payment button doesn't work, crashes
**Solution:**

1. Check API credentials are correct
2. Verify FIRST_USER_OFFER import is present
3. Check internet connection
4. Review `logs/payments.log`

### Issue: OCR Not Working

**Symptoms:** "Tesseract not found" error
**Solution:**

1. Install Tesseract OCR
2. Verify installation path
3. See [OCR_SETUP.md](OCR_SETUP.md)

### Issue: Application Won't Start

**Symptoms:** Crashes immediately, import errors
**Solution:**

1. Check all dependencies installed: `pip install -r requirements.txt`
2. Review `logs/errors.log`
3. Verify Python version compatibility (3.8+)

### Issue: Database Errors

**Symptoms:** "Database locked", corruption errors
**Solution:**

1. Close all instances of the application
2. Delete `docflow.db` (user data will be lost)
3. Restart application (new database created)
4. Import backup if available

## License Key Distribution

The application currently uses user-based licensing. Each installation:

1. Creates single user on first run (default: admin/admin123)
2. User can upgrade via payment gateway
3. License stored in database (`license_info` table)

### Recommended Improvements

- Implement license key validation
- Add machine fingerprinting
- Remote license activation
- License expiry enforcement

## Update Distribution

When releasing updates:

1. Test thoroughly on clean install
2. Verify database migration (if schema changed)
3. Increment version number
4. Create changelog
5. Distribute via auto-update or manual download
6. Notify users via email

## Support Contact

Before deployment, ensure support channels are ready:

- Support email: <support@yourcompany.com>
- Documentation: <https://docs.yourcompany.com>
- Bug reports: support ticketing system

## Production Rollout Plan

### Phase 1: Beta Testing (1-2 weeks)

- Deploy to 5-10 beta users
- Gather feedback
- Fix critical bugs
- Monitor logs daily

### Phase 2: Limited Release (1 month)

- Deploy to 50-100 users
- Collect usage analytics
- Refine based on feedback
- Build FAQ from support tickets

### Phase 3: General Availability

- Full public release
- Marketing campaign
- Scale support team
- Monitor system performance

---

**Last Updated:** 2025-12-19
**Version:** 2.0
**Status:** Production Ready (after checklist completion)
