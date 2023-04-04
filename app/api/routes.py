from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Drink, drink_schema, drinks_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'yee': 'haw'}


@api.route('/drinks', methods = ['POST'])
@token_required
def create_drinks(current_user_token):
    brand = request.json['brand']
    type = request.json['type']
    price = request.json['price']
    rating = request.json['rating']
    user_token = current_user_token.token

  
    print(f'big tester {current_user_token.token}')

    drink = Drink(brand,type,price,rating,user_token=user_token)

    db.session.add(drink)
    db.session.commit()

    response = drink_schema.dump(drink)
    return jsonify(response)

@api.route('/drinks', methods = ['GET'])
@token_required
def get_drinks(current_user_token):
    a_user = current_user_token.token
    drinks = Drink.query.filter_by(user_token = a_user).all()
    response = drinks_schema.dump(drinks)
    return jsonify(response)


@api.route('/drinks/<id>', methods = ['GET'])
@token_required
def get_single_contact(current_user_token, id):
    fan = current_user_token
    if fan:
        drink = Drink.query.get(id)
        response = drink_schema.dump(drink)
        return jsonify(response)
    else:
        return jsonify({'message':'valid token required'}), 401
    
@api.route('/drinks/<id>', methods = ['POST','PUT'])
@token_required
def update_contact(current_user_token,id):
    drink = Drink.query.get(id)
    drink.brand = request.json['brand']
    drink.type = request.json['type']
    drink.price = request.json['price']
    drink.rating = request.json['rating']
    drink.user_token = current_user_token.token

    db.session.commit()
    response = drink_schema.dump(drink)
    return jsonify(response)

@api.route('/drinks/<id>', methods = ['DELETE'])
@token_required
def delete_contact(current_user_token,id):
    drink = Drink.query.get(id)
    db.session.delete(drink)
    db.session.commit()
    response = drink_schema.dump(drink)
    return jsonify(response)
