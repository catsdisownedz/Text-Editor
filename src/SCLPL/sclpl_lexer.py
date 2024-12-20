import re

TOKEN_TYPES = [
    ('MULTI_LINE_COMMENT', r'/\*[\s\S]*?\*/'),
    ('COMMENT', r'//[^\n]*'),
    ('KEYWORDS', r'\b(if|while|for)(?=\s|\(|$)\b'),
    ('TYPE', r'\b(int|char|string|array)\b'),
    ('OPERATOR', r'\+\+|--|\*\*|//|\+=|-=|/=|%=|\+|-|\*|/|%'),
    ('CONDITIONAL_OPERATOR', r'(>=|<=|==|!=|>|<)'),
    ('BRACE_OR_PAREN', r'[\(\)\{\}]'),
    ('ASSIGNMENT_OPERATOR', r'='),
    ('TERMINAL', r';'),
    ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z_0-9]*'),
    ('DIGIT', r'\d+'),
    ('ARRAY_ACCESS', r'[a-zA-Z_][a-zA-Z_0-9]*\[\d+\]'),
    ('WHITESPACE', r'\s+'),
]

TOKEN_REGEX = "|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_TYPES)

def sclplLexer(source_code):
    tokens = []

    for match in re.finditer(TOKEN_REGEX, source_code, re.DOTALL):
        kind = match.lastgroup
        value = match.group()
        if kind == 'WHITESPACE':
            continue
        elif kind in ['COMMENT','MULTI_LINE_COMMENT']:
            tokens.append((kind, value))
        else:
            tokens.append((kind, value))
    
    return tokens

if __name__ == '__main__':
    code = """
    // This is a single-line comment
    int x = 2;
    int y = 300;
    while(x <= y){
        x*;
    }
    /* hello
    world
    */
    int z = x + y;
    """
    tokens = sclplLexer(code)  
    for token in tokens:
        print(token)
