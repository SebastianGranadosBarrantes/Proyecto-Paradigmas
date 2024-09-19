#Definicion de los patrones de los tokens usando regex
import re

token_patterns = [
    ('KEYWORD', r'(?i)\b(if|else|while|return|function|do)\b'),
    ('IO', r'(?i)\b(lea|escriba)\b'),
    ('DATATYPE', r'(?i)\b(entero|char|bool|string|float|lista|arreglo)\b'),
    ('IDENTIFIER', r'\b[a-zA-Z_][a-zA-Z_0-9]*\b'),
    ('NUMBER', r'[+-]?(\d*\.\d+|\d+\.\d*|\d+)'),
    ('CHAR', r"'.'"),
    ('BOOLEAN', r'(?i)\b(true|false)\b'),
    ('STRING', r'"[^"]*"'),
    ('ASSIGNMENT', r'='),
    ('COMPARATOR', r'(<>|==|>=|<=|>|<)'),
    ('OPERATOR', r'[+\-*/]'),
    ('LOGICAL_OPERATOR', r'(?i)\b(and|or|not)\b'),
    ('DELIMETER', r'[(),;{}]|\[\]'),
    ('WHITESPACE', r'\s+'),
    ('UNKNOWN', r'.'),
]



tokens_compiled = {name:re.compile(pattern) for name, pattern in token_patterns}

class Token:
    def __init__(self, type_, value, line, column):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type}, {self.value}, Pos({self.line}:{self.column}))"

