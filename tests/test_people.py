import json
import pytest
import mongomock

from app import app
from models.person import Person
from mongoengine import connect

@pytest.fixture
def client():
    app.config.update({"TESTING": True})

    with app.test_client() as client:
        connect('teste-tex', mongo_client_class=mongomock.MongoClient)
        yield client

def test_get_all_people(client):
    person_1 = Person(nome="João Vitor", idade=25)
    person_2 = Person(nome="José Antônio", idade=35)
    person_1.save()
    person_2.save()

    response = client.get('/api/people')
    resp = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert len(resp) == 2
    assert type(resp) is list
    assert type(resp[0]) is dict
    assert type(resp[1]) is dict
    assert resp[0]['nome'] == person_1.nome
    assert resp[1]['nome'] == person_2.nome

def test_create_new_person(client):
    data = {
        "nome": "Carlos Nascimento",
        "idade": 40
    }

    response = client.post('/api/people', json=data)
    resp = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 201
    assert type(resp) is dict
    assert resp['nome'] == data['nome']

def test_update_person_name(client):
    response = client.get('/api/people')
    resp = json.loads(response.data.decode('utf-8'))

    id = resp[0]['id']
    data = {'nome': 'João Pedro'}

    response = client.put(f'/api/people/{id}', json=data)
    resp = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert resp['nome'] == data['nome']

def test_update_person_age(client):
    response = client.get('/api/people')
    resp = json.loads(response.data.decode('utf-8'))

    id = resp[0]['id']
    data = {'idade': 23}

    response = client.put(f'/api/people/{id}', json=data)
    resp = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert resp['idade'] == data['idade']

def test_update_person(client):
    response = client.get('/api/people')
    resp = json.loads(response.data.decode('utf-8'))

    id = resp[0]['id']
    data = {'nome': 'João Pedro', 'idade': 23}

    response = client.put(f'/api/people/{id}', json=data)
    resp = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert resp['nome'] == data['nome']
    assert resp['idade'] == data['idade']

def test_delete_person(client):
    response = client.get('/api/people')
    resp = json.loads(response.data.decode('utf-8'))

    id = resp[0]['id']

    response = client.delete(f'/api/people/{id}')
    resp = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert id == resp['sucesso'].split()[1]
