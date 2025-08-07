
import sys

def remove_multiline_comments(lines):
    new_lines = []
    inside_comment = False
    for line in lines:
        if '###' in line:
            count = line.count('###')
            if count == 2:
                continue
            inside_comment = not inside_comment
            continue
        if not inside_comment:
            new_lines.append(line)
    return new_lines

def transpile_line(line):
    stripped = line.strip()

    if stripped.startswith("Say "):
        return "print(" + stripped[4:].strip() + ")"

    if " = Ask" in stripped:
        var, rest = stripped.split("=", 1)
        rest = rest.strip()
        if " as number" in rest:
            prompt = rest.replace("Ask", "").replace("as number", "").strip()
            return f"{var.strip()} = float(input({prompt}))"
        elif '"' in rest or "'" in rest:
            prompt = rest.replace("Ask", "").strip()
            return f"{var.strip()} = input({prompt})"
        else:
            return f"{var.strip()} = input()"

    if stripped.startswith("function "):
        header = stripped[len("function "):]
        return "def " + header + ":"

    if stripped.startswith("return "):
        return "return " + stripped[len("return "):]

    if stripped.startswith("if "):
        return "if " + stripped[3:] + ":"

    if stripped == "else":
        return "else:"

    if stripped.startswith("while "):
        return "while " + stripped[6:] + ":"

    if stripped.startswith("loop "):
        parts = stripped.split()
        if len(parts) >= 3 and parts[2] == "times":
            count = parts[1]
            return f"for _ in range({count}):"

    if stripped.startswith("Use "):
        lib = stripped.split()[1]
        return f"import {lib}"

    if stripped.startswith("typeof "):
        expr = stripped[len("typeof "):].strip()
        return f"type({expr}).__name__"

    if stripped == "end":
        return "# end"

    return line

def transpile_gipsy_to_python(source_code):
    output = []
    indent = 0
    lines = remove_multiline_comments(source_code.splitlines())
    for line in lines:
        line = line.rstrip()
        stripped = line.strip()

        if stripped == "":
            output.append("")
            continue

        if stripped == "end":
            indent -= 1
            continue

        if stripped == "else":
            indent -= 1
            output.append("    " * indent + transpile_line(line))
            indent += 1
            continue

        py_line = transpile_line(line)
        output.append("    " * indent + py_line)

        if stripped.startswith(("function", "if", "else", "while", "loop", "for")):
            indent += 1

    return "\n".join(output)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python gipsy_transpiler_v0.3.py archivo.gipsy archivo.py")
        sys.exit(1)

    gipsy_file = sys.argv[1]
    python_file = sys.argv[2]

    with open(gipsy_file, "r", encoding="utf-8") as f:
        gipsy_code = f.read()

    python_code = transpile_gipsy_to_python(gipsy_code)

    with open(python_file, "w", encoding="utf-8") as f:
        f.write(python_code)

    print(f"Archivo transpilado guardado en {python_file}")
