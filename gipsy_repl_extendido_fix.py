
class Environment:
    def __init__(self, parent=None):
        self.variables = {}
        self.parent = parent

    def set(self, var, value):
        self.variables[var] = value

    def get(self, var):
        if var in self.variables:
            return self.variables[var]
        elif self.parent:
            return self.parent.get(var)
        else:
            return None

class Function:
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

class GipsyInterpreter:
    def __init__(self):
        self.global_env = Environment()
        self.functions = {}

    def run(self, lines, env=None):
        if env is None:
            env = self.global_env
        self.lines = lines
        self.pos = 0
        self.env = env
        while self.pos < len(self.lines):
            self.execute_line()

    def execute_line(self):
        line = self.lines[self.pos].strip()
        if line.startswith("Say "):
            self.say(line[4:])
        elif " = Ask" in line:
            self.handle_ask(line)
        elif line.startswith("function "):
            self.define_function(line)
        elif line.startswith("if "):
            self.handle_if(line)
        elif line.startswith("while "):
            self.handle_while(line)
        elif line.startswith("loop "):
            self.handle_loop(line)
        elif line.startswith("return "):
            value = self.evaluate(line[7:].strip())
            raise ReturnException(value)
        elif "=" in line:
            self.handle_assignment(line)
        elif "(" in line and line.endswith(")"):
            self.call_function(line)
        self.pos += 1

    def say(self, expr):
        value = self.evaluate(expr)
        print(value)

    def handle_ask(self, line):
        if '"' in line:
            var, rest = line.split("=", 1)
            prompt = rest.split("Ask", 1)[1].strip()
            if "as number" in prompt:
                prompt = prompt.replace("as number", "").strip()
                val = input(eval(prompt))
                self.env.set(var.strip(), float(val))
            else:
                val = input(eval(prompt))
                self.env.set(var.strip(), val)
        else:
            var = line.split("=")[0].strip()
            self.env.set(var, input())

    def handle_assignment(self, line):
        var, expr = line.split("=", 1)
        value = self.evaluate(expr)
        self.env.set(var.strip(), value)

    
def evaluate(self, expr):
        expr = expr.strip()
        expr = expr.replace("true", "True").replace("false", "False").replace("null", "None")
        try:
            # Si es una variable sola
            if expr in self.env.variables:
                return self.env.get(expr)

            # Si es una expresión compleja, resolvemos manualmente las variables
            local_env = {}
            for var in self.env.variables:
                local_env[var] = self.env.get(var)
            return eval(expr, {}, local_env)
        except Exception:
            return expr.strip('"')

        expr = expr.strip()
        for var in self.env.variables:
            expr = expr.replace(var, f"self.env.get('{var}')")
        try:
            expr = expr.replace("true", "True").replace("false", "False").replace("null", "None")
            return eval(expr)
        except Exception:
            return expr.strip('"')

    def define_function(self, line):
        header = line[len("function "):]
        name, rest = header.split("(", 1)
        params = rest.rstrip(")").split(",") if rest.rstrip(")") else []
        params = [p.strip() for p in params if p.strip()]
        self.pos += 1
        body = self.collect_block()
        self.functions[name.strip()] = Function(name.strip(), params, body)

    def call_function(self, line):
        name, rest = line.split("(", 1)
        args = rest.rstrip(")").split(",") if rest.rstrip(")") else []
        args = [self.evaluate(arg.strip()) for arg in args if arg.strip()]
        func = self.functions.get(name.strip())
        if not func:
            print(f"Función no definida: {name}")
            return
        local_env = Environment(parent=self.env)
        for param, arg in zip(func.params, args):
            local_env.set(param, arg)
        try:
            self.run(func.body, local_env)
        except ReturnException as ret:
            self.env.set("_", ret.value)

    def handle_if(self, line):
        condition = line[3:].strip()
        self.pos += 1
        true_block = self.collect_block()
        next_line = self.lines[self.pos].strip() if self.pos < len(self.lines) else ""
        false_block = []
        if next_line == "else":
            self.pos += 1
            false_block = self.collect_block()
        if self.evaluate(condition):
            self.run(true_block, self.env)
        else:
            self.run(false_block, self.env)

    def handle_while(self, line):
        condition = line[6:].strip()
        self.pos += 1
        loop_block = self.collect_block()
        while self.evaluate(condition):
            self.run(loop_block, self.env)

    def handle_loop(self, line):
        parts = line.split()
        count = int(self.evaluate(parts[1]))
        self.pos += 1
        loop_block = self.collect_block()
        for _ in range(count):
            self.run(loop_block, self.env)

    def collect_block(self):
        block = []
        while self.pos < len(self.lines):
            line = self.lines[self.pos].strip()
            if line == "end":
                break
            block.append(self.lines[self.pos])
            self.pos += 1
        return block

# REPL EXTENDIDO
if __name__ == "__main__":
    interpreter = GipsyInterpreter()
    print("🔁 REPL de Gipsy v0.2 – Soporta bloques (function, if, while, etc.)")
    print("Escribí código. Línea vacía para ejecutar. Ctrl+C o 'exit' para salir.")
    buffer = []
    while True:
        try:
            line = input("... " if buffer else ">>> ")
        except (EOFError, KeyboardInterrupt):
            print("\nHasta luego.")
            break
        if line.strip().lower() == "exit":
            break
        if line.strip() == "":
            try:
                interpreter.run(buffer)
            except Exception as e:
                print("Error:", e)
            buffer = []
        else:
            buffer.append(line)
