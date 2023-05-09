from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Soda, soda_schema, sodas_schema

api = Blueprint('api',__name__, url_prefix='/api')

#@api.route('/getdata')
#def getdata():
    #return {'yee': 'haw'}

@api.route('/sodas', methods = ['POST'])
@token_required
def create_soda(current_user_token):
    name = request.json['name']
    brand = request.json['brand']
    flavor = request.json['flavor']
    size = request.json['size']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    soda = Soda(name, brand, flavor, size, user_token = user_token )

    db.session.add(soda)
    db.session.commit()

    response = soda_schema.dump(soda)
    return jsonify(response)

@api.route('/sodas', methods = ['GET'])
@token_required
def get_soda(current_user_token):
    a_user = current_user_token.token
    sodas = Soda.query.filter_by(user_token = a_user).all()
    response = sodas_schema.dump(sodas)
    return jsonify(response)

@api.route('/sodas/<id>', methods = ['GET'])
@token_required
def get_soda_two(current_user_token, id):
    fan = current_user_token.token
    if fan == current_user_token.token:
        soda = Soda.query.get(id)
        response = soda_schema.dump(soda)
        return jsonify(response)
    else:
        return jsonify({"message": "Valid Token Required"}),401

@api.route('/sodas/<id>', methods = ['POST','PUT'])
@token_required
def update_soda(current_user_token,id):
    soda = Soda.query.get(id) 
    soda.name = request.json['name']
    soda.brand = request.json['brand']
    soda.flavor = request.json['flavor']
    soda.size = request.json['size']
    soda.user_token = current_user_token.token

    db.session.commit()
    response = soda_schema.dump(soda)
    return jsonify(response)

@api.route('/sodas/<id>', methods = ['DELETE'])
@token_required
def delete_soda(current_user_token, id):
    soda = Soda.query.get(id)
    db.session.delete(soda)
    db.session.commit()
    response = soda_schema.dump(soda)
    return jsonify(response)