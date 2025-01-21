from flask import Flask
from config import app_config
from routes import auth_routes, file_routes

app = Flask(__name__)

# Configuration
app.config.from_object(app_config)

# Register Blueprints
app.register_blueprint(auth_routes.auth_bp)
app.register_blueprint(file_routes.file_bp)

if __name__ == '__main__':
    app.run(debug=True)
    