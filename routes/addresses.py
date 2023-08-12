import requests

from flask import Blueprint, request, jsonify
from models.address import Address
from xml.etree import ElementTree


addresses_blueprint = Blueprint('addresses', __name__)


@addresses_blueprint.route("", methods=["GET"])
def get_address():
    cep = request.args.get('cep')

    if not cep:
        return jsonify({'erro': 'insira o parâmetro CEP na requisição'}), 400
    
    response = requests.get(f"https://viacep.com.br/ws/{cep}/xml/")
    
    if response.status_code == 400:
        return jsonify({'erro': 'CEP inválido'}), 400
    
    tree = ElementTree.fromstring(response.content)
    
    if tree[0].tag == 'erro':
        return jsonify({'erro': 'CEP não localizado'}), 404
    
    address_dict = {
        'cep': tree[0].text,
        'logradouro': tree[1].text,
        'complemento': tree[2].text or '',
        'bairro': tree[3].text,
        'cidade': tree[4].text,
        'uf': tree[5].text
    }

    address_obj = Address.objects(cep=tree[0].text).first()

    if not address_obj:
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