class Program:
    def __init__(self, name, declarations, body):
        self.name = name
        self.declarations = declarations
        self.body = body

class VarDeclaration:
    def __init__(self, name, type):
        self.name = name
        self.type = type

class ConstDeclaration:
    def __init__(self, name, value):
        self.name = name
        self.value = value

class ArrayType:
    def __init__(self, lower, upper, type):
        self.lower = lower
        self.upper = upper
        self.type = type

class Body:
    def __init__(self, statements):
        self.statements = statements

class Assignment:
    def __init__(self, left, right):
        self.left = left
        self.right = right

class If:
    def __init__(self, condition, then_statement, else_statement):
        self.condition = condition
        self.then_statement = then_statement
        self.else_statement = else_statement

class While:
    def __init__(self, condition, statement):
        self.condition = condition
        self.statement = statement

class For:
    def __init__(self, variable, start, end, statement, direction):
        self.variable = variable
        self.start = start
        self.end = end
        self.statement = statement
        self.direction = direction

class Write:
    def __init__(self, command, expressions):
        self.command = command
        self.expressions = expressions

class Read:
    def __init__(self, command, variables):
        self.command = command
        self.variables = variables

class BinaryOperation:
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right