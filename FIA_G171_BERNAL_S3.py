"""
===============================================================================
ACTIVIDAD 3: HILL CLIMBING VS SIMULATED ANNEALING
===============================================================================
"""

import math
import random
import matplotlib.pyplot as plt

# 1. DEFINICIÓN DE LA FUNCIÓN OBJETIVO (Costo de transporte ponderado)
def funcion_objetivo(coords):
    x, y = coords
    # Centros de consumo: (x_i, y_i) y sus pesos w_i
    centros = [
        (1, 2, 3),
        (5, 8, 5),
        (8, 3, 2)
    ]
    costo_total = 0
    for cx, cy, peso in centros:
        distancia = math.sqrt((x - cx)**2 + (y - cy)**2)
        costo_total += peso * distancia
    return costo_total

# 2. IMPLEMENTACIÓN DE HILL CLIMBING
def hill_climbing(punto_inicial, iteraciones=100, eta=0.5):
    actual = punto_inicial
    costo_actual = funcion_objetivo(actual)
    historial_costos = [costo_actual]
    
    for _ in range(iteraciones):
        # Generar vecino aleatorio en la vecindad
        vecino = (
            actual[0] + random.gauss(0, eta),
            actual[1] + random.gauss(0, eta)
        )
        costo_vecino = funcion_objetivo(vecino)
        
        # Si el vecino mejora el costo, nos movemos a él (Greedy)
        if costo_vecino < costo_actual:
            actual = vecino
            costo_actual = costo_vecino
            
        historial_costos.append(costo_actual)
        
    return actual, costo_actual, historial_costos

# 3. IMPLEMENTACIÓN DE SIMULATED ANNEALING
def simulated_annealing(punto_inicial, iteraciones=100, T=100.0, alfa=0.95, eta=0.5):
    actual = punto_inicial
    costo_actual = funcion_objetivo(actual)
    mejor_solucion = actual
    mejor_costo = costo_actual
    historial_costos = [costo_actual]
    
    for i in range(iteraciones):
        if T < 1e-3: 
            break
            
        # Generar vecino
        vecino = (
            actual[0] + random.gauss(0, eta),
            actual[1] + random.gauss(0, eta)
        )
        costo_vecino = funcion_objetivo(vecino)
        
        delta_e = costo_vecino - costo_actual
        
        # Si mejora, o si se acepta por probabilidad con temperatura alta
        if delta_e < 0 or random.random() < math.exp(-delta_e / T):
            actual = vecino
            costo_actual = costo_vecino
            
            if costo_actual < mejor_costo:
                mejor_solucion = actual
                mejor_costo = costo_actual
                
        T *= alfa # Enfriamiento
        historial_costos.append(mejor_costo)
        
    return mejor_solucion, mejor_costo, historial_costos

# =============================================================================
# EJECUCIÓN Y GENERACIÓN DE GRÁFICA DE CONVERGENCIA
# =============================================================================
if __name__ == "__main__":
    random.seed(42) # Para reproducibilidad
    punto_salida = (0.0, 0.0)
    
    # Ejecutar ambos algoritmos
    sol_hc, costo_hc, hist_hc = hill_climbing(punto_salida)
    sol_sa, costo_sa, hist_sa = simulated_annealing(punto_salida)
    
    print("--- RESULTADOS DE OPTIMIZACIÓN ---")
    print(f"Hill Climbing       -> Mejor Posición: {sol_hc}, Costo Mínimo: {costo_hc:.4f}")
    print(f"Simulated Annealing -> Mejor Posición: {sol_sa}, Costo Mínimo: {costo_sa:.4f}")
    
    # Generar Gráfica de Convergencia
    plt.figure(figsize=(8, 5))
    plt.plot(hist_hc, label='Hill Climbing', color='crimson', linewidth=2)
    plt.plot(hist_sa, label='Simulated Annealing', color='dodgerblue', linewidth=2, linestyle='--')
    plt.title('Gráfica de Convergencia - Búsqueda Local', fontsize=12, fontweight='bold')
    plt.xlabel('Número de Iteraciones')
    plt.ylabel('Costo de la Función Objetivo')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig('grafica_convergencia_actividad3.png', dpi=300)
    plt.show()
    print("\nGráfica guardada exitosamente como: grafica_convergencia_actividad3.png")