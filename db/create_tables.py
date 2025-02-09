import sqlite3

conn = sqlite3.connect('project_database.db')
cursor = conn.cursor()

# Создание таблицы Users
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    unlocked_cars TEXT DEFAULT '',
    balance INTEGER DEFAULT 0,
    record INTEGER DEFAULT 0
);
''')


conn.commit()
conn.close()
