import requests

class AutoCompleteITBI:
    def __init__(self, cep:str):
        self.URL = "https://viacep.com.br/ws/"
        self.cep = cep
        self.cep = self.cep.split("-")
        self.cep = "".join(self.cep)
        if self.cep[0] != "0":
            self.cep  = "0" + self.cep
        if len(self.cep) != 8:
            return None
        
    def get_data(self):
        URL = self.URL + self.cep + "/json/"
        resp = requests.get(URL)
        return resp.json()