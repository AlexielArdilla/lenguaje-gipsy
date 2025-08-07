
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

    def run(self, lines):
        self.lines = lines
        self.pos = 0
        while self.pos < len(self.lines):
            self.execute_line()

    def execute_line(self):
        line = self.lines[self.pos].strip()
        if line.startswith("Say "):
            self.say(line[4:])
        elif " = Ask" in line:
            var = line.split("=")[0].strip()
            self.env.set(var, input())
        elif line.startswith("function "):
            self.skip_block()
        elif line.startswith("if "):
            self.handle_if(line)
        elif line.startswith("loop "):
            self.handle_loop(line)
        elif "=" in line:
            self.handle_assignment(line)
        self.pos += 1

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

    def handle_if(self, line):
        condition = line[3:].strip()
        self.pos += 1
        true_block = self.collect_block()
        next_line = self.lines[self.pos].strip() if self.pos < len(self.lines) else ""
        if next_line == "else":
            self.pos += 1
            false_block = self.collect_block()
        else:
            false_block = []
        if self.evaluate(condition):
            self.run_block(true_block)
        else:
            self.run_block(false_block)

    def handle_loop(self, line):
        parts = line.split()
        count = int(self.evaluate(parts[1]))
        self.pos += 1
        loop_block = self.collect_block()
        for _ in range(count):
            self.run_block(loop_block)

    def collect_block(self):
        block = []
        while self.pos < len(self.lines):
            line = self.lines[self.pos].strip()
            if line == "end":
                break
            block.append(self.lines[self.pos])
            self.pos += 1
        return block

    def run_block(self, block):
        saved_pos = self.pos
        self.run(block)
        self.pos = saved_pos

    def skip_block(self):
        while self.pos < len(self.lines):
            if self.lines[self.pos].strip() == "end":
                break
            self.pos += 1

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Uso: python gipsy_interpreter.py archivo.gipsy")
        sys.exit(1)
    filename = sys.argv[1]
    with open(filename, "r", encoding="utf-8") as f:
        code = f.readlines()
    interpreter = GipsyInterpreter()
    interpreter.run(code)
