import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from IDEController import Ui_MainWindow
from lexer import Lexer
from _parser import Parser
from d2Binder import TextModel
from interpreter import Interpreter


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.parser = None
        self.model = None
        self.text_edit = None
        self.interpreter = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.Btn_Compilar.clicked.connect(self.compile_handler)
        self.ui.AFFuncion.triggered.connect(self.function_example_handler)
        self.ui.AFProcedimiento.triggered.connect(self.proc_example_handler)
        self.ui.AFCondicionales.triggered.connect(self.conditional_example_handler)
        self.ui.AFCondicionalesAnidados.triggered.connect(self.nested_conditional_example_handler)
        self.ui.Btn_Ejecutar.clicked.connect(self.run_handler)
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
        self.model = TextModel()

        # Assuming your widgets are already created in the .ui file
        self.text_edit = self.ui.Txt_Consola  # Accessing QTextEdit from the UI

        self.setup_bindings()

    def setup_bindings(self):
        # When the model changes, update the QTextEdit
        self.model.text_changed.connect(self.text_edit.setPlainText)

        # When the model changes, update the QLabel
        self.model.text_changed.connect(self.ui.Txt_Consola.setText)

        # When the text in QTextEdit changes, update the model
        self.text_edit.textChanged.connect(self.update_model_from_text_edit)

    def update_model_from_text_edit(self):
        # Update the model's text when the text in the QTextEdit changes
        new_text = self.text_edit.toPlainText()
        self.model.text = new_text
        self.print_text_to_console()

    def print_text_to_console(self):
        # Print the current text in the QTextEdit to the console
        current_text = self.text_edit.toPlainText()
        print(f"Current Text in QTextEdit: {current_text}")

    def compile_handler(self):
        print('Se ejecuta')
        text = self.ui.Txt_Codigo.toPlainText()
        if text == "":
            QMessageBox.warning(self, 'Advertencia', '¡Se esta intentando compilar cuando no hay código que compilar!')

        else:
            self.lexer.text = text
            tokens = self.lexer.tokenize()
            self.parser = Parser(tokens)
            print(self.parser.tokens)
            try:
                self.parser.parse()
                print("""--------------------------------------------------------------------------------------------------------------------
                
                
                
                
                
                
                """)
                print('El resultado del parser es: ', self.parser.tree)
                print("""--------------------------------------------------------------------------------------------------------------------





                                """)
                QMessageBox.information(self,'Compilación correcta', 'Se compilo el código correctamente')
            except SyntaxError as e:
                QMessageBox.critical(self, 'Error', str(e))
                print(e)
            except Exception as e:
                print('Paso un error ')
                QMessageBox.critical(self, 'Error inesperado', f"{str(e)}")
                print(f"Error al parsear {e}")

    def run_handler(self):
        self.interpreter = Interpreter(self.parser.tree)
        self.interpreter.interpret()
        outputs = ''
        print(self.interpreter.outputs)
        for output in self.interpreter.outputs:
            outputs += str(output)
        print('Outputs es : ', outputs)
        self.ui.TxtSalida.setPlainText(outputs)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
