import sqlite3
from db import db

class UserModel(db.Model):

    __tablename__ = 'users'
    
    # Definimos la columna con nombre 'id' de nuestra tabla:
    id       = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))                 # Limits the username size to 80 bytes.
    password = db.Column(db.String(20))                 

    def __init__(self, username, password):
        # Hemos quitado el 'id' porque ahora que es primary key, no hace falta
        self.username = username
        self.password = password
    
    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()  # the 'username' on the left side is the table's variable.
                                                               # the 'username' on the right is the method argument 'username'    

    @classmethod
    def find_by_id(cls, idu):
        return cls.query.filter_by(id=idu).first()     
    
            
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()