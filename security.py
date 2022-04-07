# This file contains a few important functions related to 'logging' and 'authentication':

# Registered users table:

# from werkzeug.security import   # A veces la comparación de cadenas con == cambia de una versión de Python a otra. Según 
                                            # cuales sean estas versiones.
from user import User

users = [

    User(1, 'bob', 'asdf'),
    User(2, 'Barbara', 'bb4456')     # Provisionalmente usamos esta lista, pero después lo cambiaremos por una base de datos.
]

username_mapping = {u.username: u for u in users}
userid_mapping   = {u.id : u for u in users}


# Function for authenticate the user: 

def authenticate(username, password):
    user = username_mapping.get(username, None) # si no está ese usuario, se devuelve 'None'.
    if user and user.password == password:
        return user

def identity(payload):  # payload is the content of the JWT token. El argumento de esta función es importante cuando creemos
                        # el objeto jwt.
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)