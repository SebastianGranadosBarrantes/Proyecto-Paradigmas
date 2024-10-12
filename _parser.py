class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos]
        self.symbols_table = {}
        self.conditional_stack = []
        self.tree = None
        self.in_function = False
        self.function_name = ""
        self.already_main = False

    def advance(self):
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
            if self.current_token.type == 'FUNCTION':
                self.tree.append(self.parse_function())
            elif self.current_token.type == 'PROCEDURE':
                self.tree.append(self.parse_procedure())
            elif self.current_token.type == 'MAIN' and self.already_main != True:
                self.already_main = True
                self.tree.append(self.parse_main())
            else:
                raise SyntaxError(f"Token inesperado {self.current_token.value}")
            counter += 1
        if self.already_main == False:
            raise SyntaxError(f"En el código proporcionado falta el main")
    def parse_function(self):
        self.expect('FUNCTION', 'funcioncita')
        self.in_function = True
        function_name = self.parse_identificador()
        self.function_name = function_name
        self.verify_in_symbols_table(function_name, 'global')
        self.expect('DELIMETER', '(')
        parameters = self.parse_parameters()
        for _type, name in parameters:
            self.verify_in_symbols_table(name, _type)

        self.expect('DELIMETER', ')')
        self.expect('DELIMETER', ':')
        type_return = self.parse_type_return()
        self.symbols_table[function_name] = {"type": "function", "data_type": type_return, "scope": "Global", "parameters": parameters}
        self.expect('DELIMETER', "{")
        cuerpo_funcion = self.parse_function_procedure_body('funcioncita')
        self.expect('DELIMETER', "}")
        self.in_function = False
        self.function_name = ""
        return 'function', function_name, parameters, type_return, cuerpo_funcion

    def parse_procedure(self):
        self.expect('PROCEDURE')
        self.in_function = True
        prc_name = self.current_token.value
        self.function_name = prc_name
        self.expect('IDENTIFIER')
        self.expect('DELIMETER', '(')
        parameters = self.parse_parameters()
        self.expect('DELIMETER', ')')
        self.expect('DELIMETER', '{')
        prc_body = self.parse_function_procedure_body('PROCEDURE')
        self.expect('DELIMETER', '}')
        self.in_function = False
        self.function_name = ""
        self.symbols_table[prc_name] = {"type": "procedure", "scope": "Global", "parameters": parameters}
        return 'procedure', prc_name, parameters, prc_body

    def parse_parameters(self):
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
        if self.current_token.type == 'DATATYPE':
            type_r = self.current_token.value
            self.advance()
            return type_r
        else:
            print('Entra al else')
            raise SyntaxError(f"Se esperaba un type de retorno, pero se encontró {self.current_token}")

    def parse_function_procedure_body(self, _type):
        statements = []
        open_braces = 1
        while open_braces > 0:
            if self.current_token.type == 'DELIMETER' and self.current_token.value == '{':
                open_braces += 1
                self.advance()
            elif self.current_token.type == 'DELIMETER' and self.current_token.value == '}':
                open_braces -= 1
                if open_braces == 0:
                    break

            elif self.current_token.type == 'KEYWORD' and self.current_token.value.lower() == 'retorna':
                if _type != "funcioncita":
                    raise SyntaxError(f"NO puede haber un procedure con return")
                self.advance()
                valor_retorno = self.parse_valor_o_variable()
                statements.append(('retorna', valor_retorno))
            else:
                statement = self.parse_statement()
                statements.append(statement)
        return 'function_body', statements

    def parse_var_def(self):
        data_type = self.current_token.value
        self.expect('DATATYPE')
        identifier = self.parse_identificador()
        if identifier in self.symbols_table:
            raise SyntaxError(f"La variable {identifier} ya existe!")

        if self.current_token.type == 'ASSIGNMENT':
            self.advance()
            value = self.current_token.value
            if self.in_function:
                self.symbols_table[identifier] = {"type": "variable", "data_type": data_type, "scope": self.function_name, "value": value}
            else:
                self.symbols_table[identifier] = {"type": "variable", "data_type": data_type, "scope": "global", "value": value}
            self.advance()
            return data_type, identifier, value
        else:
            if self.in_function:
                self.symbols_table[identifier] = {"type": "variable", "data_type": data_type, "scope": self.function_name, "value": ""}
            else:
                self.symbols_table[identifier] = {"type": "variable", "data_type": data_type, "scope": "global", "value": ""}
            return data_type, identifier

        # cada una de las lineas del body

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
            print('entra al if')
            return self.parse_if_elif()
        elif self.current_token.type == 'KEYWORD' and self.current_token.value.lower() == 'sino':
            if self.conditional_stack[-1]:
                return self.parse_if_elif()
            raise SyntaxError(f"Sentencia inesperada {self.current_token.value} en la línea {self.current_token.line} no se puede hacer un sino sin si")
        elif self.current_token.type == 'KEYWORD' and self.current_token.value.lower() == 'tons':
            print('entra al else')
            print('el conditional stack es ', self.conditional_stack)
            if self.conditional_stack[-1]:
                return self.parse_else()
            raise SyntaxError(f"Sentencia inesperada {self.current_token.value} en la línea {self.current_token.line} no se puede hacer un tons sin si")
        elif self.current_token.type == 'KEYWORD' and self.current_token.value.lower() == 'retorna':
            self.advance()
            return_value = self.current_token.value
            print("el valor de retorna es ", return_value)
            self.advance()
            return 'retorna', return_value
        elif self.current_token.type == 'KEYWORD' and self.current_token.value.lower() == 'mientras':
            self.advance()
            self.parse_while()
        elif self.current_token.type == 'KEYWORD' and self.current_token.value.lower() == 'haga':
            self.advance()
            self.parse_for()
        elif self.current_token.type == 'IO' and self.current_token.value.lower() == 'escriba':
            print('entra al escriba')
            return self.parse_io_print()
        elif self.current_token.type == 'IO' and self.current_token.value.lower() == 'lea':
            return self.parse_io_read()
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
            raise SyntaxError(
                f"Se esperaba un IDENTIFIER, NUMBER, STRING o BOOLEAN, pero se encontró {self.current_token}")

    def parse_if_elif(self):
        conditional_type = self.current_token.value
        self.advance()
        self.expect('DELIMETER', '(')
        condition = self.parse_condition()
        print('El condition que retorna es ', condition)
        self.expect('DELIMETER', ')')
        print('despues de que se callera ')
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
        if conditional_type.lower() == 'si':

            if self.current_token.type == 'KEYWORD' and (self.current_token.value.lower() == 'sino' or self.current_token.value.lower() == 'tons'):
                self.conditional_stack.append(True)
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
                print('El valor actual del toquen antes del advance ', self.current_token)
                open_braces -= 1
                self.advance()
                print('El valor actual del toquen después del advance es ', self.current_token)
                if open_braces == 0:
                    break
            elif self.current_token.type == 'DELIMETER' and self.current_token.value == '{':
                open_braces += 1
                self.advance()
            else:
                statement = self.parse_statement()
                body.append(statement)

        self.conditional_stack.pop()
        print('vamos a salir del else')
        return 'else', body

    def parse_condition(self):
        if self.current_token.type == 'IDENTIFIER' or self.current_token.type == 'NUMBER':
            value1 = self.current_token.value
            self.advance()
            comparator = self.current_token.value
            self.expect('COMPARATOR')

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

            elif self.current_token.type == 'DELIMETER' and self.current_token.value == '(':
                self.advance()
                nested_condition = self.parse_condition()  # Llama recursivamente para procesar la sub-expresión
                self.expect('DELIMETER')  # Espera un delimitador de cierre ')'
                condition_node = ('comparison', value1, comparator, nested_condition)

                if self.current_token and self.current_token.type == 'LOGICAL_OPERATOR':
                    log_op = self.current_token.value
                    self.advance()
                    next_condition = self.parse_condition()
                    return 'logical_expression', condition_node, log_op, next_condition
                return condition_node
            else:
                raise SyntaxError(
                    f"Se esperaba un identificador, número o paréntesis después del comparador, pero se encontró {self.current_token}")
        elif self.current_token.type == 'DELIMETER' and self.current_token.value == '(':
            self.advance()
            nested_condition = self.parse_condition()
            self.expect('DELIMETER')
            if self.current_token and self.current_token.type == 'LOGICAL_OPERATOR':
                log_op = self.current_token.value
                self.advance()
                next_condition = self.parse_condition()
                return 'logical_expression', nested_condition, log_op, next_condition
            return nested_condition

        else:
            raise SyntaxError(
                f"Se esperaba un identificador, número o paréntesis al principio de la condición, pero se encontró {self.current_token}")

    def parse_io_print(self):
        arguments = []
        self.expect('IO', 'escriba')
        self.expect('DELIMETER', '(')
        while self.current_token.type != 'DELIMETER' or self.current_token.value != ')':
            if self.current_token.type == 'STRING':
                arguments.append(self.current_token.value)
            elif self.current_token.type == 'NUMBER':
                arguments.append(self.current_token.value)
            elif self.current_token.type == 'IDENTIFIER':
                arguments.append(self.current_token.value)
            elif self.current_token.type == 'NEWLINE' and self.current_token.value == 'salto':
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

    def parse_io_read(self):
        self.advance()
        self.expect('DELIMETER', '(')
        if self.current_token.type == 'IDENTIFIER':
            var_save = self.current_token.value
            self.advance()
            self.expect('DELIMETER', ')')
            return 'input', var_save
        else:
            raise SyntaxError(f"Se esperaba un argumento valido pero se encontro {self.current_token}")

    def verify_in_symbols_table(self, symbol_name, scope):
        if symbol_name in self.symbols_table and scope == 'local':
            raise SyntaxError(f"El objeto {symbol_name} ya existe!")

    def parse_main(self):
        self.advance()
        self.expect('DELIMETER', '(')
        self.expect('DELIMETER', ')')
        self.expect('DELIMETER', '{')
        main_body = self.parse_main_o_loop_body()
        self.expect('DELIMETER', '}')
        return 'main', main_body

    def parse_main_o_loop_body(self):
        open_braces = 1
        statements = []
        while open_braces > 0:
            if self.current_token.type == 'DELIMETER' and self.current_token.value == '}':
                open_braces -= 1
                self.advance()
            elif self.current_token.type == 'DELIMETER' and self.current_token.value == '{':
                open_braces += 1
                self.advance()
            else:
                statement = self.parse_statement()
                statements.append(statement)

            return 'main_body', statements

    def parse_while(self):
        print('El token con el que entra a parse while es ', self.current_token)
        self.expect('DELIMETER', '(')
        condition = self.parse_condition()
        self.expect('DELIMETER', ')')
        self.expect('DELIMETER', '{')
        while_body = self.parse_main_o_loop_body()
        self.expect('DELIMETER', '}')
        return 'while',condition, while_body

    def parse_for_condition(self):
        var_for = self.current_token.value
        self.expect('IDENTIFIER')
        self.expect('ASSIGNMENT')
        var_ini = self.current_token.value
        self.expect('NUMBER')

        self.expect('DELIMETER', ',')
        if self.current_token.type == 'IDENTIFIER' or self.current_token.type == 'NUMBER':
            val1 = self.current_token.value
            self.advance()
            if self.current_token.type == 'COMPARATOR':
                comparator = self.current_token.value
                self.advance()
                if self.current_token.type == 'IDENTIFIER' or self.current_token.type == 'NUMBER':
                    val2 = self.current_token.value  # Segundo valor (ej. 10)
                    self.advance()
                    condition_node = ('comparison', val1, comparator, val2)
                else:
                    raise SyntaxError(f"Se esperaba un número o identificador en la condición del for.")
            else:
                raise SyntaxError(f"Se esperaba un comparador en la condición del for.")

        self.expect('DELIMETER', ',')  # Coma que separa la condición del incremento/decremento

        # Incremento o decremento (se espera algo como i++ o i = i + 1)
        incremento_var = self.current_token.value  # La variable del incremento (ej. i)
        self.expect('IDENTIFIER')
        if self.current_token.type == 'OPERATOR' and self.current_token.value == '+':
            self.advance()
            if self.current_token.value == '+':
                self.advance()  # Esto sería para un incremento como i++
                incremento_node = ('incremento', incremento_var, '++')
            else:
                self.expect('ASSIGNMENT')
                increment_value = self.current_token.value
                self.advance()
                incremento_node = ('incremento', incremento_var, '+', increment_value)
        elif self.current_token.type == 'OPERATOR' and self.current_token.value == '-':
            self.advance()
            if self.current_token.value == '-':
                self.advance()  # Esto sería para un decremento como i--
                incremento_node = ('decremento', incremento_var, '--')
            else:
                self.expect('ASSIGNMENT')
                decrement_value = self.current_token.value
                self.advance()
                incremento_node = ('decremento', incremento_var, '-', decrement_value)
        else:
            raise SyntaxError(f"Se esperaba un incremento o decremento en el for.")

        return {'initialization': (var_for, '=', var_ini),'condition': condition_node,'increment': incremento_node}


    def parse_for(self):
        print('El token con el que entra a parse for for es ', self.current_token)
        self.expect('DELIMETER', '(')
        condition = self.parse_for_condition()
        self.expect('DELIMETER', ')')
        self.expect('DELIMETER', '{')
        for_body = self.parse_main_o_loop_body()
        self.expect('DELIMETER', '}')
        return 'for',condition, for_body


# if __name__ == "__main__":
#   code = 'print("Hello World")'
#  parser = Parser()
