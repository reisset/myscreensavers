#!/bin/bash
# install.sh - Install the terminal screensaver
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "=== Terminal Screensaver Installer ==="
echo

# Check for tte
if ! command -v tte &>/dev/null; then
    echo "Installing terminaltexteffects..."

    # Try pipx first (cleaner), fall back to pip with --break-system-packages
    if command -v pipx &>/dev/null; then
        pipx install terminaltexteffects
    else
        pip3 install --user --break-system-packages terminaltexteffects 2>/dev/null || \
        pip3 install --user terminaltexteffects
    fi

    # Make sure ~/.local/bin is in PATH
    if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
        export PATH="$HOME/.local/bin:$PATH"
        echo ""
        echo "NOTE: Add ~/.local/bin to your PATH permanently:"
        echo "  echo 'export PATH=\"\$HOME/.local/bin:\$PATH\"' >> ~/.bashrc"
        echo ""
    fi
fi

# Verify tte works
if ! command -v tte &>/dev/null; then
    echo "Error: tte still not found. Try: pip3 install terminaltexteffects"
    exit 1
fi

echo "✓ terminaltexteffects installed"

# Make scripts executable
chmod +x "$SCRIPT_DIR/bin/screensaver"
chmod +x "$SCRIPT_DIR/bin/screensaver-daemon"
echo "✓ Scripts are executable"

# Install systemd service
mkdir -p ~/.config/systemd/user
cp "$SCRIPT_DIR/systemd/screensaver-daemon.service" ~/.config/systemd/user/

# Update the service to point to the right location
sed -i "s|%h/screensaver|$SCRIPT_DIR|g" ~/.config/systemd/user/screensaver-daemon.service

echo "✓ Systemd service installed"

# Enable and start
systemctl --user daemon-reload
systemctl --user enable screensaver-daemon.service
systemctl --user start screensaver-daemon.service

echo "✓ Service enabled and started"
echo

# Verify
if systemctl --user is-active --quiet screensaver-daemon.service; then
    echo "=== Installation complete! ==="
    echo
    echo "The screensaver will activate after 5 minutes of idle."
    echo
    echo "Commands:"
    echo "  Test:    $SCRIPT_DIR/bin/screensaver"
    echo "  Status:  systemctl --user status screensaver-daemon"
    echo "  Logs:    journalctl --user -u screensaver-daemon -f"
    echo "  Stop:    systemctl --user stop screensaver-daemon"
    echo "  Restart: systemctl --user restart screensaver-daemon"
    echo
    echo "To customize, edit: $SCRIPT_DIR/config/ascii_art/default.txt"
else
    echo "Warning: Service may not have started. Check:"
    echo "  journalctl --user -u screensaver-daemon -n 20"
fi
