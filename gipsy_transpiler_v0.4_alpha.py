# Gipsy v0.4-alpha Transpiler (mínimo, con Use)
# Convierte un subconjunto de Gipsy a Python.
# Soporta: Say, Ask, asignación, Const (como comentario + asignación), function/end, return,
# if/else/end, while/end, loop N times/end, include (exec file), Use <mod> [as alias].

import sys, re

def strip_comments_multiline(text):
    lines = text.splitlines(True)
    out = []
    in_block = False
    for line in lines:
        if "###" in line:
            count = line.count("###")
            if count == 2 and line.strip().startswith("###") and line.strip().endswith("###"):
                continue
            in_block = not in_block
            continue
        if not in_block:
            if "//" in line:
                line = line.split("//", 1)[0] + "\n"
            out.append(line)
    return "".join(out)

def py_expr(expr):
    expr = re.sub(r"\btrue\b", "True", expr)
    expr = re.sub(r"\bfalse\b", "False", expr)
    expr = re.sub(r"\bnull\b", "None", expr)
    return expr

def transpile(gsrc:str, base_dir: str = "")->str:
    gsrc = strip_comments_multiline(gsrc)
    import os
    base_dir = base_dir or os.getcwd()
    lines = [l.rstrip("\n") for l in gsrc.splitlines()]
    i = 0
    py = []
    indent = 0
    def W(s=""):
        py.append(("    "*indent)+s)

    while i < len(lines):
        line = lines[i].strip()
        i += 1
        if not line:
            continue
        if line == "end":
            indent = max(0, indent-1)
            continue

        # Use <mod> [as alias]
        if line.startswith("Use "):
            m = re.match(r'Use\s+([A-Za-z_]\w*)(?:\s+as\s+([A-Za-z_]\w*))?$', line)
            if not m:
                raise SystemExit("Uso: Use <mod> [as alias]")
            mod = m.group(1)
            alias = m.group(2) or m.group(1)
            lower = mod.lower()
            tmpname = f"__gipsy_mod_{alias}"
            W("try:")
            indent += 1
            W(f"import {mod} as {tmpname}")
            indent -= 1
            W("except ImportError:")
            indent += 1
            W(f"import {lower} as {tmpname}")
            indent -= 1
            W(f"{alias} = {tmpname}")
            continue

        if line.startswith("include "):
            m = re.match(r'include\s+["\'](.+?)["\']', line)
            if not m:
                raise SystemExit("include inválido")
            rel = m.group(1)
            inc_path = rel if os.path.isabs(rel) else os.path.join(base_dir, rel)
            try:
                g_inc = open(inc_path, "r", encoding="utf-8").read()
            except FileNotFoundError:
                raise SystemExit(f"No se encontró include: {rel}")
            # Transpilar recursivamente el include con su propio base_dir
            inc_py = transpile(g_inc, base_dir=os.path.dirname(inc_path))
            # Inlinear el código transpilado
            for ln in inc_py.splitlines():
                W(ln)
            continue

        if line.startswith("Const "):
            rest = line[len("Const "):]
            if "=" not in rest:
                raise SystemExit("Uso: Const NOMBRE = expr")
            name, expr = rest.split("=", 1)
            name, expr = name.strip(), py_expr(expr.strip())
            W(f"# Const {name}")
            W(f"{name} = {expr}")
            continue

        if line.startswith("Say "):
            expr = py_expr(line[len("Say "):])
            W(f"print({expr})")
            continue

        if " = Ask " in line or line.startswith("Ask "):
            m = re.match(r'(?:([A-Za-z_]\w*)\s*=\s*)?Ask\s+(".*?"|\'.*?\')(\s+as\s+number)?', line)
            if not m:
                raise SystemExit('Uso: x = Ask "mensaje" [as number]')
            var = m.group(1)
            prompt = m.group(2)
            as_number = bool(m.group(3))
            code = f'float(input({prompt}))' if as_number else f'input({prompt})'
            if var:
                W(f'{var} = {code}')
            else:
                W(f'print({code})')
            continue

        if line.startswith("function "):
            m = re.match(r"function\s+([A-Za-z_]\w*)\((.*?)\)", line)
            if not m:
                raise SystemExit("Definición de función inválida")
            name = m.group(1)
            params = m.group(2).strip()
            W(f"def {name}({params}):")
            indent += 1
            continue

        if line.startswith("return"):
            rest = line[len("return"):].strip()
            if rest:
                W(f"return {py_expr(rest)}")
            else:
                W("return None")
            continue

        if line.startswith("if "):
            cond = py_expr(line[3:].strip())
            W(f"if {cond}:")
            indent += 1
            continue

        if line.startswith("else"):
            indent = max(0, indent-1)
            W("else:")
            indent += 1
            continue

        if line.startswith("while "):
            cond = py_expr(line[6:].strip())
            W(f"while {cond}:")
            indent += 1
            continue

        if line.startswith("loop "):
            m = re.match(r"loop\s+(\d+)\s+times", line)
            if not m:
                raise SystemExit("Sintaxis de loop inválida. Usa: loop N times")
            n = int(m.group(1))
            W(f"for _ in range({n}):")
            indent += 1
            continue

        # asignación o llamada suelta
        if "=" in line:
            name, expr = line.split("=", 1)
            W(f"{name.strip()} = {py_expr(expr.strip())}")
            continue

        # llamada simple (ya válida en Python)
        m = re.match(r"([A-Za-z_]\w*)\((.*)\)$", line)
        if m:
            W(line)
            continue

        raise SystemExit(f"Sentencia no reconocida: {line}")

    return "\n".join(py) + "\n"

def main():
    if len(sys.argv) != 3:
        print("Uso: python gipsy_transpiler_v0.4_alpha.py origen.gipsy salida.py")
        sys.exit(1)
    src_path = sys.argv[1]
    base_dir = __import__("os").path.dirname(__import__("os").path.abspath(src_path))
    src = open(src_path, "r", encoding="utf-8").read()
    out = transpile(src, base_dir=base_dir)
    open(sys.argv[2], "w", encoding="utf-8").write(out)
    print(f"Archivo transpilado guardado en {sys.argv[2]}")

if __name__ == "__main__":
    main()
