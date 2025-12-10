
class Scanner:
    def __init__(self):
        self.keywords = [
            "int", "float", "double", "if", "else", "while", "for", "return",
            "break", "continue", "void", "char", "struct", "class", "public",
            "private", "namespace", "include", "using", "switch", "case",
            "default", "const", "main", "printf"
        ]
        self.tokens = []

    def is_letter(self, ch):
        return ('a' <= ch <= 'z') or ('A' <= ch <= 'Z') or ch == '_'

    def is_digit(self, ch):
        return '0' <= ch <= '9'

    def tokenize(self, code):
        i = 0
        self.tokens = []
        while i < len(code):
            ch = code[i]

            if ch in [' ', '\t', '\n']:
                i += 1
                continue

            # Comments
            if ch == '/' and i + 1 < len(code):
                if code[i + 1] == '/':
                    while i < len(code) and code[i] != '\n':
                        i += 1
                    continue
                if code[i + 1] == '*':
                    i += 2
                    while i + 1 < len(code) and not (code[i] == '*' and code[i + 1] == '/'):
                        i += 1
                    i += 2
                    continue

            # Numbers
            if self.is_digit(ch) or (ch == '.' and i + 1 < len(code) and self.is_digit(code[i + 1])):
                num = ch
                i += 1
                dot_count = 1 if ch == '.' else 0
                invalid_num = False
                while i < len(code) and (self.is_digit(code[i]) or code[i] == '.'):
                    if code[i] == '.':
                        dot_count += 1
                        if dot_count > 1:
                            invalid_num = True
                    num += code[i]
                    i += 1
                if invalid_num:
                    self.tokens.append({'type': 'INVALID', 'value': num})
                else:
                    self.tokens.append({'type': 'NUMBER', 'value': num})
                continue

            # Identifiers & keywords
            if self.is_letter(ch):
                word = ch
                i += 1
                while i < len(code) and (self.is_letter(code[i]) or self.is_digit(code[i])):
                    word += code[i]
                    i += 1
                if word in self.keywords:
                    self.tokens.append({'type': 'KEYWORD', 'value': word})
                else:
                    self.tokens.append({'type': 'IDENTIFIER', 'value': word})
                continue

            # Strings
            if ch == '"':
                string_val = ""
                i += 1
                while i < len(code) and code[i] != '"':
                    string_val += code[i]
                    i += 1
                i += 1
                self.tokens.append({'type': 'STRING', 'value': string_val})
                continue

            # Characters
            if ch == "'":
                char_val = ''
                i += 1
                if i < len(code):
                    char_val = code[i]
                    i += 1
                if i < len(code) and code[i] == "'":
                    i += 1
                self.tokens.append({'type': 'CHAR', 'value': char_val})
                continue

            # Operators
            if i + 1 < len(code):
                two = ch + code[i + 1]
                if two in ["==", "!=", ">=", "<=", "&&", "||", "++", "--"]:
                    self.tokens.append({'type': 'OPERATOR', 'value': two})
                    i += 2
                    continue
            if ch in ['+', '-', '*', '/', '=', '>', '<', '%', '!', '|', '&']:
                self.tokens.append({'type': 'OPERATOR', 'value': ch})
                i += 1
                continue

            # Separators
            if ch in ['(', ')', '{', '}', '[', ']', ';', ',', '.']:
                self.tokens.append({'type': 'SEPARATOR', 'value': ch})
                i += 1
                continue

            # Unknown / Invalid
            self.tokens.append({'type': 'INVALID', 'value': ch})
            i += 1

        self.tokens.append({'type': 'END', 'value': 'END'})
        return self.tokens
