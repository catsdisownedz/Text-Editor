import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
import time
import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)
from themes import DARK_THEME
from status_bar import StatusBar
from sclpl_parser import parserpar, abstract_syntax_tree

class TabManager:
    def __init__(self, root, status_bar):
        self.root = root
        self.status_bar = status_bar
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both")
        self.language = "Text"
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


    def detect_language_and_update_ui(self, frame, text_widget):
        content = text_widget.get("1.0", "end-1c")
        is_sclpl = self.detect_language(content)
        
        if is_sclpl:
            self.add_play_button(frame)
        else:
            self.remove_play_button(frame)
        lines = content.count("\n") + 1
        self.language = "SCLPL" if is_sclpl else "Text"
        self.status_bar.update_status(lines, self.language)
        

    def detect_language(self, content):
        #this is just a placeholder for the actual langauge recognition lol 
        #it will call the actual function from sclpl_parser/language_recognition.py       
        sclpl_keywords = ["int", "while", "for", "array"]
        return any(keyword in content for keyword in sclpl_keywords)
    
    def add_play_button(self, frame):
        """
        Adds a play button to the frame with a fade-in effect.
        """
        if not hasattr(frame, "play_button"):
            play_button = ttk.Button(frame, text="▶ Run", command=self.parser_callback,
                                     bg=DARK_THEME.get("button_bg", "#default_bg"),
                                     fg=DARK_THEME.get("button_fg", "#default_fg"))
            play_button.place(relx=0.9, rely=0.02)

            # Fade-in effect
            for opacity in range(0, 100, 5):
                self.root.attributes("-alpha", opacity / 100)
                self.root.update()
                time.sleep(0.01)

            frame.play_button = play_button
            
    def remove_play_button(self, frame):
        """
        Removes the play button if it exists.
        """
        if hasattr(frame, "play_button"):
            frame.play_button.destroy()
            del frame.play_button

    
    def parser_callback(self):
        current_tab = self.notebook.select()
        if current_tab:
            tab_name = self.notebook.tab(current_tab, "text")
            text_widget = self.tabs.get(tab_name)

            if text_widget:
                content = text_widget.get("1.0", "end-1c")

                # 1. Parse the content using the Parser class
                tokens = parserpar(content).parse()  # Assuming `Parser.parse()` returns tokens or an AST

                # 2. Generate AST (ASCII tree) using the abstract_syntax_tree module
                ast_representation = abstract_syntax_tree.draw_ast(tokens)  # `draw_ast` returns the ASCII representation of the AST

                # 3. Create a new tab to display the AST
                new_tab_title = f"{tab_name}_AST.sclpl"
                self.add_uneditable_tab(new_tab_title, ast_representation)
                
        print("works")
        #placeholderrr

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


    def add_uneditable_tab(self,title,content):
        """
        Adds a new uneditable tab, useful for displaying AST.
        """
        frame = tk.Frame(self.notebook, bg=DARK_THEME["editor_background"])
        frame.pack(expand=True, fill="both")

        text_widget = tk.Text(frame, wrap="word", bg=DARK_THEME["editor_background"], fg=DARK_THEME["foreground"],
                              insertbackground=DARK_THEME["cursor_color"], state="disabled")
        text_widget.insert("1.0", content)
        text_widget.pack(expand=True, fill="both", padx=5, pady=5)

        self.notebook.add(frame, text=title)

    def update_status(self):
        current_tab = self.notebook.select()
        if current_tab:
            tab_name = self.notebook.tab(current_tab, "text")
            text_widget = self.tabs.get(tab_name)
            if text_widget:
                # Calculate the number of lines
                lines = int(text_widget.index('end-1c').split('.')[0])
                
                if not self.language:
                    self.language = "Text"
                self.status_bar.update_status(lines, self.language)