"""Core screensaver engine."""

import sys
import time
from pathlib import Path

from .terminal_controller import TerminalController
from .ascii_loader import ASCIILoader
from .effects import EffectManager


class ScreensaverEngine:
    """Main screensaver engine."""

    def __init__(
        self,
        ascii_art: str = None,
        ascii_file: str = None,
        enabled_effects: list = None,
        excluded_effects: list = None,
        cycle_mode: str = "random",
        effect_duration: int = 30
    ):
        """
        Initialize the screensaver engine.

        Args:
            ascii_art: ASCII art string to display
            ascii_file: Path to ASCII art file (used if ascii_art is None)
            enabled_effects: List of effect names to enable
            excluded_effects: List of effect names to exclude
            cycle_mode: "random" or "sequential"
            effect_duration: Seconds per effect before cycling
        """
        self.terminal = TerminalController()
        self.effect_manager = EffectManager(enabled_effects, excluded_effects, cycle_mode)
        self.effect_duration = effect_duration

        # Load ASCII art
        if ascii_art:
            self.ascii_art = ascii_art
        elif ascii_file:
            self.ascii_art = ASCIILoader.load_from_file(ascii_file)
        else:
            # Default: generate simple ASCII art
            self.ascii_art = ASCIILoader.generate_from_text("SCREENSAVER", font="slant")

    def run_single_effect(self, effect_class):
        """
        Run a single effect on the ASCII art.

        Args:
            effect_class: The effect class to instantiate

        Returns:
            bool: True if should continue, False if exit requested
        """
        try:
            self.terminal.clear_screen()

            # Create effect instance
            effect = effect_class(self.ascii_art)

            # Run the effect with timeout
            start_time = time.time()

            with effect.terminal_output() as terminal:
                for frame in effect:
                    # Check for exit condition
                    if self.terminal.check_for_input():
                        return False

                    # Check if duration exceeded
                    if time.time() - start_time > self.effect_duration:
                        break

                    # Print the frame
                    terminal.print(frame)

            return True

        except KeyboardInterrupt:
            return False
        except Exception as e:
            print(f"Error running effect: {e}", file=sys.stderr)
            return True  # Continue to next effect

    def run(self):
        """Run the screensaver with cycling effects."""
        try:
            with self.terminal:
                while True:
                    # Get next effect
                    effect_class = self.effect_manager.get_next_effect()

                    # Run the effect
                    should_continue = self.run_single_effect(effect_class)

                    if not should_continue:
                        break

        except KeyboardInterrupt:
            pass
        finally:
            self.terminal.restore_terminal()


def main():
    """Main entry point for the screensaver."""
    from .config import Config
    from .ascii_loader import ASCIILoader

    # Load configuration
    config = Config()

    if not config.validate():
        print("Configuration validation failed. Using safe defaults.")

    # Load ASCII art based on config
    ascii_art = None
    source = config.get_content_source()

    try:
        if source == "file":
            ascii_art = ASCIILoader.load_from_file(config.get_content_file_path())
        elif source == "directory":
            # Load first file from directory (could be randomized later)
            art_list = ASCIILoader.load_from_directory(config.get_content_directory())
            ascii_art = art_list[0] if art_list else None
        elif source == "pyfiglet":
            ascii_art = ASCIILoader.generate_from_text(
                config.get_pyfiglet_text(),
                config.get_pyfiglet_font()
            )
    except Exception as e:
        print(f"Warning: Could not load ASCII art: {e}")
        print("Falling back to default text generation.")
        ascii_art = ASCIILoader.generate_from_text("SCREENSAVER", "slant")

    # Create engine with configuration
    engine = ScreensaverEngine(
        ascii_art=ascii_art,
        enabled_effects=config.get_enabled_effects(),
        excluded_effects=config.get_excluded_effects(),
        cycle_mode=config.get_cycle_mode(),
        effect_duration=config.get_effect_duration()
    )

    engine.run()


if __name__ == "__main__":
    main()
