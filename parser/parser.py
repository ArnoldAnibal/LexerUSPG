# parser/parser.py
import ply.yacc as yacc
from parser.ast import *

tokens = [
    'PR_ENTERO', 'PR_DECIMAL', 'PR_CADENA', 'PR_BOOL',
    'PR_SI', 'PR_SINO', 'PR_MIENTRAS', 'PR_PARA', 'PR_IMPRIMIR',
    'PR_FUNCION', 'PR_RETORNAR',
    'ID', 'NUMERO', 'NUM_DECIMAL', 'LIT_CADENA', 'LIT_BOOLEANO',
    'ASIGNACION', 'OP_ARIT', 'OP_MODULO', 'OP_POTENCIA', 'OP_REL', 
    'OP_LOGICO', 'OP_ASIG_COMP', 'OP_INC_DEC',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'SEMI'
]

precedence = (
    ('left', 'OP_REL'),
    ('left', 'OP_ARIT'),
    ('left', 'OP_MODULO', 'OP_POTENCIA'),
)

def p_program(p):
    '''program : statement_list'''
    p[0] = Program(p[1])

def p_statement_list(p):
    '''statement_list : statement_list statement
                      | statement'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_statement(p):
    '''statement : declaration
                 | assignment
                 | if_stmt
                 | while_stmt
                 | print_stmt'''
    p[0] = p[1]

def p_declaration(p):
    '''declaration : tipo_dato ID SEMI
                   | tipo_dato ID ASIGNACION expression SEMI'''
    if len(p) == 4:
        p[0] = Declaration(p[1], p[2], None)
    else:
        p[0] = Declaration(p[1], p[2], p[4])

def p_tipo_dato(p):
    '''tipo_dato : PR_ENTERO
                 | PR_DECIMAL
                 | PR_CADENA
                 | PR_BOOL'''
    p[0] = p[1]

# --- MODIFICADO: Soporta asignación normal (=) y compuesta (+=, -=, etc.) ---
def p_assignment(p):
    '''assignment : ID ASIGNACION expression SEMI
                  | ID OP_ASIG_COMP expression SEMI'''
    p[0] = Assignment(p[1], p[3], p[2])
# --------------------------------------------------------------------------

def p_print_stmt(p):
    '''print_stmt : PR_IMPRIMIR expression SEMI'''
    p[0] = PrintStatement(p[2])

def p_expression_binop(p):
    '''expression : expression OP_ARIT expression
                  | expression OP_MODULO expression
                  | expression OP_POTENCIA expression
                  | expression OP_REL expression'''
    p[0] = BinOp(p[1], p[2], p[3])

def p_expression_group(p):
    '''expression : LPAREN expression RPAREN'''
    p[0] = p[2]

def p_expression_number(p):
    '''expression : NUMERO
                  | NUM_DECIMAL
                  | LIT_CADENA
                  | LIT_BOOLEANO'''
    p[0] = Number(p[1])

def p_expression_id(p):
    '''expression : ID'''
    p[0] = Variable(p[1])

def p_if_stmt(p):
    '''if_stmt : PR_SI LPAREN expression RPAREN LBRACE statement_list RBRACE'''
    p[0] = IfStatement(p[3], p[6])

def p_while_stmt(p):
    '''while_stmt : PR_MIENTRAS LPAREN expression RPAREN LBRACE statement_list RBRACE'''
    p[0] = WhileStatement(p[3], p[6])

def p_error(p):
    if p:
        print(f"[Error Sintáctico] Token inesperado '{p.value}' (tipo: {p.type}) en la línea {p.linea}")
    else:
        print("[Error Sintáctico] Fin de archivo inesperado (EOF)")

parser = yacc.yacc()