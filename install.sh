#!/bin/bash
# Installation script for terminal screensaver

set -e

echo "========================================="
echo "Terminal Screensaver Installation"
echo "========================================="
echo

# Check if running as root
if [ "$EUID" -eq 0 ]; then
   echo "Please don't run this script as root. It will prompt for sudo when needed."
   exit 1
fi

# Step 1: Install system dependencies
echo "Step 1: Installing system dependencies..."
echo "This requires sudo access."
echo

sudo apt update
sudo apt install -y python3-pip python3-venv python3.12-venv swayidle

echo
echo "Step 2: Creating virtual environment..."
python3 -m venv venv

echo
echo "Step 3: Installing Python packages..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo
echo "Step 4: Setting up configuration directory..."
mkdir -p ~/.config/terminal-screensaver/ascii_art

# Copy default config if it doesn't exist
if [ ! -f ~/.config/terminal-screensaver/config.yaml ]; then
    cp config/default_config.yaml ~/.config/terminal-screensaver/config.yaml
    echo "Created default configuration at ~/.config/terminal-screensaver/config.yaml"
fi

# Copy default ASCII art
cp config/ascii_art/* ~/.config/terminal-screensaver/ascii_art/ 2>/dev/null || true
echo "Copied default ASCII art to ~/.config/terminal-screensaver/ascii_art/"

echo
echo "========================================="
echo "Installation complete!"
echo "========================================="
echo
echo "Next steps:"
echo "1. Test the screensaver manually:"
echo "   ./bin/screensaver-engine"
echo
echo "2. After testing Phase 1, we'll set up automatic idle detection in Phase 4"
echo
