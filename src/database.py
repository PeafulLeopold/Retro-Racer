import sqlite3
import os

DB_DIR = 'db'
DB_PATH = os.path.join(DB_DIR, 'project_database.db')

def init_db():
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Создание таблицы Users с сохранением баланса и рекордов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            balance INTEGER DEFAULT 0,
            high_score INTEGER DEFAULT 0
        )
    ''')
    
    # Таблица Cars: информация о машинах для покупки и использования
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Cars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            speed INTEGER NOT NULL,
            acceleration REAL NOT NULL,
            price INTEGER NOT NULL,
            image_path TEXT NOT NULL
        )
    ''')
    
    # Таблица OwnedCars: связывает пользователей с купленными машинами
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS OwnedCars (
            user_id INTEGER NOT NULL,
            car_id INTEGER NOT NULL,
            PRIMARY KEY (user_id, car_id),
            FOREIGN KEY (user_id) REFERENCES Users(id),
            FOREIGN KEY (car_id) REFERENCES Cars(id)
        )
    ''')
    
    conn.commit()
    conn.close()

def create_user(username, password):
    """
    Создает нового пользователя с балансом и рекордом, равными 0.
    Возвращает id нового пользователя или None в случае ошибки.
    Изначально каждому пользователю присваивается дефолтная машина с изображением "data\\images\\car.png".
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO Users (username, password, balance, high_score)
            VALUES (?, ?, 0, 0)
        ''', (username, password))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return None
    user_id = cursor.lastrowid

    # Определяем путь до дефолтной машины
    default_image_path = r"data\images\car.png"
    # Проверяем, существует ли машина с таким изображением
    cursor.execute('SELECT id FROM Cars WHERE image_path = ?', (default_image_path,))
    result = cursor.fetchone()
    if result is None:
        # Если нет, создаем дефолтную машину с базовыми характеристиками
        cursor.execute('''
            INSERT INTO Cars (name, speed, acceleration, price, image_path)
            VALUES (?, ?, ?, ?, ?)
        ''', ("Default Car", 200, 4.0, 0, default_image_path))
        conn.commit()
        default_car_id = cursor.lastrowid
    else:
        default_car_id = result[0]
    
    cursor.execute('''
        INSERT INTO OwnedCars (user_id, car_id)
        VALUES (?, ?)
    ''', (user_id, default_car_id))
    conn.commit()
    conn.close()
    return user_id

def get_user(username):
    """
    Получает данные пользователя по имени.
    Возвращает кортеж (id, username, password, balance, high_score) или None, если пользователь не найден.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, username, password, balance, high_score
        FROM Users
        WHERE username = ?
    ''', (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def update_balance(user_id, new_balance):
    """
    Обновляет баланс пользователя.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE Users
        SET balance = ?
        WHERE id = ?
    ''', (new_balance, user_id))
    conn.commit()
    conn.close()

def update_high_score(user_id, new_score):
    """
    Обновляет рекорд пользователя, если новый результат выше текущего.
    Это позволяет корректно обновлять таблицу лидеров после заезда.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Получаем текущий рекорд пользователя
    cursor.execute('SELECT high_score FROM Users WHERE id = ?', (user_id,))
    current_high = cursor.fetchone()[0]
    if new_score > current_high:
        cursor.execute('''
            UPDATE Users
            SET high_score = ?
            WHERE id = ?
        ''', (new_score, user_id))
        conn.commit()
    conn.close()

def get_cars():
    """
    Возвращает список всех автомобилей.
    Если таблица пуста, заполняет её начальными записями.
    Каждая запись имеет формат:
    (id, name, speed, acceleration, price, image_path)
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Cars')
    cars = cursor.fetchall()
    if not cars:
        # Добавляем начальные записи (убедитесь, что файлы изображений существуют по указанным путям)
        default_cars = [
            ("Speedster", 220, 3.5, 50, "assets/cars/speedster.png"),
            ("Roadster", 240, 3.2, 60, "assets/cars/roadster.png"),
            ("Thunder", 260, 3.0, 70, "assets/cars/thunder.png")
        ]
        cursor.executemany('''
            INSERT INTO Cars (name, speed, acceleration, price, image_path)
            VALUES (?, ?, ?, ?, ?)
        ''', default_cars)
        conn.commit()
        cursor.execute('SELECT * FROM Cars')
        cars = cursor.fetchall()
    conn.close()
    return cars

def buy_car(user_id, car_id):
    """
    Добавляет автомобиль в список купленных для пользователя.
    Если автомобиль уже куплен, ничего не меняется.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR IGNORE INTO OwnedCars (user_id, car_id)
        VALUES (?, ?)
    ''', (user_id, car_id))
    conn.commit()
    conn.close()

def get_owned_cars(user_id):
    """
    Возвращает список автомобилей, купленных данным пользователем.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT Cars.* FROM Cars
        JOIN OwnedCars ON Cars.id = OwnedCars.car_id
        WHERE OwnedCars.user_id = ?
    ''', (user_id,))
    cars = cursor.fetchall()
    conn.close()
    return cars


if __name__ == '__main__':
    init_db()
