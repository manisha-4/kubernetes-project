from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import User

users_bp = Blueprint('users', __name__, url_prefix='/api/users')

@users_bp.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    """Get public user information"""
    try:
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Return limited public info
        public_info = {
            'id': user.id,
            'username': user.username,
            'created_at': user.created_at.isoformat()
        }
        
        return jsonify({'user': public_info}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/admin/list', methods=['GET'])
@jwt_required()
def list_users():
    """Get all users (admin only)"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or not user.is_admin:
            return jsonify({'error': 'Admin access required'}), 403
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        pagination = User.query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'users': [u.to_dict() for u in pagination.items],
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/admin/<user_id>/toggle-admin', methods=['PUT'])
@jwt_required()
def toggle_admin(user_id):
    """Toggle admin status for user (admin only)"""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.is_admin:
            return jsonify({'error': 'Admin access required'}), 403
        
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        user.is_admin = not user.is_admin
        db.session.commit()
        
        return jsonify({
            'message': 'User admin status updated',
            'user': user.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@users_bp.route('/admin/<user_id>/toggle-active', methods=['PUT'])
@jwt_required()
def toggle_active(user_id):
    """Toggle active status for user (admin only)"""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.is_admin:
            return jsonify({'error': 'Admin access required'}), 403
        
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        user.is_active = not user.is_active
        db.session.commit()
        
        return jsonify({
            'message': 'User active status updated',
            'user': user.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
