#!/bin/bash

echo "🚀 Starting DepositGuard AI Backend..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found. Copying from .env.example..."
    cp ../.env.example .env
    echo "Please edit .env with your API keys before running!"
    exit 1
fi

# Start database if using Docker
if grep -q "localhost:5432" .env; then
    echo "🐳 Starting PostgreSQL via Docker..."
    docker-compose up -d
    sleep 3
fi

# Initialize database
echo "🗄️  Initializing database..."
python -c "from app.database import init_db; init_db()" 2>/dev/null || echo "Database already initialized"

# Start server
echo "✅ Starting FastAPI server..."
echo "📍 API: http://localhost:8000"
echo "📚 Docs: http://localhost:8000/docs"
echo ""
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
