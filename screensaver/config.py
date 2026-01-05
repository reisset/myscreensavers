"""Configuration management for screensaver."""

import os
from pathlib import Path
from typing import Dict, List, Optional
import yaml


class Config:
    """Screensaver configuration manager."""

    DEFAULT_CONFIG = {
        "idle": {
            "timeout_seconds": 300,
            "detection_method": "swayidle"
        },
        "screensaver": {
            "effect_duration": 30,
            "cycle_mode": "random",
            "enabled_effects": [
                "matrix", "rain", "decrypt", "fireworks",
                "waves", "beams", "pour", "swarm", "rings"
            ],
            "excluded_effects": []
        },
        "content": {
            "source": "pyfiglet",
            "file_path": "~/.config/terminal-screensaver/ascii_art/default.txt",
            "directory": "~/.config/terminal-screensaver/ascii_art/",
            "pyfiglet": {
                "text": "SCREENSAVER",
                "font": "slant"
            }
        },
        "terminal": {
            "hide_cursor": True
        }
    }

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration.

        Args:
            config_path: Path to config file (default: ~/.config/terminal-screensaver/config.yaml)
        """
        if config_path:
            self.config_path = Path(config_path).expanduser()
        else:
            self.config_path = Path.home() / ".config" / "terminal-screensaver" / "config.yaml"

        self.config = self._load_config()

    def _load_config(self) -> Dict:
        """
        Load configuration from file, falling back to defaults.

        Returns:
            Dict: Configuration dictionary
        """
        # Start with default config
        config = self.DEFAULT_CONFIG.copy()

        # Try to load user config
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    user_config = yaml.safe_load(f)
                    if user_config:
                        # Merge user config with defaults
                        config = self._merge_configs(config, user_config)
            except Exception as e:
                print(f"Warning: Could not load config from {self.config_path}: {e}")
                print("Using default configuration.")

        return config

    def _merge_configs(self, default: Dict, user: Dict) -> Dict:
        """
        Recursively merge user config into default config.

        Args:
            default: Default configuration
            user: User configuration

        Returns:
            Dict: Merged configuration
        """
        result = default.copy()

        for key, value in user.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value

        return result

    def get_idle_timeout(self) -> int:
        """Get idle timeout in seconds."""
        return self.config["idle"]["timeout_seconds"]

    def get_idle_detection_method(self) -> str:
        """Get idle detection method."""
        return self.config["idle"]["detection_method"]

    def get_effect_duration(self) -> int:
        """Get effect duration in seconds."""
        return self.config["screensaver"]["effect_duration"]

    def get_cycle_mode(self) -> str:
        """Get cycle mode (random or sequential)."""
        return self.config["screensaver"]["cycle_mode"]

    def get_enabled_effects(self) -> Optional[List[str]]:
        """Get list of enabled effects, or None to use defaults."""
        effects = self.config["screensaver"].get("enabled_effects")
        return effects if effects else None

    def get_excluded_effects(self) -> List[str]:
        """Get list of excluded effects."""
        return self.config["screensaver"].get("excluded_effects", [])

    def get_content_source(self) -> str:
        """Get content source type (file, directory, or pyfiglet)."""
        return self.config["content"]["source"]

    def get_content_file_path(self) -> str:
        """Get ASCII art file path."""
        path = self.config["content"]["file_path"]
        return str(Path(path).expanduser())

    def get_content_directory(self) -> str:
        """Get ASCII art directory path."""
        path = self.config["content"]["directory"]
        return str(Path(path).expanduser())

    def get_pyfiglet_text(self) -> str:
        """Get pyfiglet text."""
        return self.config["content"]["pyfiglet"]["text"]

    def get_pyfiglet_font(self) -> str:
        """Get pyfiglet font."""
        return self.config["content"]["pyfiglet"]["font"]

    def should_hide_cursor(self) -> bool:
        """Check if cursor should be hidden."""
        return self.config["terminal"]["hide_cursor"]

    def validate(self) -> bool:
        """
        Validate configuration.

        Returns:
            bool: True if valid, False otherwise
        """
        try:
            # Validate idle timeout
            if self.get_idle_timeout() <= 0:
                print("Error: idle timeout must be positive")
                return False

            # Validate effect duration
            if self.get_effect_duration() <= 0:
                print("Error: effect duration must be positive")
                return False

            # Validate cycle mode
            if self.get_cycle_mode() not in ["random", "sequential"]:
                print("Error: cycle_mode must be 'random' or 'sequential'")
                return False

            # Validate content source
            source = self.get_content_source()
            if source not in ["file", "directory", "pyfiglet"]:
                print("Error: content source must be 'file', 'directory', or 'pyfiglet'")
                return False

            # Validate content paths exist if using file/directory
            if source == "file":
                file_path = Path(self.get_content_file_path())
                if not file_path.exists():
                    print(f"Warning: ASCII art file not found: {file_path}")
                    print("Will fall back to pyfiglet text generation.")

            elif source == "directory":
                dir_path = Path(self.get_content_directory())
                if not dir_path.exists():
                    print(f"Warning: ASCII art directory not found: {dir_path}")
                    print("Will fall back to pyfiglet text generation.")

            return True

        except Exception as e:
            print(f"Configuration validation error: {e}")
            return False
