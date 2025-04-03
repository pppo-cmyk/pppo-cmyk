
import streamlit as st
from doc_utils import classify_document
from summarizer import summarize_text
from editor_suggestions import get_suggestions
from ocr_utils import extract_text_tesseract
import os

st.set_page_config(page_title="Asystent Python SS3", layout="wide")

st.title("AsystentPythonSS3: Inteligentna analiza dokumentów")

uploaded_file = st.file_uploader("Wybierz plik PDF lub obraz", type=["pdf", "png", "jpg", "jpeg"])
if uploaded_file:
    with open("temp_input", "wb") as f:
        f.write(uploaded_file.read())

    text = extract_text_tesseract("temp_input")
    st.subheader("Tekst dokumentu:")
    st.text_area("Zawartość", text, height=200)

    doc_type = classify_document(text)
    st.success(f"**Rodzaj dokumentu:** {doc_type}")

    summary = summarize_text(text)
    st.info(f"**Podsumowanie:**\n{summary}")

    suggestions = get_suggestions(text)
    st.warning("**Sugestie edytorskie:**")
    for s in suggestions:
        st.markdown(f"- {s}")
