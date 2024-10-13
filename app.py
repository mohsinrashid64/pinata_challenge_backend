# app.py
from flask import Flask
from flask_cors import CORS
from config import Config
from models import db
from routes.test import test_bp
from routes.crud.read import read_bp 
from routes.crud.create import create_bp 
from routes.crud.delete import delete_bp



app = Flask(__name__)
CORS(app)

def create_app():
    app.config.from_object(Config)

    db.init_app(app)
    app.register_blueprint(test_bp)
    app.register_blueprint(read_bp)
    app.register_blueprint(delete_bp)
    app.register_blueprint(create_bp)

    with app.app_context():
        db.create_all()  # Create tables

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
