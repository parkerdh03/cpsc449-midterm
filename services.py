from flask_mysqldb import MySQL

mysql = MySQL()

class UserService:
    @staticmethod
    def get_users():
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        return users

    @staticmethod
    def create_user(username, password):
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        mysql.connection.commit()

    @staticmethod
    def update_user(id, username, password):
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE users SET username=%s, password=%s WHERE id=%s", (username, password, id))
        mysql.connection.commit()

    @staticmethod
    def delete_user(id):
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM users WHERE id=%s", (id,))
        mysql.connection.commit()