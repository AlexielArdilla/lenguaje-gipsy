
class Environment:
    def __init__(self):
        self.variables = {}

    def set(self, var, value):
        self.variables[var] = value

    def get(self, var):
        return self.variables.get(var, None)

class GipsyInterpreter:
    def __init__(self):
        self.env = Environment()

    def run_line(self, line):
        line = line.strip()
        if line == "":
            return
        if line.startswith("Say "):
            self.say(line[4:])
        elif " = Ask" in line:
            var = line.split("=")[0].strip()
            self.env.set(var, input())
        elif "=" in line:
            self.handle_assignment(line)
        elif line.startswith("if ") or line.startswith("loop ") or line.startswith("function "):
            print("Bloques no soportados en el REPL (usá un archivo .gipsy)")
        else:
            print("Instrucción no reconocida:", line)

    def say(self, expr):
        value = self.evaluate(expr)
        print(value)

    def evaluate(self, expr):
        expr = expr.strip()
        for var in self.env.variables:
            expr = expr.replace(var, f"self.env.get('{var}')")
        try:
            return eval(expr)
        except Exception:
            return expr.strip('"')

    def handle_assignment(self, line):
        var, expr = line.split("=", 1)
        value = self.evaluate(expr)
        self.env.set(var.strip(), value)

if __name__ == "__main__":
    interpreter = GipsyInterpreter()
    print("🎴 Bienvenido al REPL de Gipsy v0.1")
    print("Escribí comandos Gipsy. 'exit' para salir. 'vars' para ver variables.")
    while True:
        try:
            line = input(">>> ")
        except EOFError:
            break
        if line.lower() in ["exit", "quit"]:
            break
        if line.lower() == "vars":
            for k, v in interpreter.env.variables.items():
                print(f"{k} = {v}")
            continue
        interpreter.run_line(line)
