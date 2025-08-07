
import math

def cuadrado(x):
    return x * x

print("Dame un número:")
n = float(input())
print("El cuadrado es:")
print(cuadrado(n))

print("La raíz cuadrada es:")
print(math.sqrt(n))

print("Tipo de n:")
print(type(n).__name__)