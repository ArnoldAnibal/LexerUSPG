# main.py
import sys
import os
from lexer.lexer import Lexer
from parser.parser import parser

class PLYTokenAdapter:
    """Adaptador para traducir los tokens del Lexer personalizado a los tipos esperados por PLY sin modificar el lexer."""
    def __init__(self, tokens_lista):
        self.tokens_iter = iter(tokens_lista)

    def token(self):
        try:
            t = next(self.tokens_iter)
            if t.tipo == 'EOF':
                return None
            
            class PlyObj:
                pass
            obj = PlyObj()
            obj.type = t.tipo
            obj.value = t.valor
            obj.linea = t.linea

            # Mapeo inteligente de DELIM según su valor real en el texto fuente
            if t.tipo == 'DELIM':
                if t.valor == '(': obj.type = 'LPAREN'
                elif t.valor == ')': obj.type = 'RPAREN'
                elif t.valor == ';': obj.type = 'SEMI'
                elif t.valor == '{': obj.type = 'LBRACE'
                elif t.valor == '}': obj.type = 'RBRACE'
            
            return obj
        except StopIteration:
            return None

def ejecutar_prueba(nombre_prueba, codigo):
    print("=" * 60)
    print(f"PROBANDO: {nombre_prueba}")
    print("=" * 60)
    print("[CÓDIGO FUENTE]")
    print(codigo)
    print("-" * 60)
    
    try:
        lexer_obj = Lexer(codigo)
        tokens_generados = lexer_obj.analizar()
        
        adapter = PLYTokenAdapter(tokens_generados)
        ast = parser.parse(lexer=adapter)
        
        if ast:
            print("¡ÉXITO! Análisis sintáctico completado y AST generado correctamente.\n")
        else:
            print("FALLO: No se generó el AST.\n")
    except Exception as e:
        print(f"EXCEPCIÓN ENCONTRADA: {e}\n")

def main():
    valido = """
entero x = 10;
entero limite = 20;

mientras (x <= limite) {
    si (x != 15) {
        imprimir x;
    }
    x = x + 2;
}
"""

    con_error = """
entero x
x = 10 + ;
"""

    extension = """
/* Comentario de bloque para extensión */
decimal pi;
booleano activo;
pi = 3.14;
activo = verdadero;
si (activo == verdadero) {
    pi += 1.0;
}
"""

    if len(sys.argv) > 1:
        ruta = sys.argv[1]
        if os.path.exists(ruta):
            with open(ruta, 'r', encoding='utf-8') as f:
                codigo = f.read()
            ejecutar_prueba(ruta, codigo)
        else:
            print(f"No se encontró el archivo: {ruta}")
    else:
        ejecutar_prueba("valido.txt", valido)
        ejecutar_prueba("error.txt", con_error)
        ejecutar_prueba("extension.txt", extension)

if __name__ == "__main__":
    main()