from flask import Blueprint, request, jsonify
from utils import s, users, authenticate

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    user = authenticate(username, password)
    if user:
        return jsonify({'message': 'Login successful', 'role': user['role']}), 200
    return jsonify({'error': 'Invalid credentials'}), 401

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.json
    email = data.get('email')
    if email in users:
        return jsonify({'error': 'User already exists'}), 400

    users[email] = {
        'password': hashlib.sha256(data['password'].encode()).hexdigest(),
        'role': 'client',
        'verified': False
    }
    encrypted_url = s.dumps(email, salt='email-confirm')
    return jsonify({'message': 'Sign-up successful', 'encrypted_url': encrypted_url}), 201

@auth_bp.route('/email-verify', methods=['POST'])
def email_verify():
    data = request.json
    encrypted_url = data.get('encrypted_url')
    try:
        email = s.loads(encrypted_url, salt='email-confirm', max_age=3600)
        if email in users:
            users[email]['verified'] = True
            return jsonify({'message': 'Email verified successfully'}), 200
    except Exception:
        return jsonify({'error': 'Invalid or expired URL'}), 400