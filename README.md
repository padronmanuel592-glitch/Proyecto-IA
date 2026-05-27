# Proyecto-IA
# 🧠 Sistema Difuso de Evaluación del Rendimiento Estudiantil

Este proyecto aplica **Lógica Difusa (Fuzzy Logic)** para evaluar el rendimiento global de un estudiante a partir de tres factores imprecisos: nota de exámenes, participación en clase y asistencia.  
El sistema emite un índice numérico (0–100) y una categoría cualitativa (Insuficiente, Regular, Bueno, Excelente).

Está implementado completamente en **Python estándar**, sin librerías externas, para que pueda ejecutarse en cualquier entorno con Python 3.x.

## 🎯 Problema que resuelve

La evaluación tradicional en educación suele ser rígida (un número exacto) o demasiado subjetiva.  
Con la lógica difusa podemos:

- Usar términos lingüísticos como *"participación media"* o *"asistencia baja"*.
- Manejar situaciones donde un estudiante no es ni "totalmente bueno" ni "totalmente malo".
- Obtener una evaluación más humana, interpretable y ajustable por el docente.

## 📊 Variables del sistema

| Variable         | Rango      | Conjuntos difusos          |
|-----------------|------------|----------------------------|
| Nota exámenes    | 0 – 10     | baja, media, alta          |
| Participación    | 0 – 10     | poca, media, mucha         |
| Asistencia       | 0 – 100%   | baja, media, alta          |
| **Salida:** Rendimiento | 0 – 100 | insuficiente, regular, bueno, excelente |

## 🧠 Base de reglas (4 reglas)

1. **SI** examen **bajo** O participación **poca** O asistencia **baja** → rendimiento **insuficiente**
2. **SI** examen **media** Y participación **media** Y asistencia **media** → rendimiento **regular**
3. **SI** examen **alta** Y (participación **mucha** O asistencia **alta**) → rendimiento **bueno**
4. **SI** examen **alta** Y participación **mucha** Y asistencia **alta** → rendimiento **excelente**

## ⚙️ Requisitos

- Python 3.6 o superior
- Ninguna librería adicional (solo la biblioteca estándar)

## 🚀 Instalación y uso

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tuusuario/logica-difusa-educacion.git
   cd logica-difusa-educacion
```

1. Ejecuta el script:
   ```bash
   python sistema_difuso.py
   ```
2. Ingresa los valores del estudiante cuando se soliciten:
   ```
   Nota de exámenes (0-10): 8.5
   Participación en clase (0-10): 7
   Asistencia (0-100%): 90
   ```
3. El sistema mostrará:
   ```
   📊 Resultado:
     - Índice de rendimiento: 78.34 / 100
     - Categoría: Bueno
   ```

🧪 Ejemplos de prueba

Exámenes Participación Asistencia Resultado esperado
10 10 100 Excelente (≈95-100)
9 8 95 Bueno/Excelente (≈86)
5 5 75 Regular (≈50-60)
2 2 40 Insuficiente (≈20-35)

🔧 Metodología difusa utilizada

· Fuzzificación: funciones de pertenencia triangulares y trapezoidales.
· Operadores lógicos: min (AND), max (OR).
· Inferencia: método de Mamdani (mínimo para el consecuente).
· Agregación: máximo de consecuentes truncados.
· Defuzzificación: centroide (discretización cada 0.5 puntos en el rango 0–100).

📁 Estructura del repositorio

```
logica-difusa-educacion/
├── sistema_difuso.py      # Código principal
├── README.md              # Este archivo
└── docs/                  # (opcional) presentación y pre-artículo
```

📈 Posibles mejoras futuras

· Interfaz gráfica simple (tkinter) para ingresar datos.
· Permitir cargar múltiples estudiantes desde un CSV.
· Optimizar las funciones de pertenencia con datos reales.
· Añadir más reglas para casos intermedios (ej. "casi excelente").

