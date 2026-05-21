import sqlite3
your_way = "YOUR WAY TO FILES"

def init_db():
    with sqlite3.connect(f"{your_way}\\profiles.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                sex TEXT NOT NULL,
                photo_url TEXT NOT NULL,
                description TEXT NOT NULL,
                follows TEXT NOT NULL
            )
        ''')
        
        
def save_user_profile(user_id: int, name: str, age: int, sex: str, photo_url: str, description: str, follows: str):
    with sqlite3.connect(f"{your_way}\\profiles.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (user_id, name, age, sex, photo_url, description, follows)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                name = excluded.name,
                age = excluded.age,
                sex = excluded.sex,
                photo_url = excluded.photo_url,
                description = excluded.description,
                follows = excluded.follows
                ''', (user_id, name, age, sex, photo_url, description, follows))
        conn.commit()
        
        
def get_user_profile(user_id: int):
    with sqlite3.connect(f"{your_way}\\profiles.db") as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT name, age, sex, photo_url, description, follows FROM users WHERE user_id = ?', (user_id,))
        return cursor.fetchone()
    
    
def search_profiles(sex: str, age_from: int, age_to: int, user_id: int):
    with sqlite3.connect(f"{your_way}\\profiles.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM users WHERE (? = 'any' OR sex = ?) AND CAST(age AS INTEGER) BETWEEN ? AND ? AND user_id != ?''', (sex, sex, age_from, age_to, user_id))
        return cursor.fetchall()