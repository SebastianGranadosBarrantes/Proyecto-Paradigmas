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
        output_text = ''
        for name, value in self.lexer.tokenize().items():
            output_text += f'{name}: {value}\n'
        self.ui.Txt_Salida.setText(output_text)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

