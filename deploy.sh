#!/bin/bash
# deploy.sh - Easy deployment script for AI Fitness Coach

set -e

echo "🏋️ AI Fitness Coach - Docker Deployment Script"
echo "================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        echo "Visit: https://docs.docker.com/get-docker/"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        echo "Visit: https://docs.docker.com/compose/install/"
        exit 1
    fi
    
    print_success "Docker and Docker Compose are installed"
}

# Create directory structure
setup_project() {
    print_status "Setting up project structure..."
    
    # Create directories
    mkdir -p .streamlit
    mkdir -p .github/workflows
    
    # Create .streamlit/config.toml if it doesn't exist
    if [ ! -f ".streamlit/config.toml" ]; then
        cat > .streamlit/config.toml << EOF
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
        print_success "Created .streamlit/config.toml"
    fi
    
    # Create .env template if it doesn't exist
    if [ ! -f ".env" ]; then
        cat > .env << EOF
# OpenAI API Key (optional)
OPENAI_API_KEY=your_openai_api_key_here

# Streamlit Configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
EOF
        print_success "Created .env template"
        print_warning "Please update .env with your OpenAI API key if you want AI chat features"
    fi
}

# Build the Docker image
build_image() {
    print_status "Building Docker image..."
    
    if docker-compose build; then
        print_success "Docker image built successfully"
    else
        print_error "Failed to build Docker image"
        exit 1
    fi
}

# Start the application
start_app() {
    print_status "Starting AI Fitness Coach application..."
    
    if docker-compose up -d; then
        print_success "Application started successfully!"
        echo ""
        echo "🚀 Your AI Fitness Coach is now running!"
        echo "📱 Access it at: http://localhost:8501"
        echo "💪 Chat with Kartik, your AI trainer!"
        echo ""
        echo "📊 To view logs: docker-compose logs -f"
        echo "🛑 To stop: docker-compose down"
        echo ""
    else
        print_error "Failed to start application"
        exit 1
    fi
}

# Stop the application
stop_app() {
    print_status "Stopping AI Fitness Coach application..."
    
    if docker-compose down; then
        print_success "Application stopped successfully"
    else
        print_error "Failed to stop application"
        exit 1
    fi
}

# Show status
show_status() {
    print_status "Application Status:"
    docker-compose ps
    echo ""
    
    if docker-compose ps | grep -q "Up"; then
        print_success "✅ Application is running at http://localhost:8501"
    else
        print_warning "⚠️  Application is not running"
    fi
}

# Show logs
show_logs() {
    print_status "Showing application logs (Ctrl+C to exit):"
    docker-compose logs -f
}

# Clean up everything
cleanup() {
    print_status "Cleaning up Docker containers and images..."
    
    docker-compose down --rmi all --volumes --remove-orphans
    print_success "Cleanup completed"
}

# Main script logic
case "${1:-start}" in
    "start")
        check_docker
        setup_project
        build_image
        start_app
        ;;
    "stop")
        stop_app
        ;;
    "restart")
        stop_app
        sleep 2
        start_app
        ;;
    "status")
        show_status
        ;;
    "logs")
        show_logs
        ;;
    "build")
        check_docker
        build_image
        ;;
    "clean")
        cleanup
        ;;
    "setup")
        check_docker
        setup_project
        print_success "Project setup completed"
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status|logs|build|clean|setup}"
        echo ""
        echo "Commands:"
        echo "  start   - Build and start the application (default)"
        echo "  stop    - Stop the application"
        echo "  restart - Restart the application"
        echo "  status  - Show application status"
        echo "  logs    - Show application logs"
        echo "  build   - Build Docker image only"
        echo "  clean   - Clean up all containers and images"
        echo "  setup   - Setup project structure only"
        exit 1
        ;;
esac

---

# quick-start.ps1 (PowerShell script for Windows)

# AI Fitness Coach - Quick Start Script for Windows
Write-Host "🏋️ AI Fitness Coach - Windows Deployment Script" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan

# Check if Docker is installed
function Test-Docker {
    try {
        $dockerVersion = docker --version
        $dockerComposeVersion = docker-compose --version
        Write-Host "✅ Docker is installed: $dockerVersion" -ForegroundColor Green
        Write-Host "✅ Docker Compose is installed: $dockerComposeVersion" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "❌ Docker or Docker Compose is not installed" -ForegroundColor Red
        Write-Host "Please install Docker Desktop from: https://docs.docker.com/desktop/windows/" -ForegroundColor Yellow
        return $false
    }
}

# Setup project structure
function Setup-Project {
    Write-Host "📁 Setting up project structure..." -ForegroundColor Blue
    
    # Create directories
    if (!(Test-Path ".streamlit")) { New-Item -ItemType Directory -Path ".streamlit" }
    if (!(Test-Path ".github\workflows")) { New-Item -ItemType Directory -Path ".github\workflows" -Force }
    
    # Create config files
    if (!(Test-Path ".streamlit\config.toml")) {
        $configContent = @"
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
"@
        $configContent | Out-File -FilePath ".streamlit\config.toml" -Encoding UTF8
        Write-Host "✅ Created .streamlit\config.toml" -ForegroundColor Green
    }
    
    if (!(Test-Path ".env")) {
        $envContent = @"
# OpenAI API Key (optional)
OPENAI_API_KEY=your_openai_api_key_here

# Streamlit Configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
"@
        $envContent | Out-File -FilePath ".env" -Encoding UTF8
        Write-Host "✅ Created .env template" -ForegroundColor Green
        Write-Host "⚠️  Please update .env with your OpenAI API key for AI chat features" -ForegroundColor Yellow
    }
}

# Start the application
function Start-Application {
    Write-Host "🚀 Starting AI Fitness Coach application..." -ForegroundColor Blue
    
    try {
        docker-compose up --build -d
        Write-Host ""
        Write-Host "🎉 SUCCESS! Your AI Fitness Coach is now running!" -ForegroundColor Green
        Write-Host "📱 Access it at: http://localhost:8501" -ForegroundColor Cyan
        Write-Host "💪 Chat with Kartik, your AI trainer!" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "📊 To view logs: docker-compose logs -f" -ForegroundColor Yellow
        Write-Host "🛑 To stop: docker-compose down" -ForegroundColor Yellow
        Write-Host ""
    }
    catch {
        Write-Host "❌ Failed to start application" -ForegroundColor Red
        Write-Host $_.Exception.Message -ForegroundColor Red
    }
}

# Main execution
if (Test-Docker) {
    Setup-Project
    Start-Application
} else {
    Write-Host "Please install Docker Desktop and try again." -ForegroundColor Red
}

---

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