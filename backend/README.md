# Backend API Documentation

## Cat E-Commerce Backend API

A complete Flask-based REST API for a cat e-commerce platform.

### Features
- ✅ User authentication with JWT
- ✅ Product catalog management
- ✅ Shopping cart functionality
- ✅ Order management
- ✅ Product reviews and ratings
- ✅ Admin dashboard support
- ✅ Database models with relationships

### Tech Stack
- Flask 2.3
- SQLAlchemy ORM
- PostgreSQL
- JWT Authentication
- Marshmallow for serialization

### Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env with your configuration

# Initialize database
python seed.py
```

### Running the Application

```bash
# Development
export FLASK_ENV=development
flask run

# Production
gunicorn --bind 0.0.0.0:5000 app:app
```

### Database Models

#### User
- id, username, email, password_hash
- phone, address, city, state, postal_code, country
- is_admin, is_active
- Relationships: orders, reviews, cart_items

#### Product
- id, name, description, price (in paisa)
- category, image_url, stock
- rating, review_count, is_active
- Relationships: reviews, order_items, cart_items

#### CartItem
- id, user_id, product_id, quantity
- Relationships: user, product

#### Order
- id, user_id, total_price, tax, status
- shipping_address, payment_method, transaction_id
- order_date, delivery_date
- Relationships: user, items (OrderItem)

#### OrderItem
- id, order_id, product_id, quantity
- price_at_purchase
- Relationships: order, product

#### Review
- id, product_id, user_id, rating (1-5)
- comment, is_verified, helpful_count
- Relationships: product, user

### API Endpoints

#### Authentication
- `POST /api/auth/register` - Register user
- `POST /api/auth/login` - Login user
- `GET /api/auth/profile` - Get user profile (JWT required)
- `PUT /api/auth/profile` - Update profile (JWT required)
- `POST /api/auth/change-password` - Change password (JWT required)

#### Products
- `GET /api/products` - List all products
- `GET /api/products/<id>` - Get product details
- `POST /api/products` - Create product (admin only)
- `PUT /api/products/<id>` - Update product (admin only)
- `DELETE /api/products/<id>` - Delete product (admin only)
- `GET /api/products/categories` - Get categories

#### Shopping Cart
- `GET /api/cart` - Get cart (JWT required)
- `POST /api/cart` - Add to cart (JWT required)
- `PUT /api/cart/<item_id>` - Update quantity (JWT required)
- `DELETE /api/cart/<item_id>` - Remove item (JWT required)
- `DELETE /api/cart` - Clear cart (JWT required)

#### Orders
- `GET /api/orders` - Get user orders (JWT required)
- `GET /api/orders/<id>` - Get order details (JWT required)
- `POST /api/orders` - Create order (JWT required)
- `PUT /api/orders/<id>` - Update order status (admin only)
- `POST /api/orders/<id>/confirm-payment` - Confirm payment (JWT required)

#### Reviews
- `GET /api/reviews/product/<product_id>` - Get product reviews
- `POST /api/reviews/product/<product_id>` - Create review (JWT required)
- `PUT /api/reviews/<id>` - Update review (JWT required)
- `DELETE /api/reviews/<id>` - Delete review (JWT required)
- `POST /api/reviews/<id>/helpful` - Mark helpful

#### Users (Admin)
- `GET /api/users/<id>` - Get user info
- `GET /api/users/admin/list` - List all users (admin only)
- `PUT /api/users/admin/<id>/toggle-admin` - Toggle admin (admin only)
- `PUT /api/users/admin/<id>/toggle-active` - Toggle active (admin only)

### Example Usage

```bash
# Register
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"john","email":"john@example.com","password":"password123"}'

# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"john@example.com","password":"password123"}'

# Get products
curl http://localhost:5000/api/products

# Add to cart (with JWT token)
curl -X POST http://localhost:5000/api/cart \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"product_id":"xxx","quantity":1}'
```

### Environment Variables

See `.env.example` for all configuration options.

Key variables:
- `FLASK_ENV` - development/production
- `DATABASE_URL` - PostgreSQL connection string
- `JWT_SECRET_KEY` - JWT signing key
- `CORS_ORIGINS` - Allowed origins

### Deployment

For EKS deployment, see the Kubernetes manifests in the project root.

### License

MIT
