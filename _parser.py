class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos] if self.tokens else None
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
            self.current_token = None

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
            print('Iteración del ciclo numero', counter)
            print('El current token que viene es ', self.current_token.type)
            if self.current_token.type == 'FUNCTION':
                self.tree.append(self.parse_function())
            elif self.current_token.type == 'PROCEDURE':
                self.tree.append(self.parse_procedure())
            elif self.current_token.type == 'MAIN' and self.already_main != True:
                self.already_main = True
                self.tree.append(self.parse_main())
            elif self.current_token.type == 'DATATYPE':
                self.tree.append(self.parse_var_def())
            else:
                raise SyntaxError(f"Token inesperado {self.current_token.value}")
            counter += 1
        if not self.already_main:
            raise SyntaxError(f"En el código proporcionado falta el main")

    def parse_function(self):
        self.expect('FUNCTION', 'funcioncita')
        self.in_function = True
        function_name = self.parse_identificador()
        self.function_name = function_name
        self.expect('DELIMETER', '(')
        parameters = self.parse_parameters_def()

        self.expect('DELIMETER', ')')
        self.expect('DELIMETER', ':')
        type_return = self.parse_type_return()
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
        parameters = self.parse_parameters_def()
        self.expect('DELIMETER', ')')
        self.expect('DELIMETER', '{')
        prc_body = self.parse_function_procedure_body('PROCEDURE')
        self.expect('DELIMETER', '}')
        self.in_function = False
        self.function_name = ""
        return 'procedure', prc_name, parameters, prc_body

    def parse_parameters_def(self):
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
        print('el token que llega a parse_identificador es ', self.current_token)
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
        if self.current_token.type == 'DATATYPE':
            complex_data_type = self.current_token.value
            print('El complex data type es ', complex_data_type)
            self.expect('DATATYPE')
            identifier = self.parse_identificador()
            print('El identifier es ', identifier)
            if data_type == 'pila':
                if self.current_token.type == 'ASSIGNMENT':
                    self.advance()
                    value = self.parse_stack_assigment(complex_data_type)
                    return 'stack_declaration', data_type, complex_data_type, identifier, value
                return 'stack_declaration', data_type, complex_data_type, identifier
            elif data_type == 'lista':
                if self.current_token.type == 'ASSIGNMENT':
                    self.advance()
                    value = self.parse_stack_assigment(complex_data_type)
                    return 'list_declaration', data_type, complex_data_type, identifier, value
                return 'list_declaration', data_type, complex_data_type, identifier

        else:
            identifier = self.parse_identificador()
            print('El identifier parseado es ', identifier)

            if self.current_token.type == 'ASSIGNMENT':
                value = self.parse_asignacion(identifier)
                return 'var_declaration', data_type, identifier, value
            else:
                return 'var_declaration', data_type, identifier

    def parse_stack_assigment(self, pri_data_type):
        values = []
        open_braces = 1
        print('El current token es ', self.current_token)
        self.expect('DELIMETER', '[')
        while open_braces > 0:
            print('El current token dentro del while es  ', self.current_token)
            if self.current_token.type == 'DELIMETER' and self.current_token.value == '[':
                open_braces += 1
                self.advance()
            elif self.current_token.type == 'DELIMETER' and self.current_token.value == ']':

                open_braces -= 1
                self.advance()
            else:
                if self.current_token.type == 'DELIMETER' and self.current_token.value == ',':
                    self.advance()
                if pri_data_type == 'entero' and "." not in self.current_token.value:
                    print('El current token value es ', type(self.current_token.value))
                    values.append(int(self.current_token.value))
                elif pri_data_type == 'float':
                    values.append(float(self.current_token.value))
                elif pri_data_type == 'string':
                    values.append(self.current_token.value.strip('"'))
                elif pri_data_type == 'char':
                    values.append(self.current_token.value)
                elif pri_data_type == 'boolean':
                    values.append(bool(self.current_token.value))
                else:
                    raise SyntaxError("No se puede procesar correctamente uno de los valores asignados a una lista o pila, verifique el dato ingresado calze con el tipo de dato de las estructuras")

                self.advance()
        return values

    def parse_statement(self):
        print('El current token es ', self.current_token)
        if self.current_token.type == 'IDENTIFIER':
            print('El valor del identifier es ', self.current_token.value)
            sta_name = self.current_token.value
            self.advance()
            if self.current_token.value == '=':
                return self.parse_asignacion(sta_name)
            else:
                print('Vamos a parsear un fuction call')
                return self.parse_function_call(sta_name)
        elif self.current_token.type == 'DATATYPE':
            return self.parse_var_def()
        elif self.current_token.type == 'KEYWORD' and self.current_token.value.lower() == 'si':
            return self.parse_if_elif()
        elif self.current_token.type == 'KEYWORD' and self.current_token.value.lower() == 'sino':
            if self.conditional_stack[-1]:
                return self.parse_if_elif()
            raise SyntaxError(
                f"Sentencia inesperada {self.current_token.value} en la línea {self.current_token.line} no se puede "
                f"hacer un sino sin si")
        elif self.current_token.type == 'KEYWORD' and self.current_token.value.lower() == 'tons':
            if self.conditional_stack[-1]:
                return self.parse_else()
            raise SyntaxError(
                f"Sentencia inesperada {self.current_token.value} en la línea {self.current_token.line} no se puede "
                f"hacer un tons sin si")
        elif self.current_token.type == 'KEYWORD' and self.current_token.value.lower() == 'retorna':
            self.advance()
            return_value = self.current_token.value
            self.advance()
            return 'retorna', return_value
        elif self.current_token.type == 'KEYWORD' and self.current_token.value.lower() == 'mientras':
            self.advance()
            return self.parse_while()
        elif self.current_token.type == 'KEYWORD' and self.current_token.value.lower() == 'haga':
            self.advance()
            return self.parse_for()
        elif self.current_token.type == 'KEYWORD' and self.current_token.value.lower() == 'casos':
            return self.parse_switch()
        elif self.current_token.type == 'STACKMETHODS' and self.current_token.value.lower() == 'mete':
            return self.parse_mete()
        elif self.current_token.type == 'STACKMETHODS' and self.current_token.value.lower() == 'saca':
            return self.parse_saca()
        elif self.current_token.type == 'STACKMETHODS' and self.current_token.value.lower() == 'arriba':
            return self.parse_arriba()
        elif self.current_token.type == 'LISTMETHODS' and self.current_token.value.lower() == 'obtener':
            return self.parse_obtener()
        elif self.current_token.type == 'LISTMETHODS' and self.current_token.value.lower() == 'insertar':
            return self.parse_insertar()
        elif self.current_token.type == 'LISTMETHODS' and self.current_token.value.lower() == 'ultimo':
            return self.parse_ultimo()
        elif self.current_token.type == 'LISTMETHODS' and self.current_token.value.lower() == 'primero':
            return self.parse_ultimo()
        elif self.current_token.type == 'IO' and self.current_token.value.lower() == 'escriba':
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
        expression = self.parse_expresion()
        return 'assignment', var_name, expression

    def parse_function_call(self, function_name):
        self.expect('DELIMETER', '(')
        arguments = self.parse_arguments_pass()
        self.expect('DELIMETER', ')')
        print('El token que va a salir es ', self.current_token)
        return 'llamada_funcion', function_name, arguments

    def parse_arguments_pass(self):
        arguments = []
        if self.current_token.type != 'DELIMETER' and self.current_token.value != ')':
            while self.current_token.type != 'DELIMETER' and self.current_token.value != ')':
                print('El valor del token antes es ', self.current_token)
                value = self.parse_valor_o_variable()
                arguments.append(value)
                print('El valor del token despues de parse_valor es ', self.current_token)
                if self.current_token.type == 'DELIMETER' and self.current_token.value == ')':
                    break
                elif self.current_token.type == 'DELIMETER' and self.current_token.value == ',':
                    self.advance()
        return arguments

    def parse_expresion(self):
        if self.current_token.type == 'DELIMETER' and self.current_token.value == '(':
            self.advance()
            sub_expr = self.parse_expresion()
            self.expect('DELIMETER', ')')
            left_value = sub_expr
        else:
            left_value = self.parse_valor_o_variable()
            print('El valor de salida es ', left_value, ' y el token actual es ', self.current_token)
        while self.current_token.type == 'OPERATOR':
            operator = self.current_token.value
            self.advance()
            if self.current_token.type == 'DELIMETER' and self.current_token.value == '(':
                self.advance()
                right_value = self.parse_expresion()
                self.expect('DELIMETER', ')')
            else:
                right_value = self.parse_valor_o_variable()
            left_value = ('expresion_aritmetica', left_value, operator, right_value)

        return left_value

    def parse_valor_o_variable(self):
        if self.current_token.type == 'IDENTIFIER' or self.current_token.type == 'STRING':
            value = self.current_token.value
            self.advance()
            if self.current_token.type == 'DELIMETER' and self.current_token.value == '(':
                value = self.parse_function_call(value)
            print('El value de la variable va a ser ', value, ' y el tipo ', type(value))
            return value
        elif self.current_token.type == 'NUMBER':
            if '.' in self.current_token.value:
                value = float(self.current_token.value)
            else:
                value = int(self.current_token.value)
            self.advance()
            return value
        elif self.current_token.type == 'BOOLEAN':
            value = self.current_token.value.lower() == 'true'
            self.advance()
            return value
        elif self.current_token.type == 'CHAR':
            value = self.current_token.value
            self.advance()
            return value

        else:
            raise SyntaxError(
                f"Se esperaba un IDENTIFIER, NUMBER, STRING, CHAR o BOOLEAN, pero se encontró {self.current_token}")

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

            if self.current_token.type == 'KEYWORD' and (
                    self.current_token.value.lower() == 'sino' or self.current_token.value.lower() == 'tons'):
                self.conditional_stack.append(True)
            return 'if', condition, ('body',body)
        else:
            return 'elif', condition, ('body', body)

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
        return 'else', ('body', body)

    def parse_condition(self):
        if self.current_token.type == 'LOGICAL_OPERATOR' and self.current_token.value == 'not':
            self.advance()
            self.expect('DELIMETER', '(')
            not_condition = self.parse_condition()
            self.expect('DELIMETER', ')')
            print('Vamos a retornar de una ')
            if self.current_token.type == 'DELIMETER' and self.current_token.value == ')':
                return ('not', not_condition)
            elif self.current_token.type == 'LOGICAL_OPERATOR' and (self.current_token.value == 'and' or self.current_token.value == 'or'):
                operator = self.current_token.value
                self.expect('LOGICAL_OPERATOR')
                rigth = self.parse_condition()
                return 'logical_expression', ('not',not_condition), operator, rigth


        elif self.current_token.type == 'IDENTIFIER' or self.current_token.type == 'NUMBER' or self.current_token.type == 'BOOLEAN':
            value1 = self.parse_expresion()
            if (self.current_token.type == 'DELIMETER' or self.current_token.type == 'BOOLEAN') and self.current_token.value == ')':
                return 'bool_variable', value1
            comparator = self.current_token.value
            self.expect('COMPARATOR')

            if self.current_token.type == 'IDENTIFIER':
                value2 = self.parse_expresion()
                condition_node = ('comparison', value1, comparator, value2)

            elif self.current_token.type == 'NUMBER':
                value2 = float(self.parse_expresion())
                condition_node = ('comparison', value1, comparator, value2)

            elif self.current_token.type == 'BOOLEAN':
                value2 = bool(self.parse_expresion())
                condition_node = ('comparison', value1, comparator, value2)

            elif self.current_token.type == 'DELIMETER' and self.current_token.value == '(':
                self.advance()
                nested_condition = self.parse_condition()
                self.expect('DELIMETER')
                condition_node = ('comparison', value1, comparator, nested_condition)

            else:
                raise SyntaxError(
                    f"Se esperaba un identificador, número o paréntesis después del comparador, pero se encontró {self.current_token}")

            if self.current_token and self.current_token.type == 'LOGICAL_OPERATOR':
                log_op = self.current_token.value
                self.advance()
                next_condition = self.parse_condition()
                return 'logical_expression', condition_node, log_op, next_condition

            return condition_node

        elif self.current_token.type == 'DELIMETER' and self.current_token.value == '(':
            # Manejo de condiciones anidadas
            self.advance()
            nested_condition = self.parse_condition()
            self.expect('DELIMETER', ')')

            # Verificación para operadores lógicos si siguen después de la condición anidada
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
        print('entra al escriba')
        self.expect('IO', 'escriba')
        self.expect('DELIMETER', '(')
        while self.current_token.type != 'DELIMETER' or self.current_token.value != ')':
            if self.current_token.type == 'STRING':
                arguments.append(self.current_token.value)
                self.advance()
            elif self.current_token.type == 'NUMBER':
                arguments.append(self.current_token.value)
                self.advance()
            elif self.current_token.type == 'IDENTIFIER':
                arguments.append(self.current_token.value)
                self.advance()
            elif self.current_token.type == 'STACKMETHODS' and self.current_token.value == 'saca':
                arguments.append(self.parse_saca())
            elif self.current_token.type == 'STACKMETHODS' and self.current_token.value == 'arriba':
                arguments.append(self.parse_arriba())
            elif self.current_token.type == 'LISTMETHODS' and self.current_token.value == 'ultimo':
                arguments.append(self.parse_ultimo())
            elif self.current_token.type == 'LISTMETHODS' and self.current_token.value == 'primero':
                arguments.append(self.parse_primero())
            elif self.current_token.type == 'LISTMETHODS' and self.current_token.value == 'obtener':
                arguments.append(self.parse_obtener())
            elif self.current_token.type == 'NEWLINE' and self.current_token.value == 'salto':
                arguments.append("\n")
                self.advance()
            else:
                raise SyntaxError(f"Se esperaba un argumento valido pero se encontro {self.current_token}")
            if self.current_token.type == 'DELIMETER' and self.current_token.value == ',':
                self.advance()
            elif self.current_token.type == 'DELIMETER' and self.current_token.value == ')':
                print('Me voy a salir ')
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

    def parse_main(self):
        self.advance()
        self.expect('DELIMETER', '(')
        self.expect('DELIMETER', ')')
        self.expect('DELIMETER', '{')
        main_body = self.parse_main_o_loop_body()
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

    def parse_switch(self):
        print('entra al switch')
        self.advance()
        self.expect('DELIMETER', '(')
        variable = self.current_token.value
        print('El valor que estamos agarrando de variable es ', variable)
        self.expect('IDENTIFIER')
        self.expect('DELIMETER', ')')
        self.expect('DELIMETER', '{')
        switch_body = self.parse_switch_body(variable)
        self.expect('DELIMETER', '}')
        print(f"El valor del switch de salida es {variable}, {switch_body}")
        return 'switch', variable, switch_body

    def parse_switch_body(self, variable):
        switch_cases = []
        defecto = False
        while True:
            if self.current_token.type == 'KEYWORD' and self.current_token.value == 'caso':
                self.advance()
                self.expect('DELIMETER', '(')
                condition = self.parse_condition()
                print('El condition es ', condition)
                if not self.contains_variable(condition, variable):
                    raise SyntaxError(f"La condicion de un caso debe incluir la variable especificada {variable}")
                print(f"El condition del caso es {condition}")
                self.expect('DELIMETER', ')')
                self.expect('DELIMETER', '{')
                case_body = self.parse_main_o_loop_body()
                switch_cases.append(('case', condition, case_body))
            elif self.current_token.type == 'KEYWORD' and self.current_token.value == 'defecto' and not defecto:
                self.advance()
                self.expect('DELIMETER', '{')
                default_body = self.parse_main_o_loop_body()
                defecto = True
                switch_cases.append(('default', default_body))
            elif self.current_token.type == 'KEYWORD' and self.current_token.value == 'defecto' and defecto:
                raise SyntaxError(f"Un switch(casos) no puede tener multiples default(defecto)")
            elif self.current_token.type == 'DELIMETER' and self.current_token.value == '}': # Se encontro el caracter terminal del switch body
                break
            else:
                raise SyntaxError(f"Se esperaba un caso de los casos, pero se encontro {self.current_token}")
        return switch_cases

    def contains_variable(self,condition, variable):
        if isinstance(condition, tuple) and condition[0] == 'comparison':
            return variable == condition[1]
        elif isinstance(condition, tuple) and condition[0] == 'logical_expression':
            left_expr = condition[1]
            right_expr = condition[3]
            return self.contains_variable(left_expr, variable) or self.contains_variable(right_expr, variable)

        return False

    def parse_while(self):
        print('El token con el que entra a parse while es ', self.current_token)
        self.expect('DELIMETER', '(')
        condition = self.parse_condition()
        print('la condicion que se optiene es ', condition)
        self.expect('DELIMETER', ')')
        self.expect('DELIMETER', '{')
        while_body = self.parse_main_o_loop_body()
        return 'while', condition, while_body

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
                    val2 = self.current_token.value
                    self.advance()
                    condition_node = ('comparison', val1, comparator, val2)
                else:
                    raise SyntaxError(f"Se esperaba un número o identificador en la condición del for.")
            else:
                raise SyntaxError(f"Se esperaba un comparador en la condición del for.")

        self.expect('DELIMETER', ',')
        increment_var = self.current_token.value
        self.expect('IDENTIFIER')
        if self.current_token.type == 'INCREMENT':
            self.advance()
            increment_node = ('increment', increment_var, '++')
        elif self.current_token.type == 'DECREMENT':
            self.advance()
            increment_node = ('decrement', increment_var, '--')
        elif self.current_token.type == 'ASSIGNMENT':
            self.advance()
            value = self.parse_expresion()
            increment_node = ('assignment', increment_var, value)
        else:
            raise SyntaxError(f"Se esperaba un incremento o decremento en el for.")
        print('El token de salida aqui es ', self.current_token)
        return {'initialization': (var_for, '=', float(var_ini)), 'condition': condition_node, 'increment': increment_node}

    def parse_for(self):
        print('El token con el que entra a parse for for es ', self.current_token)
        self.expect('DELIMETER', '(')
        condition = self.parse_for_condition()
        self.expect('DELIMETER', ')')
        self.expect('DELIMETER', '{')
        for_body = self.parse_main_o_loop_body()
        print('Antes de retornar ')
        return 'for', condition, for_body

    def parse_mete(self):
        self.expect('STACKMETHODS', 'mete')
        self.expect('DELIMETER', '(')
        identifier = self.parse_identificador()
        self.expect('DELIMETER', ',')
        insert_value = self.parse_expresion() #TODO me  queda la duda de que esto sirva
        self.expect('DELIMETER', ')')
        return 'mete', identifier, insert_value

    def parse_saca(self):
        self.expect('STACKMETHODS', 'saca')
        self.expect('DELIMETER', '(')
        identifier = self.parse_identificador()
        self.expect('DELIMETER', ')')
        print('vamos a retornar saca')
        return 'saca', identifier

    def parse_arriba(self):
        self.expect('STACKMETHODS', 'arriba')
        self.expect('DELIMETER', '(')
        identifier = self.parse_identificador()
        self.expect('DELIMETER', ')')
        return 'arriba', identifier

    def parse_obtener(self):
        self.expect('LISTMETHODS', 'obtener')
        self.expect('DELIMETER', '(')
        identifier = self.parse_identificador()
        self.expect('DELIMETER', ',')
        index = self.current_token.value
        self.expect('NUMBER')
        self.expect('DELIMETER', ')')
        return 'obtener', identifier, int(index)

    def parse_insertar(self): # Sirve para insetar un elemento al final de una lista
        self.expect('LISTMETHODS', 'insertar')
        self.expect('DELIMETER', '(')
        identifier = self.parse_identificador()
        self.expect('DELIMETER', ',')
        value = self.parse_expresion()
        self.expect('DELIMETER', ')')
        return 'insertar', identifier, value
    def parse_primero(self):
        self.expect('LISTMETHODS', 'primero')
        self.expect('DELIMETER', '(')
        identifier = self.parse_identificador()
        self.expect('DELIMETER', ')')
        return 'primero', identifier
    def parse_ultimo(self):
        self.expect('LISTMETHODS', 'ultimo')
        self.expect('DELIMETER', '(')
        identifier = self.parse_identificador()
        self.expect('DELIMETER', ')')
        return 'ultimo', identifier



