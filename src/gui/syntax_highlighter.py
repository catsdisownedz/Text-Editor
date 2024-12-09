import re
from PyQt5.QtGui import QSyntaxHighlighter

class SyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
       
