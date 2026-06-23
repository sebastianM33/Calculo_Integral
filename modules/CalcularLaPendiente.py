import time
import matplotlib.pyplot as plt
import numpy as np
def calcular_pendiente(x1, y1, x2, y2):
    """
    Calcula la pendiente entre dos puntos y devuelve una tupla con el valor
    y el procedimiento paso a paso en formato de texto.
    """
    if x1 == x2:
        raise ValueError("x1 y x2 no pueden ser iguales (división por cero), la línea es vertical y la pendiente es indefinida.")
    
    pendiente = (y2 - y1) / (x2 - x1)
    
    # Construir el procedimiento
    procedimiento = [
        ("Fórmula de la Pendiente", "m = (y2 - y1) / (x2 - x1)"),
        ("Sustitución de Valores", f"m = ({y2} - {y1}) / ({x2} - {x1})"),
        ("Cálculo de Diferencias", f"m = ({y2 - y1}) / ({x2 - x1})"),
        ("Resultado Final", f"m = {round(pendiente, 4)}")
    ]
    
    return pendiente, procedimiento

def obtener_valor(mensaje):
    while True:
        entrada = input(mensaje).strip()
        try:
            return float(entrada)
        except ValueError:
            print("  -> Entrada inválida. Ingresa un número válido.")

def calcular_pendiente_interfaz():
    """Menú interactivo de consola para la pendiente."""
    while True:
        print("\n" + "="*45)
        print(" CÁLCULO DE PENDIENTE (DERIVADA) ".center(45, "="))
        print("="*45)
        
        print("\nIngrese las coordenadas del Primer Punto A(x1, y1):")
        x1 = obtener_valor("- x1: ")
        y1 = obtener_valor("- y1: ")
        
        print("\nIngrese las coordenadas del Segundo Punto B(x2, y2):")
        x2 = obtener_valor("- x2: ")
        y2 = obtener_valor("- y2: ")
        
        print("\nCalculando...")
        time.sleep(1)
        
        try:
            m, procedimiento = calcular_pendiente(x1, y1, x2, y2)
            print("\n" + "-"*35)
            print(" PROCEDIMIENTO Y RESULTADO ".center(35))
            print("-"*35)
            print(f"\n{procedimiento}")
            
        except ValueError as e:
            print(f"\n[!] Error: {e}")
            
        print("\n" + "-"*35)
        continuar = input("¿Deseas calcular otra pendiente? (si/no): ").strip().lower()
        if continuar != 'si':
            print("\nRegresando al menú principal...")
            time.sleep(1)
            break

def generar_figura_pendiente(x1, y1, x2, y2, m):
    """Genera una gráfica de Matplotlib para la recta que pasa por dos puntos."""
    fig, ax = plt.subplots(figsize=(8, 4.5))
    
    # Calcular rango para visualización amplia
    min_x = min(x1, x2)
    max_x = max(x1, x2)
    margen_x = max((max_x - min_x) * 0.8, 2)
    
    x_vals = np.linspace(min_x - margen_x, max_x + margen_x, 100)
    
    # Ecuación de la recta: y = m(x - x1) + y1
    y_vals = m * (x_vals - x1) + y1
    
    # Graficar la recta
    ax.plot(x_vals, y_vals, color='#9333EA', linewidth=3, label=f'Pendiente $m = {m:.2f}$', zorder=3)
    
    # Graficar los puntos
    ax.scatter([x1, x2], [y1, y2], color='#EF4444', s=80, zorder=4)
    
    # Textos de los puntos
    ax.annotate(f'A({x1}, {y1})', (x1, y1), textcoords="offset points", xytext=(0,12), ha='center', color='#B91C1C', fontweight='bold')
    ax.annotate(f'B({x2}, {y2})', (x2, y2), textcoords="offset points", xytext=(0,12), ha='center', color='#1D4ED8', fontweight='bold')
    
    # Configuración de ejes visualmente estéticos
    ax.axhline(0, color='#94A3B8', linewidth=1.2, alpha=0.8, zorder=1)
    ax.axvline(0, color='#94A3B8', linewidth=1.2, alpha=0.8, zorder=1)
    
    # Cuadrícula suave adaptada a tema claro
    ax.grid(True, linestyle='-', alpha=0.5, color='#F1F5F9', zorder=0)
    
    # Eliminar bordes fuertes
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#CBD5E1')
    ax.spines['bottom'].set_color('#CBD5E1')
    
    # Títulos y fuentes
    ax.set_title("Gráfica de la Recta", color='#1E293B', fontsize=16, fontweight='600', pad=15)
    ax.set_xlabel('Eje X', color='#475569', fontsize=11, fontweight='500')
    ax.set_ylabel('Eje Y', color='#475569', fontsize=11, fontweight='500')
    
    ax.tick_params(axis='x', colors='#475569', labelsize=10)
    ax.tick_params(axis='y', colors='#475569', labelsize=10)
    
    # Ajustes de límites (Zoom out)
    y_min, y_max = min(y_vals), max(y_vals)
    margen_y = max((y_max - y_min) * 0.3, 2)
    ax.set_ylim(y_min - margen_y, y_max + margen_y)
    ax.set_xlim(min_x - margen_x, max_x + margen_x)
    
    # Leyenda moderna y con estilo
    legend = ax.legend(loc='best', frameon=True, facecolor='#FFFFFF', edgecolor='#E2E8F0', labelcolor='#1E293B', fontsize=11)
    legend.get_frame().set_alpha(0.85)
    
    fig.patch.set_alpha(0.0)
    ax.set_facecolor((0, 0, 0, 0))
    return fig

def generar_procedimiento_pendiente_imagen(x1, y1, x2, y2, m):
    """Genera una imagen con el procedimiento paso a paso renderizado en formato matemático (LaTeX)."""
    fig, ax = plt.subplots(figsize=(3.5, 2))
    
    # Manejar signos en la sustitución para evitar "--"
    num_y1 = f"({y1})" if y1 < 0 else f"{y1}"
    num_x1 = f"({x1})" if x1 < 0 else f"{x1}"
    
    texto = (
        r"$m = \frac{y_2 - y_1}{x_2 - x_1}$" + "\n\n"
        f"$m = \\frac{{{y2} - {num_y1}}}{{{x2} - {num_x1}}}$\n\n"
        f"$m = {m:.4g}$"
    )
    
    ax.text(0.02, 0.98, texto, fontsize=14, va='top', ha='left', color='#1E293B', linespacing=1.6)
    
    ax.axis('off')
    fig.patch.set_alpha(0.0)
    ax.set_facecolor((0, 0, 0, 0))
    fig.tight_layout()
    return fig
