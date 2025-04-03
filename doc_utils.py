from ss3_classifier import ClassifierSS3

_classifier = ClassifierSS3()

def classify_document(text: str) -> str:
    return _classifier.classify(text)
