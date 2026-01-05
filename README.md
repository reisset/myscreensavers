# myscreensavers

Omarchy-style terminal screensavers for Ubuntu/GNOME.

Auto-activates after 5 minutes of idle. Shows animated ASCII art using [TerminalTextEffects](https://github.com/ChrisBuilds/terminaltexteffects). Press any key to exit.

## Install

```bash
git clone git@github.com:reisset/myscreensavers.git ~/screensaver
cd ~/screensaver
./install.sh
```

That's it. The screensaver daemon starts automatically and runs on login.

## Test it

```bash
# Run screensaver directly (Ctrl+C to exit)
./bin/screensaver

# Check daemon status
systemctl --user status screensaver-daemon

# Watch daemon logs
journalctl --user -u screensaver-daemon -f
```

## Customize

### Change the ASCII art

Edit `config/ascii_art/default.txt` with your own ASCII art.

Generate ASCII text at [patorjk.com/software/taag](https://patorjk.com/software/taag/) or use `figlet`:

```bash
figlet -f slant "HELLO" > config/ascii_art/default.txt
```

### Change idle timeout

Edit the systemd service:

```bash
systemctl --user edit screensaver-daemon
```

Add:
```ini
[Service]
Environment=IDLE_TIMEOUT_MS=600000  # 10 minutes
```

Then restart: `systemctl --user restart screensaver-daemon`

### Change effects

Edit `bin/screensaver` and modify the `EFFECTS` array. Available effects:

```
beams blackhole bouncyballs bubbles burn colorshift crumble decrypt
errorcorrect expand fireworks matrix middleout orbittingvolley overflow
pour print rain rings scattered slide smoke spotlights spray swarm
sweep synthgrid unstable vhstape waves wipe
```

## How it works

```
┌─────────────────────────────────────────────────────────────┐
│  screensaver-daemon                                         │
│  └─ polls GNOME IdleMonitor via DBus every 5 seconds        │
│  └─ when idle > 5 min, launches fullscreen terminal         │
│  └─ terminal runs: tte <effect> < ascii_art.txt             │
│  └─ on user activity, kills the terminal                    │
└─────────────────────────────────────────────────────────────┘
```

Two bash scripts, ~150 lines total:
- `bin/screensaver` - cycles through random effects
- `bin/screensaver-daemon` - monitors idle time, launches/kills screensaver

## Requirements

- Ubuntu 22.04+ with GNOME (Wayland or X11)
- Python 3 + pip (for installing tte)
- A terminal emulator (kitty, alacritty, or gnome-terminal)

## Uninstall

```bash
systemctl --user stop screensaver-daemon
systemctl --user disable screensaver-daemon
rm ~/.config/systemd/user/screensaver-daemon.service
rm -rf ~/screensaver
```

## Troubleshooting

**Screensaver doesn't auto-activate:**
```bash
# Check if daemon is running
systemctl --user status screensaver-daemon

# Check logs
journalctl --user -u screensaver-daemon -n 50

# Test idle detection manually
dbus-send --print-reply --dest=org.gnome.Mutter.IdleMonitor \
  /org/gnome/Mutter/IdleMonitor/Core \
  org.gnome.Mutter.IdleMonitor.GetIdletime
```

**tte command not found:**
```bash
pip3 install --user terminaltexteffects
# Make sure ~/.local/bin is in your PATH
export PATH="$HOME/.local/bin:$PATH"
```

**Terminal doesn't go fullscreen:**

Kitty and alacritty have better fullscreen support than gnome-terminal. Install one:
```bash
sudo apt install kitty
# or
sudo apt install alacritty
```

## Credits

- [TerminalTextEffects](https://github.com/ChrisBuilds/terminaltexteffects) by ChrisBuilds
- Inspired by [Omarchy](https://github.com/basecamp/omarchy)
