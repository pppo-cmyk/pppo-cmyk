
from ss3_classifier import ClassifierSS3

classifier = ClassifierSS3(model_path="asystent_model.pyss3")

def classify_document(text: str) -> str:
    return classifier.classify(text)
