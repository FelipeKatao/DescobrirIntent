from domain.Menssage_domain import MessagesDomain

class MensageService:
    def __init__(self) -> None:
        self.domain = MessagesDomain()

    def ReturnMensage(self,text):
        if text !="":
            return self.domain.ResponseDataDomain(text)