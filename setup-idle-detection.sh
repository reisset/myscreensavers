#!/bin/bash
# Setup script for automatic idle detection and screensaver launch

set -e

echo "========================================="
echo "Idle Detection Setup"
echo "========================================="
echo

# Get the absolute path to the screensaver directory
SCREENSAVER_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAUNCH_SCRIPT="$SCREENSAVER_DIR/bin/screensaver-launch"

# Check if swayidle is installed
if ! command -v swayidle &> /dev/null; then
    echo "Error: swayidle is not installed."
    echo "Please install it with: sudo apt install swayidle"
    exit 1
fi

# Check if launch script exists
if [ ! -f "$LAUNCH_SCRIPT" ]; then
    echo "Error: Launch script not found: $LAUNCH_SCRIPT"
    exit 1
fi

echo "Step 1: Creating swayidle configuration..."
mkdir -p ~/.config/swayidle

cat > ~/.config/swayidle/config <<EOF
# Swayidle configuration for terminal screensaver
# Timeout values in seconds

timeout 300 '$LAUNCH_SCRIPT' resume 'pkill -f screensaver-engine'
EOF

echo "Created swayidle config at ~/.config/swayidle/config"
echo

echo "Step 2: Creating systemd user service..."
mkdir -p ~/.config/systemd/user

cat > ~/.config/systemd/user/screensaver-idle.service <<EOF
[Unit]
Description=Terminal Screensaver Idle Detection
Documentation=https://github.com/reisset/myscreensavers
After=graphical-session.target

[Service]
Type=simple
ExecStart=/usr/bin/swayidle -w -C %h/.config/swayidle/config
Restart=on-failure
RestartSec=5

[Install]
WantedBy=graphical-session.target
EOF

echo "Created systemd service at ~/.config/systemd/user/screensaver-idle.service"
echo

echo "Step 3: Enabling and starting service..."
systemctl --user daemon-reload
systemctl --user enable screensaver-idle.service
systemctl --user start screensaver-idle.service

echo

# Check status
if systemctl --user is-active --quiet screensaver-idle.service; then
    echo "========================================="
    echo "Setup complete!"
    echo "========================================="
    echo
    echo "The screensaver will now launch automatically after 5 minutes of inactivity."
    echo
    echo "Useful commands:"
    echo "  - Check status:    systemctl --user status screensaver-idle"
    echo "  - Stop service:    systemctl --user stop screensaver-idle"
    echo "  - Restart service: systemctl --user restart screensaver-idle"
    echo "  - View logs:       journalctl --user -u screensaver-idle -f"
    echo
    echo "To change idle timeout, edit: ~/.config/swayidle/config"
    echo "Then restart the service: systemctl --user restart screensaver-idle"
    echo
else
    echo "Error: Service failed to start. Check logs with:"
    echo "  journalctl --user -u screensaver-idle -n 50"
    exit 1
fi
