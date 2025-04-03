
from summa.summarizer import summarize

def summarize_text(text, ratio=0.1):
    try:
        summary = summarize(text, language="polish", ratio=ratio)
        return summary if summary else "Brak podsumowania (za krótki tekst)"
    except Exception as e:
        return f"Błąd podsumowania: {str(e)}"
