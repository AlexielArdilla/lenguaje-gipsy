<p style= "text-align=center">
  <img src="Gipsy_logo_banner.png" alt="Gipsy Logo" width="1080">
</p>

# 📘 Gipsy v0.4-beta — Novedades

> **Estado:** Beta. Se agregan `match/case`, `try/catch` y `type alias`

## ✅ Nuevas features

### `match / case`
Sintaxis:
```
match x
    case 1
        Say "uno"
    case 2 or 3
        Say "dos o tres"
    else
        Say "otro"
end
```

- Compara por igualdad contra uno o varios patrones (separados por `or`).
- `else` es opcional.

### `try / catch`
```
try
    Say 1 / 0
catch e
    Say "Error: " + typeof e
end
```

- `catch` puede omitir variable: `catch` a secas.

### `type alias`
```
type alias Edad = number
type alias Texto = string
```
- En esta beta se **almacenan** los alias (no hay validación estricta todavía).

## REPL
- Compatible con todo lo anterior (Const, include, Use, Ask/Say, funciones, loops, while, if/else).
- Match/case y try/catch ejecutados en el runtime.

## Transpilador
- `match/case` → `if/elif/else` con variable temporal interna.
- `try/catch` → `try/except Exception as e`.
- `type alias` → comentario en Python.
- `include` → **inline** recursivo.

## Ejemplos rápidos
```
type alias Numero = number

match 2
    case 1
        Say "A"
    case 2 or 3
        Say "B"
end

try
    Use random as R
    Say R.randint(1, 2)
catch
    Say "No random"
end
```

---

