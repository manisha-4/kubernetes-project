import { Link } from 'react-router-dom'
import CartIcon from './CartIcon'

export default function Navigation() {
  return (
    <nav className="bg-paw-pink shadow-lg sticky top-0 z-50">
      <div className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-2 text-white text-2xl font-bold hover:opacity-90 transition-opacity">
          <span className="text-3xl">🐱</span>
          <span>Purrfect Cats</span>
        </Link>
        
        <div className="flex items-center gap-8">
          <Link to="/" className="text-white font-semibold hover:text-gray-200 transition">
            Shop
          </Link>
          <Link to="/" className="text-white font-semibold hover:text-gray-200 transition">
            About
          </Link>
          <Link to="/cart" className="hover:scale-110 transition-transform">
            <CartIcon />
          </Link>
        </div>
      </div>
    </nav>
  )
}
