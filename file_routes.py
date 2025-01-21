from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename
from utils import app_config, authenticate, allowed_file, uploaded_files, s
import os

file_bp = Blueprint('file', __name__)

@file_bp.route('/upload', methods=['POST'])
def upload_file():
    username = request.form.get('username')
    password = request.form.get('password')
    user = authenticate(username, password)
    if not user or user['role'] != 'ops':
        return jsonify({'error': 'Unauthorized'}), 403

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app_config.UPLOAD_FOLDER, filename)
        file.save(filepath)
        uploaded_files.append(filename)
        return jsonify({'message': 'File uploaded successfully'}), 201
    return jsonify({'error': 'Invalid file type'}), 400

@file_bp.route('/download', methods=['POST'])
def download_file():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    filename = data.get('filename')
    user = authenticate(username, password)

    if not user or user['role'] != 'client' or not users[username].get('verified'):
        return jsonify({'error': 'Unauthorized'}), 403

    if filename not in uploaded_files:
        return jsonify({'error': 'File not found'}), 404

    encrypted_url = s.dumps({'filename': filename, 'username': username}, salt='file-download')
    return jsonify({'download_url': encrypted_url}), 200

@file_bp.route('/fetch-file/<token>', methods=['GET'])
def fetch_file(token):
    try:
        data = s.loads(token, salt='file-download', max_age=3600)
        filename = data['filename']
        username = data['username']

        if username in users and users[username]['role'] == 'client':
            filepath = os.path.join(app_config.UPLOAD_FOLDER, filename)
            if os.path.exists(filepath):
                return send_file(filepath, as_attachment=True)
        return jsonify({'error': 'Unauthorized access'}), 403
    except Exception:
        return jsonify({'error': 'Invalid or expired URL'}), 400

@file_bp.route('/list-files', methods=['POST'])
def list_files():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    user = authenticate(username, password)

    if not user or user['role'] != 'client' or not users[username].get('verified'):
        return jsonify({'error': 'Unauthorized'}), 403

    return jsonify({'files': uploaded_files}), 200