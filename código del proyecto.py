import math
# 1. Funciones de pertenencia
def triangular(x, a, b, c):
    """Triangular: a (izquierda), b (pico), c (derecha)"""
    if x <= a or x >= c:
        return 0.0
    if a < x <= b:
        return (x - a) / (b - a)
    if b <= x < c:
        return (c - x) / (c - b)
    return 0.0

def trapezoidal(x, a, b, c, d):
    """Trapezoidal: a (izquierda), b (inicio plano), c (fin plano), d (derecha)"""
    if x <= a or x >= d:
        return 0.0
    if a < x < b:
        return (x - a) / (b - a)
    if b <= x <= c:
        return 1.0
    if c < x < d:
        return (d - x) / (d - c)
    return 0.0
# ------------------------------------------------------------
# 2. Definición de conjuntos difusos para cada variable
# ------------------------------------------------------------
def fuzzificar_examen(nota):
    """Entrada: nota 0-10. Salida: grado de pertenencia a categorías"""
    return {
        'baja': trapezoidal(nota, 0, 0, 3, 5),
        'media': triangular(nota, 3, 5, 7),
        'alta': trapezoidal(nota, 5, 7, 10, 10)
    }

def fuzzificar_participacion(part):
    """Entrada: participación 0-10"""
    return {
        'poca': trapezoidal(part, 0, 0, 3, 5),
        'media': triangular(part, 3, 5, 7),
        'mucha': trapezoidal(part, 5, 7, 10, 10)
    }

def fuzzificar_asistencia(asis):
    """Entrada: asistencia 0-100%"""
    return {
        'baja': trapezoidal(asis, 0, 0, 50, 70),
        'media': triangular(asis, 50, 70, 90),
        'alta': trapezoidal(asis, 70, 90, 100, 100)
    }

# ------------------------------------------------------------
# 3. Funciones de pertenencia de la salida (rendimiento)
# ------------------------------------------------------------
def rendimiento_triangular(x, a, b, c):
    return triangular(x, a, b, c)

def fuzzificar_rendimiento(x):
    """Para defuzzificación: dado un valor x de rendimiento (0-100),
       devuelve grados a las categorías (no se usa directamente)"""
    return {
        'insuficiente': trapezoidal(x, 0, 0, 25, 40),
        'regular': triangular(x, 25, 40, 60),
        'bueno': triangular(x, 40, 60, 80),
        'excelente': trapezoidal(x, 60, 80, 100, 100)
    }

# ------------------------------------------------------------
# 4. Base de reglas difusas (formato IF-THEN con AND/OR)
# ------------------------------------------------------------
def evaluar_reglas(examen_f, part_f, asis_f):
    """Evalúa todas las reglas y devuelve la fuerza de activación por categoría de salida"""
    # Regla 1: IF examen bajo OR participacion poca OR asistencia baja THEN rendimiento insuficiente
    r1 = max(examen_f['baja'], part_f['poca'], asis_f['baja'])
    
    # Regla 2: IF examen media AND participacion media AND asistencia media THEN rendimiento regular
    r2 = min(examen_f['media'], part_f['media'], asis_f['media'])
    
    # Regla 3: IF examen alta AND (participacion mucha OR asistencia alta) THEN rendimiento bueno
    r3 = min(examen_f['alta'], max(part_f['mucha'], asis_f['alta']))
    
    # Regla 4: IF examen alta AND participacion mucha AND asistencia alta THEN rendimiento excelente
    r4 = min(examen_f['alta'], part_f['mucha'], asis_f['alta'])
    
    return {
        'insuficiente': r1,
        'regular': r2,
        'bueno': r3,
        'excelente': r4
    }

# ------------------------------------------------------------
# 5. Agregación de consecuentes (Mamdani: min / truncado)
# ------------------------------------------------------------
def agregar_consecuente(activaciones, x_rendimiento):
    """Para cada valor de rendimiento x, calcula el grado de pertenencia agregado"""
    conjuntos_salida = fuzzificar_rendimiento(x_rendimiento)
    grado = 0.0
    for cat, act in activaciones.items():
        grado = max(grado, min(act, conjuntos_salida[cat]))
    return grado

# ------------------------------------------------------------
# 6. Defuzzificación por centroide (discretización)
# ------------------------------------------------------------
def defuzzificar(activaciones, paso=0.5):
    """Centroide sobre el rango 0-100 con paso dado"""
    suma = 0.0
    peso = 0.0
    x = 0.0
    while x <= 100:
        mu = agregar_consecuente(activaciones, x)
        suma += x * mu
        peso += mu
        x += paso
    if peso == 0:
        return 0.0
    return suma / peso

# ------------------------------------------------------------
# 7. Clasificación cualitativa final
# ------------------------------------------------------------
def clasificar_rendimiento(valor):
    if valor < 40:
        return "Insuficiente"
    elif valor < 60:
        return "Regular"
    elif valor < 80:
        return "Bueno"
    else:
        return "Excelente"

# ------------------------------------------------------------
# 8. Función principal del sistema difuso
# ------------------------------------------------------------
def evaluar_estudiante(nota_examen, participacion, asistencia):
    """
    Entradas:
        nota_examen: float 0-10
        participacion: float 0-10
        asistencia: float 0-100 (porcentaje)
    Salidas:
        rendimiento_num: float 0-100
        categoria: str
    """
    # Fuzzificación
    examen_f = fuzzificar_examen(nota_examen)
    part_f = fuzzificar_participacion(participacion)
    asis_f = fuzzificar_asistencia(asistencia)
    
    # Evaluación de reglas
    activaciones = evaluar_reglas(examen_f, part_f, asis_f)
    
    # Defuzzificación
    rendimiento = defuzzificar(activaciones, paso=0.5)
    
    # Categoría
    categoria = clasificar_rendimiento(rendimiento)
    
    return rendimiento, categoria

# ------------------------------------------------------------
# 9. Ejemplo de uso y pruebas
# ------------------------------------------------------------
if __name__ == "__main__":
    print("=== Sistema Difuso de Evaluación Estudiantil ===")
    print("Ingrese los datos del estudiante:")
    
    try:
        nota = float(input("Nota de exámenes (0-10): "))
        part = float(input("Participación en clase (0-10): "))
        asis = float(input("Asistencia (0-100%): "))
        
        if not (0 <= nota <= 10 and 0 <= part <= 10 and 0 <= asis <= 100):
            raise ValueError("Valores fuera de rango")
        
        rend, cat = evaluar_estudiante(nota, part, asis)
        print(f"\n📊 Resultado:")
        print(f"  - Índice de rendimiento: {rend:.2f} / 100")
        print(f"  - Categoría: {cat}")
        
    except ValueError as e:
        print(f"Error: {e}. Asegúrese de ingresar números válidos.")
    
    # Pruebas adicionales
    print("\n--- Pruebas predefinidas ---")
    casos = [
        (10, 10, 100, "Excelente"),
        (9, 8, 95,  "Bueno / Excelente"),
        (5, 5, 75,  "Regular"),
        (2, 2, 40,  "Insuficiente")
    ]
    for nota, part, asis, esperado in casos:
        r, c = evaluar_estudiante(nota, part, asis)
        print(f"({nota}, {part}, {asis}) → {c} ({r:.1f})")
