"""
This module defines the `SyntaxHighlighter` class for applying syntax highlighting to a text widget
based on the tokens identified by the `sclplLexer`.
"""
from themes import DARK_THEME
import re
import os
import sys
from SCLPL.sclpl_lexer import sclplLexer
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

class SyntaxHighlighter:
    """
    A class that handles syntax highlighting for a given text widget based on tokens from the `sclplLexer`.
    """
    def __init__(self, text_widget):
        """Initializes the `SyntaxHighlighter` with a text widget."""
        self.text_widget = text_widget
        self.configure_tags()

    def configure_tags(self):
        """Configures the tags for the text widget, removing any existing tags."""
        for tag in self.text_widget.tag_names():
            self.text_widget.tag_delete(tag)

    def highlight(self):
        """Highlights the syntax in the text widget based on the tokens from the lexer."""
        self.text_widget.tag_remove("Token", "1.0", "end")
        content = self.text_widget.get("1.0", "end-1c")
        tokens = sclplLexer(content)

        index = "1.0"
        for ttype, tvalue in tokens:
            start_pos = self.text_widget.search(re.escape(tvalue), index, "end", regexp=True)
            if not start_pos:
                continue
            end_pos = f"{start_pos}+{len(tvalue)}c"

            color = self.get_token_color(ttype, tvalue)

            tag_name = f"token_{start_pos}_{end_pos}"
            self.text_widget.tag_add(tag_name, start_pos, end_pos)
            self.text_widget.tag_configure(tag_name, foreground=color)
            index = end_pos

    def get_token_color(self, ttype, tvalue):
        """Returns the color for a given token type and value."""
        if ttype == 'KEYWORDS':
            pastel_keywords = DARK_THEME["pastel_keyword_colors"]
            if tvalue in pastel_keywords:
                return pastel_keywords[tvalue]
            else:
                return DARK_THEME["keyword_color"]
        elif ttype == 'BRACE_OR_PAREN':
            bracket_colors = DARK_THEME["bracket_colors"]
            return bracket_colors.get(tvalue, DARK_THEME["foreground"])
        else:
            token_colors = DARK_THEME["token_colors"]
            return token_colors.get(ttype, DARK_THEME["foreground"])
        