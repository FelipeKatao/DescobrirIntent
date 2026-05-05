import os
from .npl_processor import NLPProcessor, MODEL_PATH


class App:
    def __init__(self):
        self.processor = NLPProcessor()

    def run(self,type,text):
        print("=== NLP SYSTEM V2 ===")
        print("1 - Treinar")
        print("2 - Usar")

        mode = type

        if mode == "1":
            print("Treinando...")
            self.processor = NLPProcessor(True)
            self.processor.train()
            print("OK")

        elif mode == "2":
            if not os.path.exists(MODEL_PATH):
                print("Treine primeiro")
                return

            self.processor.load()
            print(self.processor.predict(text))

