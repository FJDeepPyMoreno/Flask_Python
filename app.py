from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList

app = Flask(__name__)
app.secret_key = 'Paco3351'  # Esta línea debe estar para que '/auth' vaya bien. 
app.config['PROPAGATE_EXCEPTIONS'] = True
api = Api(app)

jwt = JWT(app, authenticate, identity)  # It creates a new endpoint: '/auth'. This endpoint returns a JWT token.
                                        # We cand send this JWT totken to the next request we make.


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == "__main__":   # Con esto prevenimos que corra la app si se importan módulos o funciones de app.py
     app.run(port=5000)