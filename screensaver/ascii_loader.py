"""ASCII art loading utilities."""

from pathlib import Path
from typing import List
import pyfiglet


class ASCIILoader:
    """Loads ASCII art from various sources."""

    @staticmethod
    def load_from_file(file_path: str) -> str:
        """
        Load ASCII art from a text file.

        Args:
            file_path: Path to the ASCII art file

        Returns:
            str: The ASCII art content

        Raises:
            FileNotFoundError: If the file doesn't exist
            IOError: If there's an error reading the file
        """
        path = Path(file_path).expanduser()
        if not path.exists():
            raise FileNotFoundError(f"ASCII art file not found: {file_path}")

        with open(path, 'r', encoding='utf-8') as f:
            return f.read()

    @staticmethod
    def load_from_directory(directory: str) -> List[str]:
        """
        Load all ASCII art files from a directory.

        Args:
            directory: Path to directory containing .txt files

        Returns:
            List[str]: List of ASCII art contents

        Raises:
            FileNotFoundError: If the directory doesn't exist
        """
        path = Path(directory).expanduser()
        if not path.exists() or not path.is_dir():
            raise FileNotFoundError(f"Directory not found: {directory}")

        art_list = []
        for txt_file in sorted(path.glob('*.txt')):
            try:
                with open(txt_file, 'r', encoding='utf-8') as f:
                    art_list.append(f.read())
            except IOError as e:
                print(f"Warning: Could not read {txt_file}: {e}")

        if not art_list:
            raise ValueError(f"No .txt files found in directory: {directory}")

        return art_list

    @staticmethod
    def generate_from_text(text: str, font: str = 'slant') -> str:
        """
        Generate ASCII art from text using pyfiglet.

        Args:
            text: The text to convert to ASCII art
            font: The pyfiglet font to use (default: 'slant')

        Returns:
            str: The generated ASCII art

        Raises:
            ValueError: If the font is invalid
        """
        try:
            fig = pyfiglet.Figlet(font=font)
            return fig.renderText(text)
        except pyfiglet.FontNotFound:
            raise ValueError(f"Invalid pyfiglet font: {font}")

    @staticmethod
    def list_available_fonts() -> List[str]:
        """
        Get list of available pyfiglet fonts.

        Returns:
            List[str]: List of font names
        """
        return pyfiglet.FigletFont.getFonts()
