import heapq

def heuristica_manhattan(p1, p2):
    """Distancia Manhattan estándar para un solo punto."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def obtener_vecinos(pos, mapa):
    """Vecinos estándar para una sola coordenada."""
    filas, columnas = len(mapa), len(mapa[0])
    r, c = pos
    movimientos = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    vecinos = []
    for dr, dc in movimientos:
        nr, nc = r + dr, c + dc
        if 0 <= nr < filas and 0 <= nc < columnas and mapa[nr][nc] not in ['H', '#']:
            vecinos.append((nr, nc))
    return vecinos

# -------------------------------------------------------------
# ALGORITMOS ESTÁNDAR (Laberinto y otros mapas de 1 coordenada)
# -------------------------------------------------------------
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


# -------------------------------------------------------------
# FUNCIONES EXCLUSIVAS PARA SOKOBAN DE 2 CAJAS
# -------------------------------------------------------------
def heuristica_manhattan_sokoban(pos_cajas, metas):
    """Suma las distancias mínimas cruzadas de las dos cajas a las metas."""
    caja1, caja2 = pos_cajas
    meta1, meta2 = metas
    dist1 = (abs(caja1[0] - meta1[0]) + abs(caja1[1] - meta1[1])) + (abs(caja2[0] - meta2[0]) + abs(caja2[1] - meta2[1]))
    dist2 = (abs(caja1[0] - meta2[0]) + abs(caja1[1] - meta2[1])) + (abs(caja2[0] - meta1[0]) + abs(caja2[1] - meta1[1]))
    return min(dist1, dist2)

def obtener_sucesores_sokoban_2cajas(estado_actual, mapa):
    pos_j, pos_cajas = estado_actual
    caja1, caja2 = pos_cajas
    filas, columnas = len(mapa), len(mapa[0])
    movimientos = [(-1, 0), (0, 1), (1, 0), (0, -1)] # Arriba, Derecha, Abajo, Izquierda
    sucesores = []

    for dr, dc in movimientos:
        nj_r, nj_c = pos_j[0] + dr, pos_j[1] + dc
        nueva_pos_j = (nj_r, nj_c)

        if 0 <= nj_r < filas and 0 <= nj_c < columnas and mapa[nj_r][nj_c] != '#':
            # Intentar empujar Caja 1
            if nueva_pos_j == caja1:
                nc_r, nc_c = caja1[0] + dr, caja1[1] + dc
                nueva_caja1 = (nc_r, nc_c)
                if 0 <= nc_r < filas and 0 <= nc_c < columnas:
                    if mapa[nc_r][nc_c] != '#' and nueva_caja1 != caja2:
                        nuevas_cajas = tuple(sorted([nueva_caja1, caja2]))
                        sucesores.append((nueva_pos_j, nuevas_cajas))
            # Intentar empujar Caja 2
            elif nueva_pos_j == caja2:
                nc_r, nc_c = caja2[0] + dr, caja2[1] + dc
                nueva_caja2 = (nc_r, nc_c)
                if 0 <= nc_r < filas and 0 <= nc_c < columnas:
                    if mapa[nc_r][nc_c] != '#' and nueva_caja2 != caja1:
                        nuevas_cajas = tuple(sorted([caja1, nueva_caja2]))
                        sucesores.append((nueva_pos_j, nuevas_cajas))
            # Movimiento simple sobre celda vacía
            else:
                sucesores.append((nueva_pos_j, pos_cajas))
    return sucesores

def buscar_greedy_sokoban_2cajas(mapa, inicio_completo, metas_cajas):
    prioridad_queue = [(heuristica_manhattan_sokoban(inicio_completo[1], metas_cajas), inicio_completo, [inicio_completo])]
    visitados = []
    historial_pasos = []

    while prioridad_queue:
        h_act, estado_actual, camino = heapq.heappop(prioridad_queue)

        if estado_actual in visitados:
            continue
        visitados.append(estado_actual)

        pos_j, pos_cajas = estado_actual

        lista_open_limpia = []
        vistos_en_open = set()
        for h, est, _ in sorted(prioridad_queue):
            if est not in visitados and est[1] not in vistos_en_open:
                lista_open_limpia.append((est[1], h))
                vistos_en_open.add(est[1])

        if pos_cajas == metas_cajas:
            lista_closed_academicas = [est[1] for est in visitados]
            historial_pasos.append((estado_actual, [], lista_open_limpia, lista_closed_academicas))
            return camino, historial_pasos

        sucesores = obtener_sucesores_sokoban_2cajas(estado_actual, mapa)
        hijos_validos = []

        for prox_estado in sucesores:
            if prox_estado not in visitados:
                h_vec = heuristica_manhattan_sokoban(prox_estado[1], metas_cajas)
                heapq.heappush(prioridad_queue, (h_vec, prox_estado, camino + [prox_estado]))
                hijos_validos.append((prox_estado[1], h_vec))

        lista_open_limpia = []
        vistos_en_open = set()
        for h, est, _ in sorted(prioridad_queue):
            if est not in visitados and est[1] not in vistos_en_open:
                lista_open_limpia.append((est[1], h))
                vistos_en_open.add(est[1])

        lista_closed_academicas = [est[1] for est in visitados]
        historial_pasos.append((estado_actual, hijos_validos, lista_open_limpia, lista_closed_academicas))

    return None, historial_pasos

def buscar_a_estrella_sokoban_2cajas(mapa, inicio_completo, metas_cajas):
    prioridad_queue = [(heuristica_manhattan_sokoban(inicio_completo[1], metas_cajas), 0, inicio_completo, [inicio_completo])]
    visitados_eval = {}
    visitados_orden = []
    historial_pasos = []

    while prioridad_queue:
        f_act, g, estado_actual, camino = heapq.heappop(prioridad_queue)

        if estado_actual in visitados_eval and visitados_eval[estado_actual] <= g:
            continue
            
        visitados_eval[estado_actual] = g
        if estado_actual not in visitados_orden:
            visitados_orden.append(estado_actual)

        lista_open_limpia = []
        vistos_en_open = set()
        for f_val, _, est, _ in sorted(prioridad_queue):
            if est not in visitados_orden and est[1] not in vistos_en_open:
                lista_open_limpia.append((est[1], f_val))
                vistos_en_open.add(est[1])

        pos_j, pos_cajas = estado_actual

        if pos_cajas == metas_cajas:
            lista_closed_academicas = [est[1] for est in visitados_orden]
            historial_pasos.append((estado_actual, [], lista_open_limpia, lista_closed_academicas))
            return camino, historial_pasos

        sucesores = obtener_sucesores_sokoban_2cajas(estado_actual, mapa)
        hijos_validos = []

        for prox_estado in sucesores:
            nuevo_g = g + 1
            if prox_estado not in visitados_eval or nuevo_g < visitados_eval.get(prox_estado, float('inf')):
                f_nuevo = nuevo_g + heuristica_manhattan_sokoban(prox_estado[1], metas_cajas)
                heapq.heappush(prioridad_queue, (f_nuevo, nuevo_g, prox_estado, camino + [prox_estado]))
                hijos_validos.append((prox_estado[1], f_nuevo))
                
        lista_open_limpia = []
        vistos_en_open = set()
        for f_val, _, est, _ in sorted(prioridad_queue):
            if est not in visitados_orden and est[1] not in vistos_en_open:
                lista_open_limpia.append((est[1], f_val))
                vistos_en_open.add(est[1])
                
        lista_closed_academicas = [est[1] for est in visitados_orden]
        historial_pasos.append((estado_actual, hijos_validos, lista_open_limpia, lista_closed_academicas))
                
    return None, historial_pasos