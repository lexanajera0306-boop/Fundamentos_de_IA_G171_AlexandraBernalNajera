"""
===============================================================================
ACTIVIDAD 4: BÚSQUEDA CIEGA - BFS VS DFS EN LABERINTO
===============================================================================
"""

from collections import deque
import time

# 1. REPRESENTACIÓN DEL LABERINTO (0 = Camino libre, 1 = Muro/Obstáculo)
laberinto = [
    [0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0],
    [1, 1, 0, 0, 0],
    [0, 0, 0, 1, 0]
]

inicio = (0, 0)
meta = (4, 4)

def obtener_vecinos(nodo, lab):
    x, y = nodo
    filas = len(lab)
    cols = len(lab[0])
    vecinos = []
    
    # Movimientos cardinales: Norte, Sur, Este, Oeste
    direcciones = [(-1, 0), (1, 0), (0, 1), (0, -1)]
    for dx, dy in direcciones:
        nx, ny = x + dx, y + dy
        if 0 <= nx < filas and 0 <= ny < cols and lab[nx][ny] == 0:
            vecinos.append((nx, ny))
    return vecinos

# 2. IMPLEMENTACIÓN DE BFS (Búsqueda en Anchura)
def busqueda_bfs(lab, start, goal):
    frontera = deque([(start, [start])])
    visitados = {start}
    nodos_expandidos = 0
    
    inicio_tiempo = time.time()
    while frontera:
        actual, camino = frontera.popleft()
        nodos_expandidos += 1
        
        if actual == goal:
            tiempo_ejecucion = time.time() - inicio_tiempo
            return camino, nodos_expandidos, tiempo_ejecucion
            
        for vecino in obtener_vecinos(actual, lab):
            if vecino not in visitados:
                visitados.add(vecino)
                frontera.append((vecino, camino + [vecino]))
    return None, nodos_expandidos, time.time() - inicio_tiempo

# 3. IMPLEMENTACIÓN DE DFS (Búsqueda en Profundidad)
def busqueda_dfs(lab, start, goal):
    frontera = [(start, [start])]
    visitados = set()
    nodos_expandidos = 0
    
    inicio_tiempo = time.time()
    while frontera:
        actual, camino = frontera.pop()
        
        if actual in visitados:
            continue
        visitados.add(actual)
        nodos_expandidos += 1
        
        if actual == goal:
            tiempo_ejecucion = time.time() - inicio_tiempo
            return camino, nodos_expandidos, tiempo_ejecucion
            
        for vecino in obtener_vecinos(actual, lab):
            if vecino not in visitados:
                frontera.append((vecino, camino + [vecino]))
    return None, nodos_expandidos, time.time() - inicio_tiempo

# =============================================================================
# EJECUCIÓN Y COMPARATIVA EN CONSOLA
# =============================================================================
if __name__ == "__main__":
    print("--- RESULTADOS DE BÚSQUEDA EN LABERINTO ---")
    
    # Ejecutar BFS
    camino_bfs, nodos_bfs, tiempo_bfs = busqueda_bfs(laberinto, inicio, meta)
    print(f"\n[BFS - Anchura]")
    print(f" -> Ruta solución ({len(camino_bfs)} pasos): {camino_bfs}")
    print(f" -> Nodos expandidos: {nodos_bfs}")
    print(f" -> Tiempo de ejecución: {tiempo_bfs:.6f} segundos")
    
    # Ejecutar DFS
    camino_dfs, nodos_dfs, tiempo_dfs = busqueda_dfs(laberinto, inicio, meta)
    print(f"\n[DFS - Profundidad]")
    print(f" -> Ruta encontrada ({len(camino_dfs)} pasos): {camino_dfs}")
    print(f" -> Nodos expandidos: {nodos_dfs}")
    print(f" -> Tiempo de ejecución: {tiempo_dfs:.6f} segundos")