#!/bin/bash

# StrandsDocumentProcessor Startup Script

echo "🚀 Starting StrandsDocumentProcessor..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first."
    exit 1
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
if ! python -c "import strands_agents" 2>/dev/null; then
    echo "📥 Installing dependencies..."
    pip install -r requirements.txt
fi

# Check AWS configuration
echo "🔐 Checking AWS configuration..."
if ! aws sts get-caller-identity >/dev/null 2>&1; then
    echo "⚠️  Warning: AWS CLI not configured or no valid credentials found"
    echo "   Please run 'aws configure' to set up your credentials"
fi

# Start Streamlit application
echo "🌐 Starting Streamlit application..."
echo "   Access the application at: http://localhost:8501"
echo "   Press Ctrl+C to stop the application"
echo ""

streamlit run app.py --server.port 8501 --server.address 0.0.0.0
