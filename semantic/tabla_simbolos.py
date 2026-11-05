# semantic/tabla_simbolos.py

class TablaSimbolos:
    def __init__(self):
        self.tabla = {}  # Diccionario {nombre_variable: tipo}

    def declarar(self, nombre, tipo):
        if nombre in self.tabla:
            raise Exception(f"[Error Semántico] La variable '{nombre}' ya fue declarada previamente.")
        self.tabla[nombre] = tipo

    def buscar(self, nombre):
        if nombre in self.tabla:
            return self.tabla[nombre]
        raise Exception(f"[Error Semántico] Variable no declarada: '{nombre}'.")