import sqlite3
import io

from bot.config import PATH

class UserInfo:
    id = ''
    user_id = ''
    username = ''
    name = ''
    sex = ''
    description = ''
    photo = ''
    def __init__(self, user_id, username, name, sex, description, photo):
        self.user_id = user_id
        self.username = username
        self.name = name
        self.sex = sex
        self.description = description
        self.photo = photo


def add_user(user_id, username):
    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()
    cursor.execute('INSERT INTO Users (user_id, username) VALUES (?, ?)', (user_id, username))
    connection.commit()
    connection.close()

def update_user(user_id, name, sex, description, photo):
    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()
    cursor.execute(f'UPDATE users SET name = ? where user_id=?', (name, user_id))
    cursor.execute(f'UPDATE users SET sex = ? where user_id=?', (sex, user_id))
    cursor.execute(f'UPDATE users SET description = ? where user_id=?', (description, user_id))
    cursor.execute(f'UPDATE users SET photo = ? where user_id=?', (photo, user_id))
    connection.commit()
    connection.close()
def exist(user_id):
    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()
    cursor.execute(f'SELECT photo FROM users WHERE user_id={user_id}')
    if cursor.fetchone() is None:
        return False

    else:
        return True

    connection.close()

def get_user(user_id):
    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()
    cursor.execute(f'SELECT user_id, username, name, sex, description, photo FROM users WHERE user_id={user_id}')
    r = cursor.fetchone()
    user = UserInfo(r[0], '', r[2], r[3], r[4], r[5])

    connection.close()
    return user

def get_user_by_id(id):
    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()
    cursor.execute(f'SELECT user_id, username, name, sex, description, photo FROM users WHERE id={id}')
    r = cursor.fetchone()
    print(r)
    user = UserInfo(r[0], '', r[2], r[3], r[4], r[5])
    connection.close()
    return user

def get_users_list():
    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()
    cursor.execute(f'SELECT user_id FROM users')
    r = cursor.fetchall()
    l = []
    for el in r:
        l.append(el[0])
    connection.close()
    return l

def get_len():
    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()
    cursor.execute('SELECT COUNT(*) FROM users')
    r = cursor.fetchone()
    connection.close()
    return r