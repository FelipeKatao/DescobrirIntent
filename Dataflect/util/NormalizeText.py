import re

class NormalizeText:
    def __init__(self,text):
        self.text  = str(text)

    def normalize(self):
        text = self.text.lower()

        text = re.sub(
            r'[^\w\s]',
            '',
            text
        )

        text = re.sub(
            r'\s+',
            ' ',
            text
        )

        return text.strip()