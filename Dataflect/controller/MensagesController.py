from pipeline  import process_AI_data
from util.NormalizeText import NormalizeText
import json

class MensagesController:
    def __init__(self):
        self.normalize = NormalizeText("")  
    def analyze(self,text):
        data = process_AI_data.analyze(NormalizeText(text).normalize())
        return json.dumps(data)