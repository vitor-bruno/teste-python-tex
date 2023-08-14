# Teste Python/MongoDB - TEx

Projeto desenvolvido como parte do processo seletivo para a empresa TEx.

Trata-se de uma API com endpoints para consulta de CEP e cadastro de pessoas.

Bibliotecas utilizadas:
1. Flask - desenvolvimento de rotas da API.
2. mongoengine - interação com banco de dados MongoDB.
3. requests - comunicação com serviço externo para busca de CEP.
4. pytest e mongomock - testes.

Estrutura do projeto:
```
.
├── models
│   ├── __init__.py
│   ├── address.py
│   └── person.py
├── routes
│   ├── __init__.py
│   ├── addresses.py
│   └── people.py
├── tests
│   ├── __init__.py
│   ├── test_addresses.py
│   └── test_people.py
├── .gitignore
├── app.py
├── docker-compose.yml
├── Dockerfile
├── README.md
└── requirements.txt
```

* /modelos - definição das entidades do banco.
* /routes - definição de rotas da API.
* /tests - testes unitários.
* app.py - arquivo de inicialização da aplicação.

## Rodando o projeto 

1. Clone o repositório.
2. Com o Docker rodando, navegue até a pasta do projeto e digite:
```sh
docker-compose up
```

## Utilização
### Endpoints - Cadastramento de pessoas
GET http://127.0.0.1:5000/api/pessoas

RESPONSE
```json
[
    {
        "id": "64d7f537b5e9c60846650174",
        "idade": 26,
        "nome": "João Pedro"
    },
    {
        "id": "64d7f56eb5e9c60846650175",
        "idade": 40,
        "nome": "Antônio Silva"
    }
]
```

POST http://127.0.0.1:5000/api/pessoas

REQUEST
```json
{
    "nome": "José Miranda",
    "idade": 31
}
```
RESPONSE
```json
{
    "id": "64d7f5f1b5e9c60846650177",
    "idade": 31,
    "nome": "José Miranda"
}
```

PUT http://127.0.0.1:5000/api/pessoas/64d7f5f1b5e9c60846650177

REQUEST (corpo pode conter apenas nome, apenas idade ou ambos)
```json
{
    "nome": "José Alvarez",
    "idade": 35
}
```
RESPONSE
```json
{
    "id": "64d7f5f1b5e9c60846650177",
    "idade": 35,
    "nome": "José Alvarez"
}
```

DELETE http://127.0.0.1:5000/api/pessoas/64d7f5f1b5e9c60846650177

RESPONSE
```json
{
    "sucesso": "José Alvarez deletado(a) com sucesso"
}
```

### Endpoint - Busca de CEP
GET http://127.0.0.1:5000/api/addresses?cep=03113010

RESPONSE
```json
{
    "endereco": {
        "bairro": "Mooca",
        "cep": "03113-010",
        "cidade": "São Paulo",
        "compl": "",
        "logr": "Rua Canuto Saraiva",
        "uf": "SP"
    },
    "sucesso": true
}
```

## Rodando os testes 

```sh
pytest
```