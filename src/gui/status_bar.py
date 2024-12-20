"""This module defines the `StatusBar` class to manage and update the status bar in the text editor."""
import tkinter as tk
from themes import DARK_THEME

class StatusBar:
    def __init__(self, root):
        """Initializes the status bar with a label displaying default text and styling."""
        self.status_bar = tk.Label(root, text="Lines: 0  |  Language: Text", anchor="w",
                                   bg=DARK_THEME["status_bar_bg"], fg=DARK_THEME["status_bar_fg"])
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def update_status(self, lines, language):
        """Updates the status bar with the current number of lines and language type."""
        self.status_bar.config(text=f"Lines: {lines}  |  Language: {language}")
