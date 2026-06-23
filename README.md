# 🧮 Math Suite (Suite Matemática Interactiva)

¡Bienvenido a Math Suite! Una potente aplicación matemática construida en Python que permite resolver, graficar y ver el procedimiento paso a paso de problemas de cálculo, analíticos, geométricos y trigonométricos.

## ✨ Funcionalidades Principales

### 1. ∫ Cálculo de Integrales Definidas
- Motor matemático simbólico avanzado impulsado por `SymPy`.
- Soporte para detección de cualquier variable en tu función matemática (`x`, `y`, `z`, `t`, etc.).
- Resultados dobles: Resultado algebraico exacto (en fracciones reales) y resultado aproximado decimal.
- **Modo Profesor:** Genera una visualización del **procedimiento paso a paso** renderizado en LaTeX, mostrando la sustitución de límites y resolución aritmética de la integral.
- **Modo Gráfico:** Sombreado interactivo del área bajo la curva con el motor de `Matplotlib`.

### 2. 📈 Cálculo de Pendientes
- Encuentra la pendiente de una recta ($m$) ingresando únicamente dos puntos coordenados en el plano: $A(x_1, y_1)$ y $B(x_2, y_2)$.
- Incluye el desarrollo paso a paso aplicando la fórmula de la pendiente y grafica la interpolación de la recta con capacidad de hacer *zoom* y paneo dinámico.

### 3. 📐 Simulador Trigonométrico
- Resolución instantánea de triángulos rectángulos. Solo necesitas ingresar **2 valores conocidos** (ángulo, catetos o hipotenusa).
- Cálculo automático y derivación geométrica de las 6 razones trigonométricas principales (Seno, Coseno, Tangente, Cosecante, Secante, Cotangente).
- Dibujo a escala del triángulo resultante.

### 4. 🟩 Geometría Clásica
- Calculadora de Área y Perímetro optimizada para: Cuadrados, Rectángulos, Círculos, Triángulos y Polígonos Regulares (con ingreso de número de lados variables).
- Representación gráfica visual de las medidas ingresadas.

---

## 🛠️ Tecnologías y Dependencias

Para lograr la mejor experiencia interactiva (gráficas, interfaz moderna y cálculo simbólico analítico), el proyecto utiliza las siguientes librerías de vanguardia:

- **[Flet](https://flet.dev/)**: Motor de la interfaz gráfica de usuario (GUI).
- **[SymPy](https://www.sympy.org/)**: Sistema de álgebra computacional para resolución de integrales, derivadas y formateo LaTeX.
- **[Matplotlib](https://matplotlib.org/)**: Motor de renderizado para los planos cartesianos y generación del texto matemático en imágenes transparentes.
- **[NumPy](https://numpy.org/)**: Procesamiento numérico y generación de vectores continuos.

---

## 🚀 Instalación y Uso

### 1. Requisitos Previos

Asegúrate de tener Python 3.9 o superior instalado en tu sistema. Luego, descarga e instala las dependencias necesarias ejecutando en tu terminal:

```bash
pip install flet sympy matplotlib numpy
```

### 2. Iniciar la Interfaz Gráfica (Recomendado) 💻

Para arrancar la interfaz visual moderna, simplemente ejecuta el script principal de UI:

```bash
python interfazFlet.py
```
> **📱 Diseño Responsivo:** La interfaz visual fue construida bajo el patrón *Mobile-First*. Si la ventana se achica o se ejecuta desde un teléfono móvil, todos los paneles, botones y gráficas se ajustarán elásticamente a la resolución de tu pantalla para que nunca pierdas el control.

### 3. Interfaz de Terminal (CLI) 🖳

Si te encuentras en un entorno de servidor o prefieres la experiencia clásica en la consola paso a paso, también cuentas con un robusto menú interactivo de terminal:

```bash
python interfaz.py
```

---
*¡Disfruta aprendiendo, validando y resolviendo matemáticas a máxima velocidad!* 🚀
