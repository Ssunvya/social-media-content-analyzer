# Social Media Content Analyzer

A Flask-based web application that extracts text from PDF and image files and analyzes the content for social-media engagement potential.

## Features

- PDF, PNG, JPG, and JPEG upload
- Drag-and-drop and file-picker upload
- PDF text extraction using PyMuPDF
- OCR for scanned PDFs and images using Tesseract
- Engagement score out of 100
- Word and character count
- Hashtag, mention, and question detection
- Call-to-action detection
- Engagement improvement suggestions
- File type and 10 MB size validation
- Loading state during processing
- Error handling for invalid files and OCR failures
- Temporary uploaded files are removed after processing

## Approach

The application first validates the uploaded file and then selects the appropriate extraction method. For PDFs, PyMuPDF extracts selectable text while preserving the document's text structure. If a PDF contains no selectable text, its pages are rendered as images and processed using Tesseract OCR. Image files are processed directly using Tesseract OCR.

The extracted text is then analyzed using rule-based engagement metrics including word count, hashtags, mentions, questions, call-to-action keywords, content length, and paragraph structure. These signals are combined into an engagement score from 0 to 100, along with suggestions for improving the content.

The application includes basic validation, exception handling, loading feedback, temporary-file cleanup, and deployment support through Gunicorn and Docker.

## Technology Stack

- Python
- Flask
- PyMuPDF
- Pytesseract
- Pillow
- Tesseract OCR
- HTML/CSS/JavaScript
- Gunicorn
- Docker

## How It Works

1. Upload a PDF or image using the file picker or drag-and-drop area.
2. The application validates the file type and size.
3. PDF text is extracted using PyMuPDF.
4. Scanned PDFs are processed using OCR when selectable text is unavailable.
5. JPG and PNG images are processed using Tesseract OCR.
6. Extracted text is analyzed for engagement signals.
7. An engagement score and improvement suggestions are generated.
8. The extracted text and analysis results are displayed.

## Error Handling

The application handles:

- Missing uploads
- Unsupported file formats
- Files larger than 10 MB
- Invalid or corrupted PDFs
- Invalid or corrupted images
- OCR engine failures
- Files containing no readable text
- Unexpected processing errors

## Running Locally

### Clone the repository

```bash
git clone https://github.com/Ssunvya/social-media-content-analyzer.git
cd social-media-content-analyzer