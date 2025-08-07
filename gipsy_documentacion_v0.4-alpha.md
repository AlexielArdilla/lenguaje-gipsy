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

### `Use` en transpilación
```
Use Math
Say Math.sqrt(9)
```
Genera Python con un `try/except ImportError` que intenta `import Math` y, si falla, `import math`, exponiendo el alias `Math`.
