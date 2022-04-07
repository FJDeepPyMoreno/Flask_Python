import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

class Item(Resource):
    
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type = float,
                        required = True,
                        help = "This field can not be left blank!")

    @jwt_required()   # We have to authenticate before we call the get method.
    def get(self, name):
        # Retrive from database .db:
        connection = sqlite3.connect('data.db')
        cursor     = connection.cursor()
        query      = "SELECT * FROM items WHERE name = ?"
        result     = cursor.execute(query, (name,)).fetchone()
        connection.close() # Observa que no hacemos 'commit' ya que no estamos modificando la base de datos.
        if result:
            return {'item': {'name' : result[0], 'price': result[1]}}
        else:
            return {'message': 'item not found'}, 404

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
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        select_items = "SELECT * FROM items"
        result = cursor.execute(select_items)
        rows = result.fetchall()
        connection.close()
        items = []
        if rows:
            for r in rows:
                items.append({'name':  r[0],
                            'price': r[1]})
            return {'items' : items}
        else:
            return {'message': "Item list is empty"}, 404