import sqlite3
from flask_restful import Resource, reqparse


class User:
    def __init__(self, _id, username, password):
        self.id       = _id
        self.username = username
        self.password = password
    
    @classmethod
    def find_by_username(cls, username):     
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        find_query = "SELECT * FROM users WHERE username=?"
        susers = cursor.execute(find_query, (username,))  
        row = susers.fetchone()  
                                
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

class UserRegister(Resource):
    parser = reqparse.RequestParser()  # This parser passes through the json of the request and only pays attention
                                       # to the specified arguments 
    parser.add_argument('username',
                            type = str,
                            required = True,
                            help = "An user name: alphanumeric, begins with a letter." )
    parser.add_argument('password',
                            type = str,
                            required = True,
                            help = "An user password: at least 5 characters. Must contain at least one number and one special" )
    def post(self):     
        data = UserRegister.parser.parse_args()  
        if User.find_by_username(data['username']):
            return {"Message": "An user with this name already exists"}, 400               
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        insert_query = "INSERT INTO users VALUES (NULL, ?,?)"
        cursor.execute(insert_query, (data['username'], data['password']))
        connection.commit()
        connection.close()
        return {"message": "User created succesfully"}, 201
