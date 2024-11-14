#Definicion de los patrones de los tokens usando regex
import re

token_patterns = [
    ('KEYWORD', r'(?i)\b(si|sino|while|retorna|tons|mientras|haga|casos|caso|defecto)\b'),
    ('FUNCTION', r'(?i)\b(funcioncita)\b'),
    ('NEWLINE', r'(?i)\b(salto)\b'),
    ('PROCEDURE', r'(?i)\b(procedimienton)\b'),
    ('IO', r'(?i)\b(lea|escriba)\b'),
    ('DATATYPE', r'(?i)\b(entero|char|bool|string|float|pila|lista)\b'),
    ('MAIN', r'(?i)\b(main)\b'),
    ('LOGICAL_OPERATOR', r'(?i)\b(and|or|not)\b'),
    ('STACKMETHODS', r'(?i)\b(mete|saca|arriba)\b'),
    ('LISTMETHODS', r'(?i)\b(obtener|insertar|primero|ultimo)\b'),
    ('BOOLEAN', r'(?i)\b(true|false)\b'),
    ('IDENTIFIER', r'\b[a-zA-Z_][a-zA-Z_0-9]*\b'),
    ('NUMBER', r'[+-]?(\d*\.\d+|\d+\.\d*|\d+)'),
    ('CHAR', r"'.'"),
    ('STRING', r'"[^"]*"|""'),
    ('COMMENT_START', r'-\*'),
    ('COMMENT_END', r'\*\-'),
    ('COMPARATOR', r'(<>|==|>=|<=|>|<)'),
    ('INCREMENT', r'\+\+'),
    ('DECREMENT', r'--'),
    ('OPERATOR', r'[+\-*/%]'),
    ('ASSIGNMENT', r'='),
    ('DELIMETER', r'[(),:{}\[\]]'),
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

