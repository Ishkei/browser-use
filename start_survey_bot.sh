#!/bin/bash

echo "🚀 Survey Automation Bot Quick Start"
echo "===================================="

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ .env file not found. Please create it with your API keys first."
    exit 1
fi

# Check if persona.json exists
if [ ! -f persona.json ]; then
    echo "❌ persona.json not found. Please ensure it exists."
    exit 1
fi

echo "✅ Environment files found"

# Create data directory if it doesn't exist
mkdir -p data

# Choose run method
echo ""
echo "Choose your run method:"
echo "1. Docker (recommended for production)"
echo "2. Local Python (for development)"
echo "3. Docker Compose (for advanced setup)"
echo ""

read -p "Enter your choice (1-3): " choice

case $choice in
    1)
        echo "🐳 Building and running with Docker..."
        docker build -f Dockerfile.survey -t survey-bot:latest .
        if [ $? -eq 0 ]; then
            echo "✅ Docker image built successfully!"
            echo "🚀 Running Survey Bot Container..."
            docker run -it --rm \
                --name survey-bot \
                -v "$(pwd)/data:/data" \
                -v "$(pwd)/persona.json:/app/persona.json:ro" \
                -v "$(pwd)/.env:/app/.env:ro" \
                -e GOOGLE_API_KEY="$GOOGLE_API_KEY" \
                -e OPENAI_API_KEY="$OPENAI_API_KEY" \
                -p 9242:9242 \
                -p 9222:9222 \
                survey-bot:latest
        else
            echo "❌ Docker build failed!"
            exit 1
        fi
        ;;
    2)
        echo "🐍 Running with local Python..."
        echo "Installing dependencies..."
        source .venv/bin/activate
        python3 survey_automation.py
        ;;
    3)
        echo "🐙 Running with Docker Compose..."
        docker-compose -f docker-compose.survey.yml up --build
        ;;
    *)
        echo "❌ Invalid choice. Exiting."
        exit 1
        ;;
esac
