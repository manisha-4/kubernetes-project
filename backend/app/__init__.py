from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate
from config import get_config

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

def create_app(config=None):
    """Application factory"""
    app = Flask(__name__)
    
    # Load config
    if config is None:
        config = get_config()
    app.config.from_object(config)
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    CORS(app, origins=config.CORS_ORIGINS)
    
    # Register blueprints
    from app.routes import auth_bp, products_bp, cart_bp, orders_bp, reviews_bp, users_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(reviews_bp)
    app.register_blueprint(users_bp)
    
    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health():
        return {'status': 'ok', 'message': 'Cat eCommerce API is running'}, 200
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app
