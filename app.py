from flask import Flask, render_template, request
import os
import uuid

import pymupdf
import pytesseract
from PIL import Image


app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10 MB

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ---------------------------------------------------------
# TESSERACT CONFIGURATION
# ---------------------------------------------------------
# On Windows, use the normal Tesseract installation path.
# On Render/Linux, Tesseract is normally available as:
# /usr/bin/tesseract

if os.name == "nt":
    windows_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    if os.path.exists(windows_tesseract):
        pytesseract.pytesseract.tesseract_cmd = windows_tesseract
else:
    # Linux / Render
    pytesseract.pytesseract.tesseract_cmd = "tesseract"


# ---------------------------------------------------------
# FILE VALIDATION
# ---------------------------------------------------------
def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


# ---------------------------------------------------------
# CONTENT ANALYSIS
# ---------------------------------------------------------
def analyze_content(text):
    """Generate simple social-media engagement metrics."""

    words = text.split()

    word_count = len(words)
    character_count = len(text)

    hashtag_count = text.count("#")
    mention_count = text.count("@")
    question_count = text.count("?")

    cta_keywords = [
        "comment",
        "share",
        "follow",
        "subscribe",
        "click",
        "visit",
        "buy",
        "learn more",
        "sign up",
        "download",
        "contact us",
        "let us know",
    ]

    text_lower = text.lower()

    cta_detected = any(
        keyword in text_lower
        for keyword in cta_keywords
    )

    # -----------------------------------------------------
    # ENGAGEMENT SCORE
    # -----------------------------------------------------
    score = 0

    if question_count > 0:
        score += 15

    if hashtag_count > 0:
        score += 15

    if mention_count > 0:
        score += 10

    if cta_detected:
        score += 25

    if word_count <= 300:
        score += 20
    elif word_count <= 1000:
        score += 15
    elif word_count <= 2000:
        score += 10
    else:
        score += 5

    if len(text.splitlines()) >= 3:
        score += 10

    score = min(score, 100)

    # -----------------------------------------------------
    # SUGGESTIONS
    # -----------------------------------------------------
    suggestions = []

    if hashtag_count == 0:
        suggestions.append("Add relevant hashtags.")

    if question_count == 0:
        suggestions.append(
            "Ask an audience-focused question."
        )

    if not cta_detected:
        suggestions.append(
            "Add a clear call-to-action."
        )

    if word_count > 1000:
        suggestions.append(
            "Break long sections into shorter paragraphs."
        )

    if word_count > 300:
        suggestions.append(
            "Use a stronger opening hook to capture attention."
        )

    if not suggestions:
        suggestions.append(
            "Your content has a good engagement structure."
        )

    return {
        "word_count": word_count,
        "character_count": character_count,
        "hashtag_count": hashtag_count,
        "mention_count": mention_count,
        "question_count": question_count,
        "cta_detected": cta_detected,
        "engagement_score": score,
        "suggestions": suggestions,
    }


# ---------------------------------------------------------
# PDF TEXT EXTRACTION
# ---------------------------------------------------------
def extract_text_from_pdf(filepath):
    """
    Extract selectable text from a PDF.

    If the PDF contains no selectable text,
    render each page as an image and use OCR.
    """

    document = pymupdf.open(filepath)

    try:
        if document.page_count == 0:
            return ""

        # ---------------------------------------------
        # FIRST: NORMAL PDF TEXT EXTRACTION
        # ---------------------------------------------
        text_parts = []

        for page in document:
            page_text = page.get_text()
            if page_text:
                text_parts.append(page_text)

        text = "\n\n".join(text_parts).strip()

        # ---------------------------------------------
        # SECOND: OCR FOR SCANNED PDF
        # ---------------------------------------------
        if not text:

            ocr_parts = []

            for page in document:

                pix = page.get_pixmap(
                    matrix=pymupdf.Matrix(2, 2),
                    alpha=False
                )

                image = Image.frombytes(
                    "RGB",
                    [pix.width, pix.height],
                    pix.samples
                )

                try:
                    page_text = pytesseract.image_to_string(
                        image,
                        lang="eng"
                    )

                    if page_text:
                        ocr_parts.append(page_text)

                finally:
                    image.close()

            text = "\n\n".join(ocr_parts).strip()

        return text

    finally:
        document.close()


# ---------------------------------------------------------
# IMAGE OCR
# ---------------------------------------------------------
def extract_text_from_image(filepath):
    """Extract text from PNG/JPG/JPEG using Tesseract OCR."""

    image = Image.open(filepath)

    try:
        # Verify image integrity
        image.verify()

    except Exception as e:
        raise ValueError(
            "The uploaded image is corrupted or invalid."
        ) from e

    finally:
        image.close()

    # Reopen image after verify()
    image = Image.open(filepath)

    try:
        # Convert to RGB for reliable OCR
        if image.mode != "RGB":
            image = image.convert("RGB")

        text = pytesseract.image_to_string(
            image,
            lang="eng"
        )

        return text.strip()

    finally:
        image.close()


# ---------------------------------------------------------
# FILE TOO LARGE
# ---------------------------------------------------------
@app.errorhandler(413)
def file_too_large(error):

    return render_template(
        "index.html",
        error="File is too large. Maximum allowed size is 10 MB.",
        extracted_text="",
        analysis=None
    ), 413


# ---------------------------------------------------------
# MAIN ROUTE
# ---------------------------------------------------------
@app.route("/", methods=["GET", "POST"])
def home():

    extracted_text = ""
    error = ""
    analysis = None

    if request.method == "POST":

        # ---------------------------------------------
        # 1. Check file field
        # ---------------------------------------------
        if "file" not in request.files:

            error = "No file was uploaded."

            return render_template(
                "index.html",
                error=error,
                extracted_text="",
                analysis=None
            )

        file = request.files["file"]

        # ---------------------------------------------
        # 2. Check filename
        # ---------------------------------------------
        if not file.filename:

            error = (
                "Please select a file before clicking "
                "Analyze Content."
            )

            return render_template(
                "index.html",
                error=error,
                extracted_text="",
                analysis=None
            )

        # ---------------------------------------------
        # 3. Check extension
        # ---------------------------------------------
        if not allowed_file(file.filename):

            error = (
                "Unsupported file type. "
                "Please upload PDF, PNG, JPG or JPEG."
            )

            return render_template(
                "index.html",
                error=error,
                extracted_text="",
                analysis=None
            )

        # ---------------------------------------------
        # 4. Generate safe unique filename
        # ---------------------------------------------
        extension = file.filename.rsplit(
            ".", 1
        )[1].lower()

        safe_filename = (
            f"{uuid.uuid4().hex}.{extension}"
        )

        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            safe_filename
        )

        try:

            # -----------------------------------------
            # 5. Save uploaded file
            # -----------------------------------------
            file.save(filepath)

            if not os.path.exists(filepath):

                raise IOError(
                    "Uploaded file could not be saved."
                )

            # -----------------------------------------
            # 6. Extract text
            # -----------------------------------------
            if extension == "pdf":

                extracted_text = extract_text_from_pdf(
                    filepath
                )

            else:

                extracted_text = extract_text_from_image(
                    filepath
                )

            # -----------------------------------------
            # 7. Check extracted text
            # -----------------------------------------
            if not extracted_text.strip():

                error = (
                    "No readable text was detected. "
                    "Please upload a clearer document or image."
                )

                return render_template(
                    "index.html",
                    error=error,
                    extracted_text="",
                    analysis=None
                )

            # -----------------------------------------
            # 8. Analyze content
            # -----------------------------------------
            analysis = analyze_content(
                extracted_text
            )

        except pymupdf.FileDataError:

            error = (
                "The PDF appears to be corrupted or invalid. "
                "Please upload a valid PDF file."
            )

        except pytesseract.TesseractNotFoundError:

            error = (
                "OCR engine is not available on the server. "
                "Please contact the administrator."
            )

            print(
                "Tesseract executable was not found."
            )

        except ValueError as e:

            error = str(e)

        except Exception as e:

            error = (
                "Could not process the uploaded file. "
                "Please check the file and try again."
            )

            print(
                "Processing error:",
                repr(e)
            )

        finally:

            # -----------------------------------------
            # 9. Delete temporary uploaded file
            # -----------------------------------------
            if os.path.exists(filepath):

                try:
                    os.remove(filepath)

                except Exception as cleanup_error:

                    print(
                        "Cleanup error:",
                        repr(cleanup_error)
                    )

    return render_template(
        "index.html",
        extracted_text=extracted_text,
        error=error,
        analysis=analysis
    )


# ---------------------------------------------------------
# LOCAL DEVELOPMENT
# ---------------------------------------------------------
if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )