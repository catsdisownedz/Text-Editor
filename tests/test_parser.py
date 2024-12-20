import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
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

    expected_ast = [{'type': 'int', 'variable': 'x', 'assignment': {'type': 'digit', 'value': '2'}}, 
                    {'type': 'int', 'variable': 'y', 'assignment': {'type': 'digit', 'value': '300'}}, 
                    {'type': 'while', 'condition': {'left': {'type': 'variable', 'name': 'x'}, 
                                                    'operator': '<=', 'right': {'type': 'variable', 'name': 'y'}}, 
                     'body': [{'operation': '++', 'variable': 'x'}]}]
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

    expected_ast = [{'type': 'for', 'initialization': {'type': 'int', 'variable': 'i', 'assignment': {'type': 'digit', 'value': '0'}}, 
                     'condition': {'left': {'type': 'variable', 'name': 'i'}, 'operator': '<', 'right': {'type': 'digit', 'value': '10'}}, 
                     'increment': {'operation': '++', 'variable': 'i'}, 'body': [{'type': 'int', 'variable': 'sum', 
                                                                                  'assignment': {'left': {'type': 'variable', 'name': 'i'}, 
                                                                                                 'operator': '+', 'right': {'type': 'digit', 'value': '5'}}}]
                     }]
    assert ast == expected_ast, f"Expected {expected_ast} but got {ast}"

if __name__=="__main__":
    test_for_loop_parser()