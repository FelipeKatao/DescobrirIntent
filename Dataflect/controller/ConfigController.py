import os 
from config_generator import load_config_yaml, ensure_config_yaml
class ConfigController:
    def __init__(self):
        pass

    def GetAllConfigsYaml(self):
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Deteflect.yaml")
        config = ensure_config_yaml(config_path)
        return dict(config)