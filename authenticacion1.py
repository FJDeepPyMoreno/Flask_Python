from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'Paco3351'
app.config['PROPAGATE_EXCEPTIONS'] = True
api = Api(app)

jwt = JWT(app, authenticate, identity)  # It creates a new endpoint: '/auth'. This endpoint returns a JWT token.
                                        # We cand send this JWT totken to the next request we make.
items = []

class Item(Resource):
    @jwt_required()   # We have to authenticate before we call the get method.
    def get(self, name):
        item = next(filter(lambda x : x['name'] == name, items), None)
        return {'item': item}, 200 if item is not None else 404       

    def post(self, name):
        if next(filter(lambda x : x['name'] == name, items), None) is not None:
            return {'message' : f'An item with name {name} already exists.'}, 400  
        data = request.get_json() 
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201  

class ItemList(Resource):
    def get(self):
        return {'items' : items}

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=5000)