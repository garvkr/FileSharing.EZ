import os

class Config:
    UPLOAD_FOLDER = 'uploads'
    SECRET_KEY = 'your_secret_key_here'

app_config = Config()

# Ensure upload folder exists
os.makedirs(app_config.UPLOAD_FOLDER, exist_ok=True)