## TextEditor by mronz 🖋️
Welcome to TextEditor by mronz, a modern and sleek code editor that we're building from scratch to learn the ins and outs of programming languages, lexers, and parsers. This is more than just a text editor—it's a project where we explore how code editors understand and process programming languages while creating something functional and visually appealing.

#### 🚀 Features
Here’s what makes our editor special:

`Multi-tab Support:` Work on multiple files simultaneously, with each tab dynamically updating to show the file type or language logo.

`Automatic Language Recognition:` The editor detects the language you're coding in—even before you save the file!

`Custom Programming Language (SCLPL):`
We’re creating our own language called SCLPL (pronounced "Scalpel") to dive deep into the mechanics of lexers and parsers.
The editor features a lexer and parser built for SCLPL from scratch.

`Syntax Highlighting:` Bright, clear, and customizable syntax highlighting for various languages, including SCLPL.

`Word/Line Counter:` Always know how much you've written, displayed conveniently at the bottom.

`Bullet Points & Writing Features:` Great for jotting down tasks, notes, or documentation alongside code.

`File Management:` Automatically saves files with the correct extension in a dedicated folder: ~/Documents/TextEditor by mronz.

#### 🛠️ How It Works
We’re combining the basics of programming language theory with modern development practices:

Lexer: Breaks down raw text into tokens for processing.
Parser: Organizes tokens into a structured format (like a tree) to validate and understand the code.
Custom Grammar: We’ve defined rules for SCLPL, and the editor is built to process them while supporting other languages using libraries like guesslang.

#### 🎯 Goals
This project is not just about making a cool editor—it’s a learning experience for our team to:

Understand how code editors like VS Code and Sublime Text work under the hood.
Learn about language design, lexical analysis, and syntax parsing.
Build a fully functional and visually pleasing desktop application using Python.

#### 🛠️ Tech Stack
`Python:` The core language powering our editor.

`PyQt:` For the GUI, enabling a modern and clean interface.

`Custom Lexer & Parser:` Built from scratch for SCLPL, plus support for other languages using tools like guesslang.

`File Management:` Automatic directory and extension handling.

#### 📦 Getting Started
Want to try it out or contribute? Follow these steps:

Clone the Repository:

    git clone https://github.com/catsdisownedz/Text-Editor.git
    cd TextEditor

Install Dependencies:

    `pip install -r requirements.txt`

Run the Editor:

    `python src/main.py`

Explore SCLPL:

Open a new file, write some SCLPL code, and see it get parsed in real-time.