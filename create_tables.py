import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()
create_table_users = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
                                                   # Cada vez que añadamos un reistro nuevo, el campo 'id' se autoincrementa, por lo
                                                   # que no necesitaremos especificarlo todo el rato

create_table_items = "CREATE TABLE IF NOT EXISTS items (name text, price real)"

cursor.execute(create_table_users)
cursor.execute(create_table_items)

user = (1, 'jose', 'asdf')
insert_user = "INSERT INTO users VALUES (?,?,?)"  # Se pueden poner los signos '?'
cursor.execute(insert_user, user)  # 'cursor' es lo suficientemente smart como para añadir correctamente el registro.

# insertamos ahora varios registros más:

users = [(2, 'rolf', 'ffgt'),
         (3, 'agatha', 'fg4456')]

cursor.executemany(insert_user, users)

items = [('arpa', 2350),
         ('piano', 7730)]

insert_item = "INSERT INTO items VALUES (?,?)"

cursor.executemany(insert_item, items)

connection.commit()
connection.close()

