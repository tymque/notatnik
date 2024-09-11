import _mysql_connector
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
        self.cursor = db.cursor()


if __name__ == '__main__':
    baza = Database('notepad')
