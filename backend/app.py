#!/usr/bin/env python
"""Flask application entry point"""
import os
from app import create_app, db
from app.models import User, Product, CartItem, Order, OrderItem, Review

# Create app
app = create_app()

@app.shell_context_processor
def make_shell_context():
    """Add models to shell context"""
    return {
        'db': db,
        'User': User,
        'Product': Product,
        'CartItem': CartItem,
        'Order': Order,
        'OrderItem': OrderItem,
        'Review': Review
    }

@app.before_request
def before_request():
    """Log incoming requests"""
    pass

@app.after_request
def after_request(response):
    """Add CORS headers"""
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    return response

@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return {'error': 'Not found'}, 404

@app.errorhandler(500)
def internal_error(error):
    """500 error handler"""
    db.session.rollback()
    return {'error': 'Internal server error'}, 500

if __name__ == '__main__':
    # Create tables
    with app.app_context():
        db.create_all()
    
    # Run app
    debug = os.getenv('FLASK_ENV') == 'development'
    port = int(os.getenv('PORT', 5001))  # Use 5001 to avoid AirPlay conflicts
    app.run(host='0.0.0.0', port=port, debug=debug)
