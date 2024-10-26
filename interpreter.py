class Interpreter:
    def __init__(self, tree):
        self.tree = tree
        self.symbols_table = {}
        self.functions = {}
        self.current_scope = None
        self.outputs = []
        self.already_encountered = False

    def interpret(self):
        for node in self.tree:
            if node[0] == 'function' or node[0] == 'procedure':
                self.visit(node)
            elif node[0] == 'var_declaration':
                self.current_scope = 'global'
                self.visit(node)

        main_node = None
        for node in self.tree:
            if node[0] == 'main':
                main_node = node
                break

        self.visit(main_node)

    def visit(self, node):
        node_type = node[0]

        if node_type == 'function':
            self.visit_function(node)
        elif node_type == 'procedure':
            self.visit_procedure(node)
        elif node_type == 'main':
            self.visit_main(node)
        elif node_type == 'var_declaration':
            self.visit_var_declaration(node)
        elif node_type == 'assignment':
            print('Entra al assignment ')
            self.visit_assignment(node)
        elif node_type == 'llamada_funcion':
            print('El nodo de llamada a función es ', node)
            self.visit_function_call(node)
        elif node_type == 'if':
            self.visit_if(node)
        elif node_type == 'elif':
            self.visit_if(node)
        elif node_type == 'else':
            if not self.already_encountered:
                self.visit_else(node)
            self.already_encountered = False
        elif node_type == 'while':
            self.visit_while(node)
        elif node_type == 'for':
            self.visit_for(node)
        elif node_type == 'print':
            print('Entramos a imprimir')
            self.visit_print(node)
        elif node_type == 'retorna':
            return self.visit_return(node)
        elif node_type == 'input':
            self.visit_read(node)
        else:
            raise ValueError(f"Tipo de nodo desconocido: {node_type}")

    def visit_function(self, node):
        _, name, parameters, return_type, body = node
        self.current_scope = name
        self.functions[name] = {'parameters': parameters, 'body': body}
        for var_type, namee in parameters:
            self.symbols_table[namee+self.current_scope] = {'type': 'parameter', 'data_type': var_type, 'value': None, 'scope': name}

    def visit_var_declaration(self, node):
        print('El nodo que llega es ', node)
        _ = node[0]
        var_type = node[1]
        var_name = node[2]
        self.symbols_table[var_name+self.current_scope] = {'type': 'variable', 'data_type': var_type, 'value': None, 'scope': self.current_scope}
        print(f"Declaración de variable {var_name} de tipo {var_type}.")
        if len(node) == 4:
            self.visit_assignment(node[3])

    def visit_procedure(self, node):
        _, name, parameters, body = node
        self.current_scope = name
        self.functions[name] = {'parameters': parameters, 'body': body}
        for var_type, namee in parameters:
            self.symbols_table[namee+self.current_scope] = {'type': 'parameter', 'data_type': var_type, 'value': None, 'scope': name}
        print(f"Procedimiento '{name}' definido.")

    def visit_main(self, node):
        _, body = node
        print("Ejecutando main...")
        self.current_scope = 'main'
        self.execute_body(body)

    def visit_assignment(self, node):
        _, var_name, expression = node
        print('El nodo que viene es ', node)
        value = self.evaluate_expression(expression)
        print('El value es ', value, ' y el tip es ', type(value))
        print('El value en symbols table es ', self.symbols_table[var_name + self.current_scope]['value'])
        print('El token para acceder es ', var_name + self.current_scope)
        expected_type = self.cast_datatype(self.symbols_table[var_name+self.current_scope]['data_type'])
        print('El expected type es ', expected_type)
        if isinstance(value, float) and expected_type == int:
            value = int(value)
        elif isinstance(value, int) and expected_type == float:
            value = float(value)
        if isinstance(value, expected_type):
            if self.symbols_table[var_name+self.current_scope]['data_type'] == 'char':
                if len(value) > 1:
                    raise ValueError(f"Una variable de tipo char solo puede almacenar un carácter")

            print(f"Asignando {value} a la variable {var_name} con scope {self.current_scope}")
            self.symbols_table[var_name+self.current_scope]['value'] = value
        else:
            print('entra al else de exception')
            print('El var name es ', var_name)
            raise ValueError(
                f"Se esperaba un valor de tipo {self.symbols_table[var_name+self.current_scope]['data_type']}, pero se encontró {type(value).__name__}")

        print('El valor de salida del interprete es ', self.symbols_table[var_name+self.current_scope]['value'])
        self.print_symbols_table()

    def evaluate_expression(self, expr):
        print('El valor de expresion que recibimos es ', expr, ' y el datatype es ', type(expr))
        if isinstance(expr, tuple) and expr[0] == 'expresion_aritmetica':
            print('El operator que entra es ', expr[2])
            left = self.evaluate_expression(expr[1])
            operator = expr[2]
            right = self.evaluate_expression(expr[3])

            if operator == '*':
                print('Entra a multi')
                return float(left) * float(right)
            elif operator == '+':
                if isinstance(left, str) and isinstance(right, str):
                    return left + right
                return float(left) + float(right)
            elif operator == '-':
                print('Entra a resta')
                return float(left) - float(right)
            elif operator == '/':
                print('Entra a división')
                return float(left) / float(right)
            elif operator == '%':
                print('Entra a modulo')
                return float(left) % float(right)
            else:
                raise ValueError(f"Operador aritmético desconocido: {operator}")

        elif isinstance(expr, str) and expr.startswith('"') and expr.endswith('"'):
            print('Entra como is fuera un string ')
            return expr.strip('""')
        elif isinstance(expr, tuple) and expr[0] == 'llamada_funcion':
            print('Entra a llamar la función ')
            return self.visit_function_call(expr)
        else:
            self.print_symbols_table()
            if isinstance(expr, str) and expr+self.current_scope in self.symbols_table:
                return self.symbols_table[expr+self.current_scope]['value']
            elif isinstance(expr, int) or isinstance(expr, float):
                print('El valor tipo de dato es ', type(expr))
                return expr

    def visit_print(self, node):
        _, arguments = node
        output = ""
        print('El current scope en la impresion es: ', self.current_scope)
        print('Los argumentos son ', arguments)
        for arg in arguments:
            if arg+self.current_scope in self.symbols_table:
                output += str(self.symbols_table[arg+self.current_scope]['value'])
            else:
                output += str(arg.replace('"', ''))
        self.outputs.append(output)

    def visit_function_call(self, node):
        _, function_name, arguments = node
        print('La lista de funciones es ', self.functions)
        print('El nodo de entrada es ', node)
        if function_name not in self.functions:
            raise NameError(f"Función {function_name} no definida.")

        # Obtener la función
        function = self.functions[function_name]
        parameters = function['parameters']
        body = function['body']
        print('Los parametros esperados son ', parameters)
        print('Los argumentos que vienen son ', arguments)

        for i, (param_type, param_name) in enumerate(parameters):
            print('El parametro ', i, param_type, param_name)
            if self.symbols_table[param_name+function_name]['type'] == 'parameter':
                if arguments[i]+self.current_scope not in self.symbols_table:
                    print('El arugumento en la posicion ', i, ' es : ', arguments[i])
                    self.symbols_table[param_name+self.current_scope]['value'] = arguments[i]
                else:
                    self.print_symbols_table()
                    self.symbols_table[param_name+function_name]['value'] = self.symbols_table[arguments[i]+self.current_scope]['value']

        before_scope = self.current_scope
        print('llega hasta aca')
        self.current_scope = function_name
        executed_function_body = self.execute_body(body)
        self.current_scope = before_scope
        return executed_function_body

    def visit_if(self, node):
        _, condition, body = node
        if self.evaluate_condition(condition):
            self.already_encountered = True
            self.execute_body(body)

    def visit_while(self, node):
        _, condition, body = node
        while self.evaluate_condition(condition):
            print('El body del while es: ', body)
            self.execute_body(body)

    def visit_for(self, node):
        print('El nodo que entra al for es ', node)
        _, loop_data, body = node
        init_var, _, init_value = loop_data['initialization']
        print('El tipo de init_var es ', type(init_var))
        self.symbols_table[init_var+self.current_scope] = { 'type': 'variable', 'data_type': 'entero', 'value': init_value, 'scope': self.current_scope}
        condition = loop_data['condition']
        increment = loop_data['increment']
        print('El current scope es ', self.current_scope)
        print('El valor de la variable contador es ', self.symbols_table[init_var+self.current_scope])
        print('El condition es ', condition)
        print('El increment es ', increment)
        print('El body del while es: ', body)
        print('El init value es ', init_value)
        print('El resultado del condition es ', self.evaluate_condition(condition))
        while self.evaluate_condition(condition):
            print('El valor actual de la variable contador es ', self.symbols_table[init_var+self.current_scope]['value'])
            self.execute_body(body)
            print('Sale del body')
            self.update_increment(increment)

    def update_increment(self, increment):
        typee, var_name, exp_aritmetica = increment
        if typee == 'assignment':
            value = self.evaluate_expression(exp_aritmetica)
        elif typee == 'increment':
            value = self.symbols_table[var_name+self.current_scope]['value'] + 1
        else:
            value = self.symbols_table[var_name+self.current_scope]['value'] - 1

        self.symbols_table[var_name+self.current_scope]['value'] = value
        print('El valor actualizado es ', value)

    def visit_return(self, node):
        _, value = node
        if value+self.current_scope in self.symbols_table:
            return self.symbols_table[value+self.current_scope]['value']
        return value

    def execute_body(self, body):
        _, statements = body
        print(f'Los statements son {statements}')
        for statement in statements:
            result = self.visit(statement)
            if result is not None:
                return result

    def evaluate_condition(self, condition):
        print('El condition que viene es ', condition)
        if condition[0] == 'comparison':
            left, operator, right = condition[1:]
            print('El tipo del left es ', type(left))
            print('El tipo del right es ', type(right))
            if isinstance(left, int) or isinstance(left, float):
                left_value = left
            elif isinstance(left, tuple) and left[0] == 'expresion_aritmetica':
                left_value = self.evaluate_expression(left)
            elif left+self.current_scope in self.symbols_table:
                left_value = self.symbols_table[left+self.current_scope]['value']
            else:
                left_value = left

            print('El left value es ', left_value)

            if isinstance(right, int) or isinstance(right, float):
                right_value = right
            elif right+self.current_scope in self.symbols_table:
                right_value = self.symbols_table[right+self.current_scope]['value']
            elif isinstance(right, tuple) and right[0] == 'expresion_aritmetica':
                right_value = self.evaluate_expression(right)
            else: #Esto lo dejo por si acaso de los bools
                right_value = right

            print('El valor izquierdo es ', left_value, ' y  el tipo es ', type(left_value))
            print('El valor derecho es ', right_value, ' y  el tipo es ', type(right_value))
            print('El operador es ', operator)
            return self.apply_comparator(left_value, operator, right_value)
        elif condition[0] == 'logical_expression':
            left_expr, operator, right_expr = condition[1:]
            left_result = self.evaluate_condition(left_expr)
            right_result = self.evaluate_condition(right_expr)
            return self.apply_logical_operator(left_result, operator, right_result)

    def apply_comparator(self, left, operator, right):
        if operator == '==':
            return left == right
        elif operator == '!=':
            return left != right
        elif operator == '>':
            return left > right
        elif operator == '<':
            return left < right
        elif operator == '>=':
            return left >= right
        elif operator == '<=':
            return left <= right
        else:
            raise ValueError(f"Operador de comparación desconocido: {operator}")

    def apply_logical_operator(self, left, operator, right):
        if operator == '&&':
            return left and right
        elif operator == '||':
            return left or right
        else:
            raise ValueError(f"Operador lógico desconocido: {operator}")

    def print_symbols_table(self):
        print('Esta es la tabla de simbolos dentro del interprete')
        print(self.symbols_table)


    def visit_else(self, body):
        _, body = body
        self.execute_body(body)

    def cast_datatype(self, data_type):
        if data_type == 'entero':
            return int
        elif data_type == 'float':
            return float
        elif data_type == 'string':
            return str
        elif data_type == 'bool':
            return bool
        elif data_type == 'char':
            return str

    def visit_read(self, node):
        _, var_save = node

