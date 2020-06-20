# импорт библиотек
import sqlite3
import os

# ПУТЬ К БАЗЕ ДАННЫХ
path_db = "db.sqlite"

# подключение к базе
def connect_db(file_db):
    try:
        # подключение к db.sqlite
        conn = sqlite3.connect(file_db)
        return conn
    except Exception as ex:
        print(str(ex))

# закрываем подключение к базе
def close_db(conn):
    try:
        # закрываем соединение с db.sqlite
        conn.commit()
    except Exception as ex:
        print(str(ex))

def select_all_id():
    conn = connect_db(path_db)
    cursor = conn.cursor()

    query = """SELECT id FROM users"""
    cursor.execute(query)

    ids = cursor.fetchall()
    close_db(conn)

    return ids

def select_all_users():
    conn = connect_db(path_db)
    cursor = conn.cursor()

    query = """SELECT * FROM users"""
    cursor.execute(query)

    users = cursor.fetchall()
    close_db(conn)

    return users    

def select_categories(user_id):
    conn = connect_db(path_db)
    cursor = conn.cursor()

    query = """SELECT categories FROM users WHERE id = {0}
    """.format(user_id)
    cursor.execute(query)

    categories = cursor.fetchall()
    close_db(conn)
    return categories    

def select_groups(user_id):
    conn = connect_db(path_db)
    cursor = conn.cursor()

    query = """SELECT groups FROM users WHERE id = {0}
    """.format(user_id)
    cursor.execute(query)

    groups = cursor.fetchall()
    close_db(conn)
    return groups    

def select_status(user_id):
    conn = connect_db(path_db)
    cursor = conn.cursor()

    query = """SELECT status FROM users WHERE id = {0}
    """.format(user_id)
    cursor.execute(query)

    status = cursor.fetchall()
    close_db(conn)

    return status   

def select_category(category):
    conn = connect_db(path_db)
    cursor = conn.cursor()

    query = """SELECT name FROM foods WHERE category = '{0}'
    """.format(category)
    cursor.execute(query)

    foods_temp = cursor.fetchall()
    close_db(conn)

    foods = []
    for food_temp in foods_temp:
        foods.append(food_temp[0])

    return foods     

def insert_user(user_id, categories, groups, status):
    conn = connect_db(path_db)
    cursor = conn.cursor()

    query = """INSERT INTO users (id, categories, groups, status)
        VALUES ('{0}', '{1}', '{2}', '{3}')
        """.format(user_id, categories, groups, status)
    cursor.execute(query)
    close_db(conn)


def edit_category(user_id, category):
    conn = connect_db(path_db)
    cursor = conn.cursor()

    categories_temp = select_categories(user_id)
    categories = ""
    for category_temp in categories_temp:
        categories += category_temp[0]
    categories += category + ", "
    categories = categories[0:-1]

    query = """UPDATE users SET categories = '{0}'
    WHERE id = '{1}'""".format(categories, user_id)
    cursor.execute(query)
    close_db(conn)


def edit_group(user_id, group):
    conn = connect_db(path_db)
    cursor = conn.cursor()
    groups_temp = select_groups(user_id)
    groups = ""
    for group_temp in groups_temp:
        groups += group_temp[0]
    groups += group + ", "
    groups = groups[0:-1]
    query = """UPDATE users SET groups = '{0}'
    WHERE id = '{1}'""".format(groups, user_id)
    cursor.execute(query)
    close_db(conn)


def edit_status(user_id, status):
    conn = connect_db(path_db)
    cursor = conn.cursor()

    query = """UPDATE users SET status = '{0}'
    WHERE id = '{1}'""".format(status, user_id)
    cursor.execute(query)
    close_db(conn)


def del_user(user_id):
    conn = connect_db(path_db)
    cursor = conn.cursor()

    query = """DELETE FROM users WHERE id = '{0}'""".format(user_id)
    cursor.execute(query)
    close_db(conn)
