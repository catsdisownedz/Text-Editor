import re

# Sample Tokenizer for testing
TOKEN_TYPES = {
    ('MULTI_LINE_COMMENT', r'/\*.*?\*/'),
    ('KEYWORDS', r'(if|while|for)(?=\s|\(|$)'),
    ('TYPE', r'\b(int|char|string|array)\b'),
    ('OPERATOR', r'\b(\+\+|--|\*\*|//|\+=|-=|/=|%=|\+|-|\*|/|%)'),
    ('CONDITIONAL_OPERATOR', r'(>=|<=|==|!=|>|<)'),
    ('BRACE_OR_PAREN', r'[\(\)\{\}]'),
    ('ASSIGNMENT_OPERATOR', r'='),
    ('TERMINAL', r';'),
    ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z_0-9]*'),
    ('DIGIT', r'\d+'),
    ('ARRAY_ACCESS', r'[a-zA-Z_][a-zA-Z_0-9]*\[\d+\]'),
    ('WHITESPACE', r'\s+'),
    ('COMMENT', r'//.*?$')   
}

TOKEN_REGEX = "|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_TYPES)

def lexer(source_code):
    tokens = []
    for match in re.finditer(TOKEN_REGEX, source_code):
        kind = match.lastgroup
        value = match.group()
        if kind != 'WHITESPACE':
            tokens.append((kind, value))
    return tokens

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def eat(self, token_type):
        token = self.current_token()
        if token and token[0] == token_type:
            self.pos += 1
        else:
            raise SyntaxError(f"Expected {token_type}, but got {token[0] if token else 'EOF'}")

    def parse(self):
        #hi hello
        #this funcction is used for as a placeholder for the run button in the gui, if you remove it probs something will crash 
        #oki bayie 
        return self.general_statement()

    def general_statement(self):
        """<GeneralStatement> ::= <Declaration> | <ArithmeticExpression> | <Loop> | <Condition> | <Assignment> | <FlowControlStatement> | <IncrementStatement>"""
        token = self.current_token()
        if token and token[0] == 'TYPE':
            return self.declaration()  # <Declaration>
        elif token and token[0] == 'IDENTIFIER':
            return self.assignment()  # <Assignment>
        else:
            raise SyntaxError("Unrecognized general statement")

    def declaration(self):
        
        """<Declaration> ::= <Type> <Variable> | <Type> <Variable> '=' <Term> | <Type> <Variable> '=' <ArithmeticExpression>"""
        token = self.current_token()
        if token and token[0] == 'TYPE':
            type_token = token
            self.eat('TYPE')
            var_token = self.current_token()
            self.eat('IDENTIFIER')
            token = self.current_token()
            if token and token[0] == 'ASSIGNMENT_OPERATOR':
                self.eat('ASSIGNMENT_OPERATOR')
                return {'type': type_token[1], 'variable': var_token[1], 'assignment': self.term()}
            else:
                return {'type': type_token[1], 'variable': var_token[1]}
        else:
            raise SyntaxError("Invalid declaration")

    def assignment(self):
        """<Assignment> ::= <Variable> '=' <Term>"""
        var_token = self.current_token()
        self.eat('IDENTIFIER')
        self.eat('ASSIGNMENT_OPERATOR')
        term = self.term()
        return {'variable': var_token[1], 'term': term}

    def term(self):
        """<Term> ::= <Variable>|<DigitSequence>|<Identifier>|<ArrayAccess>"""
        token = self.current_token()
        if token and token[0] == 'IDENTIFIER':
            return {'type': 'variable', 'name': token[1]}
        elif token and token[0] == 'DIGIT':
            return {'type': 'digit', 'value': token[1]}
        else:
            raise SyntaxError("Invalid term")

# Example usage
source_code = """
int x = 5;
int y = 10;
x = y;
"""
tokens = lexer(source_code)
parser = Parser(tokens)
ast = parser.parse()

print(ast)
