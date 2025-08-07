# run_tests_v0_4_beta.py - transpila y ejecuta pruebas de Gipsy v0.4-beta
import io, sys, traceback, types, os
from importlib.machinery import SourceFileLoader
from pathlib import Path

ROOT = Path(__file__).parent
TP_PATH = ROOT / "gipsy_transpiler_v0_4_beta.py"

# corregir nombre real del archivo
if not TP_PATH.exists():
    TP_PATH = ROOT / "gipsy_transpiler_v0.4_beta.py"

tp_mod = SourceFileLoader("gipsy_tp_v04b", str(TP_PATH)).load_module()

def run_py_code(py_code: str) -> str:
    g = {}
    buf = io.StringIO()
    old = sys.stdout
    sys.stdout = buf
    cwd = os.getcwd()
    try:
        os.chdir(str(ROOT))
        exec(py_code, g, g)
    finally:
        os.chdir(cwd)
        sys.stdout = old
    return buf.getvalue().replace("\r\n", "\n").strip()

def transpile_file(src_path: Path) -> str:
    gsrc = src_path.read_text(encoding="utf-8")
    return tp_mod.transpile(gsrc, base_dir=str(src_path.parent))

def main():
    tests = [
        ("tests_match_v0_4_beta.gipsy", ["dos o tres"]),
        ("tests_try_v0_4_beta.gipsy", ["ZeroDivisionError"]),
        ("tests_typealias_v0_4_beta.gipsy", ["ok"]),
    ]
    ok = 0
    for fname, expected in tests:
        src = ROOT / fname
        try:
            py_code = transpile_file(src)
            out = run_py_code(py_code)
            got = out.split("\n") if out else []
            status = "OK" if got == expected else "FAIL"
            print(f"[{status}] {fname}")
            if status == "FAIL":
                print("  Esperado:", expected)
                print("  Obtenido:", got)
            else:
                ok += 1
        except Exception as e:
            print(f"[ERROR] {fname}: {e}")
            traceback.print_exc()
    print(f"\nResumen: {ok}/{len(tests)} pruebas OK")

if __name__ == "__main__":
    main()
