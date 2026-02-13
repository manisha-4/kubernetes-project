# Seed database with cat products
from app import create_app, db
from app.models import Product, User
import os

app = create_app()

def seed_products():
    """Seed database with cat products"""
    with app.app_context():
        # Clear existing products
        Product.query.delete()
        
        products = [
            {
                'name': 'Premium Cat Food - Salmon Delight',
                'description': 'High-protein salmon-based dry food with essential nutrients for healthy cats',
                'price': 2074,
                'category': 'food',
                'stock': 50,
                'rating': 4.8,
                'review_count': 156
            },
            {
                'name': 'Catnip Mouse Toy',
                'description': 'Interactive toy filled with 100% natural catnip. Hours of entertainment!',
                'price': 835,
                'category': 'toys',
                'stock': 120,
                'rating': 4.9,
                'review_count': 423
            },
            {
                'name': 'Cozy Cat Bed',
                'description': 'Soft, warm bed perfect for napping. Machine washable cover.',
                'price': 4174,
                'category': 'beds',
                'stock': 30,
                'rating': 4.7,
                'review_count': 89
            },
            {
                'name': 'Automatic Cat Feeder',
                'description': 'Smart feeder with timer. Keep your cat on schedule!',
                'price': 7507,
                'category': 'accessories',
                'stock': 25,
                'rating': 4.6,
                'review_count': 234
            },
            {
                'name': 'Cat Scratching Post',
                'description': 'Tall scratching post with multiple levels and hiding spots',
                'price': 6676,
                'category': 'furniture',
                'stock': 15,
                'rating': 4.8,
                'review_count': 345
            },
            {
                'name': 'Grooming Brush Kit',
                'description': 'Complete grooming set: brush, comb, nail clipper, and more',
                'price': 2912,
                'category': 'grooming',
                'stock': 60,
                'rating': 4.7,
                'review_count': 198
            },
            {
                'name': 'Interactive Laser Toy',
                'description': 'USB-rechargeable laser pointer for active play sessions',
                'price': 1668,
                'category': 'toys',
                'stock': 90,
                'rating': 4.9,
                'review_count': 567
            },
            {
                'name': 'Cat Treats - Tuna Flavor',
                'description': 'Delicious, healthy treats made with real tuna. No artificial flavors.',
                'price': 1086,
                'category': 'food',
                'stock': 100,
                'rating': 4.9,
                'review_count': 678
            },
        ]
        
        for product_data in products:
            product = Product(**product_data)
            db.session.add(product)
        
        db.session.commit()
        print('✅ Products seeded successfully!')

def create_admin_user():
    """Create admin user"""
    with app.app_context():
        # Check if admin exists
        admin = User.query.filter_by(username='admin').first()
        
        if not admin:
            admin = User(
                username='admin',
                email='admin@catshop.com',
                phone='9999999999',
                is_admin=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print('✅ Admin user created!')
            print('   Username: admin')
            print('   Email: admin@catshop.com')
            print('   Password: admin123')
        else:
            print('ℹ️  Admin user already exists')

if __name__ == '__main__':
    print('🌱 Seeding database...')
    seed_products()
    create_admin_user()
    print('✨ Database seeding completed!')
