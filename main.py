import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
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
        print('Se ejecuta')
        text = self.ui.Txt_Codigo.toPlainText()
        if text == "":
            QMessageBox.warning(self, 'Advertencia', '¡Se esta intentando compilar cuando no hay código que compilar!')
        else:
            self.lexer.text = text
            tokens = self.lexer.tokenize()
            output_text = ''
            self.parser = Parser(tokens)
            print(self.parser.tokens)
            try:
                self.parser.parse()
            except SyntaxError as e:
                QMessageBox.critical(self, 'Error', str(e))
            except Exception as e:
                QMessageBox.critical(self, 'Error', f"{str(e)}")
            self.ui.Txt_Salida.setText(output_text)
            print('El resultado es:', self.parser.tree)
            print(f"La siguiente es la tabla de simbolos \n{self.parser.symbols_table}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
