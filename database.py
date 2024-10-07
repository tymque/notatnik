import mysql.connector
import time
from configparser import ConfigParser


class Database:
    def __init__(self):
        config = ConfigParser()

        config.read('config.ini')
        database_host = config.get('DATABASE', 'host')
        database_user = config.get('DATABASE', 'user')
        database_password = config.get('DATABASE', 'password')
        database_name = config.get('DATABASE', 'name')

        db = mysql.connector.connect(
            host=database_host,
            user=database_user,
            password=database_password
        )
        cursor = db.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
        cursor.close()
        db.close()

        self.db = mysql.connector.connect(
            host=database_host,
            user=database_user,
            password=database_password,
            database=database_name
        )
        self.cursor = self.db.cursor(buffered=True)

    def create_database(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS user(
            id int PRIMARY KEY AUTO_INCREMENT,
            username varchar(50),
            password varchar(256)
            )
            ''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS note(
            id int PRIMARY KEY AUTO_INCREMENT,
            user_id int,
            content text,
            date timestamp,
            FOREIGN KEY (user_id) REFERENCES user(id)
            )
            ''')
        self.db.commit()

    def create_user(self, username, password):
        self.create_database()

        self.cursor.execute(f"SELECT * FROM user WHERE username LIKE '{username}'")
        if self.cursor.rowcount == 0:
            self.cursor.execute("INSERT INTO user VALUES (NULL, %s, SHA2(%s, 256))",
                                (username, password))
            self.db.commit()
            return "success"
        else:
            return "username_taken"

    def delete_user(self, uid):
        self.cursor.execute(f"DELETE FROM note WHERE user_id = {uid}")
        self.cursor.execute(f"DELETE FROM user WHERE id = {uid}")
        self.db.commit()

    def login(self, username, password):
        self.create_database()

        self.cursor.execute("SELECT * FROM user WHERE username = %s AND password = SHA2(%s, 256)",
                            (username, password))
        return self.cursor.fetchone()

    def create_note(self, user_id, content):
        self.create_database()

        self.cursor.execute("INSERT INTO note VALUES (NULL, %s, %s, NULL)",
                            (user_id, content))
        self.db.commit()

    def edit_note(self, note_id, content):
        self.create_database()

        self.cursor.execute("UPDATE note SET content = %s, date = NULL WHERE id = %s",
                            (content, note_id))
        self.db.commit()

    def delete_note(self, note_id):
        self.cursor.execute(f"DELETE FROM note WHERE id = {note_id}")
        self.db.commit()

    def select_all_notes(self, user_id):
        self.create_database()

        self.cursor.execute(f"SELECT * FROM note WHERE user_id LIKE '{user_id}' ORDER BY date DESC")
        return self.cursor.fetchall()

    def select_notes_by_date(self, user_id, date):
        self.create_database()

        self.cursor.execute("SELECT * FROM note WHERE user_id LIKE '%s' AND date = %s",
                            (user_id, date))
        return self.cursor.fetchall()

    def search(self, user_id, phrase):
        self.create_database()

        self.cursor.execute(f"SELECT * FROM note WHERE content LIKE '%{phrase}%' AND user_id = {user_id}")
        return self.cursor.fetchall()


if __name__ == '__main__':
    Base = Database()

    user_id = None
    user_username = None
    user_password = None

    while True:
        print("+------------------------+-----------------------+-----------------------+\n"
              "| 1 - opcje użytkownika  |   2 - opcje notatek   |      0 - zamknij      |\n"
              "+------------------------+-----------------------+-----------------------+")
        i = int(input("Wybierz opcję: "))

        if i == 1:
            while True:
                print(
                    "+--------------------+--------------------+--------------------+--------------------+\n"
                    "|  1 - utwórz konto  |  2 - zaloguj się   |   3 - usuń konto   |     0 - powrót     |\n"
                    "+--------------------+--------------------+--------------------+--------------------+")
                u = int(input("Wybierz opcję: "))

                if u == 1:
                    un = input("Podaj login:")
                    pw = input("Podaj hasło:")
                    query_create = Base.create_user(un, pw)
                    if query_create == "success":
                        print("Utworzono konto")
                    elif query_create == "username_taken":
                        print("Konto o podanym loginie istnieje")

                elif u == 2:
                    un = input("Podaj login:")
                    pw = input("Podaj hasło:")
                    query_login = Base.login(un, pw)
                    if query_login is None:
                        print("Błędne dane logowawnia")
                    else:
                        user_id = query_login[0]
                        user_username = query_login[1]
                        user_password = query_login[2]
                        print("Zalogowano pomyślnie")
                        break
                elif u == 3:
                    if user_id is None:
                        print("Nie zalogowano")
                    else:
                        Base.delete_user(user_id)
                        print("Usunięto konto")
                elif u == 0:
                    break
                else:
                    print("Nieprawidłowe dane")
        elif i == 2:
            while True:
                print(
                    "+------------------+------------------+------------------+------------------+------------------+\n"
                    "| 1 - nowa notatka |   2 - edytuj     |   3 - wyświetl   |     4 - usuń     |    0 - powrót    |\n"
                    "+------------------+------------------+------------------+------------------+------------------+")
                n = int(input("Wybierz opcję: "))

                if n == 1:
                    if user_id is None:
                        print("Najpierw się zaloguj")
                        break
                    else:
                        content = input("Wpisz treść notatki:")
                        date = time.time()
                        Base.create_note(user_id, content)
                        print("Utworzono notatkę")

                elif n == 2:
                    note_id = input("Podaj id notatki:")
                    new_content = input("Wpisz nową treść notatki:")
                    date = time.time()
                    Base.edit_note(note_id, new_content)
                    print("Edytowano notatkę")
                elif n == 3:
                    if user_id is None:
                        print("Najpierw się zaloguj")
                        break
                    else:
                        select_query = Base.select_all_notes(user_id)
                        if len(select_query) == 0:
                            print("Brak notatek")
                        else:
                            for row in select_query:
                                date = str(row[3].strftime("%d.%m.%Y, %H:%M"))
                                print(f"{row[2]} | {date}")
                elif n == 4:
                    note_id = int(input("Podaj id notatki:"))
                    Base.delete_note(note_id)
                elif n == 0:
                    break
                else:
                    print("Nieprawidłowe dane")
        elif i == 0:
            break
        else:
            print("Nieprawidłowe dane")
