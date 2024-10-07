import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from IDEController import Ui_MainWindow
from lexer import Lexer
from _parser import Parser

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.parser = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.Btn_Compilar.clicked.connect(self.compile_handler)
        self.lexer = Lexer('')

    def compile_handler(self):
        text = self.ui.Txt_Codigo.toPlainText()
        self.lexer.text = text
        tokens = self.lexer.tokenize()
        output_text = ''
        self.parser = Parser(tokens)
        print(self.parser.tokens)
        try:
            self.parser.parse()
        except SyntaxError as e:
            print(e)
        except Exception as e:
            print(f"Ocurrio un error al momento de parsear ${e}")
        #for token in tokens:
         #   output_text += f'Tipo: {token.type}, Valor: {token.value}, Línea: {token.line}, Columna: {token.column}\n'
        self.ui.Txt_Salida.setText(output_text)
        print('El resultado es:', self.parser.tree)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
