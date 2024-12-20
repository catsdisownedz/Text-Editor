"""
CustomStyle class for applying a dark theme
"""
from tkinter import ttk
from themes import DARK_THEME

class CustomStyle:
    """
    CustomStyle class for applying a dark theme
    """
    def __init__(self, root):
        self.style = ttk.Style(root)
        self.root = root
        self.setup_style()
    def setup_style(self):
        """Configures and applies the custom dark theme styles"""
        self.style.theme_use('clam')
        self.style.configure('.',
                             background=DARK_THEME["background"],
                             foreground=DARK_THEME["foreground"],
                             borderwidth=0)
        self.style.configure('TButton',
                             background=DARK_THEME["editor_background"],
                             foreground=DARK_THEME["foreground"],
                             borderwidth=1,
                             relief='flat',
                             highlightcolor= DARK_THEME["hover_button_1"] )
        self.style.map('TButton',
                       background=[('active', DARK_THEME["hover_button_1"])],
                       relief=[('pressed', DARK_THEME["hover_button_1"])])
        self.style.configure('TNotebook',
                             background=DARK_THEME["background"],
                             borderwidth=1,
                             relief="flat")
        self.style.configure('TNotebook.Tab',
                             background=DARK_THEME["editor_background"],
                             foreground=DARK_THEME["foreground"],
                             padding=[20, 10],
                             borderwidth=1,
                             relief="flat")
        self.style.map('TNotebook.Tab',
                       background=[('selected', DARK_THEME["editor_background"])],
                       foreground=[('selected', DARK_THEME["foreground"])],
                       bordercolor=[('selected', DARK_THEME["hover_button_4"])]
                      )
        self.style.configure('TextFrame.TFrame',
                             background=DARK_THEME["background"],
                             borderwidth=0.5,
                             bordercolor="#555555",
                             relief="flat")
        self.style.configure('TMenu',
                             background=DARK_THEME["background"],
                             foreground=DARK_THEME["foreground"],
                             relief='flat',
                             borderwidth=0)
        self.style.map('TMenu',
                       background=[('active', DARK_THEME["hover_button_1"])])
        # Menu Bar (File | Edit) customization
        self.style.configure('TMenubar',
                             background=DARK_THEME["background"],
                             foreground=DARK_THEME["foreground"],
                             relief='flat',
                             borderwidth=0)
        self.style.map('TMenubar',
                       background=[('active', DARK_THEME["hover_button_1"])])
        # Status Bar customization
        self.style.configure('StatusBar.TFrame',
                             background=DARK_THEME["background"],
                             borderwidth=0)
        # Caret customization
        self.root.option_add('*Text.insertBackground', DARK_THEME["cursor_color"])
        self.root.option_add('*Text.background', DARK_THEME["background"])
        self.root.option_add('*Text.foreground', DARK_THEME["foreground"])
    def apply_status_bar_style(self, status_bar_frame):
        """Apply styles to the status bar frame."""
        status_bar_frame.configure(style='StatusBar.TFrame')
