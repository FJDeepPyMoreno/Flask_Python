import sqlite3
from db import db

class ItemModel(db.Model):

    __tablename__ = "items"

    id    = db.Column(db.Integer, primary_key = True)
    name  = db.Column(db.String(80))
    price = db.Column(db.Float(precision = 2))
    
    @classmethod
    def find_by_name(cls, name):
                 # 'query' es un método heredado de db.Model:
        return cls.query.filter_by(name=name).first() # Equivalente al WHERE statement de SQL:
                                                      #  SELECT * FROM items WHERE name=name LIMIT 1  
                                                      # Vemos que convierte directamente el registro de la base de datos en un objeto
                                                      # ItemModel


        # Retrive from database .db:
        # Comentamos estas líneas porque al introducir SQL Alchemy el proceso se simplifica bastante. 
        # connection = sqlite3.connect('data.db')
        # cursor     = connection.cursor()
        # query      = "SELECT * FROM items WHERE name = ?"
        # result     = cursor.execute(query, (name,))
        # row        = result.fetchone()
        # connection.close() # Observa que no hacemos 'commit' ya que no estamos modificando la base de datos.
        # if row:
        #     return cls(*row)
        
    def __init__(self, name, price):
        self.name  = name
        self.price = price
    
    def json(self):
    # Returns a json representation of the model.
        return {'name': self.name, 'price': self.price}
    
    #def insert(self):
    def save_to_db(self): # con SQL Alchemy, las siguientes instrucciones valen tanto para actualizar como para insertar. 
        db.session.add(self)   # SQL Alchemy translates objects to row
        db.session.commit()

        # Al introducir SQL Alchemy comentamos estas líneas:

        # connection = sqlite3.connect('data.db')
        # cursor     = connection.cursor()
        # query      = "INSERT INTO items VALUES (?, ?)"
        # cursor.execute(query, (self.name, self.price))
        # connection.commit()
        # connection.close()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()     

    # def update(self):
    #     connection = sqlite3.connect('data.db')
    #     cursor     = connection.cursor()
    #     query      = "UPDATE items SET price = ? WHERE name = ?"
    #     cursor.execute(query, (self.price, self.name))
    #     connection.commit()
    #     connection.close()
    #     return {'message': f'Item "{self.name}" was updated'}, 201    