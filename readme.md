# Compilador Incremental — Entregas Lexer, Parser y Análisis Semántico

## Objetivo

Continuar el desarrollo del compilador incremental integrando las fases de **Análisis Léxico (Lexer)**, **Análisis Sintáctico (Parser & AST)** y **Análisis Semántico**, asegurando la validación lógica, de tipos y de declaraciones en el lenguaje fuente.

---

## Estructura del Proyecto

- `lexer/`: Contiene el analizador léxico y la definición de tokens.
- `parser/`: Contiene las clases de nodos del Árbol de Sintaxis Abstracta (`ast.py`) y las reglas gramaticales con PLY (`parser.py`).
- `semantic/`: Contiene la gestión de la tabla de símbolos y el analizador semántico con el patrón de recorrido de nodos.
- `tests/`: Archivos de código fuente para pruebas válidas, con errores y de extensión.
- `main.py`: Script principal de ejecución y orquestación de las pruebas.

---

## Implementación y Fases

### 1. Análisis Léxico (Lexer)
Reconocimiento de palabras reservadas (`entero`, `decimal`, `cadena`, `booleano`, `si`, `mientras`, `imprimir`, etc.), identificadores, literales numéricos, booleanos, cadenas, y operadores de múltiples caracteres (`OP_REL`, `OP_ASIG_COMP`, `OP_INC_DEC`).

### 2. Análisis Sintáctico (Parser & AST)
Integración mediante PLY (Python Lex-Yacc) para construir la jerarquía del Árbol de Sintaxis Abstracta reconociendo:
- Declaraciones (simples y con inicialización directa, ej. `entero x = 10;`).
- Asignaciones (normales y compuestas, ej. `pi += 1.0;`).
- Expresiones aritméticas y relacionales con precedencia.
- Estructuras de control (`si`, `mientras`).

### 3. Análisis Semántico y Tabla de Símbolos
Validación lógica del programa a través de un recorrido de AST que comprueba:
- Declaración única de variables por ámbito.
- Verificación de existencia de variables antes de su uso.
- Coherencia y compatibilidad de tipos (ej. asignaciones y operaciones aritméticas).
- Validación de que las condiciones en estructuras de control (`si`, `mientras`) retornen un valor booleano.

---

## Extensiones Personales

Este compilador incorpora las siguientes características y extensiones individuales documentadas:
- **Tipos de datos adicionales:** Soporte para tipos `decimal` y `booleano`.
- **Literales booleanos:** Reconocimiento de `verdadero` y `falso`.
- **Operador de asignación compuesta:** Soporte sintáctico y semántico para `+=` (y otros operadores compuestos).
- **Comentarios:** Omisión correcta de comentarios de línea (`//`) y de bloque (`/* ... */`) a nivel léxico.

---

## Pruebas y Evidencias de Ejecución

El compilador incluye pruebas automatizadas que se pueden ejecutar directamente desde la terminal mediante el script principal:

```bash
python main.py