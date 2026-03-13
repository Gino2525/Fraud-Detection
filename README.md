# ID Document Forgery Detection Prototype

This project is a **prototype system that analyzes an uploaded ID document image and produces a forgery risk report**.


* Problem understanding
* Image tampering detection
* OCR-based anomaly analysis
* Integration of AI and computer vision tools
* Structured fraud reporting

---

# Features

The system analyzes an uploaded ID document image using multiple techniques:

### 1. Image Validation

Checks whether the uploaded file is a valid image and not a renamed file.

### 2. Visual Tampering Detection

Detects possible manipulation using:

* Error Level Analysis (ELA)
* Blur / sharpness analysis
* Edge density detection
* Noise variance analysis
* EXIF metadata inspection
* Resolution checks
* Face-region consistency
* Boundary detection
* Lighting inconsistency detection

### 3. OCR Analysis

Text is extracted from the document using **Tesseract OCR**, then analyzed for anomalies such as:

* Missing expected fields
* Invalid text patterns
* Unusual character noise
* Text alignment inconsistencies
* Low OCR confidence

### 4. Structured Fraud Report

The API returns a JSON report including:

* Validation results
* Image tampering analysis
* OCR anomaly detection
* Risk scores and findings

---

# Project Structure

```
Fraud-Detection/
│
├── main.py        # FastAPI server
├── validator.py   # Image validation logic
├── tamper.py      # Image tampering analysis
├── ocr.py         # OCR extraction and anomaly detection
├── README.md
```

---

# Requirements

* Python 3.9+
* Git
* Tesseract OCR

Python libraries used:

```
fastapi
uvicorn
opencv-python
numpy
pillow
pytesseract
```

---

# Installation

## 1. Clone the repository

```
git clone https://github.com/Gino2525/Fraud-Detection.git
cd Fraud-Detection
```

---

## 2. Install dependencies

```
pip install fastapi uvicorn opencv-python numpy pillow pytesseract
```

---

## 3. Install Tesseract OCR

Download from:

https://github.com/UB-Mannheim/tesseract/wiki

Install and note the installation path.

Typical Windows path:

```
C:\Program Files\Tesseract-OCR\tesseract.exe
```

If needed, set the path in `ocr.py`:

```python
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

---

# Running the API

Start the FastAPI server:

```
uvicorn main:app --reload
```

The server will start at:

```
http://127.0.0.1:8000
```

---

# API Documentation

Open the interactive API docs:

```
http://127.0.0.1:8000/docs
```

You can upload an ID image and view the fraud analysis results.

---

# Example Output

```
{
  "status": "success",
  "validation": "Valid JPEG image",
  "tampering_analysis": {
    "tamper_risk_level": "Low"
  },
  "ocr_analysis": {
    "ocr_risk_level": "Medium"
  }
}
```

### Note

The current OCR module implements a **basic, generic structure for text extraction and anomaly detection**. It analyzes OCR confidence, alignment, character patterns, and missing fields to identify potential inconsistencies.

However, **document-specific validation rules are not yet fully implemented**. For example, Aadhaar cards contain structured identifiers (e.g., a 12-digit Aadhaar number and a 16-digit VID) that should be verified explicitly. Future customization can include checks such as:

* Verifying whether the **Aadhaar number (12 digits)** is present and correctly formatted.
* Checking if a **16-digit Virtual ID (VID)** appears when expected.
* Validating other structured fields like **Name, DOB, and address format**.
* Applying **document-specific OCR rules depending on the detected ID type**.

These enhancements would make the OCR analysis more accurate and reduce false anomaly detections.




Developed as part of a coding task for **ID document forgery detection using computer vision and OCR analysis**.
