# Gipsy v0.4-alpha REPL
# Features: Say, Ask, typeof, variables, Const (inmutables), function/end, return,
# if/else/end, while/end, loop N times/end, include "file", simple call stack guard
# y trazas/mensajes en español.

import sys, re, io

class GipsyError(Exception):
    pass

class GipsyStackOverflowError(GipsyError):
    pass

class ReturnSignal(Exception):
    def __init__(self, value):
        self.value = value

TRUE = True
FALSE = False
NULL = None

def strip_comments_multiline(lines):
    out = []
    in_block = False
    for line in lines:
        if "###" in line:
            # toggle every time we see ### (pair discards whole span)
            count = line.count("###")
            if count == 2 and line.strip().startswith("###") and line.strip().endswith("###"):
                # full-line ### ... ### -> omit
                continue
            in_block = not in_block
            continue
        if not in_block:
            # remove inline // comments
            if "//" in line:
                line = line.split("//", 1)[0] + "\n"
            out.append(line)
    return out

class Environment:
    def __init__(self, parent=None):
        self.vars = {}
        self.consts = set()
        self.parent = parent

    def has_local(self, name):
        return name in self.vars

    def set(self, name, value):
        if name in self.consts:
            raise GipsyError(f"No se puede reasignar la constante '{name}'.")
        self.vars[name] = value

    def define_const(self, name, value):
        if name in self.vars:
            raise GipsyError(f"No se puede redeclarar '{name}' como Const (ya existe).")
        self.vars[name] = value
        self.consts.add(name)

    def get(self, name):
        if name in self.vars:
            return self.vars[name]
        if self.parent:
            return self.parent.get(name)
        raise GipsyError(f"Variable no definida: '{name}'.")

class Function:
    def __init__(self, name, params, body, decl_line):
        self.name = name
        self.params = params
        self.body = body
        self.decl_line = decl_line

class Interpreter:
    def __init__(self, max_call_depth=1000):
        self.global_env = Environment()
        self.call_depth = 0
        self.max_call_depth = max_call_depth
        self.frames = []  # (nombre, linea)
        self.install_builtins(self.global_env)

    # ---------- Utilidades ----------
    def install_builtins(self, env):
        env.set("true", TRUE)
        env.set("false", FALSE)
        env.set("null", NULL)
        env.set("typeof", lambda x: type(x).__name__)

    def safe_eval(self, expr, env):
        # Reemplazos simples de literales estilo Gipsy
        repl = {
            r"\btrue\b": "True",
            r"\bfalse\b": "False",
            r"\bnull\b": "None",
        }
        for k, v in repl.items():
            expr = re.sub(k, v, expr)
        # variables/funciones desde el entorno
        scope = {}
        # recolectar variables del chain
        e = env
        while e:
            scope.update(e.vars)
            e = e.parent
        # eval restringido (sin builtins)
        return eval(expr, {"__builtins__": {}}, scope)

    def enter_call(self, nombre, linea):
        self.call_depth += 1
        self.frames.append((nombre, linea))
        if self.call_depth > self.max_call_depth:
            raise GipsyStackOverflowError(
                f"Desbordamiento de pila al llamar a '{nombre}'. Se superó el máximo de {self.max_call_depth} niveles."
            )

    def exit_call(self):
        if self.frames:
            self.frames.pop()
        if self.call_depth > 0:
            self.call_depth -= 1

    def format_trace(self, msg=None):
        buf = io.StringIO()
        for nombre, linea in self.frames[-8:][::-1]:
            buf.write(f'  Archivo "<repl>", línea {linea}, en {nombre}\n')
        if msg:
            buf.write(str(msg) + "\n")
        return buf.getvalue()

    # ---------- Parser muy simple basado en líneas y 'end' ----------
    def parse(self, lines):
        # Devuelve lista de nodos (stmt) a partir de líneas sin comentarios
        tokens = [l.rstrip("\n") for l in lines]
        i = 0
        def parse_block():
            nonlocal i
            block = []
            while i < len(tokens):
                line = tokens[i].strip()
                i += 1
                if not line:
                    continue
                if line == "end":
                    break
                # bloques
                if line.startswith("function "):
                    m = re.match(r"function\s+([A-Za-z_]\w*)\((.*?)\)", line)
                    if not m:
                        raise GipsyError(f"Definición de función inválida: '{line}'")
                    name = m.group(1)
                    params = [p.strip() for p in m.group(2).split(",")] if m.group(2).strip() else []
                    start_line = i
                    body = parse_block()
                    block.append(("funcdef", name, params, body, start_line))
                elif line.startswith("if "):
                    cond = line[3:].strip()
                    then_body = parse_block()
                    # soportar 'else' opcional
                    else_body = []
                    # mirar si próxima línea es 'else'
                    if i < len(tokens) and tokens[i].strip().startswith("else"):
                        i += 1  # consumir 'else'
                        else_body = parse_block()
                    block.append(("if", cond, then_body, else_body))
                elif line.startswith("while "):
                    cond = line[6:].strip()
                    body = parse_block()
                    block.append(("while", cond, body))
                elif line.startswith("loop "):
                    m = re.match(r"loop\s+(\d+)\s+times", line)
                    if not m:
                        raise GipsyError("Sintaxis de loop inválida. Usa: loop N times")
                    n = int(m.group(1))
                    body = parse_block()
                    block.append(("loop", n, body))
                else:
                    # sentencia simple (Say, Ask, include, return, asignación, llamada suelta)
                    block.append(("stmt", line, i))
            return block
        ast = parse_block()
        return ast

    # ---------- Ejecutar AST ----------
    def run_block(self, ast, env):
        for node in ast:
            kind = node[0]
            if kind == "funcdef":
                _, name, params, body, start_line = node
                env.set(name, Function(name, params, body, start_line))
            elif kind == "if":
                _, cond, then_body, else_body = node
                if self.safe_eval(cond, env):
                    self.run_block(then_body, env)
                else:
                    self.run_block(else_body, env)
            elif kind == "while":
                _, cond, body = node
                while self.safe_eval(cond, env):
                    self.run_block(body, env)
            elif kind == "loop":
                _, n, body = node
                for _ in range(n):
                    self.run_block(body, env)
            elif kind == "stmt":
                _, line, lineno = node
                self.exec_stmt(line.strip(), env, lineno)
            else:
                raise GipsyError(f"Nodo desconocido: {kind}")

    def call_function(self, func, args, env, lineno):
        # crear env hijo y bindear parámetros
        if len(args) != len(func.params):
            raise GipsyError(f"Llamada a '{func.name}' con {len(args)} argumentos, se esperaban {len(func.params)}.")
        local = Environment(parent=env)
        for name, value in zip(func.params, args):
            name = name.strip()
            if not name:
                continue
            local.set(name, value)
        self.enter_call(func.name, lineno)
        try:
            self.run_block(func.body, local)
        except ReturnSignal as r:
            return r.value
        finally:
            self.exit_call()
        return None

    def exec_stmt(self, line, env, lineno):

        # Use <mod> [as alias]
        if line.startswith("Use "):
            m = re.match(r'Use\s+([A-Za-z_]\w*)(?:\s+as\s+([A-Za-z_]\w*))?$', line)
            if not m:
                raise GipsyError("Uso: Use <mod> [as alias]")
            modname = m.group(1)
            alias = m.group(2) or m.group(1)
            try:
                try:
                    mod = __import__(modname)
                except ImportError:
                    mod = __import__(modname.lower())
                self.global_env.set(alias, mod)
            except ImportError:
                raise GipsyError(f"No se pudo importar la librería: {modname}")
            return
        # return
        if line.startswith("return "):
            expr = line[len("return "):].strip()
            val = self.safe_eval(expr, env)
            raise ReturnSignal(val)
        if line == "return":
            raise ReturnSignal(None)

        # include "archivo.gipsy"
        if line.startswith("include "):
            m = re.match(r'include\s+["\'](.+?)["\']', line)
            if not m:
                raise GipsyError('Sintaxis de include inválida. Usa: include "archivo.gipsy"')
            path = m.group(1)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    code = f.read().splitlines(True)
                code = strip_comments_multiline(code)
                ast = self.parse(code)
                self.run_block(ast, self.global_env)
            except FileNotFoundError:
                raise GipsyError(f"No se encontró el archivo: {path}")
            return

        # Const nombre = expr
        if line.startswith("Const "):
            rest = line[len("Const "):]
            if "=" not in rest:
                raise GipsyError("Uso: Const NOMBRE = expresión")
            name, expr = rest.split("=", 1)
            name = name.strip()
            expr = expr.strip()
            value = self.safe_eval(expr, env)
            self.global_env.define_const(name, value)
            return

        # Say expr
        if line.startswith("Say "):
            expr = line[len("Say "):]
            val = self.safe_eval(expr, env)
            print(val)
            return

        # x = Ask "..." [as number]
        if " = Ask " in line or line.startswith("Ask "):
            if " = Ask " in line:
                left, right = line.split("=", 1)
                var = left.strip()
                right = right.strip()
            else:
                var = None
                right = line
            m = re.match(r'(?:\w+\s*=\s*)?Ask\s+(".*?"|\'.*?\')(\s+as\s+number)?', line)
            if not m:
                raise GipsyError('Uso: x = Ask "mensaje" [as number]')
            prompt = m.group(1)
            as_number = bool(m.group(2))
            # evaluar prompt para soportar comillas/concat
            pr = self.safe_eval(prompt, env)
            user = input(str(pr))
            val = float(user) if as_number else user
            if var:
                env.set(var, val)
            else:
                # Ask solitario imprime el valor leído
                print(val)
            return

        # typeof(x) -> ya es builtin; permitir "Say typeof x"
        if line.startswith("typeof "):
            expr = line[len("typeof "):]
            val = self.safe_eval(expr, env)
            print(type(val).__name__)
            return

        # asignación simple o llamada a función
        if "=" in line:
            name, expr = line.split("=", 1)
            name = name.strip()
            expr = expr.strip()
            val = self.safe_eval(expr, env)
            env.set(name, val)
            return

        # llamada a función estilo: foo(1, 2)
        m = re.match(r"([A-Za-z_]\w*)\((.*)\)$", line)
        if m and m.group(1) in self.collect_functions(env):
            fname = m.group(1)
            args_src = m.group(2).strip()
            args = []
            if args_src:
                # separar por comas de forma simple (no soporta comas anidadas complejas)
                parts = [p.strip() for p in args_src.split(",")]
                for p in parts:
                    args.append(self.safe_eval(p, env))
            func = self.lookup_function(fname, env)
            self.call_function(func, args, env, lineno)
            return

        raise GipsyError(f"Sentencia no reconocida: '{line}'")

    def collect_functions(self, env):
        names = set()
        e = env
        while e:
            for k, v in e.vars.items():
                if isinstance(v, Function):
                    names.add(k)
            e = e.parent
        return names

    def lookup_function(self, name, env):
        e = env
        while e:
            v = e.vars.get(name)
            if isinstance(v, Function):
                return v
            e = e.parent
        raise GipsyError(f"Función no definida: '{name}'")

    def run(self, code:str):
        lines = code.splitlines(True)
        lines = strip_comments_multiline(lines)
        ast = self.parse(lines)
        try:
            self.run_block(ast, self.global_env)
        except GipsyStackOverflowError as e:
            print(self.format_trace(e))
        except GipsyError as e:
            print(self.format_trace(e))

def repl():
    print("Gipsy v0.4-alpha – escribe 'exit' para salir. Finaliza un bloque con 'end'.")
    intr = Interpreter()
    buf = []
    while True:
        try:
            line = input("... " if buf else ">>> ")
        except (EOFError, KeyboardInterrupt):
            print("\nHasta luego.")
            break
        if line.strip().lower() == "exit":
            break
        if line.strip() == "":
            code = "".join(buf)
            if code.strip():
                intr.run(code)
            buf = []
            continue
        buf.append(line + ("\n" if not line.endswith("\n") else ""))

if __name__ == "__main__":
    repl()
