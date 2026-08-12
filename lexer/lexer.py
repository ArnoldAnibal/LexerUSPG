import re
from .token import Token
from typing import List


class Lexer:

    def __init__(self, codigo_fuente: str):

        self.codigo = codigo_fuente
        self.tokens: List[Token] = []

        # ESQUEMA DE TOKENS (El orden de coincidencia es fundamental)
        self.esquema_tokens = [
            # 1. Comentarios (Se deben definir antes para que no se confundan con operadores de división /)
            ('COM_BLOQUE',   r'/\*[\s\S]*?\*/'),
            ('COM_LINEA',    r'//.*'),

            # 2. Palabras Reservadas (Con \b para límite de palabra exacta)
            ('PR_ENTERO',    r'\bentero\b'),
            ('PR_DECIMAL',   r'\bdecimal\b'),
            ('PR_CADENA',    r'\bcadena\b'),
            ('PR_BOOL',      r'\bbooleano\b'),
            ('PR_SI',        r'\bsi\b'),
            ('PR_SINO',      r'\bsino\b'),
            ('PR_MIENTRAS',  r'\bmientras\b'),
            ('PR_PARA',      r'\bpara\b'),
            ('PR_IMPRIMIR',  r'\bimprimir\b'),
            ('PR_FUNCION',   r'\bfuncion\b'),
            ('PR_RETORNAR',  r'\bretornar\b'),
            ('LIT_BOOLEANO', r'\b(verdadero|falso)\b'),

            # 3. Literales y Cadenas de Texto
            ('LIT_CADENA',   r'"[^"\n]*"'),
            ('NUM_DECIMAL',  r'\d+\.\d+'),    # Debe ir antes de NUMERO
            ('NUMERO',       r'\d+'),

            # 4. Operadores Compuestos de Múltiples Caracteres (Deben evaluarse antes de los individuales)
            ('OP_INC_DEC',   r'\+\+|--'),
            ('OP_ASIG_COMP', r'\+=|-=|\*=|/='),
            ('OP_REL',       r'==|!=|<=|>=|<|>'),
            ('OP_LOGICO',    r'&&|\|\||!'),

            # 5. Operadores Simples y Asignación
            ('ASIGNACION',   r'='),
            ('OP_MODULO',    r'%'),
            ('OP_POTENCIA',  r'\^'),
            ('OP_ARIT',      r'[+\-*/]'),

            # 6. Identificadores (Nombres de variables y funciones)
            ('ID',           r'[a-zA-Z_][a-zA-Z0-9_]*'),

            # 7. Delimitadores y Puntuación
            ('DELIM',        r'[();{}]'),
            ('CORCHETES',    r'[\[\]]'),
            ('DOS_PUNTOS',   r':'),
            ('PUNTO',        r'\.'),

            # 8. Espacios, Salto de Línea y Errores
            ('ESPACIO',      r'[ \t]+'),
            ('NUEVA_LINEA',  r'\n'),
            ('ERROR',        r'.')
        ]

        self.regex_maestro = re.compile(
            '|'.join(
                f'(?P<{nombre}>{patron})'
                for nombre, patron in self.esquema_tokens
            )
        )


    def analizar(self) -> List[Token]:

        numero_linea = 1

        for match in self.regex_maestro.finditer(self.codigo):

            tipo = match.lastgroup
            valor = match.group()

            if tipo == 'NUEVA_LINEA':
                # Contar saltos de línea dentro de comentarios de bloque
                numero_linea += 1

            elif tipo == 'ESPACIO':
                continue

            elif tipo in ('COM_LINEA', 'COM_BLOQUE'):
                # Los comentarios incrementan número de línea si abarcan varias líneas
                numero_linea += valor.count('\n')
                continue

            elif tipo == 'ERROR':
                raise RuntimeError(
                    f"[Error Lexico] "
                    f"Caracter inesperado '{valor}' "
                    f"en linea {numero_linea}"
                )

            else:
                self.tokens.append(
                    Token(
                        tipo,
                        valor,
                        numero_linea
                    )
                )

        self.tokens.append(
            Token('EOF', '', numero_linea)
        )

        return self.tokens