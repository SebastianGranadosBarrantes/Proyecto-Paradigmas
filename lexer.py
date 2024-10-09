import re
from Tokens import tokens_compiled, Token
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.actual_char = None
        self.tokens = []

    def tokenize(self):
        lines = self.text.splitlines()
        in_comment = False
        for line_number, line in enumerate(lines, start=1):
            line_pos = 0
            while line_pos < len(line):
                matched = False
                for name, pattern in tokens_compiled.items():
                    regex_match = pattern.match(line, line_pos)
                    if regex_match:
                        value = regex_match.group(0)
                        if name == 'COMMENT_START':
                            in_comment = True

                        elif name == 'COMMENT_END':
                            in_comment = False

                        elif not in_comment and name != 'WHITESPACE':
                            print("El valor del token va a ser " , value, ' y el tipo de token va a ser ', name)
                            token = Token(name, value, line_number, line_pos)
                            self.tokens.append(token)

                        line_pos += len(value)
                        matched = True
                        break

                if not matched:
                    raise ValueError(f"Caracter inesperado '{line[line_pos]}' en la línea {line_number}")
        return self.tokens


# Probar el lexer
if __name__ == '__main__':
    code = 'IF (number + 1 = 2)\nwhile (x > 0)'
    lexer = Lexer(code)
    tokens = lexer.tokenize()

    #for token in tokens:
        #print(token)
