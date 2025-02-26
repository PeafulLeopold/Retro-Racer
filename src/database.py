import sqlite3
import os

def init_db():
    if not os.path.exists('db'):
        os.makedirs('db')
    
    conn = sqlite3.connect('db/project_database.db')
    cursor = conn.cursor()
    
    # Создание таблиц
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            balance INTEGER DEFAULT 0,
            high_score INTEGER DEFAULT 0
        )''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Cars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            speed INTEGER NOT NULL,
            acceleration REAL NOT NULL,
            price INTEGER NOT NULL,
            image_path TEXT NOT NULL
        )''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS OwnedCars (
            user_id INTEGER NOT NULL,
            car_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES Users(id),
            FOREIGN KEY (car_id) REFERENCES Cars(id)
        )''')
    
    conn.commit()
    conn.close()

def get_cars():
    conn = sqlite3.connect('db/project_database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Cars')
    cars = cursor.fetchall()
    conn.close()
    return cars

def buy_car(user_id, car_id):
    conn = sqlite3.connect('db/project_database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO OwnedCars (user_id, car_id) VALUES (?, ?)', (user_id, car_id))
    conn.commit()
    conn.close()

def get_owned_cars(user_id):
    conn = sqlite3.connect('db/project_database.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT Cars.* FROM Cars
        JOIN OwnedCars ON Cars.id = OwnedCars.car_id
        WHERE OwnedCars.user_id = ?
    ''', (user_id,))
    cars = cursor.fetchall()
    conn.close()
    return cars