#!/bin/bash

# Vibe Code CAD Assistant - Quick Start Script

echo "🔧 Vibe Code CAD Assistant"
echo "=========================="

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "⚠️  Could not create virtual environment. Trying to run directly..."
        echo "💡 You may need to install: apt install python3-venv"
        USE_VENV=false
    else
        USE_VENV=true
    fi
else
    USE_VENV=true
fi

# Activate virtual environment if available
if [ "$USE_VENV" = true ]; then
    echo "🔄 Activating virtual environment..."
    source venv/bin/activate
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "⚠️  Could not install dependencies. Trying with --break-system-packages..."
    pip install -r requirements.txt --break-system-packages
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "💡 No .env file found. Creating example..."
    cp .env.example .env
    echo "📝 Edit .env file to add your OpenAI API key (optional)"
fi

# Run verification
echo "🔍 Running verification checks..."
python3 verify_setup.py

if [ $? -eq 0 ]; then
    echo ""
    echo "🚀 Starting Vibe Code CAD Assistant..."
    echo "📱 Open http://localhost:5000 in your browser"
    echo ""
    python3 app.py
else
    echo "❌ Verification failed. Please check the errors above."
    exit 1
fi