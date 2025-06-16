# install.sh - One-command installation script

#!/bin/bash
# One-command installation script for AI Fitness Coach

echo "🏋️ AI Fitness Coach - One-Command Installation"
echo "=============================================="

# Create project directory
PROJECT_NAME="ai-fitness-coach"
if [ ! -d "$PROJECT_NAME" ]; then
    echo "📁 Creating project directory..."
    mkdir -p $PROJECT_NAME
    cd $PROJECT_NAME
else
    echo "📁 Using existing directory..."
    cd $PROJECT_NAME
fi

# Download app.py if not exists
if [ ! -f "app.py" ]; then
    echo "📥 Please place your app.py file in the current directory"
    echo "Current directory: $(pwd)"
    read -p "Press Enter when app.py is ready..."
fi

# Create Dockerfile
cat > Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN mkdir -p .streamlit

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
EOF

# Create requirements.txt
cat > requirements.txt << 'EOF'
streamlit==1.29.0
openai==1.3.0
typing-extensions==4.8.0
EOF

# Create docker-compose.yml
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  fitness-app:
    build: .
    ports:
      - "8501:8501"
    environment:
      - STREAMLIT_SERVER_HEADLESS=true
      - STREAMLIT_SERVER_ENABLE_CORS=false
      - STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
EOF

# Create .dockerignore
cat > .dockerignore << 'EOF'
__pycache__
*.pyc
*.pyo
*.pyd
.Python
.env
.venv
venv/
.git
.gitignore
README.md
Dockerfile
.dockerignore
.pytest_cache
.coverage
EOF

# Create .streamlit directory and config
mkdir -p .streamlit
cat > .streamlit/config.toml << 'EOF'
[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#ff6b6b"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
EOF

echo "✅ All configuration files created!"
echo ""
echo "🚀 To start your AI Fitness Coach:"
echo "   docker-compose up --build"
echo ""
echo "📱 Access at: http://localhost:8501"
echo "🛑 To stop: docker-compose down"
echo ""
echo "🎉 Setup complete! Ready to get fit with Kartik! 💪"
