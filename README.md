# 🖥️ myscreensavers

Omarchy-style terminal screensavers for Ubuntu/GNOME.

Auto-activates after 5 minutes of idle. Displays animated ASCII art using [TerminalTextEffects](https://github.com/ChrisBuilds/terminaltexteffects).

## 🚀 Install

```bash
git clone git@github.com:reisset/myscreensavers.git ~/screensaver
cd ~/screensaver
./install.sh
```

Daemon starts automatically on login.

## Usage

**Test manually** (Ctrl+C to exit):
```bash
./bin/screensaver
```

**Check daemon:**
```bash
systemctl --user status screensaver-daemon
journalctl --user -u screensaver-daemon -f
```

## ⚙️ Configuration

### 1. Custom ASCII Art
Replace `config/ascii_art/ascii-text-art.txt` with your own text.
Generate art with [patorjk.com](https://patorjk.com/software/taag/) or `figlet`.

### 2. Idle Timeout
Default is 5 minutes. To change (e.g., to 10 mins):

```bash
systemctl --user edit screensaver-daemon
```

Add:
```ini
[Service]
Environment=IDLE_TIMEOUT_MS=600000
```
Restart: `systemctl --user restart screensaver-daemon`

### 3. Effects
Edit `bin/screensaver` and modify the `EFFECTS` array.
Available: `beams, matrix, rain, fireworks, spray, synthgrid, vhstape, blackhole, ...` (see script for full list)

## How it works

```
┌─────────────────────────────────────────────────────────────┐
│  screensaver-daemon                                         │
│  └─ polls GNOME IdleMonitor via DBus every 5s               │
│  └─ when idle > 5 min, launches fullscreen terminal         │
│  └─ terminal runs: tte <effect> < ascii_art.txt             │
│  └─ on user activity, kills the terminal                    │
└─────────────────────────────────────────────────────────────┘
```

**Requirements:**
- Ubuntu 22.04+ (GNOME Wayland/X11)
- Python 3 + `terminaltexteffects`
- Terminal: `kitty` or `alacritty` (recommended for best fullscreen), `gnome-terminal`

## Troubleshooting

- **Not activating?** Check `systemctl --user status screensaver-daemon`.
- **`tte` not found?** Ensure `~/.local/bin` is in your PATH.
- **Not fullscreen?** Install `kitty` or `alacritty` for native fullscreen support.

## Uninstall

```bash
systemctl --user stop screensaver-daemon
systemctl --user disable screensaver-daemon
rm ~/.config/systemd/user/screensaver-daemon.service
rm -rf ~/screensaver
```

## Credits

- [TerminalTextEffects](https://github.com/ChrisBuilds/terminaltexteffects)

- Inspired by [Omarchy](https://github.com/basecamp/omarchy)



## License

MIT, feel free to use as you wish! See [LICENSE](LICENSE) for details.
