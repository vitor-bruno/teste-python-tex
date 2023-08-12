from mongoengine import Document, StringField, connect

connect('teste-tex')

class Address(Document):
    bairro = StringField(required=True)
    cidade = StringField(required=True)
    uf = StringField(required=True)
    cep = StringField(required=True)
    logradouro = StringField(required=True)
    complemento = StringField()

    def to_dict(self):
        return {
            "id": str(self.id),
            "bairro": self.bairro,
            "cidade": self.cidade,
            "uf": self.uf,
            "cep": self.cep,
            "logradouro": self.logradouro,
            "complemento": self.complemento
        }
    
    def __str__(self):
        return f'{self.logradouro}, {self.bairro}, {self.cidade}/{self.uf} - CEP {self.cep}'