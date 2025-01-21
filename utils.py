import hashlib
from itsdangerous import URLSafeTimedSerializer
from config import app_config

s = URLSafeTimedSerializer(app_config.SECRET_KEY)

# Allowed file extensions for Ops User
ALLOWED_EXTENSIONS = {'pptx', 'docx', 'xlsx'}

users = {
    'ops_user': {
        'password': hashlib.sha256('ops_password'.encode()).hexdigest(),
        'role': 'ops',
    }
}
uploaded_files = []  # List to track uploaded files

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def authenticate(username, password):
    user = users.get(username)
    if user and user['password'] == hashlib.sha256(password.encode()).hexdigest():
        return user
    return None