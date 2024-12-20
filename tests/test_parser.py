import pytest
from SCLPL.sclpl_lexer import sclplLexer
from SCLPL.sclpl_parser import sclplParser

def test_basic_parser():
    code = """
    int x = 2;
    int y = 300;
    while(x <= y){
        x++;
    }
    """
    tokens = sclplLexer(code)
    parser = sclplParser(tokens)
    ast = parser.parse()

    expected_ast = [
        {'type': 'declaration', 'variable': 'x', 'assignment': {'type': 'digit', 'value': '2'}},
        {'type': 'declaration', 'variable': 'y', 'assignment': {'type': 'digit', 'value': '300'}},
        {'type': 'while', 'condition': {'left': {'type': 'variable', 'name': 'x'}, 'operator': '<=', 'right': {'type': 'variable', 'name': 'y'}}, 'body': [{'type': 'increment_statement', 'variable': 'x', 'operation': '++'}]}
    ]
    assert ast == expected_ast, f"Expected {expected_ast} but got {ast}"

def test_for_loop_parser():
    code = """
    for(int i = 0; i < 10; i++) {
        int sum = i + 5;
    }
    """
    tokens = sclplLexer(code)
    parser = sclplParser(tokens)
    ast = parser.parse()

    expected_ast = [
        {'type': 'for',
         'initialization': {'type': 'declaration', 'variable': 'i', 'assignment': {'type': 'digit', 'value': '0'}},
         'condition': {'left': {'type': 'variable', 'name': 'i'}, 'operator': '<', 'right': {'type': 'digit', 'value': '10'}},
         'increment': {'operation': '++', 'variable': 'i'},
         'body': [{'type': 'declaration', 'variable': 'sum', 'assignment': {'type': 'expression', 'left': {'type': 'variable', 'name': 'i'}, 'operator': '+', 'right': {'type': 'digit', 'value': '5'}}}]
        }
    ]
    assert ast == expected_ast, f"Expected {expected_ast} but got {ast}"

def test_while_loop_parser_with_comments():
    code = """
    int z = 100;
    while(z > 0) { /* decrementing z */ z--; }
    """
    tokens = sclplLexer(code)
    parser = sclplParser(tokens)
    ast = parser.parse()

    expected_ast = [
        {'type': 'declaration', 'variable': 'z', 'assignment': {'type': 'digit', 'value': '100'}},
        {'type': 'while', 'condition': {'left': {'type': 'variable', 'name': 'z'}, 'operator': '>', 'right': {'type': 'digit', 'value': '0'}}, 'body': [{'type': 'expression', 'left': {'type': 'variable', 'name': 'z'}, 'operator': '--', 'right': None}]}
    ]
    assert ast == expected_ast, f"Expected {expected_ast} but got {ast}"

def test_invalid_syntax():
    code = "int x = ;"  # Invalid syntax, missing value
    tokens = sclplLexer(code)
    parser = sclplParser(tokens)

    with pytest.raises(SyntaxError, match="Expected IDENTIFIER, but got EOF"):
        parser.parse()
