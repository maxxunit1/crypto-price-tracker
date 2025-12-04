#!/bin/bash

# Terminal colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo ""
echo "==============================================="
echo "💎 CRYPTO PRICE TRACKER - LAUNCHER"
echo "==============================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python not found!${NC}"
    echo ""
    echo "Please install Python 3.8 or higher:"
    echo "  macOS: brew install python3"
    echo "  Ubuntu/Debian: sudo apt install python3 python3-venv python3-pip"
    echo "  Fedora: sudo dnf install python3 python3-pip"
    echo ""
    exit 1
fi

echo -e "${GREEN}✅ Python found${NC}"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${CYAN}📦 Creating virtual environment...${NC}"
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Failed to create virtual environment${NC}"
        exit 1
    fi
    echo -e "${GREEN}✅ Virtual environment created${NC}"
    echo ""
fi

# Activate virtual environment
echo -e "${CYAN}⚡ Activating virtual environment...${NC}"
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Failed to activate virtual environment${NC}"
    exit 1
fi

# Check if requirements are installed
if [ ! -d "venv/lib/python"*"/site-packages/customtkinter" ]; then
    echo -e "${CYAN}📥 Installing dependencies...${NC}"
    echo "This may take 30-60 seconds on first run..."
    echo ""
    python3 -m pip install --upgrade pip > /dev/null 2>&1
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Failed to install dependencies${NC}"
        exit 1
    fi
    echo -e "${GREEN}✅ Dependencies installed${NC}"
    echo ""
else
    # Check if requirements.txt was updated
    pip install -r requirements.txt --quiet > /dev/null 2>&1
fi

echo -e "${CYAN}🚀 Starting Crypto Price Tracker...${NC}"
echo ""
echo "==============================================="
echo ""

# Run the application
python3 crypto_tracker.py

# If app crashes, show error
if [ $? -ne 0 ]; then
    echo ""
    echo "==============================================="
    echo -e "${RED}❌ Application exited with error${NC}"
    echo "==============================================="
    echo ""
    read -p "Press Enter to exit..."
fi
