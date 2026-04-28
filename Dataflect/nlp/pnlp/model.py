import torch

class Modelpnlp:
    def __init__(self):
        self.Model = None
        self.ObjModel = None
        self.ListText = []
        self.StopWords = ["para"]
    def SetModel(self,model):
        self.Model = model
    def GetModel(self):
        self.objModel = torch.load(self.Model+".pt")
        return self.objModel
    def CreateModel(self):
        if self.Model:
            if self.ObjModel == None:
                self.ObjModel = {}
            torch.save(self.ObjModel,self.Model+".pt")
    def CreateToken(self,token,weight):
        if self.ObjModel == None:
            self.ObjModel = {}
        if self.Model:
            startToken = token[0]
            EndToken = token[-1]
            Count = len(token)
            id = 1 
            while(self.ObjModel.get(startToken+str(Count)+str(id)+EndToken)):
                id += 1
            self.ObjModel[startToken+str(Count)+str(id)+EndToken] = [weight,token]
            return startToken+str(Count)+str(id)+EndToken
    def SaveModel(self):
        if self.Model:
            torch.save(self.ObjModel,self.Model+".pt")
    def GetWord(self,position):
        for i in self.ListText:
            if len(i) <=3:
                self.ListText.remove(i)
        return self.ListText[int(position)]
    def ExtractTokens(self,text):
        self.ObjModelbjModel = {}
        start = True
        weight = 0
        self.ListText = str(text).split(" ")
        for i in self.ListText:

            if start:
               weight = 1 
               start = False    
            else:
                weight = 0.1
            if len(i) >=3:
                self.CreateToken(str(i).lower(),weight)
        return self.ObjModel


    def GetToken(self,word):
        self.Object = self.GetModel()
        id =0
        candidatos = []
        for key, values in self.Object.items():
            if key.startswith(word[0]): 
                candidatos.append([values, key]) 
        for i in candidatos:
            if i[0][1] == word:  
                return i
        return [[0.0,word],'_']  
    
    def ReturnVectorToken(self,text):
        List_ = []
        Bias = []
        for x in str(text).split(" "):
            if len(x) >3:
                List_.append(self.GetToken(x))
                if x != None:
                    Bias.append(self.GetToken(x)[1][0])
        return List_
    
    def ContextDataObject(self,text):
        List = [ ]
        index_pos = 0
        for i in text.split(" ")[1:]:
            value = index_pos
            if self.GetToken(i)[1] != "_":
                value+=0.1
            if len(i) >3 and i not in self.StopWords:
                List.append((i,value))
            index_pos +=0.1
        return List