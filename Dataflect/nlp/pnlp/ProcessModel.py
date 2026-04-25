

class ProcessModel:
    def __init__(self):
        pass
    def ProcessModel(self,Model,TokenText):
        position = 1
        BiasToken = []
        for i in TokenText:
            Divide = len(TokenText) / position
            Minus = Divide - 1
            position += 1
            BiasToken.append(Minus)
        return BiasToken
    
    def Qualification(self,BiasToken):
        BiasToken.pop(0)
        avg= len(BiasToken)/2
        q = []
        for i in BiasToken:
            if i <= 1.1 and i > 0:
                q.append(i)
            else:
                q.append("_")
        return q
    
    def ReturnRelevanceWords(self,text,model):
      listBias = []
      for x in text:
          listBias.append(text[0][0])
      pos = []
      List_ = []
      x =0
      for i in self.Qualification(self.ProcessModel(model,listBias)):
          if i != "_":
              pos.append(text[x][0][1]) 
          x+=1
      return pos