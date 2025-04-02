import os, io, re, shutil, fitz
from datetime import datetime
from io import BytesIO
from striprtf.striprtf import rtf_to_text
from PIL import Image
import pytesseract
from pdf2image import convert_from_bytes
import docx  # python-docx

# Define keywords for classification
CATEGORY_KEYWORDS = {
    "Wyrok": ["wyrok", "sad ", "sąd", "trybunał"],       # includes lowercase "sad" to catch "Sąd" (Polish diacritic)
    "Skarga": ["skarga", "skar\u017C\u0105", "za\u017Cal"],  # using Unicode escapes for "skarżą" and "zażal"
    "Faktura": ["faktura", "vat", "nip", "invoice"],
    "Notatka": ["notatka", "memo", "protoko\u0142"],     # "protokół" (protocol can be similar to a note)
    "Wezwanie": ["wezwanie", "stawiennictwo", "stawi\u0107"]
}
# (The Unicode escapes ensure characters like ż, ó are handled in source; we will lowercase input text without diacritics issue.)

def extract_text_from_file(file_bytes: bytes, filename: str) -> str:
    """Extract text content from a file given its bytes and name (for extension)."""
    # Determine file extension in lower case
    name_lower = filename.lower()
    text = ""
    if name_lower.endswith(".pdf"):
        # Use PyMuPDF to extract text from PDF
        try:
            doc = fitz.open(stream=file_bytes, filetype="pdf")
        except Exception as e:
            # If file is encrypted or cannot open, return empty text
            return ""
        for page in doc:
            text += page.get_text()
        doc.close()
        # If no text found, perhaps a scanned PDF – use OCR
        if text.strip() == "":
            try:
                images = convert_from_bytes(file_bytes)
            except Exception as e:
                return ""  # pdf2image failed (poppler not installed or other issue)
            ocr_text = []
            for img in images:
                # Convert each page image to string
                try:
                    page_text = pytesseract.image_to_string(img)
                except Exception as oe:
                    page_text = ""
                ocr_text.append(page_text)
            text = "\n".join(ocr_text)
    elif name_lower.endswith(".docx") or name_lower.endswith(".doc"):
        # Use python-docx for .docx; .doc needs conversion (not handled fully here)
        try:
            doc = docx.Document(io.BytesIO(file_bytes))
        except Exception as e:
            text = ""
        else:
            full_text = [para.text for para in doc.paragraphs]
            text = "\n".join(full_text)
    elif name_lower.endswith(".rtf"):
        # Decode RTF (assuming CP1252 or utf-8)
        try:
            rtf_content = file_bytes.decode('cp1252', errors='ignore')
        except UnicodeDecodeError:
            rtf_content = file_bytes.decode('utf-8', errors='ignore')
        text = rtf_to_text(rtf_content)
    elif name_lower.endswith(".odt"):
        # Open ODT as a zip and extract text from content.xml
        try:
            import zipfile
            with zipfile.ZipFile(BytesIO(file_bytes)) as z:
                xml_content = z.read('content.xml').decode('utf-8', errors='ignore')
            # Remove XML tags to get raw text
            text = re.sub('<[^>]+>', ' ', xml_content)
        except Exception as e:
            text = ""
    elif name_lower.endswith(".txt"):
        # Decode plain text
        try:
            text = file_bytes.decode('utf-8')
        except UnicodeDecodeError:
            text = file_bytes.decode('cp1252', errors='ignore')
    else:
        # If it's an image (jpg, png, etc.) or unknown, attempt OCR as last resort
        try:
            img = Image.open(BytesIO(file_bytes))
        except Exception:
            text = ""
        else:
            try:
                text = pytesseract.image_to_string(img)
            except Exception:
                text = ""
    return text

def classify_document(text: str) -> str:
    """Classify document text into a category based on keywords. Returns the category name (or 'Inne' if unknown)."""
    if text is None:
        return "Inne"
    text_lower = text.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        for kw in keywords:
            if kw in text_lower:
                return category
    return "Inne"

def suggest_filename(original_name: str, category: str) -> str:
    """Generate a new filename based on current date, category, and original name."""
    date_str = datetime.now().strftime("%Y-%m-%d")
    base_name, ext = os.path.splitext(original_name)
    # Sanitize base name: remove or replace spaces and special chars
    safe_base = re.sub(r'[^A-Za-z0-9_\-]+', '_', base_name).strip('_')
    if not safe_base:
        safe_base = "dokument"
    # Avoid repeating category in name if already present (case-insensitive)
    if category and category.lower() in safe_base.lower():
        extra = safe_base  # already contains category info
    else:
        extra = safe_base
    new_name = f"{date_str}_{category}"
    if extra:
        new_name += f"_{extra}"
    new_name += ext.lower()
    return new_name

def ensure_directory(path: str):
    """Create directory if it doesn't exist."""
    os.makedirs(path, exist_ok=True)
