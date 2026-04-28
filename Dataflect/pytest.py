from nlp.pnlp.model import Modelpnlp
from nlp.pnlp.ProcessModel import ProcessModel

v = Modelpnlp()
z = ProcessModel()
v.SetModel("./nlp/model/test")


v.GetModel()
# texto =  "gerar relatorio financeiro vendas mes fevereiro valor total 15890"
texto =  "registrar chamado suporte servidor banco dados indisponivel prioridade alta"
#texto =  "deletar usuario admin acesso sistema bloqueado tentativa invasao"
# texto = "criar um login para o usuario Sergio com a senha 2354"

Relevance_obj = z.ReturnRelevanceWords(v.ReturnVectorToken(texto),v.GetModel())
Relevance_props = texto.split(" ")
Relevance_props = [
    i for i in Relevance_props
    if i not in Relevance_obj
]
print(Relevance_props)   # Ação
print(Relevance_obj)     # Contexto 

# Detectar Contexto Objeto
Return_Context = {
    "Ação_contexto": None,
    "Objetos": None,
    "entidades": [],
    "Complemento": None,
    "Complemento_valor": None
}
tokens = v.ContextDataObject(texto)
List_update = []
for i in tokens:
    print(i)

prev_peso = None

for posicao, (palavra, peso) in enumerate(tokens):
    if len(palavra) < 4:
        continue
    # 1) primeiro token = ação
    if posicao == 0:
        Return_Context["Ação_contexto"] = palavra
        prev_peso = peso
        continue
    if len(palavra) > 4:
        delta = peso - prev_peso

    # 2) segundo token = objeto
    if posicao == 1:
        Return_Context["Objetos"] = palavra

    # 3) pequena variação → entidade
    elif delta <= 0.15:
        Return_Context["entidades"].append(palavra)

    # 4) variação média → complemento
    elif delta <= 0.3:
        Return_Context["Complemento"] = palavra

    # 5) variação grande → valor
    else:
        Return_Context["Complemento_valor"] = palavra
    if len(palavra) > 4:
        prev_peso = peso


print(Return_Context)
