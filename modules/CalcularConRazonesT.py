import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from typing import Tuple, Optional

def calcular_triangulo(
    angulo: Optional[float], 
    co: Optional[float], 
    h: Optional[float], 
    ca: Optional[float]
) -> Tuple[Tuple[float, float, float, float], dict[str, float]]:
    """
    Valida y calcula todos los lados, ángulos y las 6 razones trigonométricas
    de un triángulo rectángulo a partir de al menos 2 datos conocidos.
    Valida la consistencia de los datos si se ingresan más de 2.
    """
    # 1. Validaciones básicas de rangos y negatividad
    for nombre, val in [("Cateto Opuesto", co), ("Cateto Adyacente", ca), ("Hipotenusa", h)]:
        if val is not None and val <= 0:
            raise ValueError(f"El valor de {nombre} debe ser estrictamente mayor que 0.")
            
    if angulo is not None and (angulo <= 0 or angulo >= 90):
        raise ValueError("El ángulo debe estar estrictamente entre 0 y 90 grados.")

    # 2. Contar datos disponibles
    datos = {
        'angulo': angulo,
        'co': co,
        'ca': ca,
        'h': h
    }
    presentes = {k: v for k, v in datos.items() if v is not None}
    
    if len(presentes) < 2:
        raise ValueError("Se requieren al menos 2 datos para calcular el triángulo.")

    rad = math.radians(angulo) if angulo is not None else None
    
    # 3. Resolver el triángulo usando un par mínimo de datos conocidos
    if 'angulo' in presentes and 'h' in presentes:
        angulo_calc, h_calc = angulo, h
        co_calc = h * math.sin(rad)
        ca_calc = h * math.cos(rad)
    elif 'angulo' in presentes and 'co' in presentes:
        angulo_calc, co_calc = angulo, co
        h_calc = co / math.sin(rad)
        ca_calc = co / math.tan(rad)
    elif 'angulo' in presentes and 'ca' in presentes:
        angulo_calc, ca_calc = angulo, ca
        h_calc = ca / math.cos(rad)
        co_calc = ca * math.tan(rad)
    elif 'co' in presentes and 'ca' in presentes:
        co_calc, ca_calc = co, ca
        h_calc = math.hypot(co, ca)
        angulo_calc = math.degrees(math.atan2(co, ca))
    elif 'co' in presentes and 'h' in presentes:
        co_calc, h_calc = co, h
        if co >= h:
            raise ValueError("El cateto opuesto no puede ser mayor o igual a la hipotenusa.")
        ca_calc = math.sqrt(h**2 - co**2)
        angulo_calc = math.degrees(math.asin(co / h))
    elif 'ca' in presentes and 'h' in presentes:
        ca_calc, h_calc = ca, h
        if ca >= h:
            raise ValueError("El cateto adyacente no puede ser mayor o igual a la hipotenusa.")
        co_calc = math.sqrt(h**2 - ca**2)
        angulo_calc = math.degrees(math.acos(ca / h))
    else:
        raise ValueError("Combinación de datos no soportada.")

    # 4. Validar consistencia con otros datos ingresados
    tolerancia = 1e-4
    if 'angulo' in presentes and not math.isclose(angulo, angulo_calc, abs_tol=tolerancia):
        raise ValueError(f"Inconsistencia: El ángulo ingresado ({angulo}°) no coincide con el calculado ({round(angulo_calc, 2)}°).")
    if 'co' in presentes and not math.isclose(co, co_calc, abs_tol=tolerancia):
        raise ValueError(f"Inconsistencia: El cateto opuesto ingresado ({co}) no coincide con el calculado ({round(co_calc, 2)}).")
    if 'ca' in presentes and not math.isclose(ca, ca_calc, abs_tol=tolerancia):
        raise ValueError(f"Inconsistencia: El cateto adyacente ingresado ({ca}) no coincide con el calculado ({round(ca_calc, 2)}).")
    if 'h' in presentes and not math.isclose(h, h_calc, abs_tol=tolerancia):
        raise ValueError(f"Inconsistencia: La hipotenusa ingresada ({h}) no coincide con la calculada ({round(h_calc, 2)}).")

    # 5. Calcular las 6 razones trigonométricas
    razones = {
        "sen": co_calc / h_calc,
        "cos": ca_calc / h_calc,
        "tan": co_calc / ca_calc,
        "csc": h_calc / co_calc,
        "sec": h_calc / ca_calc,
        "cot": ca_calc / co_calc
    }

    return (angulo_calc, co_calc, ca_calc, h_calc), razones

def generar_figura_trigonometria(co, ca, h, angulo):
    """Genera una gráfica de Matplotlib para un triángulo rectángulo estilizado."""
    fig, ax = plt.subplots(figsize=(5, 4))
    
    # Coordenadas de los vértices
    A = (0, co)
    B = (0, 0)
    C = (ca, 0)
    
    # Dibujar los lados
    ax.plot([B[0], C[0]], [B[1], C[1]], color='#2563EB', linewidth=3, label=f'CA = {ca:.2f}') # Cateto Adyacente (Base)
    ax.plot([B[0], A[0]], [B[1], A[1]], color='#DC2626', linewidth=3, label=f'CO = {co:.2f}') # Cateto Opuesto (Altura)
    ax.plot([C[0], A[0]], [C[1], A[1]], color='#16A34A', linewidth=3, label=f'H = {h:.2f}') # Hipotenusa
    
    # Cuadrado del ángulo recto en B
    size_rect = min(ca, co) * 0.1
    ax.plot([0, size_rect, size_rect, 0], [size_rect, size_rect, 0, 0], color='#64748B', linewidth=1.5)
    
    # Arco para el ángulo en C
    arc_size = min(ca, co) * 0.3
    arc = patches.Arc(C, width=arc_size*2, height=arc_size*2, theta1=180-angulo, theta2=180, color='#9333EA', linewidth=2)
    ax.add_patch(arc)
    
    # Texto del ángulo
    ax.text(ca - arc_size*1.2, arc_size*0.3, f"{angulo:.1f}°", color='#9333EA', fontweight='bold', fontsize=11)
    
    # Eliminar ejes
    ax.axis('off')
    
    # Ajustar límites para que encaje bien
    margen_x = ca * 0.1
    margen_y = co * 0.1
    ax.set_xlim(-margen_x, ca + margen_x)
    ax.set_ylim(-margen_y, co + margen_y)
    
    # Leyenda moderna
    legend = ax.legend(loc='upper right', frameon=True, facecolor='#F8FAFC', edgecolor='#CBD5E1', labelcolor='#1E293B', fontsize=10)
    legend.get_frame().set_alpha(0.85)
    
    fig.patch.set_alpha(0.0)
    ax.set_facecolor((0, 0, 0, 0))
    fig.tight_layout()
    return fig

def generar_imagen_lados(ang, co, ca, h, r_ang, r_co, r_ca, r_h):
    fig, ax = plt.subplots(figsize=(5, 1.2))
    
    texto_paso1 = ""
    if co is not None and ca is not None:
        texto_paso1 += r"$H = \sqrt{CO^2 + CA^2} = \sqrt{" + f"{co}^2 + {ca}^2" + r"} = " + f"{r_h:.2f}$\n"
        texto_paso1 += r"$\theta = \arctan(\frac{CO}{CA}) = \arctan(\frac{" + f"{co}" + r"}{" + f"{ca}" + r"}) = " + f"{r_ang:.2f}^\\circ$"
    elif h is not None and co is not None:
        texto_paso1 += r"$CA = \sqrt{H^2 - CO^2} = \sqrt{" + f"{h}^2 - {co}^2" + r"} = " + f"{r_ca:.2f}$\n"
        texto_paso1 += r"$\theta = \arcsin(\frac{CO}{H}) = \arcsin(\frac{" + f"{co}" + r"}{" + f"{h}" + r"}) = " + f"{r_ang:.2f}^\\circ$"
    elif h is not None and ca is not None:
        texto_paso1 += r"$CO = \sqrt{H^2 - CA^2} = \sqrt{" + f"{h}^2 - {ca}^2" + r"} = " + f"{r_co:.2f}$\n"
        texto_paso1 += r"$\theta = \arccos(\frac{CA}{H}) = \arccos(\frac{" + f"{ca}" + r"}{" + f"{h}" + r"}) = " + f"{r_ang:.2f}^\\circ$"
    elif ang is not None and h is not None:
        texto_paso1 += r"$CO = H \cdot \sin(\theta) = " + rf"{h} \cdot \sin({ang}^\circ) = {r_co:.2f}$\n"
        texto_paso1 += r"$CA = H \cdot \cos(\theta) = " + rf"{h} \cdot \cos({ang}^\circ) = {r_ca:.2f}$"
    elif ang is not None and co is not None:
        texto_paso1 += r"$H = \frac{CO}{\sin(\theta)} = \frac{" + f"{co}" + r"}{\sin(" + f"{ang}^\\circ" + r")} = " + f"{r_h:.2f}$\n"
        texto_paso1 += r"$CA = \frac{CO}{\tan(\theta)} = \frac{" + f"{co}" + r"}{\tan(" + f"{ang}^\\circ" + r")} = " + f"{r_ca:.2f}$"
    elif ang is not None and ca is not None:
        texto_paso1 += r"$H = \frac{CA}{\cos(\theta)} = \frac{" + f"{ca}" + r"}{\cos(" + f"{ang}^\\circ" + r")} = " + f"{r_h:.2f}$\n"
        texto_paso1 += r"$CO = CA \cdot \tan(\theta) = " + rf"{ca} \cdot \tan({ang}^\circ) = {r_co:.2f}$"
    else:
        texto_paso1 += f"$\\theta = {r_ang:.2f}^\\circ$\n"
        texto_paso1 += f"$CO = {r_co:.2f}, \\quad CA = {r_ca:.2f}, \\quad H = {r_h:.2f}$"
        
    ax.text(0.01, 0.9, texto_paso1, fontsize=14, va='top', ha='left', color='#1E293B', linespacing=1.6)
    ax.axis('off')
    fig.patch.set_alpha(0.0)
    ax.set_facecolor((0, 0, 0, 0))
    fig.tight_layout()
    return fig

def generar_imagen_razones(r_ang, r_co, r_ca, r_h, razones):
    fig, ax = plt.subplots(figsize=(5, 3.2))
    texto = (
        f"$\\sin(\\theta) = \\frac{{CO}}{{H}} = \\frac{{{r_co:.2f}}}{{{r_h:.2f}}} = {razones['sen']:.4f}$\n\n"
        f"$\\cos(\\theta) = \\frac{{CA}}{{H}} = \\frac{{{r_ca:.2f}}}{{{r_h:.2f}}} = {razones['cos']:.4f}$\n\n"
        f"$\\tan(\\theta) = \\frac{{CO}}{{CA}} = \\frac{{{r_co:.2f}}}{{{r_ca:.2f}}} = {razones['tan']:.4f}$\n\n"
        f"$\\csc(\\theta) = \\frac{{H}}{{CO}} = \\frac{{{r_h:.2f}}}{{{r_co:.2f}}} = {razones['csc']:.4f}$\n\n"
        f"$\\sec(\\theta) = \\frac{{H}}{{CA}} = \\frac{{{r_h:.2f}}}{{{r_ca:.2f}}} = {razones['sec']:.4f}$\n\n"
        f"$\\cot(\\theta) = \\frac{{CA}}{{CO}} = \\frac{{{r_ca:.2f}}}{{{r_co:.2f}}} = {razones['cot']:.4f}$"
    )
    ax.text(0.01, 0.95, texto, fontsize=14, va='top', ha='left', color='#1E293B', linespacing=1.6)
    ax.axis('off')
    fig.patch.set_alpha(0.0)
    ax.set_facecolor((0, 0, 0, 0))
    fig.tight_layout()
    return fig
