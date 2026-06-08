import heapq

def heuristica_manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def obtener_vecinos(pos, mapa):
    filas, columnas = len(mapa), len(mapa[0])
    r, c = pos
    movimientos = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    vecinos = []
    for dr, dc in movimientos:
        nr, nc = r + dr, c + dc
        if 0 <= nr < filas and 0 <= nc < columnas and mapa[nr][nc] not in ['H', '#']:
            vecinos.append((nr, nc))
    return vecinos

def buscar_greedy(mapa, inicio, meta):
    prioridad_queue = [(heuristica_manhattan(inicio, meta), inicio, [inicio])]
    visitados = []
    historial_pasos = []

    while prioridad_queue:
        h_act, nodo_actual, camino = heapq.heappop(prioridad_queue)

        if nodo_actual in visitados:
            continue
            
        visitados.append(nodo_actual)

        lista_open_limpia = []
        vistos_en_open = set()
        for h, n, _ in sorted(prioridad_queue):
            if n not in visitados and n not in vistos_en_open:
                lista_open_limpia.append((n, h))
                vistos_en_open.add(n)

        if nodo_actual == meta:
            historial_pasos.append((nodo_actual, [], lista_open_limpia, list(visitados)))
            return camino, historial_pasos

        vecinos = obtener_vecinos(nodo_actual, mapa)
        hijos_validos = []

        for vecino in vecinos:
            if vecino not in visitados:
                h_vec = heuristica_manhattan(vecino, meta)
                heapq.heappush(prioridad_queue, (h_vec, vecino, camino + [vecino]))
                hijos_validos.append((vecino, h_vec))
                

        lista_open_limpia = []
        vistos_en_open = set()
        for h, n, _ in sorted(prioridad_queue):
            if n not in visitados and n not in vistos_en_open:
                lista_open_limpia.append((n, h))
                vistos_en_open.add(n)
                
        historial_pasos.append((nodo_actual, hijos_validos, lista_open_limpia, list(visitados)))
                
    return None, historial_pasos

def buscar_a_estrella(mapa, inicio, meta):
    prioridad_queue = [(heuristica_manhattan(inicio, meta), 0, inicio, [inicio])]
    visitados_eval = {}
    visitados_orden = []
    historial_pasos = []

    while prioridad_queue:
        f_act, g, nodo_actual, camino = heapq.heappop(prioridad_queue)

        if nodo_actual in visitados_eval and visitados_eval[nodo_actual] <= g:
            continue
            
        visitados_eval[nodo_actual] = g
        if nodo_actual not in visitados_orden:
            visitados_orden.append(nodo_actual)

        # --- FILTRO ACADÉMICO PARA OPEN ---
        lista_open_limpia = []
        vistos_en_open = set()
        for f_val, _, n, _ in sorted(prioridad_queue):
            if n not in visitados_orden and n not in vistos_en_open:
                lista_open_limpia.append((n, f_val))
                vistos_en_open.add(n)

        if nodo_actual == meta:
            historial_pasos.append((nodo_actual, [], lista_open_limpia, list(visitados_orden)))
            return camino, historial_pasos

        vecinos = obtener_vecinos(nodo_actual, mapa)
        hijos_validos = []

        for vecino in vecinos:
            nuevo_g = g + 1
            if vecino not in visitados_eval or nuevo_g < visitados_eval.get(vecino, float('inf')):
                f_nuevo = nuevo_g + heuristica_manhattan(vecino, meta)
                heapq.heappush(prioridad_queue, (f_nuevo, nuevo_g, vecino, camino + [vecino]))
                hijos_validos.append((vecino, f_nuevo))
                
        lista_open_limpia = []
        vistos_en_open = set()
        for f_val, _, n, _ in sorted(prioridad_queue):
            if n not in visitados_orden and n not in vistos_en_open:
                lista_open_limpia.append((n, f_val))
                vistos_en_open.add(n)
                
        historial_pasos.append((nodo_actual, hijos_validos, lista_open_limpia, list(visitados_orden)))
                
    return None, historial_pasos