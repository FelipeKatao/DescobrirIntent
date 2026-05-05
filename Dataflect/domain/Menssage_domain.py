from nlp.nlp_domain.npl_run import App

class MessagesDomain():
    def __init__(self) -> None:
        self.appNpl = App()
    def ResponseDataDomain(self,text):
        return self.appNpl.run("2",text)