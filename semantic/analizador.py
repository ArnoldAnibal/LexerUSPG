# semantic/analizador.py
from semantic.tabla_simbolos import TablaSimbolos

class AnalizadorSemantico:
    def __init__(self):
        self.tabla = TablaSimbolos()

    def visitar(self, nodo):
        nombre_metodo = f'visitar_{type(nodo).__name__}'
        visitador = getattr(self, nombre_metodo, self.visitar_generico)
        return visitador(nodo)

    def visitar_generico(self, nodo):
        raise Exception(f"No se encontró un método de visita para {type(nodo).__name__}")

    # TODO 1: Validar el programa global
    def visitar_Program(self, nodo):
        for sentencia in nodo.statements:
            self.visitar(sentencia)
        print("[Semántica] Análisis semántico completado sin errores.")

    # TODO 2: Validar declaraciones de variables (con o sin inicialización)
    def visitar_Declaration(self, nodo):
        # nodo.tipo, nodo.id, nodo.expr
        tipo_expr = None
        if nodo.expr:
            tipo_expr = self.visitar(nodo.expr)
            # Validación básica de compatibilidad de tipos en asignación inicial
            if nodo.tipo != tipo_expr and not (nodo.tipo == 'decimal' and tipo_expr == 'entero'):
                raise Exception(f"[Error Semántico] Tipo incompatible en declaración de '{nodo.id}': se esperaba '{nodo.tipo}' pero se asignó '{tipo_expr}'.")
        
        self.tabla.declarar(nodo.id, nodo.tipo)

    # TODO 3: Validar asignaciones (normal y asignación compuesta de tu extensión)
    def visitar_Assignment(self, nodo):
        # nodo.id, nodo.expr, nodo.op (=, +=, etc.)
        tipo_var = self.tabla.buscar(nodo.id)
        tipo_expr = self.visitar(nodo.expr)

        # Permite asignación flexible si es decimal con entero, o booleano exacto
        if tipo_var != tipo_expr and not (tipo_var == 'decimal' and tipo_expr == 'entero'):
            raise Exception(f"[Error Semántico] Tipo incompatible en asignación a '{nodo.id}': variable es '{tipo_var}' y expresión es '{tipo_expr}'.")

        if tipo_var != tipo_expr and not (tipo_var == 'decimal' and tipo_expr == 'entero'):
            raise Exception(f"[Error Semántico] Tipo incompatible en asignación a '{nodo.id}': variable es '{tipo_var}' y expresión es '{tipo_expr}'.")

    # TODO 4: Validar el uso de variables en expresiones
    def visitar_Variable(self, nodo):
        # nodo.name
        return self.tabla.buscar(nodo.name)

    # TODO 5: Validar literales y operaciones binarias (tipos y compatibilidad aritmética/relacional)
    def visitar_Number(self, nodo):
        # Valida si el valor es booleano, decimal o entero
        val_str = str(nodo.value)
        if val_str in ('verdadero', 'falso', 'True', 'False'):
            return 'booleano'
        if '.' in val_str:
            return 'decimal'
        return 'entero'

    def visitar_BinOp(self, nodo):
        tipo_izq = self.visitar(nodo.left)
        tipo_der = self.visitar(nodo.right)

        # Operadores relacionales devuelven booleano (o se validan)
        if nodo.op in ('==', '!=', '<', '>', '<=', '>='):
            return 'booleano'

        # Operadores aritméticos
        if tipo_izq == 'cadena' or tipo_der == 'cadena':
            raise Exception("[Error Semántico] Operación aritmética no permitida con cadenas.")
        
        if tipo_izq == 'decimal' or tipo_der == 'decimal':
            return 'decimal'
        
        return 'entero'

    # TODO 6: Validar condiciones en estructuras de control (si, mientras)
    def visitar_IfStatement(self, nodo):
        tipo_cond = self.visitar(nodo.condition)
        if tipo_cond != 'booleano':
            raise Exception(f"[Error Semántico] La condición del 'si' debe ser de tipo booleano, se obtuvo '{tipo_cond}'.")
        for stmt in nodo.body:
            self.visitar(stmt)

    def visitar_WhileStatement(self, nodo):
        tipo_cond = self.visitar(nodo.condition)
        if tipo_cond != 'booleano':
            raise Exception(f"[Error Semántico] La condición del 'mientras' debe ser de tipo booleano, se obtuvo '{tipo_cond}'.")
        for stmt in nodo.body:
            self.visitar(stmt)

    def visitar_PrintStatement(self, nodo):
        self.visitar(nodo.expr)