# Terminal Screensaver

Omarchy-style terminal-based screensavers using TerminalTextEffects library for Ubuntu Linux.

## Features

- Terminal-based ASCII art animations
- 40+ animation effects from TerminalTextEffects library
- Multiple cycling effects (Matrix, Rain, Decrypt, Fireworks, Waves, etc.)
- Automatic activation after idle timeout
- Fully customizable ASCII art and effects via YAML configuration
- Easy-to-use pyfiglet integration for text generation

## Project Status

**Phase 1: Core Engine** - In Progress

Core screensaver engine has been built with:
- ✅ Project structure created
- ✅ Terminal controller (cursor hide/show, screen clear, input detection)
- ✅ ASCII art loader (file, directory, pyfiglet)
- ✅ Basic engine with Matrix effect
- ✅ Executable entry point (bin/screensaver-engine)
- ⏳ Installation and testing needed

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

## Quick Test

After installation, test the screensaver manually:

```bash
./bin/screensaver-engine
```

Press any key to exit.

## Project Structure

```
screensaver/
├── bin/
│   └── screensaver-engine          # Main executable
├── screensaver/                    # Python package
│   ├── __init__.py
│   ├── engine.py                   # Core screensaver engine
│   ├── terminal_controller.py      # Terminal control utilities
│   └── ascii_loader.py             # ASCII art loading
├── config/
│   └── ascii_art/
│       └── default.txt             # Default ASCII art
├── requirements.txt                # Python dependencies
├── install.sh                      # Installation script
└── README.md                       # This file
```

## Next Steps

- **Phase 2**: Add effect management and cycling
- **Phase 3**: Implement YAML configuration system
- **Phase 4**: Set up automatic idle detection with swayidle
- **Phase 5**: Polish and documentation

## Customization (Coming in Phase 3)

You'll be able to customize via `~/.config/terminal-screensaver/config.yaml`:

- ASCII art sources (files, directories, pyfiglet)
- Enabled/disabled effects
- Effect duration and cycling mode
- Idle timeout
- And more...

## License

Open source - feel free to use and modify!
