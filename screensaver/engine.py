"""Core screensaver engine."""

import sys
import time
from pathlib import Path
from terminaltexteffects.effects.effect_matrix import Matrix

from .terminal_controller import TerminalController
from .ascii_loader import ASCIILoader


class ScreensaverEngine:
    """Main screensaver engine."""

    def __init__(self, ascii_art: str = None, ascii_file: str = None):
        """
        Initialize the screensaver engine.

        Args:
            ascii_art: ASCII art string to display
            ascii_file: Path to ASCII art file (used if ascii_art is None)
        """
        self.terminal = TerminalController()

        # Load ASCII art
        if ascii_art:
            self.ascii_art = ascii_art
        elif ascii_file:
            self.ascii_art = ASCIILoader.load_from_file(ascii_file)
        else:
            # Default: generate simple ASCII art
            self.ascii_art = ASCIILoader.generate_from_text("SCREENSAVER", font="slant")

    def run_effect(self, effect_name: str = "matrix"):
        """
        Run a single effect on the ASCII art.

        Args:
            effect_name: Name of the effect to run (default: matrix)
        """
        try:
            with self.terminal:
                self.terminal.clear_screen()

                # Create effect instance
                if effect_name == "matrix":
                    effect = Matrix(self.ascii_art)
                else:
                    # Fallback to matrix if unknown effect
                    effect = Matrix(self.ascii_art)

                # Run the effect
                with effect.terminal_output() as terminal:
                    for frame in effect:
                        # Check for exit condition
                        if self.terminal.check_for_input():
                            break

                        # Print the frame
                        terminal.print(frame)

        except KeyboardInterrupt:
            pass
        except Exception as e:
            print(f"Error running screensaver: {e}", file=sys.stderr)
        finally:
            self.terminal.restore_terminal()

    def run(self):
        """Run the screensaver with default settings."""
        self.run_effect("matrix")


def main():
    """Main entry point for the screensaver."""
    # For now, use a simple default
    engine = ScreensaverEngine()
    engine.run()


if __name__ == "__main__":
    main()
