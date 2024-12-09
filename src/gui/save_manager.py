from tkinter import filedialog
import os
import tkinter as tk

class SaveManager:
    def __init__(self, tab_manager):
        self.tab_manager = tab_manager

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()

        # Use the file name for the tab title
        file_name = os.path.basename(file_path)
        self.tab_manager.add_tab(title=file_name, content=content, file_path=file_path)

    def save_file(self):
        current_tab = self.tab_manager.notebook.select()
        if current_tab:
            widget_index = self.tab_manager.notebook.index(current_tab)
            widget_name = self.tab_manager.notebook.tab(widget_index, "text")
            if widget_name == "Untitled":
                self.save_file_as()
            else:
                self._write_to_file(widget_name)

    def save_file_as(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            self._write_to_file(file_path)

    def _write_to_file(self, file_path):
        text_widget = self.tab_manager.get_text_widget()
        if text_widget:
            content = text_widget.get(1.0, tk.END)
            with open(file_path, "w") as file:
                file.write(content)
            current_tab = self.tab_manager.notebook.select()
            self.tab_manager.notebook.tab(current_tab, text=os.path.basename(file_path))
