import yaml

class YamlParans():
    def __init__(self):
        pass

    def GetParans(self, path):
        with open(path, 'r') as file:
            return list(yaml.safe_load_all(file))
    def SetParans(self, path, parans):
        with open(path, 'w') as file:
            yaml.dump(parans, file)
    def AddParans(self, path, parans):
        with open(path, 'a') as file:
            yaml.dump(parans, file)