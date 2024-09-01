from Tokens import tokens_compiled
import re

class Lexer:
    def __init__(self,text):
        self.text = text
        self.pos = 0
        self.actual_char = None
        self.text_tokenize = None


    def tokenize(self):
        result = {name : pattern.findall(self.text) for name, pattern in tokens_compiled.items()}
        return result





if __name__ == '__main__':
    code = 'If (number + 1 = 2)'
    lexer = Lexer(code)
    for name, value in lexer.tokenize().items():
        print(name, value)