<p style= "text-align=center">
  <img src="Gipsy_logo_banner.png" alt="Gipsy Logo" width="1080">
</p>

# 📘 Documentación Oficial – Gipsy v0.3

---

## ✨ ¿Qué es Gipsy?

**Gipsy** es un lenguaje de programación inspirado en Python, diseñado para ser más natural, expresivo y tolerante. Ideal para educación, scripting y pensamiento computacional.

---

## 🧠 Características Principales

- ✅ Sintaxis natural: `Say`, `Ask`, `Use`, `function`, `end`, etc.
- ✅ Tolerancia a indentación (usa `end` para cerrar bloques)
- ✅ Comentarios multilínea con `###`
- ✅ Importación de librerías (`Use math`)
- ✅ Tipado dinámico con `typeof`
- ✅ Soporte para listas, diccionarios y sus métodos
- ✅ Funciones anónimas tipo `fun(x) return x + 1 end`

---

## 🔤 Palabras Clave

```
Say, Ask, Use, function, return, if, else, while, loop, end, typeof, fun
```

---

## 📋 Sintaxis y Ejemplos

### Comentarios Multilínea

```gipsy
### Esto es un comentario
    que puede ocupar varias líneas
###
```

---

### Importar librerías

```gipsy
Use math
Say math.sqrt(16)
```

---

### Entrada y salida

```gipsy
nombre = Ask "¿Tu nombre?"
Say "Hola, " + nombre
```

---

### Funciones

```gipsy
function saludar(nombre)
    Say "Hola, " + nombre
end

saludar("Alex")
```

---

### Funciones anónimas

```gipsy
doble = fun(x) return x * 2 end
Say doble(5)
```

---

### Condicionales

```gipsy
if edad >= 18
    Say "Adulto"
else
    Say "Menor"
end
```

---

### Bucles

```gipsy
loop 3 times
    Say "Hola"
end

x = 0
while x < 3
    Say x
    x = x + 1
end
```

---

### Tipos dinámicos

```gipsy
x = 42
Say typeof x  # → "number"
```

---

### Listas y diccionarios

```gipsy
lista = [1, 2, 3]
lista.append(4)
Say lista[2]

dic = { "nombre": "Gipsy", "edad": 3 }
Say dic["nombre"]
```

---

## 🚀 Cómo Ejecutar

### Intérprete

```bash
python gipsy_repl_v0.3.py
```

### Transpilador

```bash
python gipsy_transpiler_v0.3_lambda.py archivo.gipsy archivo.py
python archivo.py
```

---

## 📦 Archivos incluidos

| Archivo | Descripción |
|--------|-------------|
| [`gipsy_repl_v0.3.py`](./gipsy_repl_v0.3.py) | Intérprete interactivo de Gipsy |
| [`gipsy_transpiler_v0.3_lambda.py`](./gipsy_transpiler_v0.3_lambda.py) | Transpilador Gipsy → Python |
| [`examples/*.gipsy`](./examples) | Archivos fuente en Gipsy con ejemplos |
| [`gipsy_documentacion_v0.3.md`](./gipsy_documentacion_v0.3.md) | Documentación técnica |

---

## 🔮 Próxima versión (v0.4)

- Tipado estático opcional
- Funciones anidadas
- `match` / `case` estructurado
- Módulos de usuario
- Editor online para probar Gipsy

---

## 🧑‍💻 Autor

**Gipsy** fue creado por Alejandro Gonzalo Vera, desarrollado junto a un sistema de IA para explorar nuevas formas de enseñar y programar.

---

## 🗓️ Última actualización

**Versión:** v0.3  
**Fecha:** 7 de Agosto 2025 4:22 AM
----------------------------------------------

----------------------------------------------
# 📘 Gipsy v0.4-alpha — Notas de versión

> **Estado:** Alpha. Enfocado en *Const*, `include`, guardia de *stack* y trazas en español.

## ✅ Novedades clave
- **Const**: declara inmutables a nivel de entorno global. Ej.: `Const PI = 3.14159`.
- **include "archivo.gipsy"**: ejecuta otro archivo de Gipsy antes de continuar.
- **Guardia de profundidad de llamadas**: error controlado de *StackOverflow* con traza en español.
- **Mensajes/errores en español**: `Variable no definida`, `Sentencia no reconocida`, etc.

## 🧠 Lo que ya funciona
- `Say expr`, `Ask "msg" [as number]`
- Variables, asignación simple `x = expr`
- `typeof x` (como builtin)
- `function nombre(args) ... end`, `return`
- `if ... end`, `else ... end`
- `while ... end`
- `loop N times ... end`
- Comentarios multilínea con `###` y de línea con `//`

## 🧪 Ejemplos

### Const e include
```
Const GREETING = "Hola"
include "lib.gipsy"
Say GREETING + ", " + nombre()
```

`lib.gipsy`:
```
function nombre()
    return "Gipsy"
end
```

### StackOverflow controlado
```
function f(n)
    return f(n + 1)
end

f(0)
```
**Salida (ejemplo):**
```
  Archivo "<repl>", línea 3, en f
  Archivo "<repl>", línea 3, en f
  ...
Desbordamiento de pila al llamar a 'f'. Se superó el máximo de 1000 niveles.
```

### Control de entrada
```
edad = Ask "¿Edad?" as number
if edad >= 18
    Say "OK adulto"
else
    Say "Menor"
end
```

## 🚀 Transpilación (mínima)
Uso:
```
python gipsy_transpiler_v0.4_alpha.py ejemplo.gipsy out.py
python out.py
```

## 📌 Limitaciones (alpha)
- El *parser* es lineal (por líneas) y no maneja expresiones con comas anidadas complejas en llamadas.
- No hay *pattern matching* ni `try/catch` aún (planeado para beta).
- Las constantes son globales en esta versión.
- Tipado opcional no está incluido en esta *alpha* (podemos añadirlo luego).

---

¿Feedback o algo que priorizar? Lo iteramos rápido para la beta. ✨


### Importar módulos con `Use`
```
Use Math
Say Math.sqrt(16)
Use random as R
Say R.randint(1, 6)
```
