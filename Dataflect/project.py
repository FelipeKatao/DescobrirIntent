from rules.RulesUser import RulesSintaxe
Rule_data = RulesSintaxe()

Rule_data.AddIntents({"cadastrar processo":"JURI_PROCESSO"},("process","JURI_PROCESSO"))

#Your data project here, all rules of your project added here
list_mercado = ["pera, maca, banana,limao"]

def Mostrar_list():
    return  f" Esses são os itens que preciso comprar no mercado {list_mercado}"

def FeedBackNegativo():
    return f"Obrigado pelo feedback negativo, vamos melhorar"

def RemoverItem():
    list_mercado.remove("pera")

Rule_data.NewRule(("comprar","produtos"),"READ",Mostrar_list)
Rule_data.NewRule(("compras","produtos"),"READ",Mostrar_list)
Rule_data.NewRule(("consultar","feedback"),"READ",FeedBackNegativo,"NEGATIVE")


