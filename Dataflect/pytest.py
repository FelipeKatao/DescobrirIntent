from nlp.pnlp.model import Modelpnlp
from nlp.pnlp.ProcessModel import ProcessModel

v = Modelpnlp()
z = ProcessModel()
v.SetModel("./nlp/model/test")


v.GetModel()
texto =  "gerar relatorio financeiro vendas mes fevereiro valor total 15890"
Relevance_obj = z.ReturnRelevanceWords(v.ReturnVectorToken(texto),v.GetModel())
Relevance_props = texto.split(" ")
Relevance_props = [
    i for i in Relevance_props
    if i not in Relevance_obj
]
print(Relevance_props)   # Ação
print(Relevance_obj)     # Contexto 

print("Eu posso " + str(Relevance_props[0])+" "+str(Relevance_props[1]) + " para " + str(Relevance_obj[1])+" "+str(Relevance_obj[2]))