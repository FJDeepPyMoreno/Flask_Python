from multiprocessing import connection
import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type = float,
                        required = True,
                        help = "This field can not be left blank!")
    
    
    @jwt_required()   # We have to authenticate before we call the get method.
    def get(self, name):
        result = ItemModel.find_by_name(name)        
        if result:
            return result.json()
        else:
            return {'message': 'item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message' : 'An item with name  "{}" already exists'.format(name)}, 400
        data = Item.parser.parse_args()
        item = ItemModel(name, data['price']) 

        try:
            item.insert()
            return {'message': f'Item "{item.name}" was inserted on Items database.'}, 201
        except:
            return {'message': f'An error occurred while inserting item: {item.name}'}, 500
                                                                      # No es un error del requester. Seria un Internal Server Error.
    
    def put(self, name):
        data        = Item.parser.parse_args()
        item        = ItemModel.find_by_name(name)
        updatedItem = ItemModel(name, data['price'])
        if item is not None: 
            try:         
                updatedItem.update()
                return {'message': f'Item "{updatedItem.name}" was updated'}, 201 
            except:
                return {'message': 'An error occurred at updating the Item.'}, 500       
        else:
            try:
                updatedItem.insert()
                return {'message': f'Item "{updatedItem.name}" was inserted on Items database.'}, 201
            except:
                return {'message': 'An error occurred at inserting the Item.'}, 500  
    
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