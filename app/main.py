from flask import Flask, jsonify, request
from models import Person, Address
from mongoengine.errors import FieldDoesNotExist
from xml.etree import ElementTree
import requests


app = Flask(__name__)


@app.route("/people", methods=["GET"])
def get_all_people():
    people = Person.objects

    return jsonify([p.to_dict() for p in people]), 200


@app.route("/people", methods=["POST"])
def create_new_person():
    try:
        data = request.get_json()

        person = Person(**data)
        person.save()

        return jsonify(person.to_dict()), 201
    
    except FieldDoesNotExist:
        return jsonify({'erro': 'verifique o corpo da requisição'}), 400


@app.route("/people/<id>", methods=["PUT"])
def update_person(id):
    try:
        if len(id) != 24:
            return jsonify({'erro': 'id inválido'}), 400

        person = Person.objects(id=id).first()
        
        if person:
            data = request.get_json()
            data["id"] = id

            person.modify(**data)

            return jsonify(person.to_dict()), 200

        else:
            return jsonify({'erro': 'pessoa não encontrada'}), 404
    
    except FieldDoesNotExist:
        return jsonify({'erro': 'verifique o corpo da requisição'}), 400


@app.route("/people/<id>", methods=["DELETE"])
def delete_person(id):
    if len(id) != 24:
        return jsonify({'erro': 'id inválido'}), 400

    person = Person.objects(id=id).first()
    
    if person:
        person.delete()
    else:
        return jsonify({'erro': 'pessoa não encontrada'}), 404

    return jsonify({'sucesso': 'pessoa deletada com sucesso'})


@app.route("/addresses", methods=["GET"])
def get_address():
    cep = request.args.get('cep')

    if not cep:
        return jsonify({'erro': 'insira o parâmetro CEP na requisição'}), 400
    
    response = requests.get(f"https://viacep.com.br/ws/{cep}/xml/")
    
    if response.status_code == 400:
        return jsonify({'erro': 'CEP inválido'}), 400
    
    tree = ElementTree.fromstring(response.content)
    
    if tree[0].tag == 'erro':
        return jsonify({'erro': 'CEP não localizado'}), 400
    
    address_dict = {
        'cep': tree[0].text,
        'logradouro': tree[1].text,
        'complemento': tree[2].text or '',
        'bairro': tree[3].text,
        'cidade': tree[4].text,
        'uf': tree[5].text
    }

    address_obj = Address(**address_dict)
    address_obj.save()

    return jsonify({
        'sucesso': True,
        'endereco': {
            'cep': address_obj.cep,
            'logr': address_obj.logradouro,
            'compl': address_obj.complemento,
            'bairro': address_obj.bairro,
            'cidade': address_obj.cidade,
            'uf': address_obj.uf
        }
    })


app.run(debug=True)