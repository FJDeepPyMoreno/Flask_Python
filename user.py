import sqlite3

class User:
    def __init__(self, _id, username, password):
        self.id       = _id
        self.username = username
        self.password = password
    
    @classmethod
    def find_by_username(cls, username):     # Añadido en la sección de sqlite
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        find_query = "SELECT * FROM users WHERE username=?"
        susers = cursor.execute(find_query, (username,))  # El segundo argumento debe ser un tuple
        row = susers.fetchone()  # Coge el primer elemento del iterator devolviendo un tuple.
                                 # Si no hay líneas que matcheen esto, se devuelve un None.
        if row:
           # user = cls(row[0], row[1], row[2])
            user = cls(*row)  # mucho mejor así. 
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