<p style= "text-align=center">
  <img src="Gipsy_logo_banner.png" alt="Gipsy Logo" width="1080">
</p>

# Gipsy v0.4-beta

Gipsy es un lenguaje inspirado en Python, pensado para ser **natural, expresivo y tolerante**.  
Esta versión **v0.4-beta** incluye nuevas features del lenguaje y herramientas listas para usar.

## ✨ Features (v0.4-beta)
- `Use <mod> [as alias]` para importar módulos de Python (con fallback may/min).
- `Const` inmutables globales.
- `include "archivo.gipsy"` **inline y recursivo** en el transpilador.
- `match / case / else` (comparación por igualdad; soporta `case 1 or 2`).
- `try / catch` (captura `Exception`).
- `type alias Nombre = Tipo` (almacenado/documentado; sin validación estricta todavía).
- `typeof x` devuelve el nombre del tipo.
- REPL con guardia de stack y trazas en español.

## 📦 Archivos incluidos

| Archivo                              | Descripción |
|--------------------------------------|-------------|
| [`gipsy_repl_v0.4_beta.py`](./gipsy_repl_v0.4_beta.py)| Intérprete interactivo (REPL) de Gipsy v0.4-beta |
| [`gipsy_transpiler_v0.4_beta.py`](./gipsy_transpiler_v0.4_beta.py)  | Transpilador Gipsy → Python con soporte para nuevas features de la beta |
| [`gipsy_documentacion_v0.4-beta.md`](./gipsy_documentacion_v0.4-beta.md)| Documentación técnica y notas de versión |
| [`run_tests_v0_4_beta.py`](./run_tests_v0_4_beta.py)         | Script para ejecutar el suite de pruebas automáticas |
| [`tests_match_v0_4_beta.gipsy`](./tests_match_v0_4_beta.gipsy)    | Prueba de la sintaxis `match / case / else` |
| [`tests_try_v0_4_beta.gipsy`](./tests_try_v0_4_beta.gipsy)          | Prueba de la sintaxis `try / catch` |
| [`tests_typealias_v0_4_beta.gipsy`](./tests_typealias_v0_4_beta.gipsy)    | Prueba de la sintaxis `type alias` |
| [`README.md`](./README.md) | Instrucciones de uso, ejemplos y guía rápida |

## 🧪 Prueba rápida
Crea o usa el archivo `tests_match_v0_4_beta.gipsy`:

```gipsy
match 3
    case 1
        Say "uno"
    case 2 or 3
        Say "dos o tres"
    else
        Say "otro"
end

### Transpilar y ejecutar
**Windows PowerShell** (rutas con espacios → usa comillas):
```powershell
python ".\gipsy_transpiler_v0.4_beta.py" ".\tests_match_v0_4_beta.gipsy" ".\out.py"
python ".\out.py"
```

**Linux / macOS (bash):**
```bash
python3 ./gipsy_transpiler_v0.4_beta.py ./tests_match_v0_4_beta.gipsy ./out.py
python3 ./out.py
```

### REPL
```bash
python gipsy_repl_v0.4_beta.py
```
Pegá líneas y cerrá bloques con `end`. Línea en blanco para ejecutar el buffer. `exit` para salir.

Ejemplo en REPL:
```
Use Math
Say Math.sqrt(16)

match 2
    case 1
        Say "A"
    case 2 or 3
        Say "B"
end

try
    Say 1 / 0
catch e
    Say typeof e
end
```

## 🔧 Detalles de sintaxis
- **Use**: `Use Math`, `Use random as R` → `R.randint(1,6)`
- **Const**: `Const PI = 3.14159`
- **include**: `include "lib.gipsy"` (transpilador lo inyecta inline; soporta recursión y rutas relativas)
- **match/case**: igualdad simple; `case 1 or 2` agrupa varios valores; `else` opcional
- **try/catch**: `catch` opcionalmente con variable: `catch e`
- **type alias**: `type alias Edad = number` (documental en beta)
- **typeof**: `Say typeof x` → imprime el nombre del tipo

## ⚠️ Límites conocidos (beta)
- `match` no soporta rangos ni comodín `_` (podemos agregar en RC).
- `type alias` aún no valida; planeado “tipo suave”/warnings en próxima versión.
- Parser lineal (no soporta comas anidadas complejas en llamadas dentro de una misma línea).

## 🧰 Ejecutar el suite de pruebas
```bash
python run_tests_v0_4_beta.py
```

## 🗺️ Estructura recomendada de proyecto
```
/mi-proyecto-gipsy
  ├─ src/
  │   ├─ main.gipsy
  │   └─ lib.gipsy
  ├─ tools/
  │   ├─ gipsy_repl_v0.4_beta.py
  │   └─ gipsy_transpiler_v0.4_beta.py
  └─ README.md
```

Transpilar:
```bash
python tools/gipsy_transpiler_v0_4_beta.py src/main.gipsy out.py
python out.py
```