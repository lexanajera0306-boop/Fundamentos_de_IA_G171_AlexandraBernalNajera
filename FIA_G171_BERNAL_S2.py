"""
===============================================================================
SIMULACIÓN INTERACTIVA EN TIEMPO REAL - AMBOS PROBLEMAS
===============================================================================
"""

from collections import deque
import time
import networkx as nx

print("==================================================================")
print(" 1. INICIANDO SIMULACIÓN EN VIVO: PROBLEMA DE LOGÍSTICA")
print("==================================================================")
time.sleep(1)

# Grafo de la red vial
G1 = nx.DiGraph()
for o, d, c in [
    ('Almacen', 'Cliente_A', 5), ('Almacen', 'Cliente_B', 10),
    ('Cliente_A', 'Cliente_B', 4), ('Cliente_B', 'Cliente_A', 4),
    ('Cliente_A', 'Almacen', 5), ('Cliente_B', 'Almacen', 8)
]:
    G1.add_edge(o, d, weight=c)

def simulacion_en_vivo_logistica(estado_inicial, estado_meta):
    frontera = deque([(estado_inicial, [], 0)])
    visitados = set()
    paso = 1
    
    while frontera:
        actual, camino, costo_total = frontera.popleft()
        ubicacion, pendientes = actual
        
        print(f"\n[Paso {paso}] Analizando estado...")
        print(f"   📍 Ubicación actual del camión : {ubicacion}")
        print(f"   📦 Paquetes pendientes        : {pendientes}")
        print(f"   ⛽ Costo acumulado hasta aquí : {costo_total} km")
        time.sleep(1.5) # Pausa visual de 1.5 segundos para simular el proceso
        
        if actual == estado_meta:
            print("\n" + "!"*55)
            print(f" ¡ÉXITO! Vehículo de vuelta en el Almacén sin paquetes.")
            print(f" Distancia total óptima recorrida: {costo_total} km")
            print(f" Ruta óptima de acciones: {' -> '.join(camino)}")
            print("!"*55)
            return
            
        if actual in visitados:
            print("   -> Estado ya visitado anteriormente. Ignorando...")
            continue
        visitados.add(actual)
        
        # Generar sucesores de entrega
        if ubicacion in pendientes:
            nuevos_pendientes = tuple(p for p in pendientes if p != ubicacion)
            siguiente_estado = (ubicacion, nuevos_pendientes)
            if siguiente_estado not in visitados:
                accion = f"Entregar paquete en {ubicacion}"
                print(f"   ➕ Añadiendo a frontera -> Acción: {accion}")
                frontera.append((siguiente_estado, camino + [accion], costo_total))
                
        # Generar sucesores de movimiento vial
        for vecino in G1.successors(ubicacion):
            costo_arista = G1[ubicacion][vecino]['weight']
            siguiente_estado = (vecino, pendientes)
            if siguiente_estado not in visitados:
                accion = f"Moverse a {vecino}"
                print(f"   ➕ Añadiendo a frontera -> Acción: {accion} (Costo: +{costo_arista} km)")
                frontera.append((siguiente_estado, camino + [accion], costo_total + costo_arista))
        
        paso += 1

# Ejecutar simulación 1
simulacion_en_vivo_logistica(('Almacen', ('Cliente_A', 'Cliente_B')), ('Almacen', ()))


print("\n\n==================================================================")
print(" 2. INICIANDO SIMULACIÓN EN VIVO: ROBOT EN PLANTA INDUSTRIAL")
print("==================================================================")
time.sleep(2)

# Grafo de la cuadrícula del robot
G2 = nx.DiGraph()
obstaculos = {(1, 1), (2, 1)}
zonas_pesadas = {(1, 2): 3, (2, 2): 3}

for x in range(4):
    for y in range(4):
        if (x, y) in obstaculos: continue
        for dir_n, (nx_p, ny_p) in [('Norte', (x, y+1)), ('Sur', (x, y-1)), ('Este', (x+1, y)), ('Oeste', (x-1, y))]:
            if 0 <= nx_p < 4 and 0 <= ny_p < 4 and (nx_p, ny_p) not in obstaculos:
                costo = zonas_pesadas.get((nx_p, ny_p), 1)
                G2.add_edge((x, y), (nx_p, ny_p), weight=costo, direccion=dir_n)

def simulacion_en_vivo_robot(inicio, meta):
    frontera = deque([(inicio, [], 0)])
    visitados = set()
    paso = 1
    
    while frontera:
        actual, camino, energia = frontera.popleft()
        
        print(f"\n[Paso {paso}] Robot escaneando entorno...")
        print(f"   🤖 Posición de coordenadas (x, y) : {actual}")
        print(f"   🔋 Energía total consumida       : {energia} unidades")
        time.sleep(1.2) # Pausa visual de 1.2 segundos
        
        if actual == meta:
            print("\n" + "!"*55)
            print(f" ¡ÉXITO! Robot llegó a la Estación de Ensamblado (3,3).")
            print(f" Consumo energético total óptimo  : {energia} unidades")
            print(f" Secuencia de movimientos         : {' -> '.join(camino)}")
            print("!"*55)
            return
            
        if actual in visitados:
            print("   -> Celda ya procesada. Saltando...")
            continue
        visitados.add(actual)
        
        for vecino in G2.successors(actual):
            costo_movimiento = G2[actual][vecino]['weight']
            dir_mov = G2[actual][vecino]['direccion']
            if vecino not in visitados:
                accion = f"Mover {dir_mov} a {vecino}"
                print(f"   ➕ Casilla accesible encontrada -> {accion} (Costo: {costo_movimiento})")
                frontera.append((vecino, camino + [accion], energia + costo_movimiento))
                
        paso += 1

# Ejecutar simulación 2
simulacion_en_vivo_robot((0, 0), (3, 3))