import math
import time
from typing import Any
from modules.CalcularConRazonesT import calcular_triangulo
from modules.CalcularFiguraG import calcular_figura_interfaz
from modules.CalcularLaPendiente import calcular_pendiente_interfaz
from modules.CalcularIntegral import calcular_integral_definida, generar_figura_integral
import matplotlib.pyplot as plt

#función para formatear los resultados, quitando los decimales inútiles o redondeando a 2
def formatear_resultado(valor: Any) -> Any:
    """Limpia los números: quita decimales inútiles o redondea a 2."""
    if valor is None:
        return "No calculado"
    if isinstance(valor, (int, float)):
        if valor == int(valor):
            return int(valor)
        else:
            return round(float(valor), 2)
    return valor


def obtener_valor(mensaje):
    """Captura el dato y lo convierte a número, o devuelve None si el usuario dice 'no'."""
    entrada = input(mensaje).strip().lower()
    if entrada in ["no", ""]:
        return None
    try:
        valor = float(entrada)
        if valor <= 0:
            print("  -> Error: El valor debe ser mayor a 0. Asumiendo 'no'.")
            return None
        return valor
    except ValueError:
        print("  -> Entrada inválida, asumiendo 'no'.")
        return None


def simulador_trigonometrico():
    print("=" * 45)
    print(" SIMULADOR DE RAZONES TRIGONOMÉTRICAS ".center(45, "="))
    print("=" * 45)
    time.sleep(1)

    while True:
        print("\nPor favor, ingresa los datos paso a paso.")
        print("(Escribe 'no' si no tienes el valor de ese lado/ángulo)\n")
        time.sleep(0.5)

        # 1. Captura paso a paso
        angulo = obtener_valor("- Ingrese el ángulo (en grados): ")

        if angulo is not None and (angulo <= 0 or angulo >= 90):
            print("\n[!] Error: El ángulo debe estar entre 0 y 90 grados.")
            time.sleep(1.5)
            continue

        co = obtener_valor("- Ingrese el cateto opuesto: ")
        h = obtener_valor("- Ingrese la hipotenusa: ")
        ca = obtener_valor("- Ingrese el cateto adyacente: ")

        # 2. Validación de mínimo 2 datos
        datos_ingresados = sum(x is not None for x in [angulo, co, h, ca])
        if datos_ingresados < 2:
            print(
                "\n[!] Error: Faltan datos. Ingresa mínimo 2 valores para poder calcular."
            )
            time.sleep(1.5)
            continue

        print("\nCalculando resultados...")
        time.sleep(0.8)

        try:
            # 3. Lógica de combinaciones
            (angulo, co, ca, h), (r_ang, r_co, r_ca, r_h), razones = calcular_triangulo(angulo, co, h, ca)

        except ValueError as e:
            print(f"\n[!] Error de validación: {e}")
            time.sleep(2)
            continue
        except Exception as e:
            print(f"\n[!] Ocurrió un error inesperado al calcular: {e}")
            time.sleep(1.5)
            continue

        # 4. Impresión con efecto de movimiento
        print("\n" + "-" * 35)
        print(" RESULTADOS DEL TRIÁNGULO ".center(35))
        print("-" * 35)
        time.sleep(0.5)

        print(f"📐 Ángulo:           {formatear_resultado(r_ang)}°")
        time.sleep(0.2)
        print(f"📏 Cateto Opuesto:   {formatear_resultado(r_co)}")
        time.sleep(0.2)
        print(f"📏 Cateto Adyacente: {formatear_resultado(r_ca)}")
        time.sleep(0.2)
        print(f"📐 Hipotenusa:       {formatear_resultado(r_h)}")
        time.sleep(0.5)

        print("\n" + "-" * 35)
        print(" RAZONES TRIGONOMÉTRICAS ".center(35))
        print("-" * 35)
        time.sleep(0.5)

        print(f"🔹 Seno (sen):        {formatear_resultado(razones['sen'])}")
        time.sleep(0.15)
        print(f"🔹 Coseno (cos):      {formatear_resultado(razones['cos'])}")
        time.sleep(0.15)
        print(f"🔹 Tangente (tan):    {formatear_resultado(razones['tan'])}")
        time.sleep(0.15)
        print(f"🔹 Cosecante (csc):   {formatear_resultado(razones['csc'])}")
        time.sleep(0.15)
        print(f"🔹 Secante (sec):     {formatear_resultado(razones['sec'])}")
        time.sleep(0.15)
        print(f"🔹 Cotangente (cot):  {formatear_resultado(razones['cot'])}")
        time.sleep(0.8)

        # 5. Reinicio del ciclo
        print("-" * 35)
        continuar = (
            input("\n¿Deseas resolver otro triángulo? (si/no): ").strip().lower()
        )
        if continuar != "si":
            print("\nCerrando simulador..")
            time.sleep(1.2)
            break


def calcular_integral_consola():
    print("\n" + "=" * 45)
    print(" CÁLCULO DE INTEGRAL DEFINIDA ".center(45, "="))
    print("=" * 45)
    time.sleep(0.5)

    print("\nEjemplos de función: x**2 + 2*x, sin(x), exp(x), 1/x")
    func_str = input("- Ingresa la función f(x): ").strip()
    
    a_val = obtener_valor("- Ingresa el límite inferior (a): ")
    if a_val is None: a_val = 0
    
    b_val = obtener_valor("- Ingresa el límite superior (b): ")
    if b_val is None: b_val = 1

    print("\nCalculando...")
    time.sleep(0.8)

    try:
        area, error, _, _, _, _ = calcular_integral_definida(func_str, a_val, b_val)
        
        print("\n" + "-" * 35)
        print(" RESULTADO DE LA INTEGRAL ".center(35))
        print("-" * 35)
        print(f"📐 Función: {func_str}")
        print(f"📏 Límite a: {a_val}")
        print(f"📏 Límite b: {b_val}")
        print(f"✅ Área calculada: {area:.4f}")
        print(f"⚠️ Error estimado: {error:.4e}")
        print("-" * 35)
        
        print("\nGenerando gráfica... (Cierra la ventana de la gráfica para continuar)")
        fig = generar_figura_integral(func_str, a_val, b_val, area)
        
        # Como no estamos en Flet aquí, podemos usar plt.show()
        # Es necesario crear un "manager" si plt.subplots se llamó antes.
        # Pero generar_figura_integral devuelve la fig.
        # Para mostrarla en un entorno no interactivo normal:
        plt.show()
        
    except Exception as e:
        print(f"\n[!] Ocurrió un error al calcular la integral: {e}")
        
    input("\nPresiona Enter para volver al menú...")


def menu_principal():
    """Menú principal para elegir entre el simulador trigonométrico y el cálculo de figuras."""
    while True:
        print("\n" + "=" * 45)
        print(" MENÚ PRINCIPAL ".center(45, "="))
        print("=" * 45)
        print("1. Simulador de Razones Trigonométricas")
        print("2. Calculadora de Área y Perímetro")
        print("3. Calcular Pendiente entre dos puntos")
        print("4. Calcular Integral Definida (Área bajo la curva)")
        print("5. Salir del programa")

        opcion = input("\nElige una opción (1-5): ").strip()

        if opcion == "1":
            simulador_trigonometrico()
        elif opcion == "2":
            calcular_figura_interfaz()
        elif opcion == "3":
            calcular_pendiente_interfaz()
        elif opcion == "4":
            calcular_integral_consola()
        elif opcion == "5":
            print("\nCerrando programa... ¡Hasta luego!")
            time.sleep(1.2)
            break
        else:
            print("\n[!] Opción inválida. Intente de nuevo.")
            time.sleep(1)


if __name__ == "__main__":
    menu_principal()
