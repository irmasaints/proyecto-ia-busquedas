# no_informada.py
from collections import deque

def obtener_vecinos(pos, mapa):
    filas, columnas = len(mapa), len(mapa[0])
    r, c = pos
    # ORDEN 4-CONECTADO: Arriba, Derecha, Abajo, Izquierda
    movimientos = [(-1, 0), (0, 1), (1, 0), (0, -1)] 
    vecinos = []
    for dr, dc in movimientos:
        nr, nc = r + dr, c + dc
        # Ignorar tanto agujeros de Frozen Lake (H) como muros de Sokoban (#)
        if 0 <= nr < filas and 0 <= nc < columnas and mapa[nr][nc] not in ['H', '#']:
            vecinos.append((nr, nc))
    return vecinos

def buscar_bfs(mapa, inicio, meta):
    cola = deque([(inicio, [inicio])])
    visitados = []
    historial_pasos = []
    agregados_a_cola = {inicio}

    while cola:
        nodo_actual, camino = cola.popleft()
        
        if nodo_actual not in visitados:
            visitados.append(nodo_actual)
        
        if nodo_actual == meta:
            lista_open = [n for n, _ in cola]
            historial_pasos.append((nodo_actual, [], lista_open, list(visitados)))
            return camino, historial_pasos

        vecinos = obtener_vecinos(nodo_actual, mapa)
        hijos_validos = []
        
        for vecino in vecinos:
            if vecino not in visitados and vecino not in agregados_a_cola:
                cola.append((vecino, camino + [vecino]))
                agregados_a_cola.add(vecino)
                hijos_validos.append(vecino)
                
        lista_open = [n for n, _ in cola]
        historial_pasos.append((nodo_actual, hijos_validos, lista_open, list(visitados)))
                
    return None, historial_pasos

def buscar_dfs(mapa, inicio, meta):
    pila = [(inicio, [inicio])]
    visitados = []
    historial_pasos = []

    while pila:
        nodo_actual, camino = pila.pop()
        
        if nodo_actual not in visitados:
            visitados.append(nodo_actual)
            
        if nodo_actual == meta:
            lista_open = [n for n, _ in pila]
            historial_pasos.append((nodo_actual, [], lista_open, list(visitados)))
            return camino, historial_pasos

        vecinos = obtener_vecinos(nodo_actual, mapa)
        hijos_validos = []
        
        # En DFS invertimos la inserción para que al extraer el tope de la pila
        # se siga respetando el orden original: Arriba, Derecha, Abajo, Izquierda
        for vecino in reversed(vecinos): 
            if vecino not in visitados and vecino not in [n for n, _ in pila]:
                pila.append((vecino, camino + [vecino]))
                hijos_validos.append(vecino)
                
        lista_open = [n for n, _ in pila]
        historial_pasos.append((nodo_actual, hijos_validos[::-1], lista_open, list(visitados)))
                
    return None, historial_pasos