
from nlp.nlp_domain.npl_run import App
from util.yamlParans import YamlParans
p = App()
v = YamlParans()
print(v.GetParans("Deteflect.yaml"))
#print(p.run("2","Inserir novo cliente nome guilherme idade 23"))