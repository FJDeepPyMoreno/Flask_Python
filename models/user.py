import sqlite3
from db import db

class UserModel(db.Model):

    __tablename__ = 'users'
    
    # Definimos la columna con nombre 'id' de nuestra tabla:
    id       = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))                 # Limits the username size to 80 bytes.
    password = db.Column(db.String(20))                 

    def __init__(self, _id, username, password):
        self.id       = _id
        self.username = username
        self.password = password
    
    @classmethod
    def find_by_username(cls, username):     
        connection = sqlite3.connect('data.db')
        cursor     = connection.cursor()
        find_query = "SELECT * FROM users WHERE username=?"
        susers     = cursor.execute(find_query, (username,))  
        row        = susers.fetchone()  
                                
        if row:
            user = cls(*row)   
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls, idu):     
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        find_query = "SELECT * FROM users WHERE id=?"
        susers = cursor.execute(find_query, (idu,))  
        row = susers.fetchone()                    
        if row:
            user = cls(*row)  
        else:
            user = None
        connection.close()
        return user