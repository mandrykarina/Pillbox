import sqlite3


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def addUser(self, login, password):
        try:
            self.__cur.execute(f'SELECT COUNT() as `count` FROM users WHERE login LIKE `{login}`')
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print('Пользователь с таким login уже существует')
                return False

            self.__cur.execute('INSERT INTO users VALUES(NULL, ?, ?)', (login, password))
            self.__db.commit()
        except sqlite3.Error as e:
            print('Все плохо' + str(e))
            return False

        return True

    def getUser(self, user_id):
        try:
            self.__cur.execute(f'SELECT * FROM users WHERE id = {user_id} LIMIT 1')
            res = self.__cur.fetchone()
            if not res:
                print('Пользователь пропал')
                return False
            return res
        except sqlite3.Error as e:
            print('Все плохо' + str(e))

        return False
