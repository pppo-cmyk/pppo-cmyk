
import os
import shutil
import csv
from doc_utils import classify_document
from summarizer import summarize_text
from editor_suggestions import get_suggestions
from ocr_utils import extract_text_tesseract

def process_documents(input_dir, output_dir, csv_report):
    os.makedirs(output_dir, exist_ok=True)
    with open(csv_report, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Plik", "Typ", "Podsumowanie", "Sugestie"])
        for filename in os.listdir(input_dir):
            path = os.path.join(input_dir, filename)
            try:
                text = extract_text_tesseract(path)
                doc_type = classify_document(text)
                summary = summarize_text(text)
                suggestions = get_suggestions(text)
                type_folder = os.path.join(output_dir, doc_type)
                os.makedirs(type_folder, exist_ok=True)
                shutil.copy2(path, os.path.join(type_folder, filename))
                writer.writerow([filename, doc_type, summary, " | ".join(suggestions)])
            except Exception as e:
                writer.writerow([filename, "BŁĄD", "", str(e)])
