import json
import pytest
import mongomock

from app import app
from models.address import Address
from mongoengine import connect

@pytest.fixture
def client():
    app.config.update({"TESTING": True})

    with app.test_client() as client:
        connect('teste-tex', mongo_client_class=mongomock.MongoClient)
        yield client

def test_get_valid_address(client):
    response = client.get('/api/addresses', query_string={"cep": "03113010"})
    resp = json.loads(response.data.decode('utf-8'))

    address_obj = Address.objects(cep=resp['endereco']['cep'])

    assert response.status_code == 200
    assert address_obj is not None

def test_get_invalid_address(client):
    response = client.get('/api/addresses', query_string={"cep": "123456789"})

    assert response.status_code == 400

def test_get_not_existing_address(client):
    response = client.get('/api/addresses', query_string={"cep": "12345678"})

    assert response.status_code == 404