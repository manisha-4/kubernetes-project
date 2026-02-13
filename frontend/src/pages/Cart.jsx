import { Link } from 'react-router-dom'
import { useCart } from '../store/cartStore'

export default function Cart() {
  const items = useCart(state => state.items)
  const removeItem = useCart(state => state.removeItem)
  const updateQuantity = useCart(state => state.updateQuantity)
  const getTotalPrice = useCart(state => state.getTotalPrice())
  const clearCart = useCart(state => state.clearCart)

  const totalPrice = getTotalPrice

  if (items.length === 0) {
    return (
      <div className="min-h-screen bg-paw-cream flex items-center justify-center">
        <div className="text-center">
          <p className="text-6xl mb-4">😺</p>
          <h1 className="text-4xl font-bold text-paw-dark mb-4">Your Cart is Empty</h1>
          <p className="text-gray-600 mb-8 text-lg">Add some purrfect cat products to get started!</p>
          <Link
            to="/"
            className="inline-block bg-paw-pink text-white px-8 py-3 rounded-lg font-bold text-lg hover:bg-paw-light-pink transition"
          >
            Continue Shopping 🛒
          </Link>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-paw-pale-pink polka-pink py-8">
      <div className="max-w-6xl mx-auto px-4">
        <h1 className="text-4xl font-bold text-paw-dark mb-8">Shopping Cart 🛒</h1>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Cart Items */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-lg shadow-lg overflow-hidden">
              {items.map(item => (
                <div
                  key={item.id}
                  className="flex items-center gap-4 p-6 border-b border-gray-200 hover:bg-gray-50 transition"
                >
                  {/* Product Image */}
                  <div className="text-5xl">{item.image}</div>

                  {/* Product Info */}
                  <div className="flex-grow">
                    <Link
                      to={`/product/${item.id}`}
                      className="text-lg font-bold text-paw-dark hover:text-paw-orange transition"
                    >
                      {item.name}
                    </Link>
                    <p className="text-gray-600 text-sm">{item.description}</p>
                    <p className="text-paw-pink font-bold mt-2">₹{item.price.toLocaleString('en-IN')}</p>
                  </div>

                  {/* Quantity Selector */}
                  <div className="flex items-center border-2 border-paw-pink rounded-lg">
                    <button
                      onClick={() => updateQuantity(item.id, item.quantity - 1)}
                      className="px-3 py-1 text-paw-pink font-bold hover:bg-paw-pale-pink transition"
                    >
                      −
                    </button>
                    <span className="px-4 py-1 font-bold">{item.quantity}</span>
                    <button
                      onClick={() => updateQuantity(item.id, item.quantity + 1)}
                      className="px-3 py-1 text-paw-pink font-bold hover:bg-paw-pale-pink transition"
                    >
                      +
                    </button>
                  </div>

                  {/* Subtotal */}
                  <div className="text-right min-w-[100px]">
                    <p className="text-sm text-gray-600">Subtotal</p>
                    <p className="text-2xl font-bold text-paw-pink">
                      ₹{(item.price * item.quantity).toLocaleString('en-IN')}
                    </p>
                  </div>

                  {/* Remove Button */}
                  <button
                    onClick={() => removeItem(item.id)}
                    className="text-red-500 hover:text-red-700 font-bold text-xl transition hover:scale-110"
                  >
                    ✕
                  </button>
                </div>
              ))}
            </div>

            <button
              onClick={() => clearCart()}
              className="mt-4 text-red-500 hover:text-red-700 font-semibold transition"
            >
              Clear Cart
            </button>
          </div>

          {/* Order Summary */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow-lg p-6 sticky top-20">
              <h2 className="text-2xl font-bold text-paw-dark mb-6">Order Summary</h2>

              <div className="space-y-4 mb-6">
                <div className="flex justify-between text-gray-700">
                  <span>Subtotal ({items.length} items)</span>
                  <span>₹{totalPrice.toLocaleString('en-IN')}</span>
                </div>
                <div className="flex justify-between text-gray-700">
                  <span>Shipping</span>
                  <span className="text-green-600 font-semibold">FREE</span>
                </div>
                <div className="flex justify-between text-gray-700">
                  <span>Tax</span>
                  <span>₹{(totalPrice * 0.08).toLocaleString('en-IN', { maximumFractionDigits: 0 })}</span>
                </div>
              </div>

              <div className="border-t-2 border-gray-200 pt-6 mb-6">
                <div className="flex justify-between text-2xl font-bold text-paw-dark">
                  <span>Total</span>
                  <span className="text-paw-pink">
                    ₹{(totalPrice * 1.08).toLocaleString('en-IN', { maximumFractionDigits: 0 })}
                  </span>
                </div>
              </div>

              <button className="w-full bg-paw-pink text-white font-bold py-3 rounded-lg hover:bg-paw-light-pink transition mb-3">
                Proceed to Checkout
              </button>

              <Link
                to="/"
                className="w-full block text-center border-2 border-paw-pink text-paw-pink font-bold py-2 rounded-lg hover:bg-paw-pale-pink transition"
              >
                Continue Shopping
              </Link>

              <div className="mt-6 p-4 bg-paw-pale-pink rounded-lg">
                <p className="text-sm text-gray-700">
                  ✅ Free shipping on all orders<br/>
                  ✅ 30-day money back guarantee<br/>
                  ✅ 24/7 customer support
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
