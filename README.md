# Social Media Content Analyzer

A web application that extracts text from PDF and image files and analyzes the extracted content for social-media engagement potential.

## Features

* Upload PDF, PNG, JPG, and JPEG files
* Drag-and-drop file upload
* PDF text extraction using PyMuPDF
* OCR for scanned PDFs and images using Tesseract
* Engagement score out of 100
* Word and character count
* Hashtag, mention, and question detection
* Call-to-action detection
* Engagement improvement suggestions
* File size and file type validation
* Loading state during analysis
* Temporary uploaded files are deleted after processing

## Technology Stack

* Python
* Flask
* PyMuPDF
* Pytesseract
* Pillow
* Tesseract OCR
* HTML/CSS/JavaScript
* Gunicorn
* Docker

## How It Works

1. The user uploads a PDF or image through the web interface.
2. The application validates the file type and size.
3. For PDFs, selectable text is extracted using PyMuPDF.
4. If a PDF has no selectable text, its pages are rendered and processed using OCR.
5. Images are processed directly using Tesseract OCR.
6. The extracted text is analyzed for engagement-related characteristics.
7. The application calculates an engagement score and generates suggestions.
8. The extracted text and analysis results are displayed on the web page.

## Engagement Analysis

The analyzer checks:

* Number of words
* Number of characters
* Hashtags
* Mentions
* Questions
* Call-to-action keywords
* Content length
* Paragraph structure

The application generates a score from 0 to 100 based on these characteristics and provides suggestions for improving engagement.

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

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Install Tesseract OCR

Tesseract OCR is required for image OCR and scanned PDFs.

On Windows, install Tesseract and ensure the executable is available at:

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

The application is configured for deployment using Gunicorn and Docker.

The Docker image installs Tesseract OCR inside the container so that OCR functionality is available in the deployment environment.

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
