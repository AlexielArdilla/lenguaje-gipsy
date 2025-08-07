
# 📘 Documentación Oficial – Lenguaje de Programación Gipsy v0.2

---

## ✨ Descripción General

**Gipsy** es un lenguaje de programación interpretado y transpilable, inspirado en Python, pero con una sintaxis más expresiva, natural y tolerante a errores.

- ✅ Tolerante a la indentación (usa `end` para cerrar bloques)
- ✅ Sintaxis natural: `Say`, `Ask`, `function`, `loop`, etc.
- ✅ Ideal para educación, scripting, y pseudo-código ejecutable
- ✅ Traducción directa a Python
- ✅ Intérprete propio en Python

---

## 🧩 Sintaxis y Funcionalidades

### 1. Say

```gipsy
Say "Hola mundo"
```

Equivalente a `print()` en Python.

---

### 2. Ask

```gipsy
nombre = Ask
edad = Ask "¿Tu edad?" as number
```

- Entrada de texto o número
- Soporta mensaje entre comillas

---

### 3. Variables y Asignaciones

```gipsy
x = 5
nombre = "Gipsy"
```

---

### 4. Funciones

```gipsy
function saludar(nombre)
    Say "Hola, " + nombre
end

saludar("Alejandro")
```

- Palabra clave: `function`
- Se usa `end` para cerrar

---

### 5. Return

```gipsy
function doble(x)
    return x * 2
end

resultado = doble(4)
```

---

### 6. Condicionales

```gipsy
if edad >= 18
    Say "Mayor de edad"
else
    Say "Menor de edad"
end
```

---

### 7. Bucles

#### a. Loop N times

```gipsy
loop 3 times
    Say "Hola"
end
```

#### b. While

```gipsy
x = 0
while x < 5
    Say x
    x = x + 1
end
```

---

### 8. Tipos de Datos

- `number` → `3`, `5.6`
- `text` → `"hola"`
- `boolean` → `true`, `false`
- `null` → `None`
- `list` → `[1, 2, 3]`
- `dict` → `{ "nombre": "Gipsy" }`

---

## 🛠️ Herramientas

- **Intérprete:** `gipsy_interpreter_v2.py`
- **Transpilador:** `gipsy_transpiler_v2.py`
- **REPL:** `gipsy_repl.py` (solo comandos simples)

---

## 🚀 Ejemplo Completo

```gipsy
function cuadrado(x)
    return x * x
end

n = Ask "Dame un número:" as number
Say "Resultado:"
Say cuadrado(n)
```

---

## 📦 Instalación y Uso

### Ejecutar archivo .gipsy

```bash
python gipsy_interpreter_v2.py archivo.gipsy
```

### Transpilar a Python

```bash
python gipsy_transpiler_v2.py archivo.gipsy archivo.py
python archivo.py
```

---

## 🧠 Filosofía de Gipsy

- Legibilidad y naturalidad primero.
- Expresividad sin sacrificar poder.
- Ideal para nuevos programadores, scripts rápidos y enseñanza.

---

## 📅 Versión Actual

**v0.2 – Agosto 2025**

---

## 🔮 Próximas características (v0.3)

- Comentarios multilínea con `###`
- Importación de librerías: `Use`
- REPL con bloques completos
- Tipado dinámico con `typeof`
