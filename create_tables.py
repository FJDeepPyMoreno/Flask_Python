import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()
create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
                                                   # Cada vez que añadamos un reistro nuevo, el campo 'id' se autoincrementa, por lo
                                                   # que no necesitaremos especificarlo todo el rato.
cursor.execute(create_table)
connection.commit()
connection.close()

