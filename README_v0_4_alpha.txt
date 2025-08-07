# Gipsy v0.4-alpha — Paquete listo

## Contenido
- `gipsy_repl_v0.4_alpha.py` — REPL con `Const`, `include`, `Use`, guardia de stack y errores en español.
- `gipsy_transpiler_v0.4_alpha.py` — Transpilador con soporte de `Use`, `include` (inline y recursivo), `Const`, control de flujo básico.
- `gipsy_documentacion_v0.4-alpha.md` — Notas de versión y ejemplos.
- `run_tests_v0_4.py` — Runner que transpila y ejecuta pruebas.
- `tests_*.gipsy` + `lib_v0_4.gipsy` — Pruebas mínimas.

## Uso rápido
```bash
# 1) REPL
python gipsy_repl_v0.4_alpha.py

# 2) Transpilación
python gipsy_transpiler_v0.4_alpha.py tests_include_v0_4.gipsy out.py
python out.py

# 3) Pruebas
python run_tests_v0_4.py
```
