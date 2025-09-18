import requests

class AutoCompleteITBI:
    def __init__(self, cep: str):
        self.URL = "https://viacep.com.br/ws/"
        self.cep = cep.replace("-", "").strip()
        if len(self.cep) == 7:
            self.cep = "0" + self.cep

    def get_data(self):
        if len(self.cep) != 8 or not self.cep.isdigit():
            return None
        resp = requests.get(f"{self.URL}{self.cep}/json/")
        if resp.status_code == 200:
            data = resp.json()
            if "erro" in data:
                return None
            return data
        return None