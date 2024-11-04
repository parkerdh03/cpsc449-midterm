class Config:
    SECRET_KEY = 'your_secret_key'
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'password'
    MYSQL_DB = 'flask_api_db'
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'pdf'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024 #16MB