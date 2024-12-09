import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from themes import DARK_THEME
from status_bar import StatusBar
class TabManager:
    def __init__(self, root, status_bar):
        self.root = root
        self.status_bar = status_bar
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both")

        self.tabs = {}  # Dictionary to store tabs and their Text widgets
        self.file_paths = {}
        self.add_tab("Untitled")

        # Bind <Double-1> for renaming tabs
        self.notebook.bind("<Double-1>", self.rename_tab)

    def add_tab(self, title="Untitled", content=None, file_path=None):
        # Create a new frame for the tab
        frame = tk.Frame(self.notebook, bg=DARK_THEME["editor_background"])
        frame.pack(expand=True, fill="both")

        # Add a Text widget to the frame
        text_widget = tk.Text(frame, wrap="word", bg=DARK_THEME["editor_background"], fg=DARK_THEME["foreground"],
                              insertbackground=DARK_THEME["cursor_color"], undo=True)
        text_widget.pack(expand=True, fill="both", padx=5, pady=5)

        # If content is provided, insert it into the Text widget
        if content:
            text_widget.insert("1.0", content)

        text_widget.bind("<KeyRelease>", lambda e: self.update_status())
        
        # Add the frame to the notebook
        self.notebook.add(frame, text=title)
        self.tabs[title] = text_widget
        self.file_paths[title] = file_path

    def new_file(self):
        self.add_tab(f"Untitled {len(self.tabs) + 1}")

    def close_tab(self):
        current_tab = self.notebook.select()
        if current_tab:
            tab_name = self.notebook.tab(current_tab, "text")
            del self.tabs[tab_name]
            del self.file_paths[tab_name]
            self.notebook.forget(current_tab)

    def rename_tab(self, event):
        # Detect the tab clicked
        clicked_tab = self.notebook.index("@{},{}".format(event.x, event.y))
        if clicked_tab >= 0:
            tab_name = self.notebook.tab(clicked_tab, "text")
            new_name = simpledialog.askstring("Rename Tab", f"Enter new name for tab '{tab_name}':")
            if new_name:
                # Update tab name
                self.notebook.tab(clicked_tab, text=new_name)

                # Update dictionary keys for tabs and file paths
                self.tabs[new_name] = self.tabs.pop(tab_name)
                self.file_paths[new_name] = self.file_paths.pop(tab_name)

                # Automatically save with the new name
                self.auto_save(new_name)

    def auto_save(self, tab_name):
        # Save the content of the tab to a file with the new name
        text_widget = self.tabs[tab_name]
        content = text_widget.get("1.0", "end-1c")  # Get the text content

        # Use the new tab name as the file name
        file_name = f"{tab_name}.txt"
        with open(file_name, "w") as file:
            file.write(content)

        # Update the file path in the dictionary
        self.file_paths[tab_name] = file_name

    def focused_text_widget_event(self, event_type):
        # Get the currently focused Text widget
        current_tab = self.notebook.select()
        current_text_widget = self.tabs.get(self.notebook.tab(current_tab, "text"))
        if current_text_widget:
            if event_type == "cut":
                current_text_widget.event_generate("<<Cut>>")
            elif event_type == "copy":
                current_text_widget.event_generate("<<Copy>>")
            elif event_type == "paste":
                current_text_widget.event_generate("<<Paste>>")

    def get_text_widget(self):
        current_tab = self.notebook.select()
        if current_tab:
            tab_name = self.notebook.tab(current_tab, "text")
            return self.tabs.get(tab_name)
        return None

    def update_status(self):
        current_tab = self.notebook.select()
        if current_tab:
            tab_name = self.notebook.tab(current_tab, "text")
            text_widget = self.tabs.get(tab_name)
            if text_widget:
                # Calculate the number of lines
                lines = int(text_widget.index('end-1c').split('.')[0])
                self.status_bar.update_status(lines, "Text")
