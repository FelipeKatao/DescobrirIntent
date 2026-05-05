import json
from services.MensageService import MensageService

class MensagesController:
    def __init__(self) -> None:
        self.ServiceMen = MensageService()
    def ReturnResponse(self,Text):
        return self.ServiceMen.ReturnMensage(Text)