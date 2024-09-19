import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from IDEController import Ui_MainWindow
from lexer import Lexer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.Btn_Compilar.clicked.connect(self.compile_handler)
        self.lexer = Lexer('')

    def compile_handler(self):
        text = self.ui.Txt_Codigo.toPlainText()
        self.lexer.text = text
        tokens = self.lexer.tokenize()
        output_text = ''


        for token in tokens:
            output_text += f'Tipo: {token.type}, Valor: {token.value}, Línea: {token.line}, Columna: {token.column}\n'
        self.ui.Txt_Salida.setText(output_text)  # Muestra el resultado en el área de salida


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
