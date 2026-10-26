# parser/ast.py

class Node:
    pass

class Program(Node):
    def __init__(self, statements):
        self.statements = statements

class Declaration(Node):
    def __init__(self, tipo, id, expr=None):
        self.tipo = tipo
        self.id = id
        self.expr = expr

class Assignment(Node):
    def __init__(self, id, expr, op="="):
        self.id = id
        self.expr = expr
        self.op = op  # Soporta asignación normal y compuesta (+=, -=, etc.)

class PrintStatement(Node):
    def __init__(self, expr):
        self.expr = expr

class BinOp(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Number(Node):
    def __init__(self, value):
        self.value = value

class Variable(Node):
    def __init__(self, name):
        self.name = name

class IfStatement(Node):
    def __init__(self, condition, body, else_body=None):
        self.condition = condition
        self.body = body
        self.else_body = else_body

class WhileStatement(Node):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body