from hmac import compare_digest
from user import User


def authenticate(username, password):
    user = User.find_by_username(username)
    if user and compare_digest(user.password, password):
        return user 

def identity(payload):  # payload is the content of the JWT token. El argumento de esta función es importante cuando creemos
                        # el objeto jwt.
    user_id = payload['identity']
    return User.find_by_id(user_id)
