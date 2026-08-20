# Social Media Content Analyzer

A Flask-based web application that extracts text from PDF and image files and analyzes social-media content for engagement potential.

## Features

* Upload PDF, PNG, JPG, and JPEG files
* Drag-and-drop file upload
* PDF text extraction using PyMuPDF
* OCR for scanned PDFs using Tesseract
* OCR for JPG, JPEG, and PNG images using Tesseract
* Engagement score out of 100
* Word and character count
* Hashtag, mention, and question detection
* Call-to-action detection
* Engagement improvement suggestions
* File type and file size validation
* Loading state during analysis
* Temporary uploaded files are deleted after processing

## Approach

The Social Media Content Analyzer is built as a Flask web application that accepts PDF and image uploads through a drag-and-drop interface or file picker.

For PDFs, the application first uses PyMuPDF to extract selectable text. If no selectable text is available, the PDF pages are rendered as images and processed using Tesseract OCR. PNG, JPG, and JPEG files are directly processed using Tesseract OCR.

After text extraction, the application performs rule-based engagement analysis. It calculates word and character counts and detects hashtags, mentions, questions, and common call-to-action phrases. These signals are combined to produce an engagement score from 0 to 100. The application also generates suggestions such as adding relevant hashtags, asking an audience-focused question, adding a clear call-to-action, or improving long-form content structure.

Basic error handling covers missing files, unsupported formats, oversized files, corrupted documents, unavailable OCR, and files containing no readable text. Uploaded files are temporarily stored during processing and removed afterward.

## Technology Stack

* Python
* Flask
* HTML/CSS/JavaScript
* Jinja2
* PyMuPDF
* Tesseract OCR
* pytesseract
* Pillow
* Gunicorn
* Docker

## How It Works

1. The user uploads a PDF or image.
2. The application validates the file type and size.
3. Selectable PDF text is extracted using PyMuPDF.
4. Scanned PDFs are processed using Tesseract OCR.
5. JPG, JPEG, and PNG files are processed using Tesseract OCR.
6. The extracted text is analyzed for engagement signals.
7. An engagement score and improvement suggestions are generated.
8. The extracted text and analysis results are displayed on the webpage.
9. The temporary uploaded file is deleted after processing.

## Engagement Analysis

The analyzer checks:

* Word count
* Character count
* Hashtag count
* Mention count
* Question count
* Call-to-action keywords
* Content length
* Paragraph structure

The application generates an engagement score from 0 to 100 and provides suggestions for improving social-media engagement.

## Error Handling

The application handles:

* Missing file uploads
* Unsupported file formats
* Files larger than 10 MB
* Invalid or corrupted PDFs
* Invalid or corrupted images
* Missing OCR engine
* Files with no readable text
* Unexpected processing errors

## Loading State

A loading state is displayed while the uploaded file is being processed so that the user receives visual feedback during PDF parsing and OCR operations.

## Running Locally

### 1. Clone the repository

```bash
git clone https://github.com/Ssunvya/social-media-content-analyzer.git
cd social-media-content-analyzer
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Python dependencies

```powershell
pip install -r requirements.txt
```

### 4. Install Tesseract OCR

Tesseract OCR is required for image OCR and scanned PDF OCR.

On Windows, install Tesseract OCR. The application supports the standard installation path:

```text
C:\Program Files\Tesseract-OCR\tesseract.exe
```

### 5. Run the application

```powershell
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## Deployment

The application is configured to run with Gunicorn and also includes Docker support.

The Dockerfile installs Tesseract OCR inside the container, allowing OCR functionality to be available in environments where system-level Tesseract installation is required.

## Project Structure

```text
social-media-content-analyzer/
│
├── app.py
├── Dockerfile
├── requirements.txt
├── README.md
├── .gitignore
│
└── templates/
    └── index.html
```

## Live Application

https://social-media-content-analyzer-oeip.onrender.com

## GitHub Repository

https://github.com/Ssunvya/social-media-content-analyzer
