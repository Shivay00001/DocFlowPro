# OCR Setup Guide for DocFlow Pro

## Windows Installation

### Step 1: Install Tesseract OCR

1. Download Tesseract installer from: <https://github.com/UB-Mannheim/tesseract/wiki>
2. Run the installer (tesseract-ocr-w64-setup-5.3.x.exe)
3. Install to default location: `C:\Program Files\Tesseract-OCR`
4. During installation, make sure to select "Add to PATH"

### Step 2: Verify Installation

Open Command Prompt and type:

```
tesseract --version
```

You should see version information.

### Step 3: Configure Python (if needed)

If OCR still doesn't work, add this to your code:

```python
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

## Python Package

Already installed via requirements.txt:

```
pip install pytesseract pillow
```

## Usage in DocFlow Pro

1. Go to Documents panel
2. Click "🔍 Extract Data"
3. Select image file (JPG, PNG, BMP)
4. OCR will automatically extract text
5. Review extracted invoice data
6. Create invoice or save as document

## Supported Image Formats

- JPG/JPEG
- PNG
- BMP
- TIFF

## Tips for Best Results

- Use high-resolution images (300 DPI or higher)
- Ensure text is clear and not blurry
- Good lighting and contrast
- Straight, not tilted images

## Troubleshooting

### Error: "Tesseract not found"

**Solution:**

1. Verify Tesseract is installed:

   ```
   tesseract --version
   ```

2. If not found, add to PATH manually:
   - Right-click "This PC" → Properties → Advanced System Settings
   - Click "Environment Variables"
   - Under "System Variables", find "Path"
   - Click "Edit" → "New"
   - Add: `C:\Program Files\Tesseract-OCR`
   - Click "OK" and restart your application

### Error: "Failed to load Tesseract library"

**Solution:**

1. Download and install Microsoft Visual C++ Redistributable
2. Reinstall Tesseract OCR
3. Restart your computer

### Poor OCR Results

**Solutions:**

- Use higher resolution scans (300+ DPI)
- Ensure good contrast between text and background
- Avoid handwritten text (OCR works best with printed text)
- Try enhancing image before OCR (increase contrast, sharpen)
- Save images in PNG or TIFF format (not JPG)

### Automatic Detection

The application now automatically detects Tesseract installation:

- Checks `C:\Program Files\Tesseract-OCR\tesseract.exe`
- Checks `C:\Program Files (x86)\Tesseract-OCR\tesseract.exe`
- Checks `C:\Tesseract-OCR\tesseract.exe`

If installed elsewhere, OCR may not work. Reinstall to default location.

### Still Having Issues?

Check the error logs:

- `logs/errors.log` - for detailed error messages
- `logs/docflow.log` - for general application logs

Contact support with log files for assistance.
