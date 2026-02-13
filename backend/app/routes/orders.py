from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta
from app import db
from app.models import Order, OrderItem, CartItem, Product, User

orders_bp = Blueprint('orders', __name__, url_prefix='/api/orders')

@orders_bp.route('', methods=['GET'])
@jwt_required()
def get_orders():
    """Get user's orders"""
    try:
        user_id = get_jwt_identity()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        pagination = Order.query.filter_by(user_id=user_id)\
            .order_by(Order.created_at.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'orders': [order.to_dict() for order in pagination.items],
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@orders_bp.route('/<order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    """Get order details"""
    try:
        user_id = get_jwt_identity()
        order = Order.query.filter_by(id=order_id, user_id=user_id).first()
        
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        
        return jsonify({
            'order': order.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@orders_bp.route('', methods=['POST'])
@jwt_required()
def create_order():
    """Create a new order from cart"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        
        # Validate shipping address
        if not data or 'shipping_address' not in data:
            return jsonify({'error': 'Shipping address is required'}), 400
        
        # Get cart items
        cart_items = CartItem.query.filter_by(user_id=user_id).all()
        
        if not cart_items:
            return jsonify({'error': 'Cart is empty'}), 400
        
        # Calculate total
        total_price = 0
        order_items_data = []
        
        for cart_item in cart_items:
            # Check stock
            if cart_item.product.stock < cart_item.quantity:
                return jsonify({
                    'error': f'Insufficient stock for {cart_item.product.name}'
                }), 400
            
            subtotal = cart_item.product.price * cart_item.quantity
            total_price += subtotal
            
            order_items_data.append({
                'product_id': cart_item.product_id,
                'quantity': cart_item.quantity,
                'price': cart_item.product.price
            })
        
        # Calculate tax (8% for India)
        tax = int(total_price * 0.08)
        final_total = total_price + tax
        
        # Create order
        order = Order(
            user_id=user_id,
            total_price=final_total,
            tax=tax,
            shipping_address=data['shipping_address'],
            payment_method=data.get('payment_method', 'pending'),
            status='pending'
        )
        
        db.session.add(order)
        db.session.flush()  # Get order ID
        
        # Create order items
        for item_data in order_items_data:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item_data['product_id'],
                quantity=item_data['quantity'],
                price_at_purchase=item_data['price']
            )
            db.session.add(order_item)
            
            # Reduce product stock
            product = Product.query.get(item_data['product_id'])
            product.stock -= item_data['quantity']
        
        # Clear cart
        CartItem.query.filter_by(user_id=user_id).delete()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Order created successfully',
            'order': order.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@orders_bp.route('/<order_id>', methods=['PUT'])
@jwt_required()
def update_order(order_id):
    """Update order status (admin only)"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or not user.is_admin:
            return jsonify({'error': 'Admin access required'}), 403
        
        order = Order.query.get(order_id)
        
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        
        data = request.get_json()
        
        if 'status' in data:
            valid_statuses = ['pending', 'confirmed', 'shipped', 'delivered']
            if data['status'] not in valid_statuses:
                return jsonify({'error': 'Invalid status'}), 400
            
            order.status = data['status']
            
            # Set delivery date if delivered
            if data['status'] == 'delivered':
                order.delivery_date = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Order updated successfully',
            'order': order.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@orders_bp.route('/<order_id>/confirm-payment', methods=['POST'])
@jwt_required()
def confirm_payment(order_id):
    """Confirm payment for order"""
    try:
        user_id = get_jwt_identity()
        order = Order.query.filter_by(id=order_id, user_id=user_id).first()
        
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        
        data = request.get_json()
        
        if not data or 'transaction_id' not in data:
            return jsonify({'error': 'Transaction ID is required'}), 400
        
        order.transaction_id = data['transaction_id']
        order.payment_method = data.get('payment_method', 'razorpay')
        order.status = 'confirmed'
        
        db.session.commit()
        
        return jsonify({
            'message': 'Payment confirmed',
            'order': order.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
