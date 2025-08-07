
import sys

def transpile_line(line):
    stripped = line.strip()
    
    if stripped.startswith("Say "):
        return "print(" + stripped[4:].strip() + ")"
    
    if stripped.startswith("Ask"):
        return "input()"

    if " = Ask" in stripped:
        var = stripped.split('=')[0].strip()
        return f"{var} = input()"

    if stripped.startswith("function "):
        header = stripped[len("function "):]
        return "def " + header + ":"

    if stripped.startswith("if "):
        condition = stripped[len("if "):]
        return "if " + condition + ":"

    if stripped.startswith("else"):
        return "else:"

    if stripped.startswith("loop "):
        parts = stripped.split()
        if len(parts) >= 2 and parts[2] == "times":
            count = parts[1]
            return f"for _ in range({count}):"

    if stripped == "end":
        return "# end"  # se ignora, se usó solo para delimitar bloques

    if stripped.startswith("return "):
        return "return " + stripped[len("return "):]

    return line  # por defecto, lo dejamos igual

def transpile_gipsy_to_python(source_code):
    output = []
    indent = 0
    for line in source_code.splitlines():
        line = line.rstrip()
        stripped = line.strip()

        if stripped == "":
            output.append("")
            continue

        if stripped in ["end", "else"]:
            if stripped == "end":
                indent -= 1
            elif stripped == "else":
                indent -= 1  # cerrar el if antes de else
                output.append("    " * indent + transpile_line(line))
                indent += 1
            continue

        py_line = transpile_line(line)
        output.append("    " * indent + py_line)

        if stripped.startswith(("function", "if", "else", "loop")):
            indent += 1

    return "\n".join(output)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python gipsy_transpiler.py archivo.gipsy archivo.py")
        sys.exit(1)

    gipsy_file = sys.argv[1]
    python_file = sys.argv[2]

    with open(gipsy_file, "r") as f:
        gipsy_code = f.read()

    python_code = transpile_gipsy_to_python(gipsy_code)

    with open(python_file, "w") as f:
        f.write(python_code)

    print(f"Archivo transpilado guardado en {python_file}")
