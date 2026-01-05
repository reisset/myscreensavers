# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] - 2026-01-05

### Added
- **Visuals:** Implemented seamless effect transitions using `tte --reuse-canvas`.
- **Visuals:** Added fullscreen centering and anchor controls for better visual presentation.
- **Content:** Added new default ASCII art ("LINUX GANG").
- **Documentation:** Polished `README.md` with better formatting, emojis, and clearer instructions.
- **Documentation:** Added `CHANGELOG.md`.
- **Documentation:** Added `LICENSE` (MIT).

### Changed
- **Architecture:** **Major Rewrite** - Refactored the entire application from a complex Python/YAML architecture to lightweight Bash scripts.
    - Replaced the Python-based daemon and effect manager with `bin/screensaver` and `bin/screensaver-daemon`.
    - Removed YAML configuration dependency; configuration is now handled via environment variables and script arrays.
- **System:** Improved GNOME idle detection reliability by directly querying `org.gnome.Mutter.IdleMonitor` via `dbus-send`.
- **System:** Updated `install.sh` to handle dependencies and systemd service installation more robustly.

### Fixed
- **Dependencies:** Updated `TerminalTextEffects` usage to match the current API.
- **Fullscreen:** Improved fullscreen handling for Kitty, Alacritty, and GNOME Terminal.

## [Pre-Rewrite History] - 2026-01-05

*The following changes belong to the initial Python/YAML implementation phase, which has since been superseded by the Bash rewrite.*

- **Phase 5:** Completed initial documentation and polish.
- **Phase 4:** Implemented launch controller and idle detection setup.
- **Phase 3:** Implemented YAML configuration system.
- **Phase 2:** Added effect management and cycling logic.
- **Phase 1:** Established core screensaver engine.
