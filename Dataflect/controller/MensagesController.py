from pipeline  import process_AI_data
import json

class MensagesController:
    def __init__(self):
        pass
    def analyze(self,text):
        data = process_AI_data.analyze(text)
        return json.dumps(data)