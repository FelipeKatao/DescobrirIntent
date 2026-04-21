from rules.RulesUser import RulesSintaxe
Rule_data = RulesSintaxe()

#Your data project here, all rules of your project added here
list_mercado = ["pera, maca, banana,limao"]

def Mostrar_list():
    return  f" Esses são os itens que preciso comprar no mercado {list_mercado}"

Rule_data.NewRule(("comprar","produtos"),"READ",Mostrar_list)
Rule_data.NewRule(("compras","produtos"),"READ",Mostrar_list)


