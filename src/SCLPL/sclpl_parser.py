import json
from SCLPL.sclpl_lexer import sclplLexer
from SCLPL.abstract_syntax_tree import AST

class sclplParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def eat(self, token_type):
        token = self.current_token()
        if not token or token[0] != token_type:
            raise SyntaxError(f"Expected {token_type}, but got {token[0] if token else 'EOF'}")
        print(f"Eating token: {token}")  # Debugging print
        self.pos += 1
        return token

    def parse(self):
        statements = []
        while self.current_token():
            token = self.current_token()
            if token[0] == 'MULTI_LINE_COMMENT':  # Handle multi-line comments
                statements.append(self.multi_line_comment())
                continue  # Skip to the next token
            elif token[0] == 'COMMENT':
                statements.append(self.single_line_comment())
                continue  # Skip comments

            # Check for a while loop
            elif token[0] == 'KEYWORDS' and token[1] == 'while':
                statements.append(self.parse_while_loop())
            elif token[0] == 'KEYWORDS' and token[1] == 'for':
                statements.append(self.parse_for_loop())
            else:
                statements.append(self.general_statement())
        return statements

    def multi_line_comment(self):
        comment_token = self.eat('MULTI_LINE_COMMENT')
        return {
            'type': 'multi_line_comment',
            'content': comment_token[1]
        }
    def single_line_comment(self):
        comment_token=self.eat('COMMENT')
        
        return{
            'type': 'COMMENT',
            'content': comment_token[1]
        }

    def general_statement(self):
        token = self.current_token()
        print(f"Parsing token: {token}")  # Debugging print
        
        if token[0] == 'TYPE':  # Declaration statement
            return self.declaration()
        elif token[0] == 'IDENTIFIER':  # Identifier
            next_token = self.tokens[self.pos + 1] if self.pos + 1 < len(self.tokens) else None
            if next_token and next_token[0] == 'ASSIGNMENT_OPERATOR':
                return self.assignment()
            elif next_token and next_token[0] == 'OPERATOR':
                return self.increment_statement()
                
            else:
                self.pos += 1  # Move to the next token
                return self.general_statement()
        else:
            raise SyntaxError(f"Unrecognized statement: {token}")

    def parse_while_loop(self):
        # Start parsing a while loop
        self.eat('KEYWORDS')  # Eat 'while'
        self.eat('BRACE_OR_PAREN')  # Eat '('

        # Parse the condition: left operand, operator, and right operand
        condition_left = self.term()  # Left side of the condition (e.g., 'x')
        operator = self.eat('CONDITIONAL_OPERATOR')  # The conditional operator (e.g., '<=')
        condition_right = self.term()  # Right side of the condition (e.g., 'y')

        self.eat('BRACE_OR_PAREN')  # Eat ')'
        self.eat('BRACE_OR_PAREN')  # Eat '{' (start of body)

        # Parse the body of the loop
        body = []
        while self.current_token() and (
            self.current_token()[0] != 'BRACE_OR_PAREN'
            or self.current_token()[1] != '}'
        ):
            body.append(self.general_statement())

        self.eat('BRACE_OR_PAREN')  # Eat '}' (end of body)

        return {
            'type': 'while',
            'condition': {
                'left': condition_left,
                'operator': operator[1],
                'right': condition_right
            },
            'body': body
        }
        
    def parse_for_loop(self):
        self.eat('KEYWORDS')
        self.eat('BRACE_OR_PAREN')
        
        initialization = self.general_statement()

        condition_left = self.term()
        operator = self.eat('CONDITIONAL_OPERATOR')
        condition_right = self.term()
        self.eat('TERMINAL')
        increment=self.for_loop_increment()
        
          
        self.eat('BRACE_OR_PAREN')
        self.eat('BRACE_OR_PAREN')
        
        body=[]
        while self.current_token() and (
            self.current_token()[0] != 'BRACE_OR_PAREN'
            or self.current_token()[1] != '}'
        ):
            body.append(self.general_statement())
        self.eat('BRACE_OR_PAREN')
        
        return{
            'type':'for',
            'initialization': initialization,
            'condition':{
                'left': condition_left,
                'operator': operator[1],
                'right':condition_right
            },
            'increment': increment,
            'body':body
            
        }
        

    def declaration(self):
        type_token = self.eat('TYPE')  # Type token ('int', 'char', etc.)
        var_token = self.eat('IDENTIFIER')  # Variable name token

        assignment = None
        if self.current_token() and self.current_token()[0] == 'ASSIGNMENT_OPERATOR':
            self.eat('ASSIGNMENT_OPERATOR')
            assignment = self.expression()  # Handle expressions like x + y

        self.eat('TERMINAL')  # Eat the terminal ';'
        return {
            'type': type_token[1],
            'variable': var_token[1],
            'assignment': assignment
        }

    def assignment(self):
        var_token = self.eat('IDENTIFIER')  # Eat the variable name
        self.eat('ASSIGNMENT_OPERATOR')
        value = self.expression()  # Handle assignment value
        self.eat('TERMINAL')
        return {
            'type': 'assignment',
            'assignment': var_token[1],
            'value': value
        }

    def expression(self):
        # This handles expressions, which might include operators like '+' between terms
        left = self.term()  # First term in the expression
        while self.current_token() and self.current_token()[0] == 'OPERATOR':
            operator = self.eat('OPERATOR')  # Eat the operator
            right = self.term()  # Next term in the expression
            left = {'left': left, 'operator': operator[1], 'right': right}  # Combine terms
        return left

    def term(self):
        token = self.current_token()
        if token[0] == 'IDENTIFIER':
            self.eat('IDENTIFIER')
            return {'type': 'variable', 'name': token[1]}
        elif token[0] == 'DIGIT':
            self.eat('DIGIT')
            return {'type': 'digit', 'value': token[1]}
        else:
            raise SyntaxError(f"Invalid term: {token}")

    def increment_statement(self):
        var_token = self.eat('IDENTIFIER')
        operator = self.eat('OPERATOR')
        if operator[1] == '+=' or operator[1] == '-=':
            digit = self.eat('DIGIT')
            self.eat('TERMINAL')
            return {
                'operation': operator[1],
                'variable': var_token[1],
                'DIGIT' :digit[1]
            }
        self.eat('TERMINAL')
        return {
            'operation': operator[1],
            'variable': var_token[1]
        }
    def for_loop_increment(self):
        var_token = self.eat('IDENTIFIER')
        operator_one = self.eat('OPERATOR')
        ##operator_two = self.eat('OPERATOR')
        return {
            'operation': operator_one[1],
            'variable': var_token[1]
        }
# i + + 

# Main Entry Point for Testing
if __name__ == '__main__':
    source_code = """
    int x = 2;
    int y = 300;
    while(x <= y){
        x*;
    }
    /* hello
    */
    int z = x + y;
    """
    
    # Generate tokens using the lexer
    tokens = sclplLexer(source_code)
    print(f"Tokens: {tokens}")  # Debugging print

    # Parse the tokens into an AST
    parser = sclplParser(tokens)
    ast = parser.parse()

    # Pretty-print the AST
    print(json.dumps(ast, indent=4))

    # Draw the AST and save it to a file
    visualizer = AST(ast)
    visualizer.draw_ast('ast')