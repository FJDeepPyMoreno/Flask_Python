from flask import Flask, request
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

items = []

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type = float,
                        required = True,
                        help = "This field can not be left blank!")
    def get(self, name):
        item = next(filter(lambda x : x['name'] == name, items), None)
        return {'item': item}, 200 if item is not None else 404              
                             
    def post(self, name):

        if next(filter(lambda x : x['name'] == name, items), None) is not None:
            return {'message' : f'An item with name {name} already exists.'}, 400  # 400 status code stands for 'bad request'.

        #data = request.get_json() # json payload: a body attached to the request. In this case is made by POSTMAN.
                                  # El content-type debe ser el adecuado.
                                  # Puesto que el content-type será un json, 'data' será un dictionary.
        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201  # Simplemente para que mi app sepa que esto ha ocurrido. Código 201: 'successfully created'.
    
    def delete(self, name):
        ideletion = [i for i in range(len(items)) if items[i]['name']==name]
        if ideletion:
            ditem = str(items[ideletion[0]])
            del items[ideletion[0]]
            return {"Deleted item" : ditem}
        else:
            return {"Message": f"No item with name {name} in the item list."}
    
    def put(self, name):
        #data = request.get_json()
        data = Item.parser.parse_args()
        item = next(filter(lambda x : x['name'] == name, items), None)
        if item is None:
            addItem = {'name': name, 'price': data['price']}
            items.append(addItem)
            return addItem
        else:
            item.update(data)
            return item


class ItemList(Resource):
    def get(self):
        return {'items' : items}

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=5000)