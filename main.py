import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QTextEdit
from IDEController import Ui_MainWindow
from lexer import Lexer
from _parser import Parser
from d2Binder import TextModel
from interpreter import Interpreter
from PyQt6.QtCore import Qt
from PyQt6.QtCore import pyqtSignal
import webbrowser


class MainWindow(QMainWindow):
    input_ready = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.cursor_codigo = None
        self.model = None
        self.text_edit = None
        self.interpreter = None
        self.input_text = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.Btn_Compilar.clicked.connect(self.compile_handler)
        self.ui.AFFuncion.triggered.connect(self.function_example_handler)
        self.ui.AFProcedimiento.triggered.connect(self.proc_example_handler)
        self.ui.AFCondicionales.triggered.connect(self.conditional_example_handler)
        self.ui.AFCondicionalesAnidados.triggered.connect(self.nested_conditional_example_handler)
        self.ui.AFCicloWhile.triggered.connect(self.while_loop_example_handler)
        self.ui.Btn_Ejecutar.clicked.connect(self.run_handler)
        self.ui.AFCicloFor.triggered.connect(self.for_loop_example_handler)
        self.ui.AFSwitch.triggered.connect(self.switch_example_handler)
        self.ui.AFOpenDocs.triggered.connect(self.handle_open_docu)
        self.ui.AFInsertComentario.triggered.connect(self.handle_insert_comment)
        self.ui.AFInsertInput.triggered.connect(self.handle_insert_input)
        self.ui.AFInsertPila.triggered.connect(self.handle_insert_stack)
        self.ui.AFInsertLista.triggered.connect(self.handle_insert_list)
        self.ui.AFInsertOutput.triggered.connect(self.handle_insert_output)
        self.ui.AFInsertWhile.triggered.connect(self.handle_insert_while_form)
        self.ui.AFInsertFor.triggered.connect(self.handle_insert_for)
        self.ui.AFInsertMain.triggered.connect(self.Insert_main)
        self.ui.AFInsertVar.triggered.connect(self.handle_insert_var)
        self.ui.AFInsertFunction.triggered.connect(self.handle_insert_function)
        self.ui.AFInsertProcedure.triggered.connect(self.handle_insert_procedure)
        self.ui.AFInsertSwitch.triggered.connect(self.handle_insert_switch_form)

        self.lexer = Lexer('')
        self.ui.TxtSalida.setReadOnly(True)
        self.ui.Txt_Consola.installEventFilter(self)
        self.ui.Txt_Consola.setReadOnly(True)

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
    float alto 
    float ancho 
    escriba("Digite el alto del rectangulo",salto)
    lea(alto)
    escriba("Digite el ancho del rectangulo",salto)
    lea(ancho) 
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
        self.text_edit = self.ui.Txt_Consola

    def while_loop_example_handler(self):
        while_text = """procedimienton verificar_valores(entero a, entero b) {            
        string resultado 
        si (a > b) { 
        si (a > 100) { 
        escriba("a es mayor que b y también es mayor que 100", salto) 
        resultado = "a_grande" 
        } sino (a == 100) { 
        escriba("a es igual a 100 pero mayor que b", salto) 
        resultado = "a_igual_100" 
        } tons { 
        escriba("a es mayor que b pero menor que 100", salto) 
        resultado = "a_mayor_b_menor_100" 
        } 
        } sino (a < b) { 
        escriba("b es mayor que a", salto) 
        resultado = "b_mayor_a" 
        } tons { 
        escriba("a y b son iguales", salto) 
        resultado = "a_igual_b" 
        }
        escriba("Resultado: ", resultado, salto)
        }

        funcioncita calcular_factorial(entero n) : entero { 
    entero factorial = 1 
    mientras (n > 0) { 
    factorial = factorial * n 
    n = n - 1 
    } 
    retorna factorial 
        }

    procedimienton imprimir_numeros_pares(entero limite) {
entero i = 0
mientras (i <= limite) {
si (i % 2 == 0) {
escriba("El número ", i, " es par", salto)
}
i = i + 1
}
    }

    main() {
entero a = 150
entero b = 100
verificar_valores(a, b)

entero numero_factorial = 5
entero resultado_factorial = calcular_factorial(numero_factorial)
escriba("El factorial de ", numero_factorial, " es ", resultado_factorial, salto)

entero limite_pares = 10
imprimir_numeros_pares(limite_pares)
}
"""
        self.ui.Txt_Codigo.setText(while_text)

    def for_loop_example_handler(self):
        for_text = """procedimienton imprimir_numeros_pares(entero limite) { 
    entero i 
    haga(i = 0, i < limite, i = i + 2) {
        escriba("El número par es: ", i, salto) 
    }
    } 

main() {
     entero limite_pares = 10 
    imprimir_numeros_pares(limite_pares) 
}        
        """
        self.ui.Txt_Codigo.setText(for_text)

    def switch_example_handler(self):
        switch_text ="""main(){
    float temperatura 
    escriba("A continuacion se le solicita una temperatura de agua para un experimento",salto)
    lea(temperatura)
    
    casos(temperatura) {
        caso (temperatura <= 0) {
            escriba("El agua está en estado sólido", salto)
        }
        caso (temperatura > 0 and temperatura < 100) {
            escriba("El agua está en estado líquido", salto)
        }
        caso (temperatura >= 100 and temperatura < 150) {
            escriba("El agua está en estado de ebullición, pero no en vapor sobrecalentado", salto)
        }
        caso ((temperatura >= 150 and temperatura < 300) or (temperatura == 500)) {
            escriba("El agua está en vapor sobrecalentado o a una temperatura exacta de 500 grados", salto)
        }
        defecto {
            escriba("Temperatura fuera de rango para este experimento", salto)
        }
    }
}
"""
        self.ui.Txt_Codigo.setText(switch_text)

    def compile_handler(self):
        text = self.ui.Txt_Codigo.toPlainText()
        self.ui.Txt_Consola.clear()
        self.ui.TxtSalida.clear()
        self.ui.Txt_Consola.setReadOnly(True)
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
                QMessageBox.critical(self, 'Error en compilación', str(e))
                print(e)
            except Exception as e:
                print('Paso un error ')
                QMessageBox.critical(self, 'Error inesperado en compilación ', f"{str(e)}")
                print(f"Error al parsear {e}")

    def handle_insert_comment(self):
        self.cursor_codigo = self.ui.Txt_Codigo.textCursor()
        self.cursor_codigo.insertText("-*Esto es un comentario*-")

    def handle_insert_for(self):
        self.cursor_codigo = self.ui.Txt_Codigo.textCursor()
        self.cursor_codigo.insertText("""-*la variable contador i debe declararse antes *-
    haga(i = 0, condición, incremento o decremento){
        -*código a ejecutar*-
    } """)

    def handle_insert_while_form(self):
        self.cursor_codigo = self.ui.Txt_Codigo.textCursor()
        self.cursor_codigo.insertText("""mientras (condición) {
    -*Este es el body del while*-
    }""")

    def handle_insert_switch_form(self):
        self.cursor_codigo = self.ui.Txt_Codigo.textCursor()
        self.cursor_codigo.insertText("""casos(variable del switch) {
        caso (caso1) {
            -*aqui va el contenido del caso 1*-
        }
        caso (cason) {
           -*aqui va el contenido del caso n*-
        }
        
        defecto {
            -*aqui va el contenido del caso por defecto*-
        }
    }""")

    def handle_insert_input(self):
        self.cursor_codigo = self.ui.Txt_Codigo.textCursor()
        self.cursor_codigo.insertText("lea(variable_donde_guarda)")

    def handle_insert_output(self):
        self.cursor_codigo = self.ui.Txt_Codigo.textCursor()
        self.cursor_codigo.insertText("""escriba("esto es una prueba de output")""")

    def handle_insert_procedure(self):
        self.cursor_codigo = self.ui.Txt_Codigo.textCursor()
        self.cursor_codigo.insertText("""procedimienton nombre_funcion (tipo_parametro nombre_parametro, …)  {
    -*codigo de la función-*
}""")

    def handle_insert_function(self):
        self.cursor_codigo = self.ui.Txt_Codigo.textCursor()
        self.cursor_codigo.insertText("""funcioncita nombre_funcion (tipo_parametro nombre_parametro, …) : tipo_return{
    -*codigo de la función-*
    retorna valor_o_variable 
}""")


    def run_handler(self):
        if self.parser is None:
            QMessageBox.critical(self, 'Error al momento de ejecutar','NO se puede ejecutar sin antes compilar')
        else:
            self.ui.TxtSalida.clear()
            try:
                self.interpreter = Interpreter(self.parser.tree)
                self.interpreter.error_signal.connect(self.handle_interpreter_error)
                self.interpreter.request_input.connect(self.handle_input)
                self.input_ready.connect(self.interpreter.input_ready.emit)
                self.interpreter.input_type_error.connect(self.handle_input_error)
                self.interpreter.output_act.connect(self.handle_output)
                self.interpreter.start()
            except ValueError as e:
                QMessageBox.critical(self, 'Error de valores', str(e))
            except Exception as e:
                print('Paso un error')
                QMessageBox.critical(self, 'Error inesperado en la ejecución ', f"{str(e)}")

    def handle_input(self):
        self.ui.Txt_Consola.setReadOnly(False)
        self.ui.Txt_Consola.setText('>')
        #QMessageBox.information(self, "Consola habilitada" "Se ha habilitado la consola para un input")
        self.input_text = ""
        print("Esperando entrada del usuario...")

    def eventFilter(self, source, event):
        # Verifica si el evento es para Txt_Consola y si es la tecla Enter
        if source == self.ui.Txt_Consola and event.type() == event.Type.KeyPress:
            if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
                # Captura el texto ingresado
                self.input_text = self.ui.Txt_Consola.toPlainText().strip().lstrip(">")
                self.ui.Txt_Consola.clear()
                self.ui.Txt_Consola.setReadOnly(True)
                print(f"Entrada recibida: {self.input_text}")
                self.input_ready.emit(self.input_text)
                return True
        return super().eventFilter(source, event)

    def handle_input_error(self):
        QMessageBox.critical(self, 'Input incorrecto ', 'Se esta ingresando un tipo de dato incorrecto en el input')

    def handle_open_docu(self):
        webbrowser.open("https://drive.google.com/file/d/1aEjER7-Dd3gT5nR3X6LWDnV2RRQqBfj-/view?usp=sharing")

    def Insert_main(self):
        self.cursor_codigo = self.ui.Txt_Codigo.textCursor()
        self.cursor_codigo.insertText("""main()
    {
        -*Este es el body del main*-
    }""")

    def handle_insert_var(self):
        self.cursor_codigo = self.ui.Txt_Codigo.textCursor()
        self.cursor_codigo.insertText("""data-type var-name = value""")

    def handle_insert_stack(self):
        self.cursor_codigo = self.ui.Txt_Codigo.textCursor()
        self.cursor_codigo.insertText("""pila data-type stack-name = []""")

    def handle_insert_list(self):
        self.cursor_codigo = self.ui.Txt_Codigo.textCursor()
        self.cursor_codigo.insertText("""lista data-type lista-name = []""")

    def handle_output(self):
        if not self.interpreter.error_on_execution:
            outputs = ''
            for output in self.interpreter.outputs:
                outputs += str(output)
            self.interpreter.outputs = []
            print('El valor de outputs es', outputs, 'prueba')
            self.ui.TxtSalida.insertPlainText(outputs)
            scroll_bar = self.ui.TxtSalida.verticalScrollBar()
            scroll_bar.setValue(scroll_bar.maximum())

    def handle_interpreter_error(self, error_message):
        QMessageBox.critical(self, 'Error inesperado en la ejecución ', f"{error_message}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
