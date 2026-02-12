#!/bin/bash

echo "🚀 Starting DepositGuard AI Frontend..."

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Check if .env.local exists
if [ ! -f ".env.local" ]; then
    echo "⚙️  Creating .env.local..."
    echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
fi

# Start development server
echo "✅ Starting Next.js development server..."
echo "📍 Frontend: http://localhost:3000"
echo ""
npm run dev
