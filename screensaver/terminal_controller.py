"""Terminal control utilities for screensaver."""

import sys
import termios
import tty
import select


class TerminalController:
    """Handles terminal control operations."""

    def __init__(self):
        self.old_settings = None

    def hide_cursor(self):
        """Hide the terminal cursor."""
        sys.stdout.write('\x1b[?25l')
        sys.stdout.flush()

    def show_cursor(self):
        """Show the terminal cursor."""
        sys.stdout.write('\x1b[?25h')
        sys.stdout.flush()

    def clear_screen(self):
        """Clear the terminal screen and move cursor to home."""
        sys.stdout.write('\x1b[H\x1b[2J')
        sys.stdout.flush()

    def enable_raw_mode(self):
        """Enable raw mode for immediate keypress detection."""
        if sys.stdin.isatty():
            self.old_settings = termios.tcgetattr(sys.stdin)
            tty.setcbreak(sys.stdin.fileno())

    def restore_terminal(self):
        """Restore terminal to original state."""
        self.show_cursor()
        if self.old_settings is not None:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)

    def check_for_input(self, timeout=0):
        """
        Check if there's input available without blocking.

        Args:
            timeout: Time to wait for input in seconds (default: 0 for non-blocking)

        Returns:
            bool: True if input is available, False otherwise
        """
        if not sys.stdin.isatty():
            return False

        # Use select to check for input without blocking
        readable, _, _ = select.select([sys.stdin], [], [], timeout)
        return bool(readable)

    def __enter__(self):
        """Context manager entry."""
        self.hide_cursor()
        self.enable_raw_mode()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - ensures terminal is restored."""
        self.restore_terminal()
        return False
