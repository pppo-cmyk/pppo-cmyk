
import pytesseract
import easyocr
from pdf2image import convert_from_path
from PIL import Image
import os

def extract_text_tesseract(file_path, lang="pol"):
    if file_path.lower().endswith(".pdf"):
        images = convert_from_path(file_path)
        text = ""
        for i, img in enumerate(images):
            text += pytesseract.image_to_string(img, lang=lang)
        return text
    else:
        image = Image.open(file_path)
        return pytesseract.image_to_string(image, lang=lang)

def extract_text_easyocr(file_path, lang="pl"):
    reader = easyocr.Reader([lang])
    results = reader.readtext(file_path, detail=0, paragraph=True)
    return "\n".join(results)
