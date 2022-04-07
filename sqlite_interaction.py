"""
This script shows how to interact with SQLite using Python

"""

import sqlite3   # Esta es una libreria built-in de Python

connection = sqlite3.connect('data.db')  # Crea un fichero llamado 'data.db', que será nuestra base de datos de interacción.
                                         # Realmente las bases de datos ocuparán normalmente muchos ficheros, carpetas, etc,
                                         # sqlite3 permite trabajar con single files que alberguen menos data.

cursor = connection.cursor()   # El objeto 'cursor' será el que permita ejecutar queries.

# Creamos una tabla en la base de datos: 'data.db':

create_table = "CREATE TABLE users (id int, username text, password text)"
cursor.execute(create_table)   # Una vez creada ya esta instrucción se crea la data.db. Si ya existe data.db esta instrucción
                               # dará un error.

# Insertamos un primer registro en la tabla 'users' recién creada:

user = (1, 'jose', 'asdf')
insert_query = "INSERT INTO users VALUES (?,?,?)"  # Se pueden poner los signos '?'
cursor.execute(insert_query, user)  # 'cursor' es lo suficientemente smart como para añadir correctamente el registro.

# insertamos ahora varios registros más:

users = [(2, 'rolf', 'ffgt'),
         (3, 'agatha', 'fg4456')]

cursor.executemany(insert_query, users)

# Vamos a seleccionar algunas líneas:

select_query = "SELECT * FROM users"  # Esta query devuelve todos los registros de la tabla.

for row in cursor.execute(select_query):  # cursor.execute(select_query) : an iterator.
    print(row)

# Para guardar los datos en 'data.db' debemos hacer lo siguiente:

connection.commit()
connection.close()