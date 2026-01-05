# Terminal Screensaver

Omarchy-style terminal-based screensavers using TerminalTextEffects library for Ubuntu Linux.

![Status](https://img.shields.io/badge/status-complete-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)

## Features

- **Terminal-based animations**: Beautiful ASCII art with 23+ visual effects
- **Multiple effects**: Matrix, Rain, Decrypt, Fireworks, Waves, Beams, Pour, Swarm, Rings, and more
- **Smart cycling**: Random or sequential effect rotation with configurable duration
- **Highly customizable**: YAML configuration for all aspects
- **Flexible ASCII art**: Support for files, directories, or pyfiglet text generation
- **Instant exit**: Press any key to exit immediately
- **No dependencies**: Pure Python with standard libraries (except TerminalTextEffects)

## Project Status

**✅ All Phases Complete!**

- ✅ Phase 1: Core screensaver engine with Matrix effect
- ✅ Phase 2: Effect management and cycling (23 effects)
- ✅ Phase 3: YAML configuration system
- ✅ Phase 4: Launch controller and idle detection setup
- ✅ Phase 5: Documentation and polish

## Installation

### Prerequisites

You need to install system dependencies first:

```bash
sudo apt update
sudo apt install -y python3-pip python3-venv python3.12-venv swayidle
```

### Install Script

Once prerequisites are installed, run the installation script:

```bash
./install.sh
```

This will:
1. Create a Python virtual environment
2. Install Python dependencies (terminaltexteffects, pyfiglet, PyYAML)
3. Set up configuration directory at `~/.config/terminal-screensaver/`
4. Copy default ASCII art

### Manual Installation

If you prefer manual installation:

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python packages
pip install -r requirements.txt

# Set up config directory
mkdir -p ~/.config/terminal-screensaver/ascii_art
cp config/ascii_art/* ~/.config/terminal-screensaver/ascii_art/
```

## Quick Start

After installation:

```bash
# Test manually (press any key to exit)
./bin/screensaver-engine

# Launch in fullscreen terminal
./bin/screensaver-launch

# Set up automatic idle detection (Wayland with idle protocol required)
./setup-idle-detection.sh
```

## Usage

### Running Manually

```bash
# Basic usage
./bin/screensaver-engine

# Launch in fullscreen terminal
./bin/screensaver-launch
```

### Keyboard Shortcut (Recommended)

Bind `./bin/screensaver-launch` to a keyboard shortcut in your desktop environment:

- **GNOME**: Settings → Keyboard → Custom Shortcuts
- **KDE**: System Settings → Shortcuts → Custom Shortcuts
- **XFCE**: Settings → Keyboard → Application Shortcuts

Example shortcut: `Ctrl+Alt+L`

### Automatic Idle Detection

For Wayland compositors with idle protocol support (Sway, Hyprland, etc.):

```bash
./setup-idle-detection.sh
```

This sets up a systemd user service that monitors idle time and launches the screensaver automatically.

**Note**: GNOME/Mutter and other compositors may not support the idle protocol. Use the keyboard shortcut method instead.

## Customization

All settings are configured via `~/.config/terminal-screensaver/config.yaml`

### Change ASCII Art

**Option 1: Use your own text file**
```yaml
content:
  source: "file"
  file_path: "~/.config/terminal-screensaver/ascii_art/myart.txt"
```

**Option 2: Generate from text**
```yaml
content:
  source: "pyfiglet"
  pyfiglet:
    text: "MY AWESOME TEXT"
    font: "slant"  # or banner, digital, bubble, etc.
```

**Option 3: Cycle through multiple files**
```yaml
content:
  source: "directory"
  directory: "~/.config/terminal-screensaver/ascii_art/"
```

### Change Effects

**Enable specific effects:**
```yaml
screensaver:
  enabled_effects:
    - matrix
    - rain
    - fireworks
    - decrypt
    - waves
```

**Or exclude unwanted effects:**
```yaml
screensaver:
  # Comment out or remove enabled_effects to use all except excluded
  excluded_effects:
    - unstable
    - burn
```

### Adjust Timing

```yaml
screensaver:
  effect_duration: 45  # Seconds per effect

idle:
  timeout_seconds: 600  # 10 minutes before screensaver starts
```

### Cycle Mode

```yaml
screensaver:
  cycle_mode: "random"  # or "sequential"
```

## Available Effects

The screensaver includes 23 effects from TerminalTextEffects:

| Effect | Description |
|--------|-------------|
| matrix | Classic Matrix digital rain |
| rain | Rainfall effect |
| decrypt | Decryption animation |
| fireworks | Explosive bursts |
| waves | Wavy motion |
| beams | Light beam effects |
| pour | Pouring animation |
| swarm | Particle swarm |
| rings | Concentric rings |
| bubbles | Bubble effects |
| burn | Burning effect |
| colorshift | Color transitions |
| crumble | Crumbling effect |
| expand | Expansion animation |
| middleout | Middle-out reveal |
| orbittingvolley | Orbiting particles |
| scattered | Scattered appearance |
| spotlights | Spotlight effects |
| spray | Spray pattern |
| sweep | Sweeping motion |
| synthgrid | Synthwave grid |
| blackhole | Black hole distortion |
| slide | Sliding reveal |

## Project Structure

```
screensaver/
├── bin/
│   ├── screensaver-engine          # Main screensaver executable
│   └── screensaver-launch          # Fullscreen launcher
├── screensaver/                    # Python package
│   ├── __init__.py
│   ├── engine.py                   # Core engine with effect cycling
│   ├── effects.py                  # Effect manager (23 effects)
│   ├── config.py                   # YAML configuration loader
│   ├── terminal_controller.py      # Terminal control (cursor, input)
│   └── ascii_loader.py             # ASCII art loading (file/pyfiglet)
├── config/
│   ├── default_config.yaml         # Configuration template
│   └── ascii_art/
│       └── default.txt             # Default ASCII art
├── requirements.txt                # Python dependencies
├── install.sh                      # Installation script
├── setup-idle-detection.sh         # Idle detection setup
└── README.md                       # This file
```

## Troubleshooting

### Screensaver doesn't start automatically

- Check if systemd service is running: `systemctl --user status screensaver-idle`
- View logs: `journalctl --user -u screensaver-idle -f`
- If you get "Display doesn't support idle protocol", your compositor doesn't support swayidle
- Use a keyboard shortcut instead (recommended for GNOME/KDE)

### Effects are too fast/slow

Edit `~/.config/terminal-screensaver/config.yaml` and change `effect_duration`:

```yaml
screensaver:
  effect_duration: 60  # Slower: 60 seconds per effect
```

### Want to use custom ASCII art

1. Create your ASCII art file
2. Save to `~/.config/terminal-screensaver/ascii_art/myart.txt`
3. Update config to point to your file
4. Or use an ASCII generator online and paste the result

### Terminal gets corrupted after crash

Run: `reset` or `stty sane && clear`

## Contributing

Contributions welcome! Feel free to:
- Add new ASCII art examples
- Report bugs or request features
- Submit pull requests

## Credits

- Built with [TerminalTextEffects](https://github.com/ChrisBuilds/terminaltexteffects) by ChrisBuilds
- Inspired by [Omarchy](https://github.com/basecamp/omarchy) screensavers
- ASCII art generation via [pyfiglet](https://github.com/pwaller/pyfiglet)

## License

MIT License - feel free to use and modify!
