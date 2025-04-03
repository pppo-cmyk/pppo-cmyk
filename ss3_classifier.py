from pyss3 import SS3
import os

class ClassifierSS3:
    def __init__(self, model_path="asystent_model", categories=None):
        self.model_path = model_path
        self.model = SS3()
        self.categories = categories or ["Wyrok", "Postanowienie", "Skarga", "Wezwanie", "Pełnomocnictwo", "Faktura", "Pismo"]

        if os.path.exists(f"{model_path}.pyss3"):
            self.model.load_model(model_path)
        else:
            self.model.configure(alpha=0.5, smooth=False, use_idf=True)

    def train(self, examples: dict):
        x_train, y_train = [], []
        for label, texts in examples.items():
            for t in texts:
                x_train.append(t)
                y_train.append(label)

        self.model.train(x_train, y_train)
        self.model.save_model(self.model_path)

    def classify(self, text: str) -> str:
        return self.model.classify(text)
