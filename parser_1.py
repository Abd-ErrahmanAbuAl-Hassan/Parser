from scanner25 import Scanner

class Parser:
    def __init__(self):
        self.tokens = []
        self.index = 0
        self.errors = []

    def load_tokens(self, code):
        scanner = Scanner()
        self.tokens = scanner.tokenize(code)
        self.index = 0

    def current_token(self):
        if self.index < len(self.tokens):
            return self.tokens[self.index]
        return {'type': 'END', 'value': 'END'}

    def advance(self):
        self.index += 1

    def match(self, type_, value=None):
        tok = self.current_token()
        if tok['type'] == type_ and (value is None or tok['value'] == value):
            self.advance()
            return True
        return False

    def lookahead_is(self, value):
        if self.index + 1 < len(self.tokens):
            return self.tokens[self.index + 1]['value'] == value
        return False

    def error(self, message):
        tok = self.current_token()
        err_msg = f"Syntax error at token {tok['value']} ({tok['type']}) — {message}"
        self.errors.append(err_msg)

    def parse_program(self):
        while self.current_token()['type'] != 'END':
            tok = self.current_token()
            if tok['type'] == 'KEYWORD' and tok['value'] in ['int', 'float', 'char', 'double', 'void']:
                if not self.parse_declaration():
                    self.advance()
            elif tok['type'] == 'KEYWORD' and tok['value'] == 'main':
                self.parse_main()
            else:
                self.advance()

    def parse_declaration(self):
        tok = self.current_token()
        if tok['type'] == 'KEYWORD' and tok['value'] in ['int','float','char','double','void']:
            self.advance()
            tok2 = self.current_token()
            if tok2['type'] == 'IDENTIFIER' and self.lookahead_is('('):
                self.parse_function_declaration()
                return True
            elif tok2['type'] == 'IDENTIFIER':
                self.advance()
                if self.match('OPERATOR', '='):
                    self.parse_expression()
                if not self.match('SEPARATOR', ';'):
                    self.error("Missing ';' after declaration")
                return True
            elif tok2['type'] == 'KEYWORD' and tok2['value'] == 'main':
                self.parse_main()
                return True
            else:
                self.error("Expected identifier after type")
                return False
        return False

    def parse_function_declaration(self):
        if not self.match('SEPARATOR', '('):
            self.error("Expected '(' in function declaration")
            return
        if not self.match('SEPARATOR', ')'):
            self.error("Expected ')' in function declaration")
            return
        self.parse_block()

    def parse_main(self):
        if not self.match('KEYWORD', 'main'):
            self.error("Expected 'main'")
        if not self.match('SEPARATOR', '('):
            self.error("Expected '(' after main")
        if not self.match('SEPARATOR', ')'):
            self.error("Expected ')' after main")
        self.parse_block()

    def parse_block(self):
        if not self.match('SEPARATOR', '{'):
            self.error("Expected '{'")
            return
        while self.current_token()['type'] != 'END' and self.current_token()['value'] != '}':
            self.parse_statement()
        if not self.match('SEPARATOR', '}'):
            self.error("Expected '}'")

    def parse_statement(self):
        tok = self.current_token()
        if tok['type'] == 'KEYWORD' and tok['value'] in ['int','float','char','double','void']:
            self.parse_declaration()
            return
        if tok['type'] == 'KEYWORD':
            if tok['value'] == 'if':
                self.parse_if()
                return
            elif tok['value'] == 'while':
                self.parse_while()
                return
            elif tok['value'] == 'for':
                self.parse_for()
                return
            elif tok['value'] == 'return':
                self.advance()
                self.parse_expression()
                if not self.match('SEPARATOR', ';'):
                    self.error("Expected ';' after return")
                return
        self.parse_expression()
        if not self.match('SEPARATOR', ';'):
            self.error("Expected ';' after expression")

    def parse_if(self):
        self.match('KEYWORD', 'if')
        if not self.match('SEPARATOR', '('):
            self.error("Expected '(' after 'if'")
        self.parse_expression()
        if not self.match('SEPARATOR', ')'):
            self.error("Expected ')' after condition")
        self.parse_block()
        if self.match('KEYWORD', 'else'):
            self.parse_block()

    def parse_while(self):
        self.match('KEYWORD', 'while')
        if not self.match('SEPARATOR', '('):
            self.error("Expected '(' after 'while'")
        self.parse_expression()
        if not self.match('SEPARATOR', ')'):
            self.error("Expected ')' after condition")
        self.parse_block()

    def parse_for(self):
        self.match('KEYWORD', 'for')
        if not self.match('SEPARATOR', '('):
            self.error("Expected '(' after 'for'")
        self.parse_statement()
        self.parse_expression()
        if not self.match('SEPARATOR', ';'):
            self.error("Expected ';' after for condition")
        self.parse_expression()
        if not self.match('SEPARATOR', ')'):
            self.error("Expected ')' after for increment")
        self.parse_block()

    def parse_expression(self):
        self.parse_assignment()

    def parse_assignment(self):
        self.parse_or()
        if self.match('OPERATOR', '='):
            self.parse_assignment()

    def parse_or(self):
        self.parse_and()
        while self.match('OPERATOR', '||'):
            self.parse_and()

    def parse_and(self):
        self.parse_equality()
        while self.match('OPERATOR', '&&'):
            self.parse_equality()

    def parse_equality(self):
        self.parse_relational()
        while self.match('OPERATOR', '==') or self.match('OPERATOR', '!='):
            self.parse_relational()

    def parse_relational(self):
        self.parse_additive()
        while self.match('OPERATOR', '<') or self.match('OPERATOR', '>') or self.match('OPERATOR', '<=') or self.match('OPERATOR', '>='):
            self.parse_additive()

    def parse_additive(self):
        self.parse_term()
        while self.match('OPERATOR', '+') or self.match('OPERATOR', '-'):
            self.parse_term()

    def parse_term(self):
        self.parse_factor()
        while self.match('OPERATOR', '*') or self.match('OPERATOR', '/') or self.match('OPERATOR', '%'):
            self.parse_factor()

    def parse_factor(self):
        tok = self.current_token()
        if tok['type'] in ['IDENTIFIER','KEYWORD'] and self.lookahead_is('('):
            self.advance()
            self.match('SEPARATOR','(')
            if not self.match('SEPARATOR',')'):
                while True:
                    self.parse_expression()
                    if self.match('SEPARATOR',')'):
                        break
                    if not self.match('SEPARATOR',','):
                        self.error("Expected ',' or ')' in function call")
                        break
            return
        if tok['type'] in ['NUMBER','IDENTIFIER','STRING','CHAR']:
            self.advance()
        elif self.match('SEPARATOR','('):
            self.parse_expression()
            if not self.match('SEPARATOR',')'):
                self.error("Expected ')' after expression")
        elif tok['type'] == 'INVALID':
            self.error("Invalid token in expression")
            self.advance()
        else:
            self.error("Expected expression")
            self.advance()
