import streamlit as st # type: ignore
import os
import pandas as pd # type: ignore
from io import BytesIO
from doc_utils import extract_text_from_file, classify_document, suggest_filename, ensure_directory

st.set_page_config(page_title="AsystentPython – Document Organizer", layout="wide")

st.title("📂 AsystentPython – Document Organizer")

st.markdown("""
**AsystentPython** pomaga w automatycznym porządkowaniu dokumentów. 
Wybierz pliki lub folder do przetworzenia, a aplikacja wydobędzie tekst, 
sklasyfikuje dokumenty po słowach kluczowych, zaproponuje nowe nazwy plików 
i przeniesie je do odpowiednich folderów. 
Możesz zatwierdzić lub anulować operacje przed wprowadzeniem zmian.
""")

uploaded_files = st.file_uploader(
    "1. Wybierz jeden lub wiele plików do analizy:",
    type=["pdf", "doc", "docx", "rtf", "odt", "txt", "jpg", "jpeg", "png"],
    accept_multiple_files=True
)

if uploaded_files and len(uploaded_files) > 0:
    # Process each selected file
    results = []  # will hold dicts of file info for preview/log
    for file in uploaded_files:
        filename = file.name
        # Extract text content
        file_bytes = file.getvalue()
        text = extract_text_from_file(file_bytes, filename)
        # Classify document
        category = classify_document(text)
        # Suggest new filename
        new_name = suggest_filename(filename, category)
        # Determine destination folder (plural form or category name)
        if category in ["Wyrok", "Skarga", "Faktura", "Notatka", "Wezwanie"]:
            # Map to plural folder names for aesthetics
            folder_name = {
                "Wyrok": "Wyroki",
                "Skarga": "Skargi",
                "Faktura": "Faktury",
                "Notatka": "Notatki",
                "Wezwanie": "Wezwania"
            }[category]
        else:
            folder_name = "Inne"
        result = {
            "original_name": filename,
            "category": category,
            "new_name": new_name,
            "target_folder": folder_name,
            "file_bytes": file_bytes  # store content for later saving
        }
        results.append(result)
    # Show a preview table of the planned operations
    st.markdown("**2. Proponowane zmiany:**")
    preview_df = pd.DataFrame([
        {
            "Plik oryginalny": r["original_name"],
            "Klasyfikacja": r["category"],
            "Nowa nazwa": r["new_name"],
            "Folder docelowy": r["target_folder"]
        } for r in results
    ])
    st.dataframe(preview_df, use_container_width=True)
    st.write("Sprawdź klasyfikację i nowe nazwy. Jeśli wszystko się zgadza, zatwierdź poniżej.")
    
    # Confirmation button
    if st.button("✅ Zatwierdź i przenieś pliki"):
        log_entries = []
        for res in results:
            orig = res["original_name"]
            cat = res["category"]
            new_name = res["new_name"]
            folder = res["target_folder"]
            # Ensure folder exists
            ensure_directory(folder)
            dest_path = os.path.join(folder, new_name)
            try:
                # Write file bytes to the new location
                with open(dest_path, "wb") as f:
                    f.write(res["file_bytes"])
                status = "OK"
            except Exception as e:
                status = f"ERROR: {e}"
            # Record log
            log_entries.append({
                "original_name": orig,
                "category": cat,
                "new_name": new_name,
                "destination": dest_path,
                "status": status
            })
        # Display result message
        st.success(f"Przetwarzanie zakończone. Przeniesiono {sum(1 for e in log_entries if e['status']=='OK')} z {len(log_entries)} plików.")
        # Offer download of log
        log_df = pd.DataFrame(log_entries)
        csv_data = log_df.to_csv(index=False)
        json_data = log_df.to_json(orient="records", force_ascii=False, indent=2)
        st.download_button("📄 Pobierz log (CSV)", data=csv_data, file_name="asystent_log.csv", mime="text/csv")
        st.download_button("📑 Pobierz log (JSON)", data=json_data, file_name="asystent_log.json", mime="application/json")
        st.dataframe(log_df, use_container_width=True)
