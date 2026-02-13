from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import CartItem, Product, User

cart_bp = Blueprint('cart', __name__, url_prefix='/api/cart')

@cart_bp.route('', methods=['GET'])
@jwt_required()
def get_cart():
    """Get user's shopping cart"""
    try:
        user_id = get_jwt_identity()
        cart_items = CartItem.query.filter_by(user_id=user_id).all()
        
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        total_items = sum(item.quantity for item in cart_items)
        
        return jsonify({
            'items': [item.to_dict() for item in cart_items],
            'total_items': total_items,
            'total_price': total_price
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@cart_bp.route('', methods=['POST'])
@jwt_required()
def add_to_cart():
    """Add item to cart"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data or 'product_id' not in data:
            return jsonify({'error': 'Missing product_id'}), 400
        
        product_id = data['product_id']
        quantity = int(data.get('quantity', 1))
        
        if quantity <= 0:
            return jsonify({'error': 'Quantity must be greater than 0'}), 400
        
        # Check if product exists
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        # Check stock
        if product.stock < quantity:
            return jsonify({'error': f'Only {product.stock} items available'}), 400
        
        # Check if item already in cart
        cart_item = CartItem.query.filter_by(user_id=user_id, product_id=product_id).first()
        
        if cart_item:
            # Update quantity
            cart_item.quantity += quantity
            if cart_item.quantity > product.stock:
                return jsonify({'error': f'Only {product.stock} items available'}), 400
        else:
            # Add new item
            cart_item = CartItem(user_id=user_id, product_id=product_id, quantity=quantity)
            db.session.add(cart_item)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Item added to cart',
            'cart_item': cart_item.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@cart_bp.route('/<item_id>', methods=['PUT'])
@jwt_required()
def update_cart_item(item_id):
    """Update cart item quantity"""
    try:
        user_id = get_jwt_identity()
        cart_item = CartItem.query.filter_by(id=item_id, user_id=user_id).first()
        
        if not cart_item:
            return jsonify({'error': 'Cart item not found'}), 404
        
        data = request.get_json()
        
        if 'quantity' not in data:
            return jsonify({'error': 'Missing quantity'}), 400
        
        quantity = int(data['quantity'])
        
        if quantity <= 0:
            return jsonify({'error': 'Quantity must be greater than 0'}), 400
        
        # Check stock
        if cart_item.product.stock < quantity:
            return jsonify({'error': f'Only {cart_item.product.stock} items available'}), 400
        
        cart_item.quantity = quantity
        db.session.commit()
        
        return jsonify({
            'message': 'Cart item updated',
            'cart_item': cart_item.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@cart_bp.route('/<item_id>', methods=['DELETE'])
@jwt_required()
def remove_from_cart(item_id):
    """Remove item from cart"""
    try:
        user_id = get_jwt_identity()
        cart_item = CartItem.query.filter_by(id=item_id, user_id=user_id).first()
        
        if not cart_item:
            return jsonify({'error': 'Cart item not found'}), 404
        
        db.session.delete(cart_item)
        db.session.commit()
        
        return jsonify({
            'message': 'Item removed from cart'
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@cart_bp.route('', methods=['DELETE'])
@jwt_required()
def clear_cart():
    """Clear entire cart"""
    try:
        user_id = get_jwt_identity()
        CartItem.query.filter_by(user_id=user_id).delete()
        db.session.commit()
        
        return jsonify({
            'message': 'Cart cleared'
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
