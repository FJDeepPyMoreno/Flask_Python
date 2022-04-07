from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security_db import authenticate, identity
from user_signUp import UserRegister

app = Flask(__name__)
app.secret_key = 'Paco3351'  # Esta línea debe estar para que '/auth' vaya bien. 
app.config['PROPAGATE_EXCEPTIONS'] = True
api = Api(app)

jwt = JWT(app, authenticate, identity)  # It creates a new endpoint: '/auth'. This endpoint returns a JWT token.
                                        # We cand send this JWT totken to the next request we make.
items = []

class Item(Resource):
    
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type = float,
                        required = True,
                        help = "This field can not be left blank!")

    @jwt_required()   # We have to authenticate before we call the get method.
    def get(self, name):
        item = next(filter(lambda x : x['name'] == name, items), None)
        return {'item': item}, 200 if item is not None else 404       

    def post(self, name):
        if next(filter(lambda x : x['name'] == name, items), None) is not None:
            return {'message' : f'An item with name {name} already exists.'}, 400 
        data = Item.parser.parse_args() 
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201
    
    def put(self, name):
        data = Item.parser.parse_args()
        item = next(filter(lambda x : x['name'] == name, items), None)
        if item is None:
            new_item = {'name' : name, 'price' : data['price']}
            items.append(new_item)
            return new_item
        else:
            item.update(data)
            return item  
    
    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'Message': 'Item deleted.'}

class ItemList(Resource):
    def get(self):
        return {'items' : items}

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

app.run(port=5000)