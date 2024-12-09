import tkinter as tk
from tkinter import ttk
from themes import DARK_THEME

class CustomStyle:
    def __init__(self, root):
        self.style = ttk.Style(root)
        self.root = root
        self.setup_style()

    def setup_style(self):
        # Set the base theme to 'clam' for a modern look
        self.style.theme_use('clam')

        # General settings for all widgets
        self.style.configure('.', 
                             background=DARK_THEME["background"],  # Dark background
                             foreground=DARK_THEME["foreground"],  # White text
                             borderwidth=0)  # Remove default borders

        # Customize buttons
        self.style.configure('TButton',
                             background=DARK_THEME["editor_background"],
                             foreground=DARK_THEME["foreground"],
                             borderwidth=1,
                             relief='flat',
                             highlightcolor= DARK_THEME["hover_button_1"] )
        self.style.map('TButton',
                       background=[('active', DARK_THEME["hover_button_1"])],  # Pastel pink on hover
                       relief=[('pressed', DARK_THEME["hover_button_1"])])

        # Customize Notebook (Tabs)
        self.style.configure('TNotebook',
                             background=DARK_THEME["background"],
                             borderwidth=1,  # Faint gray border
                             relief="flat")
        
        self.style.configure('TNotebook.Tab',
                             background=DARK_THEME["editor_background"],
                             foreground=DARK_THEME["foreground"],
                             padding=[20, 10],  # Bigger padding for tabs
                             borderwidth=1,
                             relief="flat")
        self.style.map('TNotebook.Tab',
                       background=[('selected', DARK_THEME["editor_background"])],  # Same background for selected tab
                       foreground=[('selected', DARK_THEME["foreground"])],  # Text color for selected tab
                       bordercolor=[('selected', DARK_THEME["hover_button_4"])]  # Thin orange border for selected tab
                      ) 
        # Customize the border around the text widget
        self.style.configure('TextFrame.TFrame',
                             background=DARK_THEME["background"],
                             borderwidth=1,# Thin gray border
                             bordercolor="#555555",
                             relief="flat")
        
        # Customize menus
        self.style.configure('TMenu',
                             background=DARK_THEME["background"],
                             foreground=DARK_THEME["foreground"],
                             relief='flat',
                             borderwidth=0)
        self.style.map('TMenu',
                       background=[('active', DARK_THEME["hover_button_1"])])  # Pink hover for menu items

        # Menu Bar (File | Edit) customization
        self.style.configure('TMenubar',
                             background=DARK_THEME["background"],  # Black background
                             foreground=DARK_THEME["foreground"],
                             relief='flat',
                             borderwidth=0)
        self.style.map('TMenubar',
                       background=[('active', DARK_THEME["hover_button_1"])])  # Pink hover

        # Status Bar customization
        self.style.configure('StatusBar.TFrame',
                             background=DARK_THEME["background"],  # Seamless blending with text area
                             borderwidth=0)

        # Caret customization
        self.root.option_add('*Text.insertBackground', DARK_THEME["cursor_color"])  # Green caret
        self.root.option_add('*Text.background', DARK_THEME["background"])  # Text background
        self.root.option_add('*Text.foreground', DARK_THEME["foreground"])  # Text color

    def apply_status_bar_style(self, status_bar_frame):
        """Apply styles to the status bar frame."""
        status_bar_frame.configure(style='StatusBar.TFrame')
