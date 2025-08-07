import re
import math

class GipsyREPL:
    def __init__(self):
        self.env = {"math": math}
        self.functions = {}
        self.types = {}
        self.constants = set()
        self.buffer = []
        self.in_block = False

    def run(self):
        print("🧙‍♂️ Gipsy REPL v0.4 — Tipado + funciones + Const + Say/Ask/Use/etc.")
        while True:
            try:
                line = input("... " if self.in_block else ">>> ").strip()
                if line.lower() in ["exit", "quit"]:
                    print("Saliendo de Gipsy REPL.")
                    break
                if self.in_block:
                    if line == "end":
                        self.buffer.append("# end")
                        self.execute_block(self.buffer)
                        self.buffer = []
                        self.in_block = False
                    else:
                        self.buffer.append(line)
                elif line.endswith(":") or line.startswith(("function", "if", "while", "loop", "else")):
                    self.in_block = True
                    self.buffer = [line]
                else:
                    self.execute_line(line)
            except KeyboardInterrupt:
                print("\nSaliendo de Gipsy REPL por interrupción (Ctrl + C).")
                break
            except Exception as e:
                print(f"❌ {e}")

    def execute_block(self, lines):
        py_code = self.transpile_block(lines)
        exec(py_code, {}, self.env)

    def execute_line(self, line):
        py_line = self.transpile_line(line)
        if py_line.startswith("#skip") or py_line.strip() == "":
            return
        try:
            is_expr = (
                not any(py_line.strip().startswith(kw) for kw in [
                    "def ", "return", "import", "for ", "while ", "if ", "print", "else", "try", "except"
                ]) and "=" not in py_line
            )
            if is_expr:
                result = eval(py_line, {}, self.env)
                if result is not None:
                    print(result)
            else:
                if "=" in py_line:
                    var_check = py_line.split("=")[0].strip()
                    if var_check in self.constants and not line.strip().startswith("Const "):
                        raise Exception(f"No se puede reasignar la constante: {var_check}")
                exec(py_line, {}, self.env)
                if line.strip().startswith("Const "):
                    const_decl = line[6:].strip()
                    const_var = const_decl.split("=")[0].strip()
                    self.constants.add(const_var)
                var_name = py_line.split("=")[0].strip() if "=" in py_line else None
                if var_name and var_name in self.types:
                    self.validate_type(var_name)
        except Exception as e:
            print(f"❌ {e}")

    def transpile_block(self, lines):
        result = []
        indent = 0
        for line in lines:
            stripped = line.strip()
            if stripped == "end":
                indent -= 1
                continue
            if stripped == "else":
                indent -= 1
                result.append("    " * indent + "else:")
                indent += 1
                continue
            py = self.transpile_line(line)
            result.append("    " * indent + py)
            if stripped.startswith(("function", "if", "while", "loop", "else", "for")):
                indent += 1
        return "\n".join(result)

    def transpile_line(self, line):
        line = re.sub(r"typeof\s+(\w+)", r"type(\1).__name__", line)
        line = line.replace("true", "True").replace("false", "False")

        if line.startswith("Say "):
            contenido = line[4:]
            contenido = contenido.split("#")[0].strip()
            return f"print({contenido})"
        if " = Ask" in line:
            var, rest = line.split("=", 1)
            rest = rest.strip()
            prompt = re.findall(r'["\'].*?["\']', rest)[0] if '"' in rest or "'" in rest else '"?"'
            return f"{var.strip()} = input({prompt})"
        if line.startswith("Use "):
            lib = line.split()[1]
            return f"import {lib}"
        if line.startswith("function "):
            return "def " + line[len("function "):] + ":"
        if line.startswith("return "):
            return "return " + line[len("return "):]
        if line.startswith("if "):
            return "if " + line[3:] + ":"
        if line == "else":
            return "else:"
        if line.startswith("while "):
            return "while " + line[6:] + ":"
        if line.startswith("loop "):
            n = re.findall(r"loop (\d+) times", line)
            return f"for _ in range({n[0]}):" if n else line
        if " = fun(" in line and "return" in line and "end" in line:
            match = re.match(r"(\w+)\s*=\s*fun\((.*?)\)\s*return\s+(.*?)\s*end", line)
            if match:
                var, args, expr = match.groups()
                return f"{var} = lambda {args}: {expr}"
        match = re.match(r"(\w+):\s*(\w+)\s*=\s*(.+)", line)
        if match:
            var, tipo, expr = match.groups()
            self.types[var] = tipo
            return f"{var} = {expr}"
        if line.startswith("Const "):
            const_decl = line[6:].strip()
            var, value = const_decl.split("=", 1)
            return f"{var.strip()} = {value.strip()}"

        return line

    def validate_type(self, var_name):
        tipo = self.types[var_name]
        valor = self.env[var_name]
        if tipo == "number" and not isinstance(valor, (int, float)):
            raise TypeError(f"{var_name} debía ser number, recibió {type(valor).__name__}")
        elif tipo == "string" and not isinstance(valor, str):
            raise TypeError(f"{var_name} debía ser string, recibió {type(valor).__name__}")
        elif tipo == "bool" and not isinstance(valor, bool):
            raise TypeError(f"{var_name} debía ser bool, recibió {type(valor).__name__}")
        elif tipo == "list" and not isinstance(valor, list):
            raise TypeError(f"{var_name} debía ser list, recibió {type(valor).__name__}")

if __name__ == "__main__":
    GipsyREPL().run()