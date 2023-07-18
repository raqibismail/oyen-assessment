import sqlite3

conn = sqlite3.connect('database.db')

cursor = conn.cursor()

data = ('admin', 'admin')  # Example data to be inserted
# data = (2, 'test', 'password')  # Example data to be inserted
# data = (3, 'raqib', 'password')  # Example data to be inserted
cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", data)


# cursor.execute('''CREATE TABLE users
#                   (id INTEGER PRIMARY KEY AUTOINCREMENT,
#                   username TEXT NOT NULL,
#                   password TEXT NOT NULL);''')


conn.commit()  # Commit the changes
conn.close()  # Close the connection
