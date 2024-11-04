from flask_mysqldb import MySQL
from config import Config

mysql = MySQL()

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    @staticmethod
    def authenticate(username, password):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        return user