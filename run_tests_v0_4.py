# run_tests_v0.4.py - transpila y ejecuta pruebas de Gipsy v0.4-alpha
import io, sys, traceback, types
from importlib.machinery import SourceFileLoader
from pathlib import Path

ROOT = Path(__file__).parent
TP_PATH = ROOT / "gipsy_transpiler_v0.4_alpha.py"

tp_mod = SourceFileLoader("gipsy_tp_v04", str(TP_PATH)).load_module()

def run_py_code(py_code: str) -> str:
    # Ejecuta el código en un globals aislado y captura stdout
    g = {}
    buf = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = buf
    import os
    cwd = os.getcwd()
    try:
        os.chdir(str(ROOT))
        exec(py_code, g, g)
    finally:
        os.chdir(cwd)
        sys.stdout = old_stdout
    return buf.getvalue().replace("\r\n", "\n").strip()

def transpile_file(src_path: Path) -> str:
    gsrc = src_path.read_text(encoding="utf-8")
    return tp_mod.transpile(gsrc, base_dir=str(src_path.parent))

def main():
    tests = [
        ("tests_use_v0_4.gipsy", ["4.0", "120"]),
        ("tests_const_v0_4.gipsy", ["3.14"]),
        ("tests_include_v0_4.gipsy", ["Hola, Gipsy"]),
        ("tests_control_v0_4.gipsy", ["0","1","2","L","L","L","OK"]),
    ]
    ok = 0
    for fname, expected in tests:
        src = ROOT / fname
        try:
            py_code = transpile_file(src)
            out = run_py_code(py_code)
            got = out.split("\n") if out else []
            passed = got == expected
            status = "OK" if passed else "FAIL"
            print(f"[{status}] {fname}")
            if not passed:
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
