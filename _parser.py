class Parser:
    def __init__(self, tokens):
        self.tokens = tokens  # Lista de tokens generada por el lexer
        self.pos = 0  # Posición actual en la lista de tokens
        self.current_token = self.tokens[self.pos]  # Token actual
        self.symbols_table = {}
        self.conditional_stack = []
        self.tree = None

    def advance(self):
        """Avanza al siguiente token"""
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None  # Fin de los tokens

    def expect(self, token_type, token_value=None):
        if self.current_token and self.current_token.type == token_type:
            if token_value is None or self.current_token.value.lower() == token_value:
                self.advance()
            else:
                raise SyntaxError(
                    f"Se esperaba {token_type} con valor '{token_value}', pero se encontró {self.current_token}")
        else:
            raise SyntaxError(f"Se esperaba {token_type}, pero se encontró {self.current_token}")

    def parse(self):
        counter = 1
        self.tree = []
        while self.current_token is not None:
            print('El current token es ', self.current_token)
            print('Iteración del ciclo numero', counter)
            if self.current_token.type == 'FUNCTION' :
                self.tree.append(self.parse_function())
            elif self.current_token.type == 'PROCEDURE' :
                self.tree.append(self.parse_procedure())
            else:
                print('No esta pasando de aqui')
                raise SyntaxError(f"Token inesperado {self.current_token.value}")
            counter += 1


    def parse_function(self):
        self.expect('FUNCTION', 'funcioncita')
        nombre_funcion = self.parse_identificador()
        self.expect('DELIMETER', '(')
        parametros = self.parse_parametros()
        self.expect('DELIMETER', ')')
        self.expect('DELIMETER', ':')
        type_return = self.parse_type_return()
        self.expect('DELIMETER', "{")
        cuerpo_funcion = self.parse_function_procedure_body('funcioncita')
        self.expect('DELIMETER', "}")

        return 'function', nombre_funcion, parametros, type_return, cuerpo_funcion

    def parse_procedure(self):
        self.expect('PROCEDURE')
        prc_name = self.current_token.value
        self.expect('IDENTIFIER')
        self.expect('DELIMETER','(')
        parameters = self.parse_parametros()
        self.expect('DELIMETER', ')')
        self.expect('DELIMETER', '{')
        prc_body = self.parse_function_procedure_body('PROCEDURE')
        self.expect('DELIMETER', '}')
        return 'procedure', prc_name, parameters, prc_body


    def parse_parametros(self):
        parametros = []
        if self.current_token.type != 'DELIMETER' or self.current_token.value != ')':
            while True:
                type_parametro = self.parse_type_return()
                nombre_parametro = self.parse_identificador()
                parametros.append((type_parametro, nombre_parametro))
                if self.current_token.type == 'DELIMETER' and self.current_token.value == ')':
                    break
                self.expect('DELIMETER')
        return parametros

    def parse_identificador(self):
        if self.current_token.type == 'IDENTIFIER':
            identificador = self.current_token.value
            self.advance()
            return identificador
        else:
            raise SyntaxError(f"Se esperaba un IDENTIFIER, pero se encontró {self.current_token}")

    def parse_type_return(self):
        """Parsea el type de retorno"""
        if self.current_token.type == 'DATATYPE':
            type_r = self.current_token.value
            self.advance()
            return type_r
        else:
            print('Entra al else')
            raise SyntaxError(f"Se esperaba un type de retorno, pero se encontró {self.current_token}")

    def parse_function_procedure_body(self, type):
        statements = []
        open_braces = 1
        while open_braces > 0:
            print('El valor actual del token es ', self.current_token)
            if self.current_token.type == 'DELIMETER' and self.current_token.value == '{':
                open_braces += 1
                self.advance()
            elif self.current_token.type == 'DELIMETER' and self.current_token.value == '}':
                open_braces -= 1
                if open_braces == 0:
                    break

            elif self.current_token.type == 'KEYWORD' and self.current_token.value.lower() == 'retorna':
                if type != "funcioncita":
                    raise SyntaxError(f"NO puede haber un procedure con return")
                self.advance()
                valor_retorno = self.parse_valor_o_variable()
                print('El token actual es', self.current_token)
                statements.append(('retorna', valor_retorno))
            else:
                statement = self.parse_statement()
                print('El valor del token despues de entrar a statement es ', self.current_token)
                statements.append(statement)
        print('El token actual es', self.current_token)
        return 'function_body', statements

    def parse_var_def(self):
        data_type = self.current_token.value
        self.expect('DATATYPE')
        print('El token actual es', self.current_token)
        identifier = self.parse_identificador()
        print('El token actual es', self.current_token)
        if self.current_token.type == 'ASSIGNMENT':
            self.expect('ASSIGNMENT')
            value = self.current_token.value
            print('El valor de la salida de la funcion es ', data_type, identifier,value)
            return data_type, identifier, value
        else:
            print('El valor de la salida de la funcion es ', data_type, identifier)
            return data_type, identifier

        #cada una de las lineas del body
    def parse_statement(self):
        if self.current_token.type == 'IDENTIFIER':
            sta_name = self.current_token.value
            self.advance()
            if self.current_token.value == '=':
                return self.parse_asignacion(sta_name)
            else:
                return self.parse_function_call()
        elif self.current_token.type == 'DATATYPE':
            return self.parse_var_def()
        elif self.current_token.type == 'KEYWORD' and self.current_token.value.lower() == 'si':
            return self.parse_if_elif()
        elif self.current_token.type == 'KEYWORD' and self.current_token.value.lower() == 'sino':
            if self.conditional_stack[-1]:
                return self.parse_if_elif()
            raise SyntaxError(f"Sentencia inesperada {self.current_token.value} en la línea {self.current_token.line} no se puede hacer un sino sin si")
        elif self.current_token.type == 'KEYWORD' and self.current_token.value.lower() == 'tons':
            if self.conditional_stack[-1]:
                return self.parse_else()
            raise SyntaxError(
                f"Sentencia inesperada {self.current_token.value} en la línea {self.current_token.line} no se puede hacer un tons sin si")
        elif self.current_token.type == 'KEYWORD' and self.current_token.value.lower() == 'retorna':
            self.advance()
            return_value = self.current_token.value
            print("el valor de retorna es ", return_value)
            self.advance()
            return 'retorna', return_value
        elif self.current_token.type == 'IO' and self.current_token.value.lower() == 'escriba':
            return self.parse_io_print()
        elif self.current_token.type == 'IO' and self.current_token.value.lower() == 'lea':
            return self.parse_io_lea()
        else:
            print('Se va al else')
            raise SyntaxError(f"Sentencia inesperada {self.current_token.value} en la línea {self.current_token.line}")

    def parse_asignacion(self, var_name):
        self.expect('ASSIGNMENT')
        if self.current_token.type == 'STRING':
            expression = self.current_token.value
            self.advance()
            return 'assignment', var_name, expression
        expression = self.parse_expresion()  # Parseamos la expresión a la derecha del "="
        return 'assignment', var_name, expression

    def parse_function_call(self):
        nombre_funcion = self.parse_identificador()
        self.expect('DELIMETER')  # Esperamos "("
        argumentos = self.parse_function_arguments()  # Parseamos los argumentos de la función
        self.expect('DELIMETER')  # Esperamos ")"
        return 'llamada_funcion', nombre_funcion, argumentos

    def parse_function_arguments(self):
        arguments = []
        if self.current_token.type != 'DELIMETER' and self.current_token.value != ')':
            while self.current_token.type != 'DELIMETER' and self.current_token.value != ')':
                value = self.parse_valor_o_variable()
                arguments.append(value)
                self.expect('DELIMETER')
        return arguments

    def parse_expresion(self):

        if self.current_token.type == 'DELIMETER' and self.current_token.value == '(':
            self.advance()
            sub_expr = self.parse_expresion()
            self.expect('DELIMETER', ')')
            left_value = sub_expr
        else:
            left_value = self.parse_valor_o_variable()
        while self.current_token.type == 'OPERATOR':
            operator = self.current_token.value
            self.advance()
            if self.current_token.type == 'DELIMETER' and self.current_token.value == '(':
                self.advance()  # Saltamos el '('
                right_value = self.parse_expresion()
                self.expect('DELIMETER', ')')  # Esperamos el cierre ')'
            else:
                right_value = self.parse_valor_o_variable()  # Parseamos el valor derecho
            left_value = ('expresion_aritmetica', left_value, operator, right_value)

        return left_value

    def parse_valor_o_variable(self):
        if self.current_token.type == 'IDENTIFIER' or self.current_token.type == 'NUMBER' or self.current_token.type == 'STRING':
            value = self.current_token.value
            self.advance()
            return value
        elif self.current_token.type == 'BOOLEAN':
            value = self.current_token.value.lower() == 'true'
            self.advance()
            return value
        else:
            raise SyntaxError(f"Se esperaba un IDENTIFIER, NUMBER, STRING o BOOLEAN, pero se encontró {self.current_token}")

    def parse_if_elif(self):
        self.conditional_stack.append(True)
        conditional_type = self.current_token.value
        self.advance()
        self.expect('DELIMETER', '(')
        condition = self.parse_condition()
        self.expect('DELIMETER', ')')
        self.expect('DELIMETER','{')
        body = []
        open_braces = 1
        while open_braces > 0:
            print('El valor actual del toquen en el while es ', self.current_token)
            if self.current_token.type == 'DELIMETER' and self.current_token.value == '}':
                open_braces -= 1
                self.advance()
                if open_braces == 0:
                    print('Termino el while')
                    break
            elif self.current_token.type == 'DELIMETER' and self.current_token.value == '{':
                open_braces += 1
                self.advance()
            else:
                print('si entra')
                statement = self.parse_statement()
                body.append(statement)
        if conditional_type.lower() == 'si':
            return 'if', condition, body
        else:
            return 'elif', condition, body

    def parse_else(self):
        print('El token que llega es ', self.current_token)
        self.advance()
        self.expect('DELIMETER', '{')
        body = []
        open_braces = 1
        while open_braces > 0:
            if self.current_token.type == 'DELIMETER' and self.current_token.value == '}':
                open_braces -= 1
                self.advance()
                if open_braces == 0:
                    break
            elif self.current_token.type == 'DELIMETER' and self.current_token.value == '{':
                open_braces += 1
                self.advance()
            else:
                statement = self.parse_statement()
                body.append(statement)

        self.conditional_stack.pop()
        return 'else', body

    def parse_condition(self):
        if self.current_token.type == 'IDENTIFIER' or self.current_token.type == 'NUMBER':
            value1 = self.current_token.value
            self.advance()
            if self.current_token.type == 'COMPARATOR':
                comparator = self.current_token.value
                self.advance()
                if self.current_token.type == 'IDENTIFIER' or self.current_token.type == 'NUMBER':
                    value2 = self.current_token.value
                    self.advance()
                    condition_node = ('comparison', value1, comparator, value2)
                    if self.current_token and self.current_token.type == 'LOGICAL_OPERATOR':
                        log_op = self.current_token.value
                        self.advance()
                        next_condition = self.parse_condition()
                        return 'logical_expression', condition_node, log_op, next_condition
                    return condition_node
                else:
                    raise SyntaxError(
                        f"Se esperaba un identificador o número después del comparador, pero se encontró {self.current_token}")
            else:
                raise SyntaxError(f"Se esperaba un comparador, pero se encontró {self.current_token}")
        else:
            raise SyntaxError(f"Se esperaba un identificador o número al principio de la condición, pero se encontró {self.current_token}")

    def parse_io_print(self):
        arguments = []
        self.expect('IO','escriba')
        self.expect('DELIMETER', '(')
        while self.current_token.type != 'DELIMETER' or self.current_token.value != ')':
            if self.current_token.type == 'STRING':
                arguments.append(self.current_token.value)
            elif self.current_token.type == 'NUMBER':
                arguments.append(self.current_token.value)
            elif self.current_token.type == 'IDENTIFIER':
                arguments.append(self.current_token.value)
            elif self.current_token.type == 'KEYWORD' and self.current_token.value == 'salto':
                arguments.append(self.current_token.value)
            else:
                raise SyntaxError(f"Se esperaba un argumento valido pero se encontro {self.current_token}")
            self.advance()

            if self.current_token.type == 'DELIMETER' and self.current_token.value == ',':
                self.advance()
            elif self.current_token.type == 'DELIMETER' and self.current_token.value == ')':
                break
            else:
                raise SyntaxError(f"Se esperaba una , pero se encontro {self.current_token}")

        self.expect('DELIMETER', ')')
        return 'print', arguments

    def parse_io_lea(self):
        self.advance()
        self.expect('DELIMETER', '(')
        if self.current_token.type == 'IDENTIFIER':
            var_save = self.current_token.value
            self.advance()
            self.expect('DELIMETER', ')')
            return 'input', var_save
        else:
            raise SyntaxError(f"Se esperaba un argumento valido pero se encontro {self.current_token}")




#if __name__ == "__main__":
 #   code = 'print("Hello World")'
  #  parser = Parser()
