from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from db import db

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList

app                                          = Flask(__name__)
app.secret_key                               = 'Paco3351'  # Esta línea debe estar para que '/auth' vaya bien.
app.config['SQLALCHEMY_DATABASE_URI']        = 'sqlite:///data.db'  # Especifica que leeremos la base de datos desde el rrot path
                                                                    # Es decir, desde donde se lanza este script. 
app.config['PROPAGATE_EXCEPTIONS']           = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False       # Los cambios en los objetos se transfieren igualmente a la Base de Datos.
api                                          = Api(app)
jwt                                          = JWT(app, authenticate, identity)  
                                               # It creates a new endpoint: '/auth'. This endpoint returns a JWT token.
                                               # We cand send this JWT totken to the next request we make.

@app.before_first_request  # llama al método decorado antes del primer request que se haga de la app.
def create_tables():
     db.create_all()  # Crea el archivo data.db según la línea 12 de este script.

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == "__main__":   # Con esto prevenimos que corra la app si se importan módulos o funciones de app.py
     db.init_app(app)
     app.run(port=5000, debug=True)
    