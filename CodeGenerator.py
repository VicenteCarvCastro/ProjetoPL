"""
Code generator for Pascal to Stack-Based Assembly
"""

class CodeGenerator:
    def __init__(self):
        self.code = []          # List to store generated assembly code
        self.data_section = []  # For constants and static data
        self.temp_counter = 0   # Counter for temporary variables
        self.label_counter = 0  # Counter for labels
        self.symbols = {}       # Symbol table for variables
        self.current_scope = "global"  # Track current scope
        self.scopes = {"global": {}}   # Track all scopes
        self.string_counter = 0 # Counter for string constants
        
    def generate(self, ast):
        """Main entry point for code generation"""
        self._generate_program(ast)
        return self._format_output()
    
    def _format_output(self):
        """Format the final assembly output"""
        # Add START instruction at the beginning
        output = ["START"]
        
        # Add string constant declarations
        if self.data_section:
            output.append("// String Constants")
            output.extend(self.data_section)
            output.append("")
        
        # Add main code
        output.extend(self.code)
        
        # Add STOP at the end
        output.append("STOP")
        
        return "\n".join(output)
    
    def _generate_program(self, node):
        """Generate code for the program node"""
        if node[0] == "programa":
            _, cabecalho, corpo = node
            self._generate_cabecalho(cabecalho)
            self._generate_corpo(corpo)
    
    def _generate_cabecalho(self, node):
        """Generate code for program header"""
        _, titulo, funcoes, declaracoes = node
        
        # Add comment with program title
        self.code.append(f"// Program: {titulo}")
        self.code.append("")
        
        # Process global variable declarations
        # For stack-based assembly, we'll allocate space in global memory (GP section)
        global_offset = 0
        for declaracao in declaracoes:
            if declaracao[0] == "declaracao":
                _, var_list, tipo = declaracao
                for var_name in var_list:
                    # Add variable to symbol table
                    self.symbols[var_name] = {
                        "type": tipo,
                        "scope": "global",
                        "offset": global_offset
                    }
                    global_offset += 1  # Each variable takes 1 cell in our simplified model
                    
                    # Initialize variable to zero 
                    self.code.append(f"// Initialize global variable {var_name}")
                    self.code.append("PUSHI 0")
                    self.code.append(f"STOREG {self.symbols[var_name]['offset']}")
        
        if declaracoes:
            self.code.append("")  # Add blank line after declarations
            
        # Process function declarations
        for funcao in funcoes:
            self._process_function(funcao)
    
    def _process_function(self, func_node):
        """Process function declarations"""
        if func_node[0] == "funcao":
            _, name, params, ret_type, block, _ = func_node
            
            # Create new scope for function
            old_scope = self.current_scope
            self.current_scope = name
            self.scopes[name] = {}
            
            # Generate function label
            self.code.append(f"// Function: {name}")
            self.code.append(f"{name}:")
            
            # Process function body
            self._generate_bloco_funcao(block)
            
            # Return from function
            self.code.append("RETURN")
            self.code.append("")  # Add blank line after function
            
            # Restore scope
            self.current_scope = old_scope
    
    def _generate_bloco_funcao(self, node):
        """Generate code for function block"""
        if node[0] == "bloco_funcao":
            _, declaracoes, corpo = node
            
            # Process local variable declarations
            local_offset = 0
            for declaracao in declaracoes:
                if declaracao[0] == "declaracao":
                    _, var_list, tipo = declaracao
                    for var_name in var_list:
                        # Add to symbol table with offset
                        self.symbols[var_name] = {
                            "type": tipo,
                            "scope": self.current_scope,
                            "is_local": True,
                            "offset": local_offset
                        }
                        self.scopes[self.current_scope][var_name] = self.symbols[var_name]
                        local_offset += 1
                        
                        # Initialize local variable to zero
                        self.code.append(f"// Initialize local variable {var_name}")
                        self.code.append("PUSHI 0")
                        self.code.append(f"STOREL {self.symbols[var_name]['offset']}")
            
            if declaracoes:
                self.code.append("")  # Add blank line after declarations
                
            # Generate code for function body
            self._generate_corpo(corpo)
    
    def _generate_corpo(self, node):
        """Generate code for program body"""
        if node[0] == "corpo":
            _, instrucoes = node
            for instrucao in instrucoes:
                self._generate_instrucao(instrucao)
    
    def _generate_instrucao(self, node):
        """Generate code for an instruction"""
        if node is None or node[0] == "vazio":
            return
            
        if node[0] == "atribuicao":
            self._generate_atribuicao(node)
        elif node[0] == "atribuicao_array":
            self._generate_atribuicao_array(node)
        elif node[0] == "read" or node[0] == "readln":
            self._generate_read(node)
        elif node[0] == "write" or node[0] == "writeln":
            self._generate_write(node)
        elif node[0] == "if":
            self._generate_if(node)
        elif node[0] == "if-else":
            self._generate_if_else(node)
        elif node[0] == "while":
            self._generate_while(node)
        elif node[0] == "for-to":
            self._generate_for_to(node)
        elif node[0] == "for-downto":
            self._generate_for_downto(node)
        elif node[0] == "bloco":
            self._generate_bloco(node)
        # Add other instruction types as needed
    
    def _generate_atribuicao(self, node):
        """Generate code for assignment"""
        _, var_name, expr = node
        
        self.code.append(f"// Assignment: {var_name} = expression")
        
        # Generate code for expression, result will be on top of stack
        self._generate_expressao(expr)
        
        # Store result in variable
        if var_name in self.symbols:
            var_info = self.symbols[var_name]
            if var_info.get("is_local", False):
                # Local variable 
                self.code.append(f"STOREL {var_info['offset']}")
            else:
                # Global variable
                self.code.append(f"STOREG {var_info['offset']}")
        else:
            # Error: variable not declared
            raise Exception(f"Variable {var_name} not declared")
    
    def _generate_atribuicao_array(self, node):
        """Generate code for array assignment"""
        _, array_name, index_expr, value_expr = node
        
        self.code.append(f"// Array assignment: {array_name}[index] = value")
        
        # For array access, we need:
        # 1. Base address of the array
        # 2. Index value
        # 3. Value to store
        
        # Get base address of array 
        if array_name in self.symbols:
            var_info = self.symbols[array_name]
            if var_info.get("is_local", False):
                self.code.append(f"PUSHFP")  # Push frame pointer
                self.code.append(f"PUSHI {var_info['offset']}")  # Push offset
                self.code.append("PADD")  # Calculate address: FP + offset
            else:
                self.code.append(f"PUSHGP")  # Push global pointer
                self.code.append(f"PUSHI {var_info['offset']}")  # Push offset
                self.code.append("PADD")  # Calculate address: GP + offset
        else:
            raise Exception(f"Array {array_name} not declared")
        
        # Calculate index offset
        self._generate_expressao(index_expr)
        
        # Calculate element address: base_addr + index
        self.code.append("PADD")  # Add index to base address
        
        # Generate value to store
        self._generate_expressao(value_expr)
        
        # Store value at calculated address
        self.code.append("STORE 0")  # Store value at address
    
    def _generate_if(self, node):
        """Generate code for if statement"""
        _, condition, then_block = node
        
        end_label = self._new_label("endif")
        
        self.code.append("// IF statement")
        
        # Generate code for condition
        self._generate_expressao(condition)
        
        # Jump to end if condition is false (0)
        self.code.append(f"JZ {end_label}")
        
        # Generate then block
        self._generate_instrucao(then_block)
        
        # End label
        self.code.append(f"{end_label}:")
    
    def _generate_if_else(self, node):
        """Generate code for if-else statement"""
        _, condition, then_block, else_block = node
        
        else_label = self._new_label("else")
        end_label = self._new_label("endif")
        
        self.code.append("// IF-ELSE statement")
        
        # Generate code for condition
        self._generate_expressao(condition)
        
        # Jump to else if condition is false (0)
        self.code.append(f"JZ {else_label}")
        
        # Generate then block
        self._generate_instrucao(then_block)
        
        # Jump to end (skip else block)
        self.code.append(f"JUMP {end_label}")
        
        # Else block
        self.code.append(f"{else_label}:")
        self._generate_instrucao(else_block)
        
        # End label
        self.code.append(f"{end_label}:")
    
    def _generate_while(self, node):
        """Generate code for while loop"""
        _, condition, body = node
        
        start_label = self._new_label("whilestart")
        end_label = self._new_label("whileend")
        
        self.code.append("// WHILE loop")
        
        # Start label
        self.code.append(f"{start_label}:")
        
        # Generate code for condition
        self._generate_expressao(condition)
        
        # Jump to end if condition is false (0)
        self.code.append(f"JZ {end_label}")
        
        # Generate body
        self._generate_instrucao(body)
        
        # Jump back to start
        self.code.append(f"JUMP {start_label}")
        
        # End label
        self.code.append(f"{end_label}:")
    
    def _generate_for_to(self, node):
        """Generate code for for-to loop"""
        _, var_name, start_expr, end_expr, body = node
        
        start_label = self._new_label("forstart")
        end_label = self._new_label("forend")
        
        self.code.append(f"// FOR-TO loop: {var_name}")
        
        # Check if variable exists
        if var_name not in self.symbols:
            raise Exception(f"Variable {var_name} not declared")
        
        var_info = self.symbols[var_name]
        
        # Initialize counter variable with start expression
        self._generate_expressao(start_expr)
        
        # Store initial value in counter variable
        if var_info.get("is_local", False):
            self.code.append(f"STOREL {var_info['offset']}")
        else:
            self.code.append(f"STOREG {var_info['offset']}")
        
        # Generate end expression and store temporarily
        self._generate_expressao(end_expr)
        temp_var = self._new_temp()
        temp_offset = len(self.scopes[self.current_scope])
        
        # Store loop limit in temporary variable
        if self.current_scope == "global":
            self.code.append(f"STOREG {temp_offset}")
        else:
            self.code.append(f"STOREL {temp_offset}")
        
        # Start of loop
        self.code.append(f"{start_label}:")
        
        # Compare counter with end value
        # Load counter variable
        if var_info.get("is_local", False):
            self.code.append(f"PUSHL {var_info['offset']}")
        else:
            self.code.append(f"PUSHG {var_info['offset']}")
        
        # Load end value
        if self.current_scope == "global":
            self.code.append(f"PUSHG {temp_offset}")
        else:
            self.code.append(f"PUSHL {temp_offset}")
        
        # Compare counter <= end value
        self.code.append("INFEQ")
        
        # If counter > end value, exit loop
        self.code.append(f"JZ {end_label}")
        
        # Generate loop body
        self._generate_instrucao(body)
        
        # Increment counter
        if var_info.get("is_local", False):
            self.code.append(f"PUSHL {var_info['offset']}")
        else:
            self.code.append(f"PUSHG {var_info['offset']}")
        
        self.code.append("PUSHI 1")
        self.code.append("ADD")
        
        # Store incremented value back to counter
        if var_info.get("is_local", False):
            self.code.append(f"STOREL {var_info['offset']}")
        else:
            self.code.append(f"STOREG {var_info['offset']}")
        
        # Jump back to start
        self.code.append(f"JUMP {start_label}")
        
        # End label
        self.code.append(f"{end_label}:")
    
    def _generate_for_downto(self, node):
        """Generate code for for-downto loop"""
        _, var_name, start_expr, end_expr, body = node
        
        start_label = self._new_label("for_start")
        end_label = self._new_label("for_end")
        
        self.code.append(f"// FOR-DOWNTO loop: {var_name}")
        
        # Check if variable exists
        if var_name not in self.symbols:
            raise Exception(f"Variable {var_name} not declared")
            
        var_info = self.symbols[var_name]
        
        # Initialize counter variable with start expression
        self._generate_expressao(start_expr)
        
        # Store initial value in counter variable
        if var_info.get("is_local", False):
            self.code.append(f"STOREL {var_info['offset']}")
        else:
            self.code.append(f"STOREG {var_info['offset']}")
        
        # Generate end expression and store temporarily
        self._generate_expressao(end_expr)
        temp_var = self._new_temp()
        temp_offset = len(self.scopes[self.current_scope])
        
        # Store loop limit in temporary variable
        if self.current_scope == "global":
            self.code.append(f"STOREG {temp_offset}")
        else:
            self.code.append(f"STOREL {temp_offset}")
        
        # Start of loop
        self.code.append(f"{start_label}:")
        
        # Compare counter with end value
        # Load counter variable
        if var_info.get("is_local", False):
            self.code.append(f"PUSHL {var_info['offset']}")
        else:
            self.code.append(f"PUSHG {var_info['offset']}")
        
        # Load end value
        if self.current_scope == "global":
            self.code.append(f"PUSHG {temp_offset}")
        else:
            self.code.append(f"PUSHL {temp_offset}")
        
        # Compare counter >= end value
        self.code.append("SUPEQ")
        
        # If counter < end value, exit loop
        self.code.append(f"JZ {end_label}")
        
        # Generate loop body
        self._generate_instrucao(body)
        
        # Decrement counter
        if var_info.get("is_local", False):
            self.code.append(f"PUSHL {var_info['offset']}")
        else:
            self.code.append(f"PUSHG {var_info['offset']}")
        
        self.code.append("PUSHI 1")
        self.code.append("SUB")
        
        # Store decremented value back to counter
        if var_info.get("is_local", False):
            self.code.append(f"STOREL {var_info['offset']}")
        else:
            self.code.append(f"STOREG {var_info['offset']}")
        
        # Jump back to start
        self.code.append(f"JUMP {start_label}")
        
        # End label
        self.code.append(f"{end_label}:")
    
    def _generate_bloco(self, node):
        """Generate code for a block"""
        _, instrucoes = node
        self.code.append("// Block of instructions")
        
        for instrucao in instrucoes:
            self._generate_instrucao(instrucao)
    
    def _generate_read(self, node):
        """Generate code for read statement"""
        _, var_name = node
        
        self.code.append(f"// Read into {var_name}")
        
        # Check if variable exists
        if var_name not in self.symbols:
            raise Exception(f"Variable {var_name} not declared")
            
        var_info = self.symbols[var_name]
        
        # Read input
        self.code.append("READ")  # Reads a string from keyboard
        
        # Convert to appropriate type based on variable type
        if var_info["type"] == "integer":
            self.code.append("ATOI")  # Convert string to integer
        elif var_info["type"] == "real":
            self.code.append("ATOF")  # Convert string to float
        
        # Store to variable
        if var_info.get("is_local", False):
            self.code.append(f"STOREL {var_info['offset']}")
        else:
            self.code.append(f"STOREG {var_info['offset']}")
    
    def _generate_write(self, node):
        """Generate code for write statement"""
        _, expr_list = node
        
        self.code.append("// Write statement")
        
        for expr in expr_list:
            # Generate code for expression
            self._generate_expressao(expr)
            
            # Write based on type
            if isinstance(expr, str) and expr.startswith("'"):
                # It's a string literal
                self.code.append("WRITES")
            elif isinstance(expr, str) and expr in self.symbols:
                # Variable - check its type
                var_type = self.symbols[expr]["type"]
                if var_type == "integer":
                    self.code.append("WRITEI")
                elif var_type == "real":
                    self.code.append("WRITEF")
                elif var_type == "string":
                    self.code.append("WRITES")
                elif var_type == "char":
                    self.code.append("WRITECHR")
            else:
                # Default to integer for numeric literals and expressions
                self.code.append("WRITEI")
        
        # Add newline for writeln
        if node[0] == "writeln":
            self.code.append("WRITELN")
    
    def _generate_expressao(self, node):
        """Generate code for an expression"""
        if isinstance(node, int):
            # Literal integer
            self.code.append(f"PUSHI {node}")
        elif isinstance(node, float):
            # Literal float
            self.code.append(f"PUSHF {node}")
        elif isinstance(node, str) and node.startswith("'"):
            # String literal - remove quotes and add to string heap
            string_content = node[1:-1]
            string_label = f"str_{self.string_counter}"
            self.string_counter += 1
            
            # Add string to data section
            self.data_section.append(f"// String: {string_content}")
            self.code.append(f"PUSHS \"{string_content}\"")
        elif isinstance(node, str):
            # Variable
            if node in self.symbols:
                var_info = self.symbols[node]
                if var_info.get("is_local", False):
                    self.code.append(f"PUSHL {var_info['offset']}")
                else:
                    self.code.append(f"PUSHG {var_info['offset']}")
            else:
                # Assume it's a string constant if not a variable
                self.code.append(f"PUSHS \"{node}\"")
        elif isinstance(node, bool):
            # Boolean literal
            self.code.append(f"PUSHI {1 if node else 0}")
        elif isinstance(node, tuple):
            # Expression with operator
            if node[0] == "+":
                self._generate_expressao(node[1])
                self._generate_expressao(node[2])
                self.code.append("ADD")
            elif node[0] == "-":
                self._generate_expressao(node[1])
                self._generate_expressao(node[2])
                self.code.append("SUB")
            elif node[0] == "*":
                self._generate_expressao(node[1])
                self._generate_expressao(node[2])
                self.code.append("MUL")
            elif node[0] == "/":
                self._generate_expressao(node[1])
                self._generate_expressao(node[2])
                self.code.append("DIV")
            elif node[0] == "div":
                self._generate_expressao(node[1])
                self._generate_expressao(node[2])
                self.code.append("DIV")  # Integer division
            elif node[0] == "mod":
                self._generate_expressao(node[1])
                self._generate_expressao(node[2])
                self.code.append("MOD")
            elif node[0] == "relop":
                op, left, right = node[1], node[2], node[3]
                self._generate_expressao(left)
                self._generate_expressao(right)
                
                if op == "=":
                    self.code.append("EQUAL")
                elif op == "<>":
                    self.code.append("EQUAL")
                    self.code.append("NOT")  # Invert the result
                elif op == "<":
                    self.code.append("INF")
                elif op == "<=":
                    self.code.append("INFEQ")
                elif op == ">":
                    self.code.append("SUP")
                elif op == ">=":
                    self.code.append("SUPEQ")
            elif node[0] == "and":
                self._generate_expressao(node[1])
                self._generate_expressao(node[2])
                self.code.append("AND")
            elif node[0] == "or":
                self._generate_expressao(node[1])
                self._generate_expressao(node[2])
                self.code.append("OR")
            elif node[0] == "not":
                self._generate_expressao(node[1])
                self.code.append("NOT")
            elif node[0] == "menos":
                # Unary minus
                self.code.append("PUSHI 0")  # Push 0
                self._generate_expressao(node[1])  # Push the value
                self.code.append("SUB")  # 0 - value = -value
            elif node[0] == "array_acesso":
                array_name, index_expr = node[1], node[2]
                
                # Get base address
                if array_name in self.symbols:
                    var_info = self.symbols[array_name]
                    if var_info.get("is_local", False):
                        self.code.append(f"PUSHFP")  # Push frame pointer
                        self.code.append(f"PUSHI {var_info['offset']}")  # Push offset
                        self.code.append("PADD")  # Calculate address: FP + offset
                    else:
                        self.code.append(f"PUSHGP")  # Push global pointer
                        self.code.append(f"PUSHI {var_info['offset']}")  # Push offset
                        self.code.append("PADD")  # Calculate address: GP + offset
                else:
                    raise Exception(f"Array {array_name} not declared")
                
                # Calculate index offset
                self._generate_expressao(index_expr)
                
                # Calculate element address: base_addr + index
                self.code.append("PADD")  # Add index to base address
                
                # Load value at calculated address
                self.code.append("LOAD 0")  # Load value from address
            elif node[0] == "call":
                func_name, args = node[1], node[2:]
                
                # Push arguments in reverse order
                for arg in reversed(args):
                    self._generate_expressao(arg)
                
                # Call function by stacking its address then using CALL
                self.code.append(f"PUSHA {func_name}")
                self.code.append("CALL")
            else:
                # Unknown operator
                raise Exception(f"Unknown operator {node[0]}")
    
    def _new_temp(self):
        """Generate a new temporary variable name"""
        self.temp_counter += 1
        return f"t{self.temp_counter}"
    
    def _new_label(self, prefix="L"):
        """Generate a new label"""
        self.label_counter += 1
        return f"{prefix}_{self.label_counter}"

# Example usage
if __name__ == "__main__":
    # Example AST (simplified)
    ast = ("programa", 
           ("cabecalho", 
            ("titulo", "hello"), 
            [], 
            [("declaracao", ["x"], "integer")]), 
           ("corpo", 
            [("atribuicao", "x", 42), 
             ("write", [("x",)])]))
    
    generator = CodeGenerator()
    assembly = generator.generate(ast)
    print(assembly)