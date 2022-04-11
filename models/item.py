import sqlite3

class ItemModel:
    
    @classmethod
    def find_by_name(cls, name):
        # Retrive from database .db:
        connection = sqlite3.connect('data.db')
        cursor     = connection.cursor()
        query      = "SELECT * FROM items WHERE name = ?"
        result     = cursor.execute(query, (name,))
        row        = result.fetchone()
        connection.close() # Observa que no hacemos 'commit' ya que no estamos modificando la base de datos.
        if row:
            return cls(*row)
        
    def __init__(self, name, price):
        self.name  = name
        self.price = price
    
    def json(self):
    # Returns a json representation of the model.
        return {'name': self.name, 'price': self.price}
    
    def insert(self):
        connection = sqlite3.connect('data.db')
        cursor     = connection.cursor()
        query      = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (self.name, self.price))
        connection.commit()
        connection.close()
        return {'message': f'Item "{self.name}" was inserted on Items database.'}, 201 

    def update(self):
        connection = sqlite3.connect('data.db')
        cursor     = connection.cursor()
        query      = "UPDATE items SET price = ? WHERE name = ?"
        cursor.execute(query, (self.price, self.name))
        connection.commit()
        connection.close()
        return {'message': f'Item "{self.name}" was updated'}, 201    