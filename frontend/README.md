# Cat E-Commerce Frontend 🐱

A modern, cat-themed e-commerce store built with React, Vite, and Tailwind CSS.

## Features

✅ **Product Catalog** - Browse all cat products with search and filter  
✅ **Product Detail Pages** - View detailed information about each product  
✅ **Shopping Cart** - Add items, adjust quantities, remove items  
✅ **Responsive Design** - Works great on mobile, tablet, and desktop  
✅ **State Management** - Zustand for cart management  
✅ **Cat-Themed UI** - Fun, colorful design for cat lovers  

## Products Available

- 🐟 Cat Food
- 🐭 Cat Toys
- 🛏️ Cat Beds
- ⏰ Smart Feeders
- 🌳 Scratching Posts
- ✨ Grooming Supplies
- 🔴 Interactive Toys
- 🍖 Cat Treats

## Getting Started

### Installation

```bash
cd frontend
npm install
```

### Development

```bash
npm run dev
```

The app will be available at `http://localhost:3000`

### Build for Production

```bash
npm run build
```

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── Navigation.jsx
│   │   ├── ProductCard.jsx
│   │   ├── ProductGrid.jsx
│   │   └── CartIcon.jsx
│   ├── pages/
│   │   ├── Home.jsx
│   │   ├── ProductDetail.jsx
│   │   └── Cart.jsx
│   ├── store/
│   │   └── cartStore.js
│   ├── data/
│   │   └── products.js
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
├── index.html
├── vite.config.js
├── tailwind.config.js
└── package.json
```

## Technologies Used

- **React 18** - UI framework
- **Vite** - Build tool
- **React Router** - Page routing
- **Zustand** - State management
- **Tailwind CSS** - Styling
- **PostCSS** - CSS processing

## Features to Add Next

- User authentication
- Checkout page with payment integration
- Order history
- Product reviews and ratings
- Wishlist functionality
- Admin panel
- API integration with backend

Enjoy shopping for cat products! 🐾
