import sqlite3 as sql


def create_user_password_table():
    with sql.connect('database.db') as conn:
        cur = conn.cursor()
        try:
            cur.execute('''
                    CREATE TABLE users (
                        username VARCHAR(50) PRIMARY KEY,
                        password VARCHAR(50)
                    )''')
        except Exception as e:
            pass

        conn.commit()


def create_user_squares_table():
    with sql.connect('database.db') as conn:
        cur = conn.cursor()
        try:
            cur.execute('''
                    CREATE TABLE squares (
                        username VARCHAR(50),
                        x_coord INT,
                        y_coord INT,
                        PRIMARY KEY(username, x_coord, y_coord)
                    )''')
        except Exception as e:
            pass

        conn.commit()


def drop_tables():
    with sql.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute('DROP TABLE IF EXISTS users')
        cur.execute('DROP TABLE IF EXISTS squares')


def add_user(username, password):
    with sql.connect('database.db') as conn:
        cur = conn.cursor()
        query = '''
                INSERT INTO users (username, password)
                    VALUES ('{}', '{}')'''.format(username, password)
        cur.execute(query)
        conn.commit()


def is_name_unique(username):
    with sql.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute('''
                SELECT 
                    *
                FROM
                    users
                WHERE users.username = '{}' '''.format(username))

        return len(cur.fetchall()) == 0


def check_password(username, password):
    with sql.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute('''
                    SELECT 
                        users.password
                    FROM
                        users
                    WHERE users.username = '{}' '''.format(username))

        result = cur.fetchone()
        if result is not None:
            return password == result[0]
        return False


def add_square(user, coords):
    with sql.connect('database.db') as conn:
        cur = conn.cursor()
        if coords[0] is None:
            query = '''
                    INSERT INTO squares
                        VALUES ('{}', Null, Null)'''.format(user)
        else:
            query = '''
                    INSERT INTO squares
                        VALUES ('{}', {}, {})'''.format(user, coords[0], coords[1])

        cur.execute(query)
        conn.commit()


def get_squares(username):
    with sql.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute('''
                    SELECT 
                        squares.x_coord,
                        squares.y_coord
                    FROM
                        squares
                    WHERE squares.username = '{}' '''.format(username))

        return cur.fetchall()





