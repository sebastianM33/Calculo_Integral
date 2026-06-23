import flet as ft
import math
import os
import warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)
from typing import Any
import io
import base64
import matplotlib.pyplot as plt
plt.rcParams['mathtext.fontset'] = 'cm'

# Importaciones lógicas
from modules.CalcularConRazonesT import calcular_triangulo, generar_figura_trigonometria, generar_imagen_lados, generar_imagen_razones
import modules.CalcularFiguraG as cp
from modules.CalcularFiguraG import generar_figura_geometria, generar_procedimiento_geometria_imagen
from modules.CalcularLaPendiente import calcular_pendiente, generar_figura_pendiente, generar_procedimiento_pendiente_imagen
from modules.CalcularIntegral import calcular_integral_definida, generar_figura_integral, generar_procedimiento_integral_imagen

def main(page: ft.Page):
    page.title = "Suite Matemática"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#F8FAFC"
    page.window_width = 1350
    page.window_height = 900
    page.padding = 0

    integral_steps_data = []
    trig_steps_data = []
    geo_steps_data = []
    pend_steps_data = []

    def format_val(v):
        if v is None: return "N/A"
        if int(v) == v: return str(int(v))
        return f"{v:.2f}"

    input_style = {
        "border_radius": 8, 
        "border_width": 1, 
        "height": 45,
        "bgcolor": "#FFFFFF",
        "border_color": "#CBD5E1",
        "color": "#1E293B",
        "content_padding": 12,
        "cursor_color": ft.Colors.BLUE_500
    }
    
    panel_style = {
        "bgcolor": ft.Colors.WHITE,
        "border_radius": 16,
        "padding": 30,
        "border": ft.Border.all(1, "#E2E8F0"),
        "shadow": ft.BoxShadow(
            spread_radius=0, blur_radius=15, 
            color=ft.colors.with_opacity(0.04, ft.Colors.BLACK) if hasattr(ft, 'colors') else ft.Colors.with_opacity(0.04, ft.Colors.BLACK), 
            offset=ft.Offset(0, 4)
        )
    }

    def page_header(title, subtitle, icon_name, color):
        return ft.Column([
            ft.Row([
                ft.Icon(icon_name, size=32, color=color),
                ft.Text(title, size=32, weight=ft.FontWeight.W_800, color="#0F172A"),
            ], alignment=ft.MainAxisAlignment.START, spacing=15),
            ft.Text(subtitle, color="#64748B", size=15),
            ft.Divider(height=30, color="transparent")
        ], spacing=5)

    def section_title(text, color="#0F172A"):
        return ft.Column([
            ft.Text(text, weight=ft.FontWeight.BOLD, color=color, size=14),
            ft.Divider(color="#F1F5F9", height=15)
        ], spacing=2)

    def format_math_expression(expr_str):
        import re
        s = str(expr_str)
        s = re.sub(r'(\d+)\*(x|[a-zA-Z\(])', r'\1\2', s)
        s = s.replace('**2', '²').replace('**3', '³').replace('**4', '⁴').replace('**5', '⁵')
        s = s.replace('**', '^')
        s = s.replace('*', ' · ')
        s = s.replace('pi', 'π')
        s = s.replace('sqrt', '√')
        return s

    def crear_placeholder(icon_name, title, subtitle, color):
        return ft.Container(
            content=ft.Column([
                ft.Icon(icon_name, size=44, color=color),
                ft.Text(title, size=15, weight=ft.FontWeight.BOLD, color="#475569"),
                ft.Text(subtitle, size=12, color="#94A3B8", text_align=ft.TextAlign.CENTER),
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=6),
            alignment=ft.Alignment(0, 0),
            expand=True,
            padding=20
        )

    def build_steps_list(steps, color="#6366F1"):
        controls = []
        for i, step_data in enumerate(steps):
            title = step_data[0]
            detail = step_data[1]
            img_b64 = step_data[2] if len(step_data) > 2 else None
            
            content_col = [
                ft.Text(title, size=13, weight=ft.FontWeight.BOLD, color="#1E293B"),
            ]
            if detail:
                content_col.append(ft.Text(detail, size=13, color="#475569", font_family="monospace" if ("=" in detail or "\n" in detail) else None))
            if img_b64:
                content_col.append(
                    ft.Container(
                        content=ft.Image(src=f"data:image/png;base64,{img_b64}", fit="contain"),
                        alignment=ft.Alignment(0, 0),
                        width=500
                    )
                )
                
            step_row = ft.Row([
                ft.Container(
                    content=ft.Text(str(i+1), size=11, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    bgcolor=color,
                    width=22,
                    height=22,
                    border_radius=11,
                    alignment=ft.Alignment(0, 0)
                ),
                ft.Column(content_col, spacing=2, expand=True)
            ], vertical_alignment=ft.CrossAxisAlignment.START)
            
            controls.append(
                ft.Container(
                    content=step_row,
                    padding=12,
                    bgcolor="#F8FAFC",
                    border_radius=8,
                    border=ft.Border.all(1, "#E2E8F0")
                )
            )
            
            if i < len(steps) - 1:
                controls.append(
                    ft.Row([
                        ft.Container(width=10),
                        ft.Container(width=2, height=10, bgcolor="#E2E8F0")
                    ])
                )
                
        return ft.Column(controls, spacing=0)

    # ==========================================
    # VISTA 1: TRIGONOMETRÍA
    # ==========================================
    trig_angulo = ft.TextField(label="Ángulo (°)", expand=1, focused_border_color=ft.Colors.BLUE_500, **input_style)
    trig_co = ft.TextField(label="Cat. Opuesto", expand=1, focused_border_color=ft.Colors.BLUE_500, **input_style)
    trig_ca = ft.TextField(label="Cat. Adyacente", expand=1, focused_border_color=ft.Colors.BLUE_500, **input_style)
    trig_h = ft.TextField(label="Hipotenusa", expand=1, focused_border_color=ft.Colors.BLUE_500, **input_style)
    trig_error = ft.Text(color=ft.Colors.RED_600, weight=ft.FontWeight.W_500, size=13)
    
    trig_canvas_container = ft.Container(visible=False, padding=0, height=250, alignment=ft.Alignment(0, 0))
    
    trig_res_angulo = ft.Text(size=15, color="#334155")
    trig_res_co = ft.Text(size=15, color="#334155")
    trig_res_ca = ft.Text(size=15, color="#334155")
    trig_res_h = ft.Text(size=15, color="#334155")
    
    trig_res_sen = ft.Text(size=15, color=ft.Colors.BLUE_700, weight=ft.FontWeight.W_500)
    trig_res_cos = ft.Text(size=15, color=ft.Colors.BLUE_700, weight=ft.FontWeight.W_500)
    trig_res_tan = ft.Text(size=15, color=ft.Colors.BLUE_700, weight=ft.FontWeight.W_500)
    trig_res_csc = ft.Text(size=15, color=ft.Colors.BLUE_700, weight=ft.FontWeight.W_500)
    trig_res_sec = ft.Text(size=15, color=ft.Colors.BLUE_700, weight=ft.FontWeight.W_500)
    trig_res_cot = ft.Text(size=15, color=ft.Colors.BLUE_700, weight=ft.FontWeight.W_500)

    trig_placeholder = ft.Container(
        content=crear_placeholder(ft.Icons.GRID_VIEW_ROUNDED, "Esperando Datos", "Ingresa al menos 2 valores conocidos en el panel de la izquierda y haz clic en calcular.", ft.Colors.BLUE_400),
        **panel_style,
        width=600,
        height=420
    )

    def toggle_procedimiento_trig(e):
        if not trig_steps_data: return
        def close_dlg_instance(ev):
            ev.control.page.pop_dialog()
            ev.control.page.update()
        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Row([
                ft.Icon(ft.Icons.RECEIPT_LONG, color="#2563EB"),
                ft.Text("Procedimiento Paso a Paso", weight=ft.FontWeight.W_700, size=16, color="#0F172A"),
            ], spacing=8),
            content=ft.Container(
                width=550, padding=0,
                content=ft.Column([build_steps_list(trig_steps_data, ft.Colors.BLUE_600)], tight=True, scroll=ft.ScrollMode.AUTO)
            ),
            actions=[ft.TextButton("Cerrar", on_click=close_dlg_instance)],
            actions_alignment=ft.MainAxisAlignment.END,
            shape=ft.RoundedRectangleBorder(radius=16)
        )
        page.show_dialog(dlg)
        page.update()

    btn_ver_procedimiento_trig = ft.ElevatedButton(
        "Ver Procedimiento Paso a Paso", icon=ft.Icons.RECEIPT_LONG,
        on_click=toggle_procedimiento_trig, disabled=True,
        width=465, height=42, bgcolor="#FFFFFF", color="#2563EB",
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), side=ft.BorderSide(1, "#93C5FD"))
    )

    trig_results_column = ft.Column([
        ft.Container(
            content=ft.Column([
                ft.Container(content=trig_canvas_container, width=500, alignment=ft.Alignment(0,0)),
                ft.Divider(color="#F1F5F9", height=20),
                ft.Row([btn_ver_procedimiento_trig], alignment=ft.MainAxisAlignment.CENTER)
            ]),
            **panel_style,
            width=600
        )
    ], spacing=20, visible=False, width=600)

    def calcular_trig(e):
        trig_error.value = ""
        def parse(tf):
            val = tf.value.strip()
            if not val: return None
            try: return float(val)
            except: return None
            
        ang = parse(trig_angulo)
        co = parse(trig_co)
        ca = parse(trig_ca)
        h = parse(trig_h)
        
        try:
            (r_ang, r_co, r_ca, r_h), razones = calcular_triangulo(ang, co, h, ca)
            trig_res_angulo.value = f"📐 Ángulo: {format_val(r_ang)}°"
            trig_res_co.value = f"📏 Cat. Opuesto: {format_val(r_co)}"
            trig_res_ca.value = f"📏 Cat. Adyacente: {format_val(r_ca)}"
            trig_res_h.value = f"📏 Hipotenusa: {format_val(r_h)}"
            
            trig_res_sen.value = f"Seno: {format_val(razones['sen'])}"
            trig_res_cos.value = f"Coseno: {format_val(razones['cos'])}"
            trig_res_tan.value = f"Tangente: {format_val(razones['tan'])}"
            trig_res_csc.value = f"Cosecante: {format_val(razones['csc'])}"
            trig_res_sec.value = f"Secante: {format_val(razones['sec'])}"
            trig_res_cot.value = f"Cotangente: {format_val(razones['cot'])}"
            
            # Generar imagen LaTeX de lados
            fig_lados = generar_imagen_lados(ang, co, ca, h, r_ang, r_co, r_ca, r_h)
            buf_lados = io.BytesIO()
            fig_lados.savefig(buf_lados, format="png", bbox_inches='tight', transparent=True, dpi=120)
            buf_lados.seek(0)
            img_lados_base64 = base64.b64encode(buf_lados.read()).decode("utf-8")
            plt.close(fig_lados)

            # Generar imagen LaTeX de razones
            fig_razones = generar_imagen_razones(r_ang, r_co, r_ca, r_h, razones)
            buf_razones = io.BytesIO()
            fig_razones.savefig(buf_razones, format="png", bbox_inches='tight', transparent=True, dpi=120)
            buf_razones.seek(0)
            img_razones_base64 = base64.b64encode(buf_razones.read()).decode("utf-8")
            plt.close(fig_razones)
            
            trig_steps_data.clear()
            
            trig_steps_data.extend([
                ("Datos Iniciales Conocidos", f"Ángulo = {ang if ang else r_ang}°, Cateto Adyacente = {ca if ca else r_ca}, ..."),
                ("Cálculo de Lados y Ángulo Faltantes", None, img_lados_base64),
                ("Cálculo de Razones Trigonométricas", None, img_razones_base64)
            ])
            
            btn_ver_procedimiento_trig.disabled = False
            
            fig_trig = generar_figura_trigonometria(r_co, r_ca, r_h, r_ang)
            buf = io.BytesIO()
            fig_trig.savefig(buf, format="png", bbox_inches='tight', transparent=True)
            buf.seek(0)
            img_base64 = base64.b64encode(buf.read()).decode("utf-8")
            plt.close(fig_trig)
            
            trig_canvas_container.content = ft.Image(src=f"data:image/png;base64,{img_base64}", fit="contain")
            trig_canvas_container.visible = True
            
            trig_placeholder.visible = False
            trig_results_column.visible = True
            
        except Exception as ex:
            trig_error.value = str(ex)
            trig_canvas_container.visible = False
            trig_placeholder.visible = True
            trig_results_column.visible = False
            
        page.update()

    def limpiar_trig(e):
        for tf in [trig_angulo, trig_co, trig_ca, trig_h]: tf.value = ""
        trig_error.value = ""
        for t in [trig_res_angulo, trig_res_co, trig_res_ca, trig_res_h, trig_res_sen, trig_res_cos, trig_res_tan, trig_res_csc, trig_res_sec, trig_res_cot]:
            t.value = ""
        trig_canvas_container.visible = False
        trig_placeholder.visible = True
        trig_results_column.visible = False
        btn_ver_procedimiento_trig.disabled = True
        page.update()

    view_trigonometria = ft.Container(
        content=ft.Column([
            page_header("Simulador Trigonométrico", "Ingresa al menos 2 valores conocidos para calcular el resto.", ft.Icons.CHANGE_HISTORY, ft.Colors.BLUE_600),
            
            ft.ResponsiveRow([
                ft.Container(
                    content=ft.Column([
                        section_title("DATOS CONOCIDOS", ft.Colors.BLUE_600),
                        ft.Row([trig_angulo, trig_h], spacing=20),
                        ft.Row([trig_co, trig_ca], spacing=20),
                        ft.Container(height=10),
                        ft.Row([
                            ft.ElevatedButton("Calcular", icon=ft.Icons.CALCULATE, on_click=calcular_trig, bgcolor=ft.Colors.BLUE_600, color=ft.Colors.WHITE, height=45, expand=1),
                            ft.OutlinedButton("Limpiar", icon=ft.Icons.CLEANING_SERVICES, on_click=limpiar_trig, height=45, expand=1)
                        ]),
                        trig_error,
                    ]),
                    **panel_style,
                    col={"sm": 12, "md": 5, "lg": 5}
                ),
                
                ft.Column([
                    trig_placeholder,
                    trig_results_column
                ], col={"sm": 12, "md": 7, "lg": 7})
                
            ], vertical_alignment=ft.CrossAxisAlignment.START, spacing=30)
            
        ], scroll=ft.ScrollMode.HIDDEN),
        padding=40, expand=True, alignment=ft.Alignment(-1, -1)
    )

    # ==========================================
    # VISTA 2: FIGURAS GEOMÉTRICAS
    # ==========================================
    fig_inputs = ft.Column(spacing=15)
    fig_error = ft.Text(color=ft.Colors.RED_600, weight=ft.FontWeight.W_500, size=13)
    fig_res_area = ft.Text(size=22, weight=ft.FontWeight.W_700, color=ft.Colors.GREEN_700)
    fig_res_perim = ft.Text(size=22, weight=ft.FontWeight.W_700, color=ft.Colors.GREEN_700)
    fig_canvas_container = ft.Container(visible=False, padding=0, alignment=ft.Alignment(0, 0))

    tf_refs = {}

    def change_figura(e=None):
        fig_inputs.controls.clear()
        tf_refs.clear()
        fig_error.value = ""
        fig_res_area.value = ""
        fig_res_perim.value = ""
        fig_canvas_container.visible = False
        
        fig_placeholder.visible = True
        fig_results_container.visible = False
        
        sel = figura_dropdown.value
        w_full = 390
        w_half = 185
        w_third = 116
        
        if sel == "Cuadrado":
            tf_refs['lado'] = ft.TextField(label="Lado", expand=1, focused_border_color=ft.Colors.GREEN_500, **input_style)
            fig_inputs.controls.append(ft.Row([tf_refs['lado']]))
        elif sel == "Rectángulo":
            tf_refs['base'] = ft.TextField(label="Base", expand=1, focused_border_color=ft.Colors.GREEN_500, **input_style)
            tf_refs['altura'] = ft.TextField(label="Altura", expand=1, focused_border_color=ft.Colors.GREEN_500, **input_style)
            fig_inputs.controls.append(ft.Row([tf_refs['base'], tf_refs['altura']], spacing=20))
        elif sel == "Círculo":
            tf_refs['radio'] = ft.TextField(label="Radio", expand=1, focused_border_color=ft.Colors.GREEN_500, **input_style)
            fig_inputs.controls.append(ft.Row([tf_refs['radio']]))
        elif sel == "Triángulo":
            tf_refs['base'] = ft.TextField(label="Base", expand=1, focused_border_color=ft.Colors.GREEN_500, **input_style)
            tf_refs['altura'] = ft.TextField(label="Altura", expand=1, focused_border_color=ft.Colors.GREEN_500, **input_style)
            tf_refs['l1'] = ft.TextField(label="Lado 1", expand=1, focused_border_color=ft.Colors.GREEN_500, **input_style)
            tf_refs['l2'] = ft.TextField(label="Lado 2", expand=1, focused_border_color=ft.Colors.GREEN_500, **input_style)
            tf_refs['l3'] = ft.TextField(label="Lado 3", expand=1, focused_border_color=ft.Colors.GREEN_500, **input_style)
            fig_inputs.controls.extend([
                ft.Row([tf_refs['base'], tf_refs['altura']], spacing=20),
                ft.Divider(height=10, color="transparent"),
                ft.Text("Lados (Opcional para Perímetro):", color="#64748B", size=12),
                ft.Row([tf_refs['l1'], tf_refs['l2'], tf_refs['l3']], spacing=20)
            ])
        elif sel == "Polígono Regular":
            tf_refs['n_lados'] = ft.TextField(label="Nº Lados", expand=1, focused_border_color=ft.Colors.GREEN_500, **input_style)
            tf_refs['lado'] = ft.TextField(label="Long. Lado", expand=1, focused_border_color=ft.Colors.GREEN_500, **input_style)
            fig_inputs.controls.append(ft.Row([tf_refs['n_lados'], tf_refs['lado']], spacing=20))
            
        page.update()

    figura_dropdown = ft.Dropdown(
        label="Selecciona una figura",
        options=[
            ft.dropdown.Option("Cuadrado"),
            ft.dropdown.Option("Rectángulo"),
            ft.dropdown.Option("Círculo"),
            ft.dropdown.Option("Triángulo"),
            ft.dropdown.Option("Polígono Regular"),
        ],
        width=390, border_color="#CBD5E1", border_radius=8,
        bgcolor="#FFFFFF", color="#1E293B", focused_border_color=ft.Colors.GREEN_500,
        on_select=change_figura
    )

    fig_placeholder = ft.Container(
        content=crear_placeholder(ft.Icons.SHAPE_LINE_ROUNDED, "Esperando Datos", "Selecciona una figura e ingresa sus dimensiones a la izquierda para comenzar.", ft.Colors.GREEN_400),
        **panel_style,
        width=600
    )

    def toggle_procedimiento_geo(e):
        if not geo_steps_data: return
        def close_dlg_instance(ev):
            ev.control.page.pop_dialog()
            ev.control.page.update()
        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Row([
                ft.Icon(ft.Icons.RECEIPT_LONG, color="#16A34A"),
                ft.Text("Procedimiento Paso a Paso", weight=ft.FontWeight.W_700, size=16, color="#0F172A"),
            ], spacing=8),
            content=ft.Container(
                width=550, padding=0,
                content=ft.Column([build_steps_list(geo_steps_data, ft.Colors.GREEN_600)], tight=True, scroll=ft.ScrollMode.AUTO)
            ),
            actions=[ft.TextButton("Cerrar", on_click=close_dlg_instance)],
            actions_alignment=ft.MainAxisAlignment.END,
            shape=ft.RoundedRectangleBorder(radius=16)
        )
        page.show_dialog(dlg)
        page.update()

    btn_ver_procedimiento_geo = ft.ElevatedButton(
        "Ver Procedimiento Paso a Paso", icon=ft.Icons.RECEIPT_LONG,
        on_click=toggle_procedimiento_geo, disabled=True,
        width=465, height=42, bgcolor="#FFFFFF", color="#16A34A",
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), side=ft.BorderSide(1, "#86EFAC"))
    )

    fig_results_container = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Column([
                    ft.Column([
                        ft.Text("ÁREA", size=12, color="#64748B", weight=ft.FontWeight.BOLD),
                        fig_res_area
                    ]),
                    ft.Container(height=10),
                    ft.Column([
                        ft.Text("PERÍMETRO", size=12, color="#64748B", weight=ft.FontWeight.BOLD),
                        fig_res_perim
                    ])
                ], expand=1, alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(content=fig_canvas_container, height=250, alignment=ft.Alignment(0,0), expand=True)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            ft.Divider(color="#F1F5F9", height=15),
            ft.Row([btn_ver_procedimiento_geo], alignment=ft.MainAxisAlignment.CENTER)
        ]),
        **panel_style,
        width=600,
        visible=False
    )

    def calcular_figura(e: Any):
        fig_error.value = ""
        sel = figura_dropdown.value
        if not sel:
            fig_error.value = "Primero selecciona una figura geométrica."
            fig_placeholder.visible = True
            fig_results_container.visible = False
            page.update()
            return
            
        def get_val(key):
            try: 
                v = float(tf_refs[key].value)
                if v <= 0: raise ValueError
                return v
            except:
                if key in ['l1','l2','l3']: return 0
                raise ValueError(f"Ingresa un número válido (> 0) para '{tf_refs[key].label}'")

        try:
            param_vals = {}
            if sel == "Cuadrado":
                l = get_val('lado')
                param_vals['lado'] = l
                a, p = cp.calcular_cuadrado(l)
            elif sel == "Rectángulo":
                b, h = get_val('base'), get_val('altura')
                param_vals['base'] = b
                param_vals['altura'] = h
                a, p = cp.calcular_rectangulo(b, h)
            elif sel == "Círculo":
                r = get_val('radio')
                param_vals['radio'] = r
                a, p = cp.calcular_circulo(r)
            elif sel == "Triángulo":
                b, h, l1, l2, l3 = get_val('base'), get_val('altura'), get_val('l1'), get_val('l2'), get_val('l3')
                param_vals['base'] = b
                param_vals['altura'] = h
                a, p = cp.calcular_triangulo(b, h, l1, l2, l3)
            elif sel == "Polígono Regular":
                n, l = int(get_val('n_lados')), get_val('lado')
                if n < 3: raise ValueError("Un polígono debe tener al menos 3 lados.")
                param_vals['n_lados'] = n
                param_vals['lado'] = l
                a, p = cp.calcular_poligono_regular(n, l)
                
            fig_res_area.value = f"Área: {format_val(a)}"
            fig_res_perim.value = f"Perímetro: {format_val(p)}"
            
            # Procedimiento Paso a Paso (LaTeX Image)
            fig_proc = generar_procedimiento_geometria_imagen(sel, param_vals, a, p)
            buf_proc = io.BytesIO()
            fig_proc.savefig(buf_proc, format="png", bbox_inches='tight', transparent=True, dpi=120)
            buf_proc.seek(0)
            img_proc_base64 = base64.b64encode(buf_proc.read()).decode("utf-8")
            plt.close(fig_proc)
            
            geo_steps_data.clear()
            geo_steps_data.extend([("Fórmulas y Sustitución", None, img_proc_base64)])
            btn_ver_procedimiento_geo.disabled = False
            
            fig_geo = generar_figura_geometria(sel, param_vals)
            buf = io.BytesIO()
            fig_geo.savefig(buf, format="png", bbox_inches='tight', transparent=True)
            buf.seek(0)
            img_base64 = base64.b64encode(buf.read()).decode("utf-8")
            plt.close(fig_geo)
            
            fig_canvas_container.content = ft.Image(src=f"data:image/png;base64,{img_base64}", fit="contain")
            fig_canvas_container.visible = True
            
            fig_placeholder.visible = False
            fig_results_container.visible = True
            
        except ValueError as ex:
            fig_error.value = str(ex)
            fig_canvas_container.visible = False
            fig_placeholder.visible = True
            fig_results_container.visible = False
        except Exception as ex:
            fig_error.value = f"Error inesperado: {str(ex)}"
            fig_canvas_container.visible = False
            fig_placeholder.visible = True
            fig_results_container.visible = False
            
        page.update()

    view_figuras = ft.Container(
        content=ft.Column([
            page_header("Geometría Clásica", "Calcula el área y perímetro de formas geométricas.", ft.Icons.SHAPE_LINE, ft.Colors.GREEN_600),
            
            ft.ResponsiveRow([
                ft.Container(
                    content=ft.Column([
                        section_title("SELECCIÓN Y DATOS", ft.Colors.GREEN_700),
                        figura_dropdown,
                        ft.Container(content=fig_inputs, padding=ft.Padding.only(top=10, bottom=15) if hasattr(ft, 'Padding') else 10),
                        ft.Row([
                            ft.ElevatedButton("Calcular Figura", icon=ft.Icons.CALCULATE, on_click=calcular_figura, bgcolor=ft.Colors.GREEN_600, color=ft.Colors.WHITE, height=45, expand=1)
                        ]),
                        fig_error,
                    ]),
                    **panel_style,
                    col={"sm": 12, "md": 5, "lg": 5}
                ),
                
                ft.Column([
                    fig_placeholder,
                    fig_results_container
                ], col={"sm": 12, "md": 7, "lg": 7})
            ], vertical_alignment=ft.CrossAxisAlignment.START, spacing=30)
        ], scroll=ft.ScrollMode.HIDDEN),
        padding=40, expand=True, visible=False, alignment=ft.Alignment(-1, -1)
    )
    # VISTA 3: PENDIENTE (DERIVADA)
    # ==========================================
    w_pend = 185
    pend_x1 = ft.TextField(label="X₁", expand=1, focused_border_color=ft.Colors.PURPLE_500, **input_style)
    pend_y1 = ft.TextField(label="Y₁", expand=1, focused_border_color=ft.Colors.PURPLE_500, **input_style)
    pend_x2 = ft.TextField(label="X₂", expand=1, focused_border_color=ft.Colors.PURPLE_500, **input_style)
    pend_y2 = ft.TextField(label="Y₂", expand=1, focused_border_color=ft.Colors.PURPLE_500, **input_style)
    
    pend_error = ft.Text(color=ft.Colors.RED_600, weight=ft.FontWeight.W_500, size=13)
    pend_placeholder_container = ft.Container(
        content=crear_placeholder(ft.Icons.SHOW_CHART, "Sin Resultados", "Ingresa las coordenadas de los puntos a la izquierda.", ft.Colors.PURPLE_400),
        expand=True,
        alignment=ft.Alignment(0, 0)
    )

    pend_res_m = ft.Text(size=36, weight=ft.FontWeight.W_800, color="#0F172A", selectable=True)
    
    def toggle_procedimiento_pend(e):
        if not pend_steps_data: return
        def close_dlg_instance(ev):
            ev.control.page.pop_dialog()
            ev.control.page.update()
        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Row([
                ft.Icon(ft.Icons.RECEIPT_LONG, color="#9333EA"),
                ft.Text("Procedimiento Paso a Paso", weight=ft.FontWeight.W_700, size=16, color="#0F172A"),
            ], spacing=8),
            content=ft.Container(
                width=550, padding=0,
                content=ft.Column([build_steps_list(pend_steps_data, ft.Colors.PURPLE_600)], tight=True, scroll=ft.ScrollMode.AUTO)
            ),
            actions=[ft.TextButton("Cerrar", on_click=close_dlg_instance)],
            actions_alignment=ft.MainAxisAlignment.END,
            shape=ft.RoundedRectangleBorder(radius=16)
        )
        page.show_dialog(dlg)
        page.update()

    btn_ver_procedimiento_pend = ft.ElevatedButton(
        "Ver Procedimiento Paso a Paso", icon=ft.Icons.RECEIPT_LONG,
        on_click=toggle_procedimiento_pend, disabled=True,
        width=465, height=42, bgcolor="#FFFFFF", color="#9333EA",
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), side=ft.BorderSide(1, "#D8B4FE"))
    )

    pend_results_column = ft.Column([
        ft.Row([
            ft.Icon(ft.Icons.FACT_CHECK_OUTLINED, color="#9333EA", size=20),
            ft.Text("RESULTADO EXACTO", weight=ft.FontWeight.W_700, color="#64748B", size=12)
        ]),
        ft.Divider(color="#F1F5F9", height=8),
        pend_res_m,
        ft.Divider(color="#F1F5F9", height=8),
        btn_ver_procedimiento_pend
    ], alignment=ft.MainAxisAlignment.START, spacing=6, tight=True, visible=False)

    pend_right_card = ft.Container(
        content=ft.Column([pend_placeholder_container, pend_results_column], expand=True),
        **panel_style,
        width=600
    )
    
    pend_chart_container = ft.Container(
        width=1000, height=450, visible=False, alignment=ft.Alignment(0, 0)
    )

    def abrir_interactivo_pend(e):
        data = pend_chart_container.data
        if data:
            fig = generar_figura_pendiente(data["x1"], data["y1"], data["x2"], data["y2"], data["m"])
            plt.show()

    btn_interactivo_pend = ft.ElevatedButton(
        "Abrir Gráfico Interactivo", icon=ft.Icons.OPEN_IN_NEW,
        on_click=abrir_interactivo_pend, visible=False,
        bgcolor=ft.Colors.PURPLE_800, color=ft.Colors.WHITE
    )

    def calcular_pend(e):
        pend_error.value = ""
        btn_ver_procedimiento_pend.disabled = True
        def parse(tf):
            val = tf.value.strip()
            if not val: raise ValueError(f"Falta el valor para {tf.label}")
            try: return float(val)
            except: raise ValueError(f"Entrada inválida en {tf.label}")
            
        try:
            x1, y1, x2, y2 = parse(pend_x1), parse(pend_y1), parse(pend_x2), parse(pend_y2)
            m, proc = calcular_pendiente(x1, y1, x2, y2)
            
            # Procedimiento Paso a Paso (LaTeX Image)
            fig_proc = generar_procedimiento_pendiente_imagen(x1, y1, x2, y2, m)
            buf_proc = io.BytesIO()
            fig_proc.savefig(buf_proc, format="png", bbox_inches='tight', transparent=True, dpi=120)
            buf_proc.seek(0)
            img_proc_base64 = base64.b64encode(buf_proc.read()).decode("utf-8")
            plt.close(fig_proc)
            
            pend_steps_data.clear()
            pend_steps_data.extend([
                ("Datos del Problema", f"P1({x1}, {y1}), P2({x2}, {y2})"),
                ("Cálculo de la Pendiente", None, img_proc_base64)
            ])
            
            pend_res_m.value = f"m = {format_val(m)}"
            
            btn_ver_procedimiento_pend.disabled = False
            pend_placeholder_container.visible = False
            pend_results_column.visible = True
            
            fig = generar_figura_pendiente(x1, y1, x2, y2, m)
            buf = io.BytesIO()
            fig.savefig(buf, format="png", bbox_inches='tight', transparent=True, dpi=300)
            buf.seek(0)
            img_base64 = base64.b64encode(buf.read()).decode("utf-8")
            plt.close(fig)
            
            pend_chart_container.content = ft.InteractiveViewer(
                content=ft.Image(src=f"data:image/png;base64,{img_base64}", fit="contain"),
                max_scale=5.0,
                min_scale=0.5,
                boundary_margin=ft.Margin.all(50)
            )
            pend_chart_container.data = {"x1": x1, "y1": y1, "x2": x2, "y2": y2, "m": m}
            pend_chart_container.visible = True
            btn_interactivo_pend.visible = True
            
        except ValueError as ex:
            pend_error.value = str(ex)
            pend_placeholder_container.visible = True
            pend_results_column.visible = False
            pend_chart_container.visible = False
            btn_interactivo_pend.visible = False
        except Exception as ex:
            pend_error.value = f"Error: {str(ex)}"
            pend_placeholder_container.visible = True
            pend_results_column.visible = False
            pend_chart_container.visible = False
            btn_interactivo_pend.visible = False
            
        page.update()

    view_pendiente = ft.Container(
        content=ft.Column([
            page_header("Cálculo de Pendiente", "Calcula la pendiente (m) de una recta dados dos puntos y visualiza el procedimiento paso a paso.", ft.Icons.SHOW_CHART, ft.Colors.PURPLE_600),
            
            ft.ResponsiveRow([
                ft.Container(
                    content=ft.Column([
                        section_title("COORDENADAS", ft.Colors.PURPLE_700),
                        ft.Text("Punto A", weight=ft.FontWeight.BOLD, color=ft.Colors.RED_600, size=13),
                        ft.Row([pend_x1, pend_y1], spacing=20),
                        ft.Container(height=5),
                        ft.Text("Punto B", weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_600, size=13),
                        ft.Row([pend_x2, pend_y2], spacing=20),
                        ft.Container(height=10),
                        ft.Row([
                            ft.ElevatedButton("Calcular Recta", icon=ft.Icons.SHOW_CHART, on_click=calcular_pend, bgcolor=ft.Colors.PURPLE_600, color=ft.Colors.WHITE, height=45, expand=1)
                        ]),
                        pend_error,
                    ]),
                    **panel_style,
                    col={"sm": 12, "md": 5, "lg": 5}
                ),
                # Columna Derecha: Resultados
                ft.Container(
                    content=pend_right_card,
                    col={"sm": 12, "md": 7, "lg": 7}
                )
            ], vertical_alignment=ft.CrossAxisAlignment.START, spacing=30),
            
            ft.Container(height=15),
            
            ft.Container(
                content=ft.Column([
                    pend_chart_container,
                    ft.Row([btn_interactivo_pend], alignment=ft.MainAxisAlignment.END)
                ]),
                **panel_style
            )
        ], scroll=ft.ScrollMode.HIDDEN),
        padding=40, expand=True, visible=False, alignment=ft.Alignment(-1, -1)
    )

    # ==========================================
    # VISTA 4: INTEGRAL DEFINIDA (REFINAMIENTO UI/UX)
    # ==========================================
    
    estado_teclado = {"activo": None}

    def set_foco(e):
        estado_teclado["activo"] = e.control
    
    # Inputs con Auto-Focus tracker
    int_func = ft.TextField(label="Función f(x)", expand=1, focused_border_color=ft.Colors.INDIGO_500, on_focus=set_foco, **input_style, hint_text="Ej: x**2 + 2*x", prefix_icon=ft.Icons.FUNCTIONS)
    int_a = ft.TextField(label="Límite a (inf)", expand=1, focused_border_color=ft.Colors.INDIGO_500, on_focus=set_foco, **input_style, prefix_icon=ft.Icons.ARROW_DOWNWARD)
    int_b = ft.TextField(label="Límite b (sup)", expand=1, focused_border_color=ft.Colors.INDIGO_500, on_focus=set_foco, **input_style, prefix_icon=ft.Icons.ARROW_UPWARD)
    
    int_error = ft.Text(color=ft.Colors.RED_600, weight=ft.FontWeight.W_500, size=13)
    
    # Textos de Resultados Duales
    int_res_area_frac = ft.Text(size=36, weight=ft.FontWeight.W_800, color="#0F172A", selectable=True)
    int_res_area_dec = ft.Text(size=18, color="#64748B", weight=ft.FontWeight.W_500, selectable=True)
    int_res_err = ft.Text(size=13, color="#94A3B8", italic=True)
    
    # Contenedores
    int_chart_container = ft.Container(
        width=1000, height=450, visible=False, alignment=ft.Alignment(0, 0)
    )

    def abrir_interactivo_int(e):
        data = int_chart_container.data
        if data:
            fig = generar_figura_integral(data["func_str"], data["a_val"], data["b_val"], data["area_num"])
            plt.show()

    btn_interactivo_int = ft.ElevatedButton(
        "Abrir Gráfico Interactivo", icon=ft.Icons.OPEN_IN_NEW,
        on_click=abrir_interactivo_int, visible=False,
        bgcolor="#1E293B", color=ft.Colors.WHITE
    )

    int_procedimiento_container = ft.Container(visible=False, width=600, padding=10, alignment=ft.Alignment(-1, -1), bgcolor="#FFFFFF", border_radius=16, border=ft.Border.all(1, "#E2E8F0"))

    # --- TECLADO VIRTUAL ---

    def set_cursor(e):
        try:
            page.mouse_cursor = ft.MouseCursor.CLICK if e.data == "true" else None
            page.update()
        except:
            pass
    def btn_teclado(text, append_val, color_bg="#F8FAFC", font_w=ft.FontWeight.NORMAL, width=50):
        def on_click(e):
            tf = estado_teclado["activo"]
            if not tf: tf = int_func
            if text == "DEL": tf.value = (tf.value or "")[:-1]
            elif text == "C": tf.value = ""
            else: tf.value = (tf.value or "") + append_val
            page.update()
            
        return ft.ElevatedButton(
            text, 
            on_click=on_click, 
            bgcolor=color_bg, color="#0F172A", 
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=6), padding=0),
            width=width, height=45, on_hover=set_cursor
        )

    teclado_virtual = ft.Container(
        content=ft.Column([
            ft.Row([btn_teclado("x", "x", "#E2E8F0", ft.FontWeight.BOLD), btn_teclado("sin", "sin("), btn_teclado("cos", "cos("), btn_teclado("tan", "tan("), btn_teclado("π", "pi", "#E2E8F0"), btn_teclado("C", "C", "#FECDD3")], spacing=8),
            ft.Row([btn_teclado("7", "7"), btn_teclado("8", "8"), btn_teclado("9", "9"), btn_teclado("(", "("), btn_teclado(")", ")"), btn_teclado("DEL", "DEL", "#FECACA")], spacing=8),
            ft.Row([btn_teclado("4", "4"), btn_teclado("5", "5"), btn_teclado("6", "6"), btn_teclado("*", "*", "#E0E7FF"), btn_teclado("/", "/", "#E0E7FF"), btn_teclado("^", "**", "#E0E7FF")], spacing=8),
            ft.Row([btn_teclado("1", "1"), btn_teclado("2", "2"), btn_teclado("3", "3"), btn_teclado("+", "+", "#E0E7FF"), btn_teclado("-", "-", "#E0E7FF"), btn_teclado("e", "E", "#E2E8F0")], spacing=8),
            ft.Row([btn_teclado("0", "0", width=108), btn_teclado(".", "."), btn_teclado(",", ","), btn_teclado("ln", "log("), btn_teclado("√", "sqrt(")], spacing=8),
        ], spacing=8),
        padding=15, bgcolor="#FFFFFF", border_radius=12, border=ft.Border.all(1, "#E2E8F0"),
        visible=False
    )
    
    def toggle_teclado(e):
        teclado_virtual.visible = not teclado_virtual.visible
        btn_toggle_teclado.icon = ft.Icons.KEYBOARD_ARROW_UP if teclado_virtual.visible else ft.Icons.KEYBOARD
        page.update()
        
    btn_toggle_teclado = ft.TextButton("Teclado Matemático Inteligente", icon=ft.Icons.KEYBOARD, on_click=toggle_teclado, style=ft.ButtonStyle(color="#2563EB"))

    def toggle_procedimiento(e):
        if not integral_steps_data: return
        
        def close_dlg_instance(ev):
            ev.control.page.pop_dialog()
            ev.control.page.update()

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Row([
                ft.Icon(ft.Icons.RECEIPT_LONG, color="#6366F1"),
                ft.Text("Procedimiento Paso a Paso", weight=ft.FontWeight.W_700, size=16, color="#0F172A"),
            ], spacing=8),
            content=ft.Container(
                width=550, padding=0,
                content=ft.Column([build_steps_list(integral_steps_data, ft.Colors.INDIGO_600)], tight=True, scroll=ft.ScrollMode.AUTO)
            ),
            actions=[
                ft.TextButton("Cerrar", on_click=close_dlg_instance)
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            shape=ft.RoundedRectangleBorder(radius=16)
        )
        page.show_dialog(dlg)
        page.update()

    btn_ver_procedimiento = ft.ElevatedButton(
        "Ver Procedimiento Paso a Paso", icon=ft.Icons.RECEIPT_LONG,
        on_click=toggle_procedimiento, disabled=True,
        width=465, height=42, bgcolor="#FFFFFF", color="#2563EB",
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
            side=ft.BorderSide(1, "#BFDBFE")
        ),
        on_hover=set_cursor
    )

    int_placeholder_container = ft.Container(
        content=crear_placeholder(ft.Icons.FACT_CHECK_OUTLINED, "Sin Resultados", "Define la función y límites a la izquierda para obtener los resultados.", ft.Colors.INDIGO_400),
        expand=True,
        alignment=ft.Alignment(0, 0)
    )
    
    int_results_column = ft.Column([
        ft.Row([
            ft.Icon(ft.Icons.FACT_CHECK_OUTLINED, color="#2563EB", size=20),
            ft.Text("RESULTADO EXACTO", weight=ft.FontWeight.W_700, color="#64748B", size=12)
        ]),
        ft.Divider(color="#F1F5F9", height=8),
        int_res_area_frac,
        int_res_area_dec,
        int_res_err,
        ft.Divider(color="#F1F5F9", height=8),
        btn_ver_procedimiento
    ], alignment=ft.MainAxisAlignment.START, spacing=6, tight=True, visible=False)

    int_right_card = ft.Container(
        content=ft.Column([
            int_placeholder_container,
            int_results_column
        ], expand=True),
        **panel_style,
        width=600
    )

    def calcular_int(e):
        int_error.value = ""
        btn_ver_procedimiento.disabled = True
        try:
            func_str = int_func.value.strip() if int_func.value else ""
            if not func_str: raise ValueError("Ingresa una función válida.")
            
            def parse_lim(v_str, default):
                if not v_str: return default
                if "." not in v_str: return int(v_str)
                return float(v_str)
            a_val = parse_lim(int_a.value.strip(), 0)
            b_val = parse_lim(int_b.value.strip(), 1)
            
            area_num, error, func, expr, area_simbolica, res_exacto_latex = calcular_integral_definida(func_str, a_val, b_val)
            
            area_fmt = f"{int(round(area_num))}" if abs(area_num - round(area_num)) < 1e-9 else f"{area_num:.4f}"
            if area_simbolica is not None:
                v_frac = str(area_simbolica).replace("**", "^")
                if v_frac.endswith(".0000000000000"): v_frac = v_frac.replace(".0000000000000", "")
                if v_frac.endswith(".0"): v_frac = v_frac[:-2]
                int_res_area_frac.value = v_frac
                int_res_area_dec.value = f"≈ {area_fmt}"
            else:
                int_res_area_frac.value = area_fmt
                int_res_area_dec.value = ""
                
            int_res_err.value = f"Margen de error: ±{error:.2e}"
            
            fig = generar_figura_integral(func_str, a_val, b_val, area_num)
            buf = io.BytesIO()
            fig.savefig(buf, format="png", bbox_inches='tight', transparent=True, dpi=300)
            buf.seek(0)
            img_base64 = base64.b64encode(buf.read()).decode("utf-8")
            plt.close(fig)
            int_chart_container.content = ft.InteractiveViewer(
                content=ft.Image(src=f"data:image/png;base64,{img_base64}", fit="contain"),
                max_scale=5.0,
                min_scale=0.5,
                boundary_margin=ft.Margin.all(50)
            )
            int_chart_container.data = {"func_str": func_str, "a_val": a_val, "b_val": b_val, "area_num": area_num}
            int_chart_container.visible = True
            btn_interactivo_int.visible = True
            
            # Procedimiento Paso a Paso (LaTeX Image)
            fig_proc = generar_procedimiento_integral_imagen(expr, a_val, b_val, area_simbolica, area_num)
            buf_proc = io.BytesIO()
            fig_proc.savefig(buf_proc, format="png", bbox_inches='tight', transparent=True, dpi=300)
            buf_proc.seek(0)
            img_proc_base64 = base64.b64encode(buf_proc.read()).decode("utf-8")
            plt.close(fig_proc)
            
            integral_steps_data.clear()
            integral_steps_data.extend([("Cálculo de la Integral", None, img_proc_base64)])
            
            int_placeholder_container.visible = False
            int_results_column.visible = True
            btn_ver_procedimiento.disabled = False
            
        except ValueError as ex:
            int_error.value = str(ex)
            int_chart_container.visible = False
            int_placeholder_container.visible = True
            int_results_column.visible = False
            btn_interactivo_int.visible = False
        except Exception as ex:
            int_error.value = f"Error: {str(ex)}"
            int_chart_container.visible = False
            int_placeholder_container.visible = True
            int_results_column.visible = False
            btn_interactivo_int.visible = False
            
        page.update()

    btn_calcular = ft.ElevatedButton(
        "Calcular y Graficar", icon=ft.Icons.CALCULATE_OUTLINED,
        on_click=calcular_int, bgcolor="#2563EB", color=ft.Colors.WHITE,
        height=45, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)), on_hover=set_cursor, expand=1
    )

    view_integral = ft.Container(
        content=ft.Column([
            page_header("Integral Definida", "Cálculo analítico con evaluación de resultados exactos.", ft.Icons.AREA_CHART, "#2563EB"),
            
            ft.ResponsiveRow([
                # Columna Izquierda: Entradas
                ft.Container(
                    content=ft.Column([
                        section_title("FUNCIÓN A INTEGRAR", "#1E293B"),
                        ft.Row([int_func]),
                        ft.Container(height=5),
                        ft.Row([int_a, int_b], spacing=20),
                        btn_toggle_teclado,
                        teclado_virtual,
                        ft.Container(height=10),
                        ft.Row([btn_calcular]),
                        int_error,
                    ]), 
                    **panel_style,
                    col={"sm": 12, "md": 5, "lg": 5},
                    alignment=ft.Alignment(-1, -1)
                ),
                
                # Columna Derecha: Resultados
                ft.Container(
                    content=int_right_card,
                    col={"sm": 12, "md": 7, "lg": 7}
                )
                
            ], vertical_alignment=ft.CrossAxisAlignment.START, spacing=30),
            
            ft.Container(height=15),
            
            ft.Container(
                content=ft.Column([
                    int_chart_container,
                    ft.Row([btn_interactivo_int], alignment=ft.MainAxisAlignment.END)
                ]), 
                **panel_style
            )
        ], scroll=ft.ScrollMode.HIDDEN),
        padding=40, expand=True, visible=False, alignment=ft.Alignment(-1, -1)
    )

    # ==========================================
    # NAVEGACIÓN Y LAYOUT GENERAL
    # ==========================================
    def on_nav_change(e):
        idx = e.control.selected_index
        view_trigonometria.visible = (idx == 0)
        view_figuras.visible = (idx == 1)
        view_pendiente.visible = (idx == 2)
        view_integral.visible = (idx == 3)
        page.update()

    nav_rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=200,
        group_alignment=-0.95,
        bgcolor="#FFFFFF",
        indicator_color="#E0E7FF",
        destinations=[
            ft.NavigationRailDestination(icon=ft.Icons.CHANGE_HISTORY, label="Trigonometría"),
            ft.NavigationRailDestination(icon=ft.Icons.SHAPE_LINE, label="Geometría"),
            ft.NavigationRailDestination(icon=ft.Icons.SHOW_CHART, label="Pendiente"),
            ft.NavigationRailDestination(icon=ft.Icons.AREA_CHART, label="Integrales"),
        ],
        on_change=on_nav_change
    )

    page.add(
        ft.Row(
            [
                nav_rail,
                ft.VerticalDivider(width=1, color="#E2E8F0"),
                view_trigonometria,
                view_figuras,
                view_pendiente,
                view_integral
            ],
            expand=True,
            spacing=0
        )
    )

if __name__ == '__main__':
    puerto = int(os.environ.get("PORT", 8550))
    ft.app(target=main, host="0.0.0.0", port=puerto, view=ft.AppView.WEB_BROWSER)
