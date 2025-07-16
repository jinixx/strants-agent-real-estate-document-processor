#!/bin/bash

# Startup script for StrandsDocumentProcessor with AI Agents
echo "🚀 Starting StrandsDocumentProcessor with AI Agents..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first."
    echo "   python3 -m venv venv"
    echo "   source venv/bin/activate"
    echo "   pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check if required packages are installed
echo "📦 Checking dependencies..."
python -c "import streamlit, boto3, pandas" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Missing dependencies. Installing..."
    pip install -r requirements.txt
fi

# Check AWS configuration
echo "🔐 Checking AWS configuration..."
if [ ! -f ~/.aws/credentials ] && [ -z "$AWS_ACCESS_KEY_ID" ]; then
    echo "⚠️  Warning: AWS credentials not configured."
    echo "   Please configure AWS CLI or set environment variables."
    echo "   The app will still run but AWS Bedrock features may not work."
fi

# Check .env file
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found. Creating default..."
    cat > .env << EOF
AWS_REGION=us-west-2
AWS_PROFILE=default
BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0
MAX_PAGES=500
MAX_FILE_SIZE=50MB
PROCESSING_TIMEOUT=300
DEBUG=False
EOF
fi

# Start the application
echo "🌟 Starting Streamlit application..."
echo "📱 The app will open in your browser at: http://localhost:8501"
echo ""
echo "🆕 New Features Available:"
echo "   🔍 Property Research with Agentic AI"
echo "   💬 Document Q&A with RAG"
echo "   📄 Multi-format document support"
echo ""

streamlit run app.py --server.port 8501 --server.address 0.0.0.0
