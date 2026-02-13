import { useState, useMemo } from 'react'
import ProductGrid from '../components/ProductGrid'
import { catProducts } from '../data/products'

const CATEGORIES = ['all', 'food', 'toys', 'beds', 'furniture', 'accessories', 'grooming']

export default function Home() {
  const [selectedCategory, setSelectedCategory] = useState('all')
  const [searchTerm, setSearchTerm] = useState('')

  const filteredProducts = useMemo(() => {
    return catProducts.filter(product => {
      const matchesCategory = selectedCategory === 'all' || product.category === selectedCategory
      const matchesSearch = product.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           product.description.toLowerCase().includes(searchTerm.toLowerCase())
      return matchesCategory && matchesSearch
    })
  }, [selectedCategory, searchTerm])

  return (
    <div className="min-h-screen bg-paw-pale-pink polka-pink">
      {/* Hero Section */}
      <div className="bg-gradient-to-r from-paw-pink to-paw-light-pink text-white py-12 text-center">
        <h1 className="text-5xl font-bold mb-2">🐱 Welcome to Purrfect Cats!</h1>
        <p className="text-xl opacity-90">Everything your feline friend needs and wants</p>
      </div>

      <div className="max-w-6xl mx-auto px-4 py-8">
        {/* Search Bar */}
        <div className="mb-8">
          <input
            type="text"
            placeholder="🔍 Search for cat products..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full px-4 py-3 rounded-lg border-2 border-paw-pink focus:outline-none focus:ring-2 focus:ring-paw-pink"
          />
        </div>

        {/* Category Filter */}
        <div className="mb-8 flex flex-wrap gap-2">
          {CATEGORIES.map(category => (
            <button
              key={category}
              onClick={() => setSelectedCategory(category)}
              className={`px-4 py-2 rounded-lg font-semibold transition-all capitalize ${
                selectedCategory === category
                  ? 'bg-paw-pink text-white shadow-lg scale-105'
                  : 'bg-white text-paw-dark border-2 border-paw-pink hover:bg-paw-pale-pink'
              }`}
            >
              {category === 'all' ? '🐾 All Products' : category}
            </button>
          ))}
        </div>

        {/* Results Count */}
        <p className="text-gray-600 mb-6 font-semibold">
          Showing {filteredProducts.length} product{filteredProducts.length !== 1 ? 's' : ''}
        </p>

        {/* Products Grid */}
        {filteredProducts.length > 0 ? (
          <ProductGrid products={filteredProducts} />
        ) : (
          <div className="text-center py-12">
            <p className="text-2xl text-gray-500 mb-2">😹 No products found</p>
            <p className="text-gray-400">Try a different search or category</p>
          </div>
        )}
      </div>
    </div>
  )
}
