from os.path import curdir

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
        self.cursor = self.db.cursor(buffered=True)

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
            return "success"
        else:
            return "username_taken"

    def delete_user(self, user_id):
        self.cursor.execute(f"DELETE FROM user WHERE id = {user_id}")
        self.db.commit()

    def login(self, username, password):
        self.create_database()

        query = self.cursor.execute("SELECT * FROM user WHERE username = %s AND password = %s",
                                    (username, password))
        return query

    def create_note(self, user_id, content, date):
        self.create_database()

        self.cursor.execute("INSERT INTO note VALUES (NULL, %s, %s, %s)",
                            (user_id, content, date))
        self.db.commit()

    def edit_note(self, note_id, content, date):
        self.create_database()

        self.cursor.execute("UPDATE note SET content = %s, date = %s WHERE id = %s",
                            (content, date, note_id))
        self.db.commit()

    def delete_note(self, note_id):
        self.cursor.execute(f"DELETE FROM note WHERE id = {note_id}")
        self.db.commit()

    def select_all_notes(self, user_id):
        self.create_database()

        query = self.cursor.execute(f"SELECT * FROM note WHERE user_id LIKE '{user_id}'")
        return query

    def select_notes_by_date(self, user_id, date):
        self.create_database()

        query = self.cursor.execute("SELECT * FROM note WHERE user_id LIKE '%s' AND date = %s",
                                    (user_id, date))
        return query


if __name__ == '__main__':
    baza = Database('notepad')

    un = "kamil"
    pw = "dda"

    # creating account
    # query_create = baza.create_user(un, pw)
    # if  query_create == "success":
    #    print("user created")
    # elif query_create == "username_taken":
    #    print("user alredy exists")

    # login
    # q = baza.login(un, pw)
    # if q is None:
    #    print("Nie mo")
    # else:
    #    print("logged")
