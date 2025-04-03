
from pyss3 import SS3
import os

class ClassifierSS3:
    def __init__(self, model_path="asystent_model.pyss3"):
        self.model_path = model_path
        self.model = SS3()
        if os.path.exists(self.model_path):
            self.model.load_model(self.model_path)
        else:
            print("Model nie został znaleziony.")

    def classify(self, text: str) -> str:
        return self.model.classify(text)
