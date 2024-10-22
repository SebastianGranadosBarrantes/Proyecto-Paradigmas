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
        self.ui.AFFuncion.triggered.connect(self.function_example_handler)
        self.ui.AFProcedimiento.triggered.connect(self.proc_example_handler)
        self.ui.AFCondicionales.triggered.connect(self.conditional_example_handler)
        self.ui.AFCondicionalesAnidados.triggered.connect(self.nested_conditional_example_handler)
        self.lexer = Lexer('')

    def function_example_handler(self):
        function_text = """funcioncita calcular_area_circulo(float radio) : float {
    float area
    area = 3.14 * radio * radio
    escriba("El área del círculo con radio ", radio, " es: ", area, salto)
    retorna area 
}
main(){
    float radio = 4
    calcular_area_circulo(radio) 
}
"""

        self.ui.Txt_Codigo.setText(function_text)

    def proc_example_handler(self):
        proc_text = """procedimienton calcular_area_rectangulo(float alto, float ancho){
    float area = alto * ancho
    escriba("El area del rectangulo es ",area, salto)
}
        
main(){
    float alto = 20
    float ancho = 3
    calcular_area_rectangulo(alto, ancho)
}
        """

        self.ui.Txt_Codigo.setText(proc_text)

    def conditional_example_handler(self):
        conditional_text = """main(){
    float alto = 20
    float ancho = 3
    si (ancho > alto){
        escriba("El rectangulo es paisa")
    } 
    sino (ancho < alto){
        escriba("El rectangulo NO es paisa")
    }
    tons{
        escriba("No es un rectangulo, es un cuadrado")
    }
    
}"""

        self.ui.Txt_Codigo.setText(conditional_text)

    def nested_conditional_example_handler(self):
        conditional_text = """main(){
    float alto = 20
    float ancho = 3
    si (ancho > alto){
        escriba("El rectangulo es paisa")
        si (alto > 5){
            escriba("El rectangulo va a tener enanismo")
        }
    } 
    sino (ancho < alto){
        escriba("El rectangulo NO es paisa")
    }
    tons{
        escriba("No es un rectangulo, es un cuadrado")
    }

}"""

        self.ui.Txt_Codigo.setText(conditional_text)

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
                print(e)
            except Exception as e:
                print('Paso un error ')
                QMessageBox.critical(self, 'Error inesperado', f"{str(e)}")
                print(f"Error al parsear {e}")
            self.ui.TxtSalida.setText(output_text)
            print('El resultado es:', self.parser.tree)
            print(f"La siguiente es la tabla de simbolos \n{self.parser.symbols_table}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
