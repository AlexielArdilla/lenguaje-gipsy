# 🧙‍♂️ Gipsy v0.4 — Lenguaje de Programación

**Gipsy** es un lenguaje de programación inspirado en Python, diseñado para ser expresivo, amigable y tolerante a errores comunes como la indentación. Su objetivo es acercar la programación a personas con poca experiencia, usando una sintaxis clara y natural.

---

## ✅ Características implementadas hasta v0.4

### 1. 🗣 Comandos naturales
- `Say` en lugar de `print`
- `Ask` para entradas interactivas
- `Use` para importar módulos de Python (por ejemplo: `Use math`)

### 2. 🎯 Tipado opcional
Podés declarar tipos opcionales para tus variables:

```gipsy
x: number = 5
nombre: string = Ask "¿Tu nombre?"
```

Soporta los tipos: `number`, `string`, `bool`, `list`.

### 3. 🔁 Estructuras de control
```gipsy
if x > 3
    Say "Mayor a 3"
end

loop 3 times
    Say "Repetir"
end
```

### 4. 🧩 Funciones
```gipsy
function cuadrado(n)
    return n * n
end

Say cuadrado(4)   # Imprime: 16
```

### 5. 🔒 Constantes
Podés declarar valores inmutables:

```gipsy
Const PI = 3.14
Say PI

PI = 4   # ❌ Error: no se puede reasignar la constante
```

### 6. ⚡ Funciones lambda
```gipsy
doble = fun(x) return x * 2 end
Say doble(5)   # 10
```

---

## 📁 Archivos del proyecto

| Archivo | Descripción |
|--------|-------------|
| `gipsy_repl_v0.4_const_CLEAN_REBUILD.py` | Intérprete interactivo REPL con Say, Ask, Const, tipado, funciones, etc. |
| `.gipsy` | Archivos fuente escritos en lenguaje Gipsy |
| `README.md` | Documentación general del proyecto |

---

## 🚀 Cómo usar el REPL

```bash
python gipsy_repl_v0.4_const_CLEAN_REBUILD.py
```

Escribí tus instrucciones directamente.  
Para salir: `Ctrl + C` o escribí `exit`.

---

## 🛠 En desarrollo para próximas versiones

- `match / case`
- `try / catch`
- `include archivo.gipsy`
- alias de tipos (`type alias`)
- control de errores mejorado
- archivo ejecutable `.gipsy` por línea de comandos

---

Creado con ❤️ por Alejandro Gonzalo Vera y ChatGPT