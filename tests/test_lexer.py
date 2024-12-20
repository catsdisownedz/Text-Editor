import pytest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from SCLPL.sclpl_lexer import sclplLexer

def test_basic_lexer():

    code = """
    int x = 2;
    int y = 300;  // This is a comment
    while(x <= y) {
        x++;
        int z = x * y;
    }
    """
    expected_tokens = [('TYPE', 'int'), ('IDENTIFIER', 'x'), ('ASSIGNMENT_OPERATOR', '='), ('DIGIT', '2'), 
                       ('TERMINAL', ';'), ('TYPE', 'int'), ('IDENTIFIER', 'y'), ('ASSIGNMENT_OPERATOR', '='), 
                       ('DIGIT', '300'), ('TERMINAL', ';'), ('COMMENT', '// This is a comment'), ('KEYWORDS', 'while'), 
                       ('BRACE_OR_PAREN', '('), ('IDENTIFIER', 'x'), ('CONDITIONAL_OPERATOR', '<='), ('IDENTIFIER', 'y'),
                       ('BRACE_OR_PAREN', ')'), ('BRACE_OR_PAREN', '{'), ('IDENTIFIER', 'x'), ('OPERATOR', '++'), 
                       ('TERMINAL', ';'), ('TYPE', 'int'), ('IDENTIFIER', 'z'), ('ASSIGNMENT_OPERATOR', '='), 
                       ('IDENTIFIER', 'x'), ('OPERATOR', '*'), ('IDENTIFIER', 'y'), ('TERMINAL', ';'), 
                       ('BRACE_OR_PAREN', '}')]
    tokens = sclplLexer(code)
    assert tokens == expected_tokens, f"Expected {expected_tokens} \n but got {tokens}"

def test_array_access():
    code = "int arr[10];"
    expected_tokens = [('TYPE', 'int'), ('IDENTIFIER', 'arr'), ('DIGIT', '10'), ('TERMINAL', ';')]
    tokens = sclplLexer(code)
    assert tokens == expected_tokens, f"Expected {expected_tokens} but got {tokens}"

def test_arithmetic_expression():
    code = "int sum = 10 + 20 * 30 / 2 % 7;"
    expected_tokens = [
        ('TYPE', 'int'), ('IDENTIFIER', 'sum'), ('ASSIGNMENT_OPERATOR', '='), 
        ('DIGIT', '10'), ('OPERATOR', '+'), ('DIGIT', '20'), ('OPERATOR', '*'), 
        ('DIGIT', '30'), ('OPERATOR', '/'), ('DIGIT', '2'), ('OPERATOR', '%'), 
        ('DIGIT', '7'), ('TERMINAL', ';')
    ]
    tokens = sclplLexer(code)
    assert tokens == expected_tokens, f"Expected {expected_tokens} but got {tokens}"

def test_comment_and_whitespace_ignored():
    code = """
    int x = 10;  // Comment
    int y = x + 5;  /* Block comment */
    """
    expected_tokens = [('TYPE', 'int'), ('IDENTIFIER', 'x'), ('ASSIGNMENT_OPERATOR', '='), ('DIGIT', '10'),
                       ('TERMINAL', ';'), 
                       ('COMMENT', '// Comment'), ('TYPE', 'int'), ('IDENTIFIER', 'y'), 
                       ('ASSIGNMENT_OPERATOR', '='), ('IDENTIFIER', 'x'), ('OPERATOR', '+'), 
                       ('DIGIT', '5'), ('TERMINAL', ';'), ('MULTI_LINE_COMMENT', '/* Block comment */')]
    tokens = sclplLexer(code)
    assert tokens == expected_tokens, f"Expected {expected_tokens} but got {tokens}"

def test_invalid_identifier():
    code = "int 1x = 100;"
    expected_tokens = [('TYPE', 'int'), ('DIGIT', '1'), ('IDENTIFIER', 'x'), 
                       ('ASSIGNMENT_OPERATOR', '='), ('DIGIT', '100'), ('TERMINAL', ';')]
    tokens = sclplLexer(code)
    assert tokens == expected_tokens, f"Expected {expected_tokens} but got {tokens}"

if __name__=="__main__":
    test_invalid_identifier()
