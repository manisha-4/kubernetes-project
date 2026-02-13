import { useCart } from '../store/cartStore'

export default function CartIcon() {
  const totalItems = useCart(state => state.getTotalItems())

  return (
    <div className="relative">
      <button className="text-3xl hover:scale-110 transition-transform">
        🛒
      </button>
      {totalItems > 0 && (
        <span className="absolute -top-2 -right-2 bg-paw-pink text-white text-xs font-bold rounded-full w-6 h-6 flex items-center justify-center">
          {totalItems}
        </span>
      )}
    </div>
  )
}
