import sqlite3

class UserModel:
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