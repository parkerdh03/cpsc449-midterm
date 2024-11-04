from flask import Flask, request, jsonify, make_response
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
import os
import jwt
from config import Config
from models import User
from services import UserService

app = Flask(__name__)
app.config.from_object(Config)

mysql = MySQL(app)

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad Request'}), 400

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({'error': 'Unauthorized'}), 401

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not Found'}), 404

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({'error': 'Internal Server Error'}), 500

@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({'error': 'File size exceeds limit'}), 413

## JWT Authentication
@app.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
    # Authenticate user
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()
    if user:
        payload = {'username': username}
        access_token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'access_token': access_token})
    return jsonify({'error': 'Invalid credentials'}), 401

## Protected Route
@app.route('/protected', methods=['GET'])
def protected():
    access_token = request.headers.get('Authorization')
    try:
        payload = jwt.decode(access_token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return jsonify({'message': f'Hello, {payload["username"]}!'})
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401

## File Upload
@app.route('/upload', methods=['GET'])
def upload_form():
    return '''
    <html>
    <form action="/upload-file" method="POST" enctype="multipart/form-data">
        <input type="file" name="file"/><br>
        <input type="submit"/>
    </form>
    </html>
    '''

## File Upload Endpoint
@app.route('/upload-file', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            filename = secure_filename(uploaded_file.filename)
            file_extension = os.path.splitext(filename)[1]
            if file_extension in app.config['ALLOWED_EXTENSIONS']:
                uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return jsonify({'message': 'File uploaded successfully'}), 201
            else:
                return jsonify({'error': 'Invalid file extension'}), 400
        else:
            return jsonify({'error': 'No file selected'}), 400
    return jsonify({'error': 'Invalid request method'}), 405

## Public Route
@app.route('/public', methods=['GET'])
def public():
    return jsonify({'message': 'Hello, Public!'})

@app.route('/users', methods=['GET'])
def get_users():
    users = UserService.get_users()
    return jsonify(users)

@app.route('/create-user', methods=['POST'])
def create_user():
    username = request.json['username']
    password = request.json['password']
    UserService.create_user(username, password)
    return jsonify({'message': 'User created'})

@app.route('/update-user', methods=['PUT'])
def update_user():
    id = request.json['id']
    username = request.json['username']
    password = request.json['password']
    UserService.update_user(id, username, password)
    return jsonify({'message': 'User updated'})

@app.route('/delete-user', methods=['DELETE'])
def delete_user():
    id = request.json['id']
    UserService.delete_user(id)
    return jsonify({'message': 'User deleted'})

if __name__ == '__main__':
    app.run(debug=True)