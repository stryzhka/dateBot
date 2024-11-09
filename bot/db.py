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
    watch_toggle = ''
    def __init__(self, user_id, username, name, sex, description, photo):
        self.user_id = user_id
        self.username = username
        self.name = name
        self.sex = sex
        self.description = description
        self.photo = photo
        self.watch_toggle = "True"

def add_user(user_id, username, name, sex, description, photo):
    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()
    cursor.execute('INSERT INTO Users (user_id, username) VALUES (?, ?)', (user_id, username))
    cursor.execute(f'UPDATE users SET name = ? where user_id=?', (name, user_id))
    cursor.execute(f'UPDATE users SET sex = ? where user_id=?', (sex, user_id))
    cursor.execute(f'UPDATE users SET description = ? where user_id=?', (description, user_id))
    cursor.execute(f'UPDATE users SET photo = ? where user_id=?', (photo, user_id))
    cursor.execute(f'UPDATE users SET watch_toggle = ? where user_id=?', ("True", user_id))
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
        connection.close()
        return False
    else:
        connection.close()
        return True

    

def get_user(user_id):
    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()
    cursor.execute(f'SELECT user_id, username, name, sex, description, photo, watch_toggle FROM users WHERE user_id={user_id}')
    r = cursor.fetchone()
    #print(r)
    user = UserInfo(r[0], r[1], r[2], r[3], r[4], r[5])
    user.watch_toggle = r[6]
    connection.close()
    return user

def get_user_by_id(id):
    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()
    cursor.execute(f'SELECT user_id, username, name, sex, description, photo FROM users WHERE id={id}')
    r = cursor.fetchone()
    #print(r)
    user = UserInfo(r[0], '', r[2], r[3], r[4], r[5])
    user.watch_toggle = r[6]
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

def add_match(send_id, got_id):
    if not match_exist(send_id, got_id):
        connection = sqlite3.connect(PATH)
        cursor = connection.cursor()
        cursor.execute('INSERT INTO matches (send_id, got_id) VALUES (?, ?)', (send_id, got_id))
        connection.commit()
        connection.close()

#return db response, find all who liked got_id
def get_got_id(user_id):
    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()
    cursor.execute(f'SELECT send_id FROM matches where got_id={user_id}')
    r = cursor.fetchall()
    connection.close()
    return r



def match_exist(send_id, got_id):
    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()
    cursor.execute(f'SELECT got_id FROM matches WHERE send_id={send_id}')
    for e in cursor.fetchall():
        if e[0] == got_id:
            return True
    connection.close()

    

def get_matches(id):
    l = []
    l2 = []
    if len(get_got_id(id)) > 0:
        for e in get_got_id(id):
            l.append(e[0])
        l.sort(reverse=True)
        for e in l:
            l2.append(get_user(e))
    return l2

def remove_match(send_id, got_id):
    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()
    cursor.execute(f'DELETE FROM matches where send_id={send_id} and got_id={got_id}')
    connection.commit()
    #print('cursor', cursor.fetchall())
    connection.close()

def set_watch_toggle_true(user_id):
    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()
    cursor.execute(f'UPDATE users SET watch_toggle = ? where user_id=?', ("True", user_id))
    connection.commit()
    connection.close()

def set_watch_toggle_false(user_id):
    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()
    cursor.execute(f'UPDATE users SET watch_toggle = ? where user_id=?', ("False", user_id))
    connection.commit()
    connection.close()

def is_watch_toggle(user_id):
    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()
    cursor.execute(f'SELECT watch_toggle FROM users WHERE user_id = {user_id}')
    r = cursor.fetchone()
    connection.close()
    return (r[0])

def is_user_admin(user_id):
    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()
    cursor.execute(f'SELECT * FROM admins where user_id={user_id}')
    r = cursor.fetchone()
    connection.close()
    if r is None:
        return False
    return True

def add_complain(user_id):
    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO complains (user_id) VALUES({user_id})")
    connection.commit()

def get_complains():
    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()
    cursor.execute(f'SELECT * FROM complains')
    r = cursor.fetchall()
    l = []
    for e in r:
        l.append(e[0])
    #l.sort(reverse=True)
    l2 = []
    for e in l:
        l2.append(get_user(e))
    connection.close()
    #print(l)
    return l2

def complain_exists(user_id):
    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()
    cursor.execute(f'SELECT user_id FROM complains WHERE user_id={user_id}')
    r = cursor.fetchall()
    connection.close()
    return r

def remove_complain(user_id):
    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()
    cursor.execute(f'DELETE FROM complains where user_id={user_id}')
    connection.commit()
    connection.close()

def clean_complains():
    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()
    cursor.execute(f'DELETE FROM complains')
    connection.commit()
    connection.close()

def get_blacklist():
    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()
    cursor.execute(f'SELECT * FROM blacklist')
    r = cursor.fetchall()
    connection.close()
    #print(r)
    return r

def add_to_blacklist(user_id):
    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()
    cursor.execute(f'INSERT INTO blacklist (user_id) VALUES({user_id})')
    connection.commit()
    connection.close()

def remove_from_blacklist(user_id):
    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()
    cursor.execute(f'DELETE FROM blacklist WHERE user_id={user_id}')
    connection.commit()
    connection.close()

def blacklist_exist(user_id):
    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()
    cursor.execute(f'SELECT user_id FROM blacklist WHERE user_id={user_id}')
    r = cursor.fetchall()
    connection.close()
    return r

def add_admin(user_id):
    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()
    cursor.execute(f'INSERT INTO admins (user_id) VALUES({user_id})')
    connection.commit()
    connection.close()

def delete_admin(user_id):
    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()
    cursor.execute(f'DELETE FROM admins WHERE user_id={user_id}')
    connection.commit()
    connection.close()

def admin_exist(user_id):
    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()
    cursor.execute(f'SELECT user_id FROM admins WHERE user_id={user_id}')
    r = cursor.fetchall()
    connection.close()
    return r