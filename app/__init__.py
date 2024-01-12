from flask import Flask
from flask_pymongo import PyMongo
from config import Config
import cloudinary
from flask_cors import CORS

db = None

def init_db(mongo):
    global db
    db = mongo.db

def register_blueprints(app):
    from app.routes.post_routes import post_bp
    from app.routes.user_routes import user_bp 
    from app.routes.file_routes import file_bp # Import Blueprints
    app.register_blueprint(post_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(file_bp)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    mongo = PyMongo(app)
    init_db(mongo)

    CORS(app, supports_credentials=True)
    cloudinary.config(cloud_name = Config.CLOUD_NAME, api_key=Config.API_KEY, 
    api_secret=Config.API_SECRET)

    register_blueprints(app)
    
    return app
