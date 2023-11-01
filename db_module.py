import sqlite3

PATH = 'db.db'

class UserInfo:
    user_id = ''
    username = ''
    def __init__(self, user_id, username):
        self.user_id = user_id
        self.username = username

def add_user(user_id, username):
    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()
    cursor.execute('INSERT INTO Users (user_id, username) VALUES (?, ?)', (user_id, username))
    connection.commit()
    connection.close()

def exist(user_id):
    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()
    cursor.execute(f'SELECT EXISTS(SELECT 1 FROM users WHERE user_id={user_id})')
    if cursor.fetchone():
        return True
    else:
        return False
    connection.close()

def getUser(user_id):
    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()
    cursor.execute(f'SELECT user_id, username FROM users WHERE user_id={user_id}')
    r = cursor.fetchone()
    user = UserInfo(r[0], r[1])
    connection.close()
    return user
