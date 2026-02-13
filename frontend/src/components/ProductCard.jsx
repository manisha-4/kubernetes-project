import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useCart } from '../store/cartStore'

export default function ProductCard({ product }) {
  const [showAdded, setShowAdded] = useState(false)
  const addItem = useCart(state => state.addItem)

  const handleAddToCart = () => {
    addItem(product)
    setShowAdded(true)
    setTimeout(() => setShowAdded(false), 1500)
  }

  return (
    <Link to={`/product/${product.id}`}>
      <div className="bg-white rounded-lg shadow-md hover:shadow-xl transition-shadow p-4 cursor-pointer h-full flex flex-col">
        <div className="text-6xl mb-4 flex justify-center">
          {product.image}
        </div>
        <h3 className="text-lg font-semibold text-paw-dark mb-2 line-clamp-2">
          {product.name}
        </h3>
        <p className="text-gray-600 text-sm mb-3 flex-grow line-clamp-2">
          {product.description}
        </p>
        
        <div className="flex items-center mb-3">
          <span className="text-yellow-500">⭐</span>
          <span className="text-sm font-semibold ml-1">{product.rating}</span>
          <span className="text-gray-500 text-sm ml-1">({product.reviews})</span>
        </div>
        
        <div className="flex items-center justify-between">
          <span className="text-2xl font-bold text-paw-pink">
            ₹{product.price.toLocaleString('en-IN')}
          </span>
        </div>

        <button
          onClick={(e) => {
            e.preventDefault()
            handleAddToCart()
          }}
          className={`mt-3 w-full py-2 rounded-lg font-semibold transition-all ${
            showAdded
              ? 'bg-green-500 text-white'
              : 'bg-paw-pink text-white hover:bg-paw-light-pink'
          }`}
        >
          {showAdded ? '✅ Added!' : 'Add to Cart'}
        </button>
      </div>
    </Link>
  )
}
