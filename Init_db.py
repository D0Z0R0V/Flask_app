import sqlite3

connection = sqlite3.connect("database.db")

with open("schema.sql") as f:
    connection.executescript(f.read())

cur = connection.cursor()

#cur.execute("INSERT INTO posts (context, tempr, icon) VALUES (?, ?, ?)", ("New York", 5, "04d"))

connection.commit()
connection.close()
