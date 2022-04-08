from multiprocessing import connection
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
        result = self.find_by_name(name)        
        if result:
            return {'item': {'name' : result[0], 'price': result[1]}}
        else:
            return {'message': 'item not found'}, 404
    
    @classmethod
    def find_by_name(cls, name):
        # Retrive from database .db:
        connection = sqlite3.connect('data.db')
        cursor     = connection.cursor()
        query      = "SELECT * FROM items WHERE name = ?"
        result     = cursor.execute(query, (name,))
        row        = result.fetchone()
        connection.close() # Observa que no hacemos 'commit' ya que no estamos modificando la base de datos.
        return row

    def post(self, name):
        if self.find_by_name(name):
            return {'message' : 'An item with name  "{}" already exists'.format(name)}, 400
        data = Item.parser.parse_args() 
        item = {'name': name, 'price': data['price']}
        connection = sqlite3.connect('data.db')
        cursor     = connection.cursor()
        query      = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item['name'], item['price']))
        connection.commit()
        connection.close() 
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
    
    @jwt_required()
    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor     = connection.cursor()
        query      = "DELETE FROM items WHERE name = ?"
        cursor.execute(query, (name,))
        connection.commit()
        connection.close()
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