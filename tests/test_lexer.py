import pytest
from SCLPL.sclpl_lexer import sclplLexer  # Assuming the lexer code is in lexer.py

def test_basic_lexer():
    code = """
    int x = 2;
    int y = 300;  // This is a comment
    while(x <= y) {
        x++;
        int z = x * y;
    }
    """
    expected_tokens = [
        ('TYPE', 'int'), ('IDENTIFIER', 'x'), ('ASSIGNMENT_OPERATOR', '='), ('DIGIT', '2'), ('TERMINAL', ';'),
        ('TYPE', 'int'), ('IDENTIFIER', 'y'), ('ASSIGNMENT_OPERATOR', '='), ('DIGIT', '300'), ('TERMINAL', ';'),
        ('KEYWORDS', 'while'), ('BRACE_OR_PAREN', '('), ('IDENTIFIER', 'x'), ('CONDITIONAL_OPERATOR', '<='), ('IDENTIFIER', 'y'), ('BRACE_OR_PAREN', ')'),
        ('BRACE_OR_PAREN', '{'), ('IDENTIFIER', 'x'), ('OPERATOR', '++'), ('TERMINAL', ';'), ('TYPE', 'int'), 
        ('IDENTIFIER', 'z'), ('ASSIGNMENT_OPERATOR', '='), ('IDENTIFIER', 'x'), ('OPERATOR', '*'), ('IDENTIFIER', 'y'), ('TERMINAL', ';')
    ]
    tokens = sclplLexer(code)
    assert tokens == expected_tokens, f"Expected {expected_tokens} but got {tokens}"

def test_array_access():
    code = "int arr[10];"
    expected_tokens = [('TYPE', 'int'), ('IDENTIFIER', 'arr'), ('ARRAY_ACCESS', 'arr[10]'), ('TERMINAL', ';')]
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
    expected_tokens = [
        ('TYPE', 'int'), ('IDENTIFIER', 'x'), ('ASSIGNMENT_OPERATOR', '='), ('DIGIT', '10'), ('TERMINAL', ';'),
        ('TYPE', 'int'), ('IDENTIFIER', 'y'), ('ASSIGNMENT_OPERATOR', '='), ('IDENTIFIER', 'x'), ('OPERATOR', '+'), ('DIGIT', '5'), ('TERMINAL', ';')
    ]
    tokens = sclplLexer(code)
    assert tokens == expected_tokens, f"Expected {expected_tokens} but got {tokens}"

def test_invalid_identifier():
    code = "int 1x = 100;"  # Invalid identifier
    expected_tokens = [('TYPE', 'int'), ('IDENTIFIER', '1x'), ('ASSIGNMENT_OPERATOR', '='), ('DIGIT', '100'), ('TERMINAL', ';')]
    tokens = sclplLexer(code)
    assert tokens == expected_tokens, f"Expected {expected_tokens} but got {tokens}"
