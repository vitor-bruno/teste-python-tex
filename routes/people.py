from flask import Blueprint, request, jsonify
from models.person import Person
from mongoengine.errors import FieldDoesNotExist, ValidationError


people_blueprint = Blueprint('people', __name__)


@people_blueprint.route("", methods=["GET"])
def get_all_people():
    people = Person.objects

    return jsonify([p.to_dict() for p in people]), 200


@people_blueprint.route("", methods=["POST"])
def create_new_person():
    try:
        data = request.get_json()

        person = Person(**data)
        person.save()

        return jsonify(person.to_dict()), 201
    
    except (FieldDoesNotExist, ValidationError):
        return jsonify({'erro': 'verifique o corpo da requisição'}), 400


@people_blueprint.route("/<id>", methods=["PUT"])
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
    
    except (FieldDoesNotExist, ValidationError):
        return jsonify({'erro': 'verifique o corpo da requisição'}), 400


@people_blueprint.route("/<id>", methods=["DELETE"])
def delete_person(id):
    if len(id) != 24:
        return jsonify({'erro': 'id inválido'}), 400

    person = Person.objects(id=id).first()
    
    if person:
        person.delete()
    else:
        return jsonify({'erro': 'pessoa não encontrada'}), 404

    return jsonify({'sucesso': f'Pessoa {person.id} ({person.nome}) removida com sucesso'})