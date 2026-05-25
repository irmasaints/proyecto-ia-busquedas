# no_informada.py
from collections import deque

def obtener_vecinos(pos, mapa):
    filas, columnas = len(mapa), len(mapa[0])
    r, c = pos
    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)] # Arriba, Abajo, Izquierda, Derecha
    vecinos = []
    for dr, dc in movimientos:
        nr, nc = r + dr, c + dc
        if 0 <= nr < filas and 0 <= nc < columnas and mapa[nr][nc] != 'H':
            vecinos.append((nr, nc))
    return vecinos

def buscar_bfs(mapa, inicio, meta):
    cola = deque([[inicio]])
    visitados = []
    historial_pasos = [] # Guardará tuplas de (nodo_actual, lista_OPEN, lista_CLOSED)

    while cola:
        # Reconstruir lista OPEN actual (solo las posiciones de destino en la cola)
        lista_open = [camino[-1] for camino in cola]
        
        camino = cola.popleft()
        nodo_actual = camino[-1]
        
        if nodo_actual not in visitados:
            visitados.append(nodo_actual)
            
            # Registrar el paso con copias de las listas
            historial_pasos.append((nodo_actual, list(lista_open), list(visitados)))
            
            if nodo_actual == meta:
                return camino, historial_pasos

            for vecino in obtener_vecinos(nodo_actual, mapa):
                if vecino not in visitados and vecino not in [c[-1] for c in cola]:
                    cola.append(list(camino) + [vecino])
                    
    return None, historial_pasos

def buscar_dfs(mapa, inicio, meta):
    pila = [[inicio]]
    visitados = []
    historial_pasos = []

    while pila:
        lista_open = [camino[-1] for camino in pila]
        
        camino = pila.pop()
        nodo_actual = camino[-1]

        if nodo_actual not in visitados:
            visitados.append(nodo_actual)
            historial_pasos.append((nodo_actual, list(lista_open), list(visitados)))

            if nodo_actual == meta:
                return camino, historial_pasos

            for vecino in reversed(obtener_vecinos(nodo_actual, mapa)):
                if vecino not in visitados:
                    pila.append(list(camino) + [vecino])
                    
    return None, historial_pasos