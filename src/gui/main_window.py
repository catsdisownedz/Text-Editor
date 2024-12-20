"""A Tkinter-based text editor application with tabs, file management, and a custom dark theme."""
import tkinter as tk
from tab_manager import TabManager
from save_manager import SaveManager
from status_bar import StatusBar
from themes import DARK_THEME
from custom_style import CustomStyle


class TextEditor:
    """A text editor with tab management, file operations, and a custom dark theme, built using Tkinter."""
    def __init__(self, root):
        self.root = root
        self.root.title("SCLPL")
        self.root.geometry("800x600")
        self.root.configure(bg=DARK_THEME["background"])
        self.style = CustomStyle(self.root)
        self.status_bar = StatusBar(self.root)
        self.tab_manager = TabManager(self.root, self.status_bar)
        self.save_manager = SaveManager(self.tab_manager)
        self.create_menu_bar()
        
    def create_menu_bar(self):
        menu_bar = tk.Menu(self.root)
        file_menu = tk.Menu(menu_bar, tearoff=0, bg=DARK_THEME["background"], fg=DARK_THEME["foreground"])
        file_menu.add_command(label="New File", command=self.tab_manager.new_file)
        file_menu.add_command(label="Open File", command=self.save_manager.open_file)
        file_menu.add_command(label="Save File", command=self.save_manager.save_file)
        file_menu.add_command(label="Save As", command=self.save_manager.save_file_as)
        file_menu.add_command(label="Close Tab", command=self.tab_manager.close_tab)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        edit_menu = tk.Menu(menu_bar, tearoff=0, bg=DARK_THEME["background"], fg=DARK_THEME["foreground"])
        edit_menu.add_command(label="Cut", command=lambda: self.tab_manager.focused_text_widget_event("cut"))
        edit_menu.add_command(label="Copy", command=lambda: self.tab_manager.focused_text_widget_event("copy"))
        edit_menu.add_command(label="Paste", command=lambda: self.tab_manager.focused_text_widget_event("paste"))
        menu_bar.add_cascade(label="Edit", menu=edit_menu)

        self.root.config(menu=menu_bar)
    def update_status(self):
        self.tab_manager.update_status()
    def run(self):
        self.root.mainloop()
if __name__ == "__main__":
    root = tk.Tk()
    app = TextEditor(root)
    app.run()
