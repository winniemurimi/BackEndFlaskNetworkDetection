import sqlite3

def create_users_table():
    conn = sqlite3.connect('db.sqlite')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              username TEXT NOT NULL UNIQUE,
              password TEXT NOT NULL,
              salt TEXT NOT NULL,
              session_token TEXT  
              )''')
    conn.commit()
    conn.close()


if __name__ == '__main__':
    create_users_table()