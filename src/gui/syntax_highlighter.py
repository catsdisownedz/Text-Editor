import re
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)
from themes import DARK_THEME

class SyntaxHighlighter:
    def __init__(self, text_widget):
        self.text_widget = text_widget

        # Define syntax patterns
        # This pattern matches both double- and single-quoted strings:
        # ".*?" or '.*?'
        self.patterns = {
            "keyword":  r"\b(int|while|for|array)\b",
            "number":   r"\b\d+\b",
            "string": r"(\".*?\"|\'.*?\')",
            "comment":  r"#.*",
            "operator": r"[+\-*/=]"
        }

        self.setup_tags()

    def setup_tags(self):
        # Configure tags for different syntax elements using DARK_THEME
        self.text_widget.tag_configure("keyword",  foreground=DARK_THEME["keyword_color"])
        self.text_widget.tag_configure("number",   foreground=DARK_THEME["number_color"])
        self.text_widget.tag_configure("string",   foreground=DARK_THEME["string_color"])
        self.text_widget.tag_configure("comment",  foreground=DARK_THEME["comment_color"])
        self.text_widget.tag_configure("operator", foreground=DARK_THEME["operator_color"])

    def highlight(self):
        # Remove existing tags
        for token_type in self.patterns.keys():
            self.text_widget.tag_remove(token_type, "1.0", "end")

        content = self.text_widget.get("1.0", "end-1c")

        # Apply tags based on regex matches
        for token_type, pattern in self.patterns.items():
            for match in re.finditer(pattern, content, flags=re.DOTALL):
                start, end = match.span()
                start_index = self.text_widget.index(f"1.0+{start}c")
                end_index   = self.text_widget.index(f"1.0+{end}c")
                self.text_widget.tag_add(token_type, start_index, end_index)
