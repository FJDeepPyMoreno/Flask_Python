from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):

    def get(self, name):
        result = StoreModel.find_by_name(name)        
        if result:
            return result.json()
        else:
            return {'message': 'Store not found'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message' : 'An item with name  "{}" already exists'.format(name)}, 400
        store = StoreModel(name) 
        try:
            store.save_to_db()
        except:
            return {'message': f'An error occurred while inserting store: {store.name}'}, 500
        
        return store.json()
                                                                         
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {'Message': 'Store deleted.'}

class StoreList(Resource):
    def get(self):
        return {'stores': [sto.json() for sto in StoreModel.query.all()]}
        