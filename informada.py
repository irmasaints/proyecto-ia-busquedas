# informada.py
import heapq

def heuristica_manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def obtener_vecinos(pos, mapa):
    filas, columnas = len(mapa), len(mapa[0])
    r, c = pos
    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    vecinos = []
    for dr, dc in movimientos:
        nr, nc = r + dr, c + dc
        if 0 <= nr < filas and 0 <= nc < columnas and mapa[nr][nc] != '#':
            vecinos.append((nr, nc))
    return vecinos

def buscar_greedy(mapa, inicio, meta):
    # Formato: (heuristica, nodo, camino)
    prioridad_queue = [(heuristica_manhattan(inicio, meta), inicio, [inicio])]
    visitados = []
    historial_pasos = []

    while prioridad_queue:
        # Generar lista OPEN ordenada por prioridad para la bitácora h(n)
        lista_open = [(nodo, h) for h, nodo, _ in sorted(prioridad_queue)]
        
        h_act, nodo_actual, camino = heapq.heappop(prioridad_queue)

        if nodo_actual in visitados:
            continue
            
        visitados.append(nodo_actual)
        historial_pasos.append((nodo_actual, lista_open, list(visitados)))

        if nodo_actual == meta:
            return camino, historial_pasos

        for vecino in obtener_vecinos(nodo_actual, mapa):
            if vecino not in visitados and vecino not in [n for _, n, _ in prioridad_queue]:
                h_vec = heuristica_manhattan(vecino, meta)
                heapq.heappush(prioridad_queue, (h_vec, vecino, camino + [vecino]))
                
    return None, historial_pasos

def buscar_a_estrella(mapa, inicio, meta):
    # Formato: (f_total, g_costo, nodo, camino)
    prioridad_queue = [(heuristica_manhattan(inicio, meta), 0, inicio, [inicio])]
    visitados_eval = {}
    visitados_orden = []
    historial_pasos = []

    while prioridad_queue:
        lista_open = [(nodo, f) for f, _, nodo, _ in sorted(prioridad_queue)]
        
        f, g, nodo_actual, camino = heapq.heappop(prioridad_queue)

        if nodo_actual in visitados_eval and visitados_eval[nodo_actual] <= g:
            continue
            
        visitados_eval[nodo_actual] = g
        if nodo_actual not in visitados_orden:
            visitados_orden.append(nodo_actual)
            
        historial_pasos.append((nodo_actual, lista_open, list(visitados_orden)))

        if nodo_actual == meta:
            return camino, historial_pasos

        for vecino in obtener_vecinos(nodo_actual, mapa):
            nuevo_g = g + 1
            if vecino not in visitados_eval or nuevo_g < visitados_eval.get(vecino, float('inf')):
                f_nuevo = nuevo_g + heuristica_manhattan(vecino, meta)
                heapq.heappush(prioridad_queue, (f_nuevo, nuevo_g, vecino, camino + [vecino]))
                
    return None, historial_pasos