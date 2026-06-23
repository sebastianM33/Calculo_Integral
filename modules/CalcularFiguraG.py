import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def calcular_cuadrado(lado):
    area = lado ** 2
    perimetro = 4 * lado
    return area, perimetro

def calcular_rectangulo(base, altura):
    area = base * altura
    perimetro = 2 * (base + altura)
    return area, perimetro

def calcular_circulo(radio):
    area = math.pi * (radio ** 2)
    perimetro = 2 * math.pi * radio
    return area, perimetro

def calcular_triangulo(base, altura, l1, l2, l3):
    area = (base * altura) / 2
    perimetro = l1 + l2 + l3
    return area, perimetro

def calcular_poligono_regular(n, lado):
    perimetro = n * lado
    apotema = lado / (2 * math.tan(math.pi / n))
    area = (perimetro * apotema) / 2
    return area, perimetro

def calcular_figura_interfaz():
    import time
    def obtener_valor(mensaje):
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

    def formatear_resultado(valor):
        if valor is None:
            return "No calculado"
        if isinstance(valor, (int, float)):
            if valor == int(valor):
                return int(valor)
            else:
                return round(float(valor), 2)
        return valor

    while True:
        print("\n" + "=" * 45)
        print(" CALCULADORA DE ÁREA Y PERÍMETRO ".center(45, "="))
        print("=" * 45)
        print("1. Cuadrado")
        print("2. Rectángulo")
        print("3. Círculo")
        print("4. Triángulo")
        print("5. Polígono Regular")
        print("6. Volver al menú principal")

        opcion = input("\nElige una figura (1-6): ").strip()

        if opcion == "6":
            break

        if opcion == "1":
            lado = obtener_valor("Ingrese el lado del cuadrado: ")
            if lado is not None:
                a, p = calcular_cuadrado(lado)
                print(f"\nÁrea: {formatear_resultado(a)}")
                print(f"Perímetro: {formatear_resultado(p)}")
                
        elif opcion == "2":
            base = obtener_valor("Ingrese la base del rectángulo: ")
            altura = obtener_valor("Ingrese la altura del rectángulo: ")
            if base is not None and altura is not None:
                a, p = calcular_rectangulo(base, altura)
                print(f"\nÁrea: {formatear_resultado(a)}")
                print(f"Perímetro: {formatear_resultado(p)}")
        elif opcion == "3":
            radio = obtener_valor("Ingrese el radio del círculo: ")
            if radio is not None:
                a, p = calcular_circulo(radio)
                print(f"\nÁrea: {formatear_resultado(a)}")
                print(f"Perímetro: {formatear_resultado(p)}")
        elif opcion == "4":
            base = obtener_valor("Ingrese la base del triángulo (para área): ")
            altura = obtener_valor("Ingrese la altura del triángulo (para área): ")
            l1 = obtener_valor("Ingrese el lado 1 (para perímetro): ")
            l2 = obtener_valor("Ingrese el lado 2 (para perímetro): ")
            l3 = obtener_valor("Ingrese el lado 3 (para perímetro): ")
            if base is not None and altura is not None and l1 is not None and l2 is not None and l3 is not None:
                a, p = calcular_triangulo(base, altura, l1, l2, l3)
                print(f"\nÁrea: {formatear_resultado(a)}")
                print(f"Perímetro: {formatear_resultado(p)}")
        elif opcion == "5":
            n = obtener_valor("Ingrese el número de lados del polígono: ")
            lado = obtener_valor("Ingrese la longitud del lado: ")
            if n is not None and lado is not None:
                n_int = int(n)
                if n_int < 3:
                    print("\n[!] Error: El número de lados debe ser al menos 3.")
                else:
                    a, p = calcular_poligono_regular(n_int, lado)
                    print(f"\nÁrea: {formatear_resultado(a)}")
                    print(f"Perímetro: {formatear_resultado(p)}")
        else:
            print("\n[!] Opción inválida.")
            
        time.sleep(1)

def generar_figura_geometria(tipo, valores):
    """Genera una gráfica de Matplotlib para una forma geométrica."""
    fig, ax = plt.subplots(figsize=(4, 4))
    
    if tipo == "Cuadrado":
        l = valores['lado']
        rect = patches.Rectangle((-l/2, -l/2), l, l, linewidth=2, edgecolor='#16A34A', facecolor='#BBF7D0', alpha=0.8)
        ax.add_patch(rect)
        ax.set_xlim(-l*1.2, l*1.2)
        ax.set_ylim(-l*1.2, l*1.2)
        ax.text(0, -l/2 - l*0.1, f"L = {l:.2f}", ha='center', fontweight='bold', color='#15803D')
        ax.text(l/2 + l*0.1, 0, f"L = {l:.2f}", va='center', fontweight='bold', color='#15803D')
        
    elif tipo == "Rectángulo":
        b, h = valores['base'], valores['altura']
        rect = patches.Rectangle((-b/2, -h/2), b, h, linewidth=2, edgecolor='#D97706', facecolor='#FDE68A', alpha=0.8)
        ax.add_patch(rect)
        max_dim = max(b, h)
        ax.set_xlim(-max_dim*1.2, max_dim*1.2)
        ax.set_ylim(-max_dim*1.2, max_dim*1.2)
        ax.text(0, -h/2 - max_dim*0.1, f"b = {b:.2f}", ha='center', fontweight='bold', color='#B45309')
        ax.text(b/2 + max_dim*0.1, 0, f"h = {h:.2f}", va='center', fontweight='bold', color='#B45309')
        
    elif tipo == "Círculo":
        r = valores['radio']
        circ = patches.Circle((0, 0), r, linewidth=2, edgecolor='#DB2777', facecolor='#FBCFE8', alpha=0.8)
        ax.add_patch(circ)
        ax.plot([0, r], [0, 0], color='#BE185D', linewidth=2, linestyle='--')
        ax.set_xlim(-r*1.3, r*1.3)
        ax.set_ylim(-r*1.3, r*1.3)
        ax.text(r/2, r*0.1, f"r = {r:.2f}", ha='center', fontweight='bold', color='#9D174D')
        
    elif tipo == "Triángulo":
        b, h = valores['base'], valores['altura']
        triangle = patches.Polygon([(-b/2, -h/2), (b/2, -h/2), (0, h/2)], linewidth=2, edgecolor='#CA8A04', facecolor='#FEF08A', alpha=0.8)
        ax.add_patch(triangle)
        ax.plot([0, 0], [-h/2, h/2], color='#A16207', linewidth=2, linestyle='--') # Altura punteada
        max_dim = max(b, h)
        ax.set_xlim(-max_dim*1.2, max_dim*1.2)
        ax.set_ylim(-max_dim*1.2, max_dim*1.2)
        ax.text(0, -h/2 - max_dim*0.1, f"b = {b:.2f}", ha='center', fontweight='bold', color='#854D0E')
        ax.text(max_dim*0.1, 0, f"h = {h:.2f}", va='center', fontweight='bold', color='#854D0E')
        
    elif tipo == "Polígono Regular":
        n, l = valores['n_lados'], valores['lado']
        R = l / (2 * math.sin(math.pi / n))
        pts = []
        for i in range(n):
            angle = 2 * math.pi * i / n - math.pi / 2
            pts.append((R * math.cos(angle), R * math.sin(angle)))
            
        poly = patches.Polygon(pts, linewidth=2, edgecolor='#7E22CE', facecolor='#E9D5FF', alpha=0.8)
        ax.add_patch(poly)
        ax.set_xlim(-R*1.3, R*1.3)
        ax.set_ylim(-R*1.3, R*1.3)
        ax.text(0, -R*1.15, f"L = {l:.2f}  |  n = {n}", ha='center', va='top', fontweight='bold', color='#6B21A8')
        
    ax.axis('off')
    ax.set_aspect('equal', adjustable='box')
    fig.patch.set_alpha(0.0)
    fig.tight_layout()
    return fig

def generar_procedimiento_geometria_imagen(tipo, valores, a, p):
    """Genera una imagen con el procedimiento paso a paso renderizado en formato matemático (LaTeX)."""
    fig, ax = plt.subplots(figsize=(4.5, 2.5))
    
    texto = ""
    
    if tipo == "Cuadrado":
        l = valores['lado']
        texto += r"$\mathbf{Perimetro:}$" + "\n"
        texto += r"$P = 4 \cdot L$" + "\n"
        texto += rf"$P = 4 \cdot {l} = {p:.4g}$" + "\n\n"
        texto += r"$\mathbf{Area:}$" + "\n"
        texto += r"$A = L^2$" + "\n"
        texto += f"$A = {l}^2 = {a:.4g}$"
        
    elif tipo == "Rectángulo":
        b, h = valores['base'], valores['altura']
        texto += r"$\mathbf{Perimetro:}$" + "\n"
        texto += r"$P = 2 \cdot (b + h)$" + "\n"
        texto += rf"$P = 2 \cdot ({b} + {h}) = {p:.4g}$" + "\n\n"
        texto += r"$\mathbf{Area:}$" + "\n"
        texto += r"$A = b \cdot h$" + "\n"
        texto += rf"$A = {b} \cdot {h} = {a:.4g}$"
        
    elif tipo == "Círculo":
        r = valores['radio']
        texto += r"$\mathbf{Perimetro\;(Circunferencia):}$" + "\n"
        texto += r"$P = 2 \cdot \pi \cdot r$" + "\n"
        texto += rf"$P = 2 \cdot \pi \cdot {r} \approx {p:.4g}$" + "\n\n"
        texto += r"$\mathbf{Area:}$" + "\n"
        texto += r"$A = \pi \cdot r^2$" + "\n"
        texto += rf"$A = \pi \cdot {r}^2 \approx {a:.4g}$"
        
    elif tipo == "Triángulo":
        b, h = valores['base'], valores['altura']
        l1, l2, l3 = valores.get('l1', 0), valores.get('l2', 0), valores.get('l3', 0)
        
        texto += r"$\mathbf{Perimetro:}$" + "\n"
        if l1 > 0 and l2 > 0 and l3 > 0:
            texto += r"$P = L_1 + L_2 + L_3$" + "\n"
            texto += f"$P = {l1} + {l2} + {l3} = {p:.4g}$\n\n"
        else:
            texto += r"$P = L_1 + L_2 + L_3$" + "\n"
            texto += "*(Lados incompletos para calcular perimetro)*\n\n"
            
        texto += r"$\mathbf{Area:}$" + "\n"
        texto += r"$A = \frac{b \cdot h}{2}$" + "\n"
        texto += rf"$A = \frac{{{b} \cdot {h}}}{{2}} = {a:.4g}$"
        
    elif tipo == "Polígono Regular":
        n, l = valores['n_lados'], valores['lado']
        texto += r"$\mathbf{Perimetro:}$" + "\n"
        texto += r"$P = n \cdot L$" + "\n"
        texto += rf"$P = {n} \cdot {l} = {p:.4g}$" + "\n\n"
        
        texto += r"$\mathbf{Apotema\;y\;Area:}$" + "\n"
        texto += r"$ap = \frac{L}{2 \cdot \tan(\frac{\pi}{n})}$" + "\n"
        texto += r"$A = \frac{P \cdot ap}{2}$" + "\n"
        texto += f"$A \approx {a:.4g}$"
        
    ax.text(0.02, 0.98, texto, fontsize=14, va='top', ha='left', color='#1E293B', linespacing=1.6)
    
    ax.axis('off')
    fig.patch.set_alpha(0.0)
    ax.set_facecolor((0, 0, 0, 0))
    fig.tight_layout()
    return fig