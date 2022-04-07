from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class Student(Resource):     # Creamos clases y las añadimos como recursos.
    def get(self, name):
        return {'student' : name}

api.add_resource(Student, '/student/<string:name>') # El segundo argumento especifica el entry point.

app.run(port=5000)