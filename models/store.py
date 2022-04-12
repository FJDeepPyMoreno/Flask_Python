from db import db

class StoreModel(db.Model):

    __tablename__ = "stores"

    id    = db.Column(db.Integer, primary_key = True)
    name  = db.Column(db.String(80))
    items = db.relationship('ItemModel', lazy='dynamic')  # Is a list of itemModel objects, puesto que un mismo Store puede corresponder
                                                          # a varios items
    # NOTA: Cada vez que creemos un Storemodel object se crearán tantos objetos ItemModel como macheos haya en la tabla 'items'
    # con el 'id' del Store. Esto si la tabla items es muy grande puede ser una operación costosa. El empleo de la keyword:
    # lazy = 'dynamic' evita quse se haga esto cada vez que se cree un objeto StoreModel.
        
    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first() 
        
    def __init__(self, name):
        self.name  = name
    
    def json(self):
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]} # .all() debido a la keyword: lazy = 'dynamic'
        # Si lazy = 'dynamic', self.items deja de ser una lista de ItemModel objects y pasa a ser un 'query builder' que tiene la
        # capacidad de mirar en la tabla 'items'. 
        # Es decir, con esto se llamará a la tabla 'items' no cada vez que creemos un StoreModel object sino cuando llamemos al 
        # método .json(). Así que el método .json() será más lento.  
    
    def save_to_db(self):      
        db.session.add(self)   
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()