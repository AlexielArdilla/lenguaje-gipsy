# Gipsy v0.4-beta Transpiler
# Soporta: Say, Ask, asignación, Const, function/end, return,
# if/else/end, while/end, loop N times/end, include (inline recursivo),
# Use <mod> [as alias], match/case, try/catch, type alias, typeof.

import sys, re, os

def strip_comments_multiline(text: str) -> str:
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

def py_expr(expr: str) -> str:
    # Literales
    expr = re.sub(r"\btrue\b", "True", expr)
    expr = re.sub(r"\bfalse\b", "False", expr)
    expr = re.sub(r"\bnull\b", "None", expr)
    # typeof <ident>  ->  type(<ident>).__name__
    expr = re.sub(r"\btypeof\s+([A-Za-z_]\w*)", r"type(\1).__name__", expr)
    return expr

def transpile(gsrc: str, base_dir: str = "") -> str:
    base_dir = base_dir or os.getcwd()
    gsrc = strip_comments_multiline(gsrc)
    lines = [l.rstrip("\n") for l in gsrc.splitlines()]
    i = 0
    py = []
    indent = 0
    in_match = False
    have_case = False

    def W(s=""):
        py.append(("    " * indent) + s)

    while i < len(lines):
        line = lines[i].strip()
        i += 1
        if not line:
            continue

        # cierre de bloque
        if line == "end":
            indent = max(0, indent - 1)
            if in_match and indent >= 0:
                # cerrar estado de match al salir del bloque
                in_match = False
                have_case = False
            continue

        # Use <mod> [as alias]
        if line.startswith("Use "):
            m = re.match(r'Use\s+([A-Za-z_]\w*)(?:\s+as\s+([A-Za-z_]\w*))?$', line)
            if not m:
                raise SystemExit("Uso: Use <mod> [as alias]")
            mod = m.group(1)
            alias = m.group(2) or m.group(1)
            lower = mod.lower()
            tmp = f"__gipsy_mod_{alias}"
            W("try:"); indent += 1
            W(f"import {mod} as {tmp}"); indent -= 1
            W("except ImportError:"); indent += 1
            W(f"import {lower} as {tmp}"); indent -= 1
            W(f"{alias} = {tmp}")
            continue

        # include "archivo.gipsy"  (inline recursivo)
        if line.startswith("include "):
            m = re.match(r'include\s+["\'](.+?)["\']', line)
            if not m:
                raise SystemExit('include inválido (usa: include "archivo.gipsy")')
            rel = m.group(1)
            inc_path = rel if os.path.isabs(rel) else os.path.join(base_dir, rel)
            try:
                g_inc = open(inc_path, "r", encoding="utf-8").read()
            except FileNotFoundError:
                raise SystemExit(f"No se encontró include: {rel}")
            inc_py = transpile(g_inc, base_dir=os.path.dirname(inc_path))
            for ln in inc_py.splitlines():
                W(ln)
            continue

        # type alias Nombre = expr   (solo documenta en Python)
        if line.startswith("type alias "):
            rest = line[len("type alias "):]
            if "=" not in rest:
                raise SystemExit("Uso: type alias Name = expr")
            name, expr = rest.split("=", 1)
            name, expr = name.strip(), py_expr(expr.strip())
            W(f"# type alias {name} = {expr}")
            continue

        # try / catch
        if line == "try":
            W("try:")
            indent += 1
            continue

        if line.startswith("catch"):
            parts = line.split()
            err = parts[1] if len(parts) > 1 else "_e"
            indent = max(0, indent - 1)
            W(f"except Exception as {err}:")
            indent += 1
            continue

        # match/case/else
        if line.startswith("match "):
            subject = py_expr(line[6:].strip())
            W(f"__gipsy_match_subject = {subject}")
            in_match = True
            have_case = False
            continue

        if line.startswith("case "):
            pat = line[5:].strip()
            parts = [p.strip() for p in pat.split(" or ")]
            conds = [f"__gipsy_match_subject == {py_expr(p)}" for p in parts if p]
            if not conds:
                raise SystemExit("case vacío")
            if have_case:
                indent = max(0, indent - 1)
                W(f"elif {' or '.join(conds)}:")
                indent += 1
            else:
                W(f"if {' or '.join(conds)}:")
                indent += 1
                have_case = True
            continue

        if line.startswith("else"):
            # si venimos de 'case', cerramos un nivel
            if in_match:
                indent = max(0, indent - 1)
            W("else:")
            indent += 1
            continue

        # Const
        if line.startswith("Const "):
            rest = line[len("Const "):]
            if "=" not in rest:
                raise SystemExit("Uso: Const NOMBRE = expr")
            name, expr = rest.split("=", 1)
            name, expr = name.strip(), py_expr(expr.strip())
            W(f"# Const {name}")
            W(f"{name} = {expr}")
            continue

        # Say
        if line.startswith("Say "):
            raw = line[len("Say "):]
            expr = py_expr(raw)
            # soporte typeof X en Say si quedó sin convertir
            if raw.strip().startswith("typeof "):
                tgt = raw.strip()[len("typeof "):].strip()
                expr = f"type({py_expr(tgt)}).__name__"
            W(f"print({expr})")
            continue

        # Ask / x = Ask
        if " = Ask " in line or line.startswith("Ask "):
            m = re.match(r'(?:([A-Za-z_]\w*)\s*=\s*)?Ask\s+(".*?"|\'.*?\')(\s+as\s+number)?', line)
            if not m:
                raise SystemExit('Uso: x = Ask "mensaje" [as number]')
            var = m.group(1)
            prompt = m.group(2)
            as_number = bool(m.group(3))
            code = f'float(input({prompt}))' if as_number else f'input({prompt})'
            if var:
                W(f"{var} = {code}")
            else:
                W(f"print({code})")
            continue

        # function
        if line.startswith("function "):
            m = re.match(r"function\s+([A-Za-z_]\w*)\((.*?)\)", line)
            if not m:
                raise SystemExit("Definición de función inválida")
            name = m.group(1)
            params = m.group(2).strip()
            W(f"def {name}({params}):")
            indent += 1
            continue

        # return
        if line.startswith("return"):
            rest = line[len("return"):].strip()
            W(f"return {py_expr(rest)}" if rest else "return None")
            continue

        # if
        if line.startswith("if "):
            cond = py_expr(line[3:].strip())
            W(f"if {cond}:")
            indent += 1
            continue

        # while
        if line.startswith("while "):
            cond = py_expr(line[6:].strip())
            W(f"while {cond}:")
            indent += 1
            continue

        # loop N times
        if line.startswith("loop "):
            m = re.match(r"loop\s+(\d+)\s+times", line)
            if not m:
                raise SystemExit("Sintaxis de loop inválida. Usa: loop N times")
            n = int(m.group(1))
            W(f"for _ in range({n}):")
            indent += 1
            continue

        # asignación o llamada
        if "=" in line:
            name, expr = line.split("=", 1)
            W(f"{name.strip()} = {py_expr(expr.strip())}")
            continue

        m = re.match(r"([A-Za-z_]\w*)\((.*)\)$", line)
        if m:
            W(line)
            continue

        raise SystemExit(f"Sentencia no reconocida: {line}")

    return '\n'.join(py) + '\n'

def main():
    if len(sys.argv) != 3:
        print("Uso: python gipsy_transpiler_v0.4_beta.py origen.gipsy salida.py")
        sys.exit(1)
    src_path = sys.argv[1]
    out_path = sys.argv[2]
    base_dir = os.path.dirname(os.path.abspath(src_path))
    src = open(src_path, "r", encoding="utf-8").read()
    out = transpile(src, base_dir=base_dir)
    open(out_path, "w", encoding="utf-8").write(out)
    print(f"Archivo transpilado guardado en {out_path}")

if __name__ == "__main__":
    main()
