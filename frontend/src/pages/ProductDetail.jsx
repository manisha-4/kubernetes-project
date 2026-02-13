import { useParams, useNavigate } from 'react-router-dom'
import { useState } from 'react'
import { useCart } from '../store/cartStore'
import { catProducts } from '../data/products'

export default function ProductDetail() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [quantity, setQuantity] = useState(1)
  const [added, setAdded] = useState(false)
  const addItem = useCart(state => state.addItem)

  const product = catProducts.find(p => p.id === parseInt(id))

  if (!product) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <p className="text-3xl mb-4">😹 Product not found!</p>
          <button
            onClick={() => navigate('/')}
            className="bg-paw-orange text-white px-6 py-2 rounded-lg font-semibold hover:bg-orange-500"
          >
            Back to Shop
          </button>
        </div>
      </div>
    )
  }

  const handleAddToCart = () => {
    for (let i = 0; i < quantity; i++) {
      addItem(product)
    }
    setAdded(true)
    setTimeout(() => setAdded(false), 2000)
  }

  const relatedProducts = catProducts
    .filter(p => p.category === product.category && p.id !== product.id)
    .slice(0, 4)

  return (
    <div className="min-h-screen bg-paw-pale-pink polka-pink py-8">
      <div className="max-w-6xl mx-auto px-4">
        {/* Back Button */}
        <button
          onClick={() => navigate('/')}
          className="mb-8 flex items-center gap-2 text-paw-pink font-semibold hover:text-paw-light-pink"
        >
          ← Back to Shop
        </button>

        <div className="grid md:grid-cols-2 gap-8 mb-12 bg-white p-8 rounded-lg shadow-lg">
          {/* Product Image */}
          <div className="flex items-center justify-center">
            <div className="text-9xl">{product.image}</div>
          </div>

          {/* Product Info */}
          <div>
            <h1 className="text-4xl font-bold text-paw-dark mb-4">{product.name}</h1>
            
            <div className="flex items-center gap-4 mb-6">
              <div className="flex items-center gap-2">
                <span className="text-3xl">⭐</span>
                <span className="text-2xl font-bold">{product.rating}</span>
              </div>
              <span className="text-gray-600">({product.reviews} reviews)</span>
            </div>

            <p className="text-xl text-gray-700 mb-6">{product.description}</p>

            <div className="mb-6">
              <span className="text-4xl font-bold text-paw-pink">
                ₹{product.price.toLocaleString('en-IN')}
              </span>
              {product.stock < 10 && product.stock > 0 && (
                <p className="text-orange-600 font-semibold mt-2">
                  ⚠️ Only {product.stock} left in stock!
                </p>
              )}
              {product.stock === 0 && (
                <p className="text-red-600 font-semibold mt-2">Out of Stock</p>
              )}
            </div>

            {/* Quantity Selector */}
            <div className="flex items-center gap-4 mb-6">
              <label className="font-semibold text-gray-700">Quantity:</label>
              <div className="flex items-center border-2 border-paw-pink rounded-lg">
                <button
                  onClick={() => setQuantity(Math.max(1, quantity - 1))}
                  className="px-4 py-2 text-paw-pink font-bold hover:bg-paw-pale-pink transition"
                >
                  −
                </button>
                <input
                  type="number"
                  min="1"
                  max={product.stock}
                  value={quantity}
                  onChange={(e) => setQuantity(Math.max(1, Math.min(product.stock, parseInt(e.target.value) || 1)))}
                  className="w-16 text-center font-bold border-0 outline-none"
                />
                <button
                  onClick={() => setQuantity(Math.min(product.stock, quantity + 1))}
                  className="px-4 py-2 text-paw-pink font-bold hover:bg-paw-pale-pink transition"
                >
                  +
                </button>
              </div>
            </div>

            {/* Add to Cart Button */}
            <button
              onClick={handleAddToCart}
              disabled={product.stock === 0}
              className={`w-full py-3 rounded-lg font-bold text-lg transition-all mb-4 ${
                product.stock === 0
                  ? 'bg-gray-300 text-gray-600 cursor-not-allowed'
                  : added
                  ? 'bg-green-500 text-white'
                  : 'bg-paw-pink text-white hover:bg-paw-light-pink shadow-lg'
              }`}
            >
              {added ? '✅ Added to Cart!' : 'Add to Cart 🛒'}
            </button>

            <button
              onClick={() => navigate('/cart')}
              className="w-full py-2 border-2 border-paw-pink text-paw-pink rounded-lg font-bold hover:bg-paw-pale-pink transition"
            >
              View Cart
            </button>

            {/* Product Details */}
            <div className="mt-8 pt-8 border-t-2 border-gray-200">
              <h3 className="text-xl font-bold text-paw-dark mb-4">Product Details</h3>
              <ul className="space-y-2 text-gray-700">
                <li>✅ Free shipping on orders over $50</li>
                <li>✅ 30-day money back guarantee</li>
                <li>✅ Loved by cats everywhere</li>
                <li>✅ Fast delivery (2-3 business days)</li>
              </ul>
            </div>
          </div>
        </div>

        {/* Related Products */}
        {relatedProducts.length > 0 && (
          <div>
            <h2 className="text-3xl font-bold text-paw-dark mb-6">Related Products 🐾</h2>
            <div className="grid md:grid-cols-4 gap-4">
              {relatedProducts.map(p => (
                <div
                  key={p.id}
                  onClick={() => navigate(`/product/${p.id}`)}
                  className="bg-white p-4 rounded-lg shadow-md hover:shadow-xl cursor-pointer transition-all"
                >
                  <div className="text-6xl text-center mb-2">{p.image}</div>
                  <h3 className="font-semibold text-paw-dark line-clamp-2 mb-2">{p.name}</h3>
                  <p className="text-paw-orange font-bold">${p.price.toFixed(2)}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
