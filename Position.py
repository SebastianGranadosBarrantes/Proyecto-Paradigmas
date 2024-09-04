#Esto lo vamos a usar para el parser (sintactico) para la cuestion de los errores
# y demas
class Position:
    def __init__(self, index, line, column):
        self.index = index
        self.line = line
        self.column = column

    def walk(self, actual_char):
        self.index += 1
        self.column += 1

        if actual_char == '\n':
            self.line += 1
