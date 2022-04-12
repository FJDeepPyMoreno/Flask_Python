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
        
    def __init__(self, name, price):
        self.name  = name
        self.price = price
    
    def json(self):
    # Returns a json representation of the model.
        return {'name': self.name, 'price': self.price}
    
    #def insert(self):
    def save_to_db(self):      
        db.session.add(self)   # SQL Alchemy translates objects to row
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()     