#!/bin/bash
echo "💝 Terminal AI Companion - One-Click Setup and Run"
echo

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if Python3 is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 not found! Please install Python 3.8+ first.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Python3 found: $(python3 --version)${NC}"
echo

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "${BLUE}🏗️  Creating virtual environment...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✅ Virtual environment created${NC}"
else
    echo -e "${GREEN}✅ Virtual environment already exists${NC}"
fi
echo

# Activate virtual environment and install packages
echo -e "${BLUE}📦 Installing/updating packages...${NC}"
venv/bin/python -m pip install --upgrade pip
venv/bin/python -m pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Package installation failed!${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Packages installed successfully${NC}"
echo

# Setup environment file if it doesn't exist
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        echo -e "${BLUE}⚙️  Setting up environment...${NC}"
        cp .env.example .env
        echo -e "${GREEN}✅ .env file created from example${NC}"
        echo -e "${YELLOW}🔑 Please edit .env file and add your OpenAI API key${NC}"
        echo
        
        # Try to open .env file in default editor
        if command -v nano &> /dev/null; then
            echo "Opening .env file in nano editor..."
            echo "Press Ctrl+X to save and exit after editing"
            read -p "Press Enter to continue..."
            nano .env
        elif command -v vim &> /dev/null; then
            echo "Opening .env file in vim editor..."
            echo "Press ESC then :wq to save and exit after editing"
            read -p "Press Enter to continue..."
            vim .env
        else
            echo "Please edit .env file manually with your preferred editor"
            echo "Example: nano .env"
            read -p "Press Enter when you've finished editing .env file..."
        fi
        echo
    else
        echo -e "${RED}❌ .env.example not found${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✅ .env file already exists${NC}"
    echo
fi

# Check if OpenAI API key is set
if grep -q "your_openai_api_key_here" .env; then
    echo -e "${YELLOW}⚠️  Warning: OpenAI API key not configured in .env file${NC}"
    echo "Please edit .env file and set your API key"
    echo
    read -p "Do you want to edit .env file now? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if command -v nano &> /dev/null; then
            nano .env
        elif command -v vim &> /dev/null; then
            vim .env
        else
            echo "Please edit .env file manually"
        fi
    else
        echo "Continuing with current configuration..."
    fi
    echo
fi

# Create logs directory
mkdir -p logs

# Make sure the script has execute permissions
chmod +x "$0"

# Run the application
echo -e "${BLUE}🚀 Starting Terminal AI Companion...${NC}"
echo
venv/bin/python main.py

echo
echo -e "${GREEN}👋 Terminal AI Companion has ended.${NC}"