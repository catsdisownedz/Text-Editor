import re

# Defining the tokens
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

# Combine the patterns into one
TOKEN_REGEX = "|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_TYPES)


# Lexer function yay
def lexer(source_code):
    tokens = []
    inside_comment = False
    multiline_comment_buffer = ""
    
    lines = source_code.splitlines()
    
    for line_number, line in enumerate(lines, start=1):
        if inside_comment:
            multiline_comment_buffer += "\n" + line
            
            if "*/" in line:
                inside_comment = False
                multiline_comment_buffer += "\n" + line
                
                tokens.append(("MULTILINE_COMMENT", multiline_comment_buffer.strip(), line_number))
                multiline_comment_buffer = ""
            continue
            
        if "/*" in line:
            inside_comment = True
            start_index = line.index("/*")
            multiline_comment_buffer += line[start_index:]
            
            if  "*/" in line:
                inside_comment = False
                end_index = line.index("*/") + 2
                multiline_comment_buffer += line[end_index:]
                tokens.append(("MULTILINE_COMMENT", multiline_comment_buffer.strip(), line_number))
                multiline_comment_buffer = ""
            continue
            
        for match in re.finditer(TOKEN_REGEX, line, re.DOTALL):
            kind = match.lastgroup
            value = match.group()

            if kind == 'WHITESPACE':
                continue # Skip whitespace
            
            tokens.append((kind, value, line_number))
    
    return tokens


if __name__ == '__main__':
    code = """
    int x = 2;
    int y = 300;
    while(x <= y){
    x**;
    }
    /* hello
    */
    int z = x+y;
    """


    
    tokens = lexer(code)
    
    for token in tokens:
        print(token)