import sqlite3

conn = sqlite3.connect("professores.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS professores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL
)
""")

conn.commit()
conn.close()