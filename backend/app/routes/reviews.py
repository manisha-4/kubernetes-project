from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Review, Product, User, Order, OrderItem

reviews_bp = Blueprint('reviews', __name__, url_prefix='/api/reviews')

@reviews_bp.route('/product/<product_id>', methods=['GET'])
def get_product_reviews(product_id):
    """Get all reviews for a product"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        pagination = Review.query.filter_by(product_id=product_id)\
            .order_by(Review.created_at.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'reviews': [review.to_dict() for review in pagination.items],
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reviews_bp.route('/product/<product_id>', methods=['POST'])
@jwt_required()
def create_review(product_id):
    """Create a review for a product"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        product = Product.query.get(product_id)
        
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        data = request.get_json()
        
        # Validate
        if not data or 'rating' not in data:
            return jsonify({'error': 'Rating is required'}), 400
        
        rating = int(data['rating'])
        
        if rating < 1 or rating > 5:
            return jsonify({'error': 'Rating must be between 1 and 5'}), 400
        
        # Check if user has purchased this product
        order_item = OrderItem.query.join(Order).filter(
            Order.user_id == user_id,
            OrderItem.product_id == product_id,
            Order.status == 'delivered'
        ).first()
        
        is_verified = order_item is not None
        
        # Check if user already reviewed
        existing_review = Review.query.filter_by(
            product_id=product_id,
            user_id=user_id
        ).first()
        
        if existing_review:
            # Update review
            existing_review.rating = rating
            existing_review.comment = data.get('comment', '')
            existing_review.is_verified = is_verified
            review = existing_review
        else:
            # Create new review
            review = Review(
                product_id=product_id,
                user_id=user_id,
                rating=rating,
                comment=data.get('comment', ''),
                is_verified=is_verified
            )
            db.session.add(review)
            product.review_count += 1
        
        # Update product rating
        avg_rating = db.session.query(db.func.avg(Review.rating))\
            .filter_by(product_id=product_id).scalar()
        product.rating = float(avg_rating) if avg_rating else 0
        
        db.session.commit()
        
        return jsonify({
            'message': 'Review submitted successfully',
            'review': review.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@reviews_bp.route('/<review_id>', methods=['PUT'])
@jwt_required()
def update_review(review_id):
    """Update a review"""
    try:
        user_id = get_jwt_identity()
        review = Review.query.get(review_id)
        
        if not review:
            return jsonify({'error': 'Review not found'}), 404
        
        if review.user_id != user_id:
            return jsonify({'error': 'You can only edit your own reviews'}), 403
        
        data = request.get_json()
        
        if 'rating' in data:
            rating = int(data['rating'])
            if rating < 1 or rating > 5:
                return jsonify({'error': 'Rating must be between 1 and 5'}), 400
            review.rating = rating
        
        if 'comment' in data:
            review.comment = data['comment']
        
        # Update product rating
        product = review.product
        avg_rating = db.session.query(db.func.avg(Review.rating))\
            .filter_by(product_id=product.id).scalar()
        product.rating = float(avg_rating) if avg_rating else 0
        
        db.session.commit()
        
        return jsonify({
            'message': 'Review updated successfully',
            'review': review.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@reviews_bp.route('/<review_id>', methods=['DELETE'])
@jwt_required()
def delete_review(review_id):
    """Delete a review"""
    try:
        user_id = get_jwt_identity()
        review = Review.query.get(review_id)
        
        if not review:
            return jsonify({'error': 'Review not found'}), 404
        
        if review.user_id != user_id:
            return jsonify({'error': 'You can only delete your own reviews'}), 403
        
        product = review.product
        product.review_count = max(0, product.review_count - 1)
        
        db.session.delete(review)
        
        # Update product rating
        avg_rating = db.session.query(db.func.avg(Review.rating))\
            .filter_by(product_id=product.id).scalar()
        product.rating = float(avg_rating) if avg_rating else 0
        
        db.session.commit()
        
        return jsonify({
            'message': 'Review deleted successfully'
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@reviews_bp.route('/<review_id>/helpful', methods=['POST'])
def mark_helpful(review_id):
    """Mark review as helpful"""
    try:
        review = Review.query.get(review_id)
        
        if not review:
            return jsonify({'error': 'Review not found'}), 404
        
        review.helpful_count += 1
        db.session.commit()
        
        return jsonify({
            'message': 'Marked as helpful',
            'helpful_count': review.helpful_count
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
