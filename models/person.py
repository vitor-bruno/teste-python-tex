from mongoengine import Document, StringField, IntField, connect


class Person(Document):
    nome = StringField(required=True)
    idade = IntField(required=True)

    def to_dict(self):
        return {
            "id": str(self.id),
            "nome": self.nome,
            "idade": self.idade
        }
    
    def __str__(self):
        return f'{self.nome} - {self.idade} anos'