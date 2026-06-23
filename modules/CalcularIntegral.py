import numpy as np
import scipy.integrate as integrate
import matplotlib.pyplot as plt
import sympy as sp

from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

def interpretar_funcion(func_str):
    try:
        func_str_clean = func_str.lower().replace('np.', '').replace('math.', '')
        func_str_clean = func_str_clean.replace('^', '**')
        
        transformations = (standard_transformations + (implicit_multiplication_application,))
        expr = parse_expr(func_str_clean, transformations=transformations)
        
        simbolos = list(expr.free_symbols)
        if len(simbolos) > 1:
            raise ValueError("La expresión solo puede tener una variable.")
        var_sym = simbolos[0] if simbolos else sp.Symbol('x')
        
        def func_numpy(val):
            pass
            
        func = sp.lambdify(var_sym, expr, "numpy")
        return func, expr, var_sym
    except Exception as e:
        raise ValueError("Expresión matemática inválida o no soportada. Revisa la sintaxis.")

def calcular_integral_definida(func_str, a, b):
    func, expr, x_sym = interpretar_funcion(func_str)
    
    # Calcular usando scipy
    area_num, error = integrate.quad(func, a, b)
    
    # Intentar cálculo Simbólico para fracción exacta
    area_simbolica = None
    resultado_exacto_latex = ""
    try:
        integral_indefinida = sp.integrate(expr, x_sym)
        res_exacto = integral_indefinida.subs(x_sym, b) - integral_indefinida.subs(x_sym, a)
        res_exacto = sp.simplify(res_exacto)
        
        if not res_exacto.has(sp.Integral):
            area_simbolica = res_exacto
            resultado_exacto_latex = sp.latex(res_exacto)
    except:
        pass
        
    return area_num, error, func, expr, area_simbolica, resultado_exacto_latex

def generar_procedimiento_integral_imagen(expr, a, b, area_simbolica, area_num):
    fig, ax = plt.subplots(figsize=(6, 4.5))
    
    simbolos = list(expr.free_symbols)
    var_sym = simbolos[0] if simbolos else sp.Symbol('x')
    var_name = var_sym.name
    
    latex_expr = sp.latex(expr)
    
    try:
        indefinida = sp.integrate(expr, var_sym)
        latex_indefinida = sp.latex(indefinida)
        latex_sub_b = sp.latex(indefinida.subs(var_sym, sp.Symbol(f"({b})", evaluate=False)))
        latex_sub_a = sp.latex(indefinida.subs(var_sym, sp.Symbol(f"({a})", evaluate=False)))
        
        val_b = sp.simplify(indefinida.subs(var_sym, b))
        val_a = sp.simplify(indefinida.subs(var_sym, a))
        latex_val_b = sp.latex(val_b)
        latex_val_a = sp.latex(val_a)
    except:
        latex_indefinida = "\\dots"
        latex_sub_b = "\\dots"
        latex_sub_a = "\\dots"
        latex_val_b = "\\dots"
        latex_val_a = "\\dots"
    
    texto = f"$I = \\int_{{{a}}}^{{{b}}} \\left( {latex_expr} \\right) d{var_name}$\n\n"
    texto += f"$F({var_name}) = {latex_indefinida}$\n\n"
    if latex_sub_b != "\\dots":
        texto += f"$I = \\left[ {latex_sub_b} \\right] - \\left[ {latex_sub_a} \\right]$\n\n"
        # Mostrar el resultado parcial si es diferente a la sustitución en bruto
        if latex_val_b != latex_sub_b or latex_val_a != latex_sub_a:
            texto += f"$I = \\left[ {latex_val_b} \\right] - \\left[ {latex_val_a} \\right]$\n\n"
    else:
        texto += f"$I = F({b}) - F({a})$\n\n"
    
    area_fmt = f"{int(round(area_num))}" if abs(area_num - round(area_num)) < 1e-9 else f"{area_num:.4f}"
    if area_simbolica is not None:
        latex_res = sp.latex(area_simbolica)
        texto += f"$I = {latex_res} \\approx {area_fmt}$"
    else:
        texto += f"$I \\approx {area_fmt}$"
        
    ax.text(0.02, 0.98, texto, fontsize=12.5, va='top', ha='left', color='#1E293B', linespacing=1.6)
    
    ax.axis('off')
    fig.patch.set_alpha(0.0)
    ax.set_facecolor((0, 0, 0, 0))
    fig.tight_layout()
    return fig

def generar_figura_integral(func_str, a, b, area):
    func, expr, x_sym = interpretar_funcion(func_str)
    
    fig, ax = plt.subplots(figsize=(8, 4.5))
    
    rango = b - a
    if rango == 0:
        rango = 2
        a = a - 1
        b = b + 1
        
    margen = rango * 0.8
    x_vals = np.linspace(a - margen, b + margen, 600)
    
    try:
        y_vals = func(x_vals)
        if np.isscalar(y_vals):
            y_vals = np.full_like(x_vals, float(y_vals))
    except:
        y_vals = np.array([func(val) for val in x_vals])
        
    ax.plot(x_vals, y_vals, color='#F472B6', linewidth=3, label=f'$f(x)$', zorder=3)
    
    ix = np.linspace(a, b, 200)
    try:
        iy = func(ix)
        if np.isscalar(iy):
            iy = np.full_like(ix, float(iy))
    except:
        iy = np.array([func(val) for val in ix])
        
    ax.fill_between(ix, iy, color='#818CF8', alpha=0.35, label=f'Área $\\approx$ {area:.4f}', zorder=2)
    
    y_min, y_max = np.min(y_vals), np.max(y_vals)
    rango_y = y_max - y_min if y_max != y_min else 2
    ax.set_ylim(y_min - rango_y * 0.3, y_max + rango_y * 0.4)
    ax.set_xlim(a - margen, b + margen)
    
    ax.axhline(0, color='#94A3B8', linewidth=1.2, alpha=0.8, zorder=1)
    ax.axvline(0, color='#94A3B8', linewidth=1.2, alpha=0.8, zorder=1)
    
    ax.grid(True, linestyle='-', alpha=0.5, color='#F1F5F9', zorder=0)
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#CBD5E1')
    ax.spines['bottom'].set_color('#CBD5E1')
    
    ax.set_title("Gráfica de la Integral Definida", color='#1E293B', fontsize=16, fontweight='600', pad=15)
    ax.set_xlabel('Eje X', color='#475569', fontsize=11, fontweight='500')
    ax.set_ylabel('Eje Y ( f(x) )', color='#475569', fontsize=11, fontweight='500')
    
    ax.tick_params(axis='x', colors='#475569', labelsize=10)
    ax.tick_params(axis='y', colors='#475569', labelsize=10)
    
    legend = ax.legend(loc='best', frameon=True, facecolor='#FFFFFF', edgecolor='#E2E8F0', labelcolor='#1E293B', fontsize=11)
    legend.get_frame().set_alpha(0.85)
    
    fig.patch.set_alpha(0.0)
    ax.set_facecolor((0, 0, 0, 0))
    
    fig.tight_layout()
    return fig
