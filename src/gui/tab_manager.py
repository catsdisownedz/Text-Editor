from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
import os
import sys
import json
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)
from themes import DARK_THEME
from status_bar import StatusBar
from SCLPL.abstract_syntax_tree import AST
from SCLPL.sclpl_lexer import sclplLexer
from SCLPL.sclpl_parser import sclplParser
from syntax_highlighter import SyntaxHighlighter
from PIL import Image, ImageTk
from PIL.Image import Resampling

class TabManager:
    def __init__(self, root, status_bar):
        self.root = root
        self.status_bar = status_bar
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both")
        self.language = "Text"
        self.tabs = {}
        self.file_paths = {}
                
        self.bracket_pairs = {
            '(': ')',
            '{': '}',
            '[': ']',
            '<': '>',
            '"': '"',
            "'": "'"
        }
                
        
        self.add_tab("Untitled")

        self.notebook.bind("<Double-1>", self.rename_tab)


    def add_tab(self, title="Untitled", content=None, file_path=None):
        frame = tk.Frame(self.notebook, bg=DARK_THEME["editor_background"])
        frame.pack(expand=True, fill="both")

        text_widget = tk.Text(frame, wrap="word", bg=DARK_THEME["editor_background"], fg=DARK_THEME["foreground"],
                              insertbackground=DARK_THEME["cursor_color"], undo=True)
        text_widget.pack(expand=True, fill="both", padx=5, pady=5)

        if content:
            text_widget.insert("1.0", content)
            
        
        text_widget.bind("<KeyRelease>", lambda e: self.update_status())
        text_widget.bind("<KeyPress>", self.handle_bracket)
        
        self.notebook.add(frame, text=title)
        self.tabs[title] = text_widget
        self.file_paths[title] = file_path

        frame.toolbar_frame = tk.Frame(frame, bg=DARK_THEME["editor_background"])
        frame.toolbar_frame.pack(side='top', fill='x')
        
        if not hasattr(self, 'syntax_highlighters'):
            self.syntax_highlighters = {}
        self.syntax_highlighters[title] = SyntaxHighlighter(text_widget)


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
        tokens = sclplLexer(content)
        sclpl_token_types = {'KEYWORDS', 'TYPE', 'OPERATOR', 'CONDITIONAL_OPERATOR', 'ASSIGNMENT_OPERATOR', 'DIGIT', 'BRACE_OR_PAREN'}

        for ttype, _ in tokens:
            if ttype in sclpl_token_types:
                return True
        return False

    
    def add_play_button(self, frame):
        if not hasattr(frame, "play_button"):
            play_button = ttk.Button(frame, text="▶ Run", command=self.parser_callback)
            play_button.pack(side='right', padx=5, pady=5)
            frame.play_button = play_button
            
    def remove_play_button(self, frame):
        if hasattr(frame, "play_button"):
            frame.play_button.destroy()
            del frame.play_button

    
    def parser_callback(self):
        print("function called!")
        
        if current_tab := self.notebook.select():
            print("first if condition!")
            tab_name = self.notebook.tab(current_tab, "text")
            print(f"tab dict: {self.tabs}")
            print(f"tab name: {tab_name}")

            text_widget = self.tabs.get(tab_name)
            print(f"text widget name: {text_widget}")

            if text_widget:
                print("second if condition!")
                content = text_widget.get("1.0", "end-1c")
                tokens = sclplLexer(content)
                

                # 1. Parse the content using the Parser class
                parser = sclplParser(tokens)
                ast = parser.parse()  # Assuming `Parser.parse()` returns tokens or an AST
                print(json.dumps(ast, indent=4))

                # 2. Generate AST (ASCII tree) using the abstract_syntax_tree module
                visualizer = AST(ast)
                image_path = visualizer.draw_ast('AST')

                # 3. Create a new tab to display the AST
                new_tab_title = f"{tab_name}_AST.sclpl"
                self.add_uneditable_tab(new_tab_title, image_path)

        print("works")


    def new_file(self):
        self.add_tab(f"Untitled {len(self.tabs) + 1}")

    def close_tab(self):
        if current_tab := self.notebook.select():
            tab_name = self.notebook.tab(current_tab, "text")
            del self.tabs[tab_name]
            del self.file_paths[tab_name]
            del self.syntax_highlighters[tab_name]
            self.notebook.forget(current_tab)

    def rename_tab(self, event):
        # Detect the tab clicked
        clicked_tab = self.notebook.index(f"@{event.x},{event.y}")
        if clicked_tab >= 0:
            tab_name = self.notebook.tab(clicked_tab, "text")
            if new_name := simpledialog.askstring(
                "Rename Tab", f"Enter new name for tab '{tab_name}':"
            ):
                # Update tab name
                self.notebook.tab(clicked_tab, text=new_name)

                # Update dictionary keys for tabs and file paths
                self.tabs[new_name] = self.tabs.pop(tab_name)
                self.file_paths[new_name] = self.file_paths.pop(tab_name)

                self.syntax_highlighters[new_name] = self.syntax_highlighters.pop(tab_name)
                # Automatically save with the new name
                self.auto_save(new_name)
                print(f"New tab name {self.tabs}")

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
        if current_text_widget := self.tabs.get(
            self.notebook.tab(current_tab, "text")
        ):
            if event_type == "cut":
                current_text_widget.event_generate("<<Cut>>")
            elif event_type == "copy":
                current_text_widget.event_generate("<<Copy>>")
            elif event_type == "paste":
                current_text_widget.event_generate("<<Paste>>")

    def get_text_widget(self):
        if current_tab := self.notebook.select():
            tab_name = self.notebook.tab(current_tab, "text")
            return self.tabs.get(tab_name)
        return None


    def add_uneditable_tab(self, title, image_path):
        frame = tk.Frame(self.notebook, bg=DARK_THEME["editor_background"])
        frame.pack(expand=True, fill="both")

        label = tk.Label(frame, bg=DARK_THEME["editor_background"])
        label.pack(expand=True, fill="both", padx=5, pady=5)

        try:
            original_image = Image.open(image_path)

            def resize_image(event):
                new_width = event.width - 20
                new_height = event.height - 20
                original_width, original_height = original_image.size
                aspect_ratio = original_width / original_height
                if (new_width / new_height) > aspect_ratio:
                    new_width = int(new_height * aspect_ratio)
                else:
                    new_height = int(new_width / aspect_ratio)
                resized = original_image.resize((new_width, new_height), Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(resized)
                label.config(image=photo)
                label.image = photo  
            frame.bind("<Configure>", resize_image)

        except Exception as e:
            print(f"Error loading image: {e}")
            label.config(text="Failed to load AST image")

        self.notebook.add(frame, text=title)
        self.notebook.select(frame)


    def update_status(self):
        current_tab = self.notebook.select()
        if current_tab:
            tab_name = self.notebook.tab(current_tab, "text")
            text_widget = self.tabs.get(tab_name)
            if text_widget:
                lines = int(text_widget.index('end-1c').split('.')[0])
                frame = text_widget.master
                self.detect_language_and_update_ui(frame, text_widget)
                
                self.syntax_highlighters[tab_name].highlight()
                
                if not self.language:
                    self.language = "Text"
                self.status_bar.update_status(lines, self.language)
                
    def handle_bracket(self, event):
        if current_tab := self.notebook.select():
            tab_name = self.notebook.tab(current_tab, "text")
            text_widget = self.tabs.get(tab_name)

            if text_widget and self.language == "SCLPL":
                opening_bracket = event.char
                if opening_bracket in self.bracket_pairs:
                    closing_bracket = self.bracket_pairs[opening_bracket]

                    text_widget.insert("insert", opening_bracket + closing_bracket)
                    text_widget.mark_set("insert", "insert-1c")

                    return "break"
        return None