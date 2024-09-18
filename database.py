import mysql.connector


class Database:
    def __init__(self, database_name):
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""
        )
        cursor = db.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
        cursor.close()
        db.close()

        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database=database_name
        )
        self.cursor = self.db.cursor()

    def create_database(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS user(
            id int PRIMARY KEY AUTO_INCREMENT,
            username varchar(50),
            password varchar(100)
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
            self.cursor.execute("INSERT INTO user VALUES (NULL, %s, %s)",
                                (username, password))
            self.db.commit()
            return True

    def login(self, username, password):
        self.create_database()

        query = self.cursor.execute("SELECT * FROM user WHERE username = %s AND password = %s",
                                    (username, password))
        return query


if __name__ == '__main__':
    baza = Database('notepad')

    un = "kamil"
    pw = "dda"

    query = baza.create_user(un, pw)
    if query:
        print("created")
    else:
        print("username taken")

    # if baza.login(un, pw):
    #    print("hooi")
    # else:
    #    print("logged")
