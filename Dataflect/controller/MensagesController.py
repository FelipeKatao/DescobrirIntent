from pipeline  import process_AI_data
from util.NormalizeText import NormalizeText
from project import Rule_data
import json

class MensagesController:
    def __init__(self):
        self.normalize = NormalizeText("")  
        self.MaxTry = 4
        self.tryAnalyze = 0
    def analyze(self,text):
        DataMemo = Rule_data.GetMemory(text)
        if DataMemo != None:
            return json.dumps({"Rule":DataMemo["action"]()})
        
        data = process_AI_data.analyze(NormalizeText(text).normalize())
        DetectRules = Rule_data.ResponseRule(data["MajorKeywords"],data["intent"])
        
        if DetectRules == None:
            self.analyze(text)
            self.tryAnalyze += 1
            if self.tryAnalyze <= self.MaxTry:
                return json.dumps({"Error":"I do know this, but you need to try again."})
        
        if DetectRules != None:
            return json.dumps({"Rule":DetectRules["action"]()})
        return json.dumps(data)
    
    