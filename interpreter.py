class Interpreter:
    def __init__(self, tree):
        self.tree = tree
        self.symbols_table = {}
        self.functions = {}
        self.current_scope = None

    def interpret(self):
        for node in self.tree:
            if node[0] == 'function' or node[0] == 'procedure':
                self.visit(node)
            elif node[0] == 'var_declaration':  # Registrar variables globales
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
            self.visit_assignment(node)
        elif node_type == 'llamada_funcion':
            self.visit_function_call(node)
        elif node_type == 'if':
            self.visit_if(node)
        elif node_type == 'elif':
            self.visit_if(node)
        elif node_type == 'else':
            self.visit_else(node)
        elif node_type == 'while':
            self.visit_while(node)
        elif node_type == 'for':
            self.visit_for(node)
        elif node_type == 'print':
            self.visit_print(node)
        elif node_type == 'retorna':
            return self.visit_return(node)
        else:
            raise ValueError(f"Tipo de nodo desconocido: {node_type}")

    def visit_function(self, node):
        _, name, parameters, return_type, body = node
        self.functions[name] = {'parameters': parameters, 'body': body}
        for var_type, namee in parameters:
            self.symbols_table[namee] = {'type': 'parameter', 'data_type': var_type, 'value': None, 'scope': name}

    def visit_var_declaration(self, node):
        print('El nodo que llega es ', node)
        _ = node[0]
        var_type = node[1]
        var_name = node[2]
        self.symbols_table[var_name] = {'type': 'variable', 'data_type': var_type, 'value': None, 'scope': self.current_scope}
        print(f"Declaración de variable {var_name} de tipo {var_type}.")
        if len(node) == 4:
            self.visit_assignment(node[3])

    def visit_procedure(self, node):
        _, name, parameters, body = node
        self.functions[name] = {'parameters': parameters, 'body': body}
        for var_type, namee in parameters:
            self.symbols_table[namee] = {'type': 'parameter', 'data_type': var_type, 'value': None, 'scope': name}
        print(f"Procedimiento '{name}' definido.")

    def visit_main(self, node):
        _, body = node
        print("Ejecutando main...")
        self.current_scope = 'main'
        self.execute_body(body)

    def visit_assignment(self, node):
        _, var_name, expression = node
        print('antes de que se caiga')
        value = self.evaluate_expression(expression)
        print(f"Asignando {value} a la variable {var_name}.")
        self.symbols_table[var_name]['value'] = value
        print('El valor de salida del interprete es ', self.symbols_table[var_name]['value'])
        self.print_symbols_table()

    def evaluate_expression(self, expr):
        print('El valor de expresion que recibimos es ', expr)
        if isinstance(expr, tuple) and expr[0] == 'expresion_aritmetica':
            left = self.evaluate_expression(expr[1])
            operator = expr[2]
            right = self.evaluate_expression(expr[3])
            if operator == '*':
                return float(left) * float(right)
            elif operator == '+':
                return float(left) + float(right)
            elif operator == '-':
                return float(left) - float(right)
            elif operator == '/':
                return float(left) / float(right)
            else:
                raise ValueError(f"Operador aritmético desconocido: {operator}")
        else:
            print('Entra al else ')
            self.print_symbols_table()
            if isinstance(expr, str) and expr in self.symbols_table:
                print('El value en la tabla de simbolos es ', self.symbols_table[expr]['value'])
                return float(self.symbols_table[expr]['value'])
            return float(expr)

    def visit_print(self, node):
        _, arguments = node
        output = ""
        for arg in arguments:
            if arg in self.symbols_table:
                output += str(self.symbols_table[arg]['value'])
            else:
                output += str(arg.replace('"', ''))
        print(output)

    def visit_function_call(self, node):
        _, function_name, arguments = node
        before_scope = self.current_scope
        self.current_scope = function_name
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
            if self.symbols_table[param_name]['type'] == 'parameter':
                if arguments[i] not in self.symbols_table:
                    print('El arugumento en la posicion ', i, ' es : ', arguments[i])
                    self.symbols_table[param_name]['value'] = arguments[i]
                else:
                    print('entra al de symbols table')
                    self.symbols_table[param_name]['value'] = self.symbols_table[arguments[i]]['value']

        executed_function_body = self.execute_body(body)
        self.current_scope = before_scope
        return executed_function_body

    def visit_if(self, node):
        _, condition, body = node
        if self.evaluate_condition(condition):
            self.execute_body(body)

    def visit_while(self, node):
        _, condition, body = node
        while self.evaluate_condition(condition):
            self.execute_body(body)

    def visit_for(self, node):
        _, loop_data, body = node
        init, condition, increment = loop_data.values()
        self.symbols_table[init[0]] = int(init[2])
        while self.evaluate_condition(condition):
            self.execute_body(body)
            self.update_increment(increment)

    def visit_return(self, node):
        _, value = node
        if value in self.symbols_table:
            return self.symbols_table[value]['value']
        return value

    def execute_body(self, body):
        _, statements = body
        print(f'Los statements son {statements}')
        for statement in statements:
            result = self.visit(statement)
            if result is not None:
                return result

    def evaluate_condition(self, condition):
        print('El input uno es ', condition[1])
        if condition[0] == 'comparison':
            left, operator, right = condition[1:] #el 1: indica que va a agarrar todos los elementos desde el 1
            left_value = self.symbols_table[left]['value']
            right_value = self.symbols_table[right]['value']
            print('El valor izquierdo es ', left_value)
            print('El valor derecho es ', right_value)
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

    def update_increment(self, increment):
        var, op, value = increment
        if op == '++':
            self.symbols_table[var] += 1
        elif op == '--':
            self.symbols_table[var] -= 1
        elif op == '=':
            self.symbols_table[var] = value

    def visit_else(self, body):
        _, body = body
        self.execute_body(body)
