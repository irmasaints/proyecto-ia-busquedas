# adversaria.py

LINEAS_GANADORAS = [
    [0,1,2],[3,4,5],[6,7,8],
    [0,3,6],[1,4,7],[2,5,8],
    [0,4,8],[2,4,6]
]

# Revisa si alguna de las 8 líneas está completa con el mismo símbolo
def verificar_ganador(tablero):
    for a, b, c in LINEAS_GANADORAS:
        if tablero[a] == tablero[b] == tablero[c] and tablero[a] != " ":
            return tablero[a]
    if " " not in tablero: 
        return "empate" # Si no hay espacios vacíos y nadie ganó, es empate.
    return None # Si el juego sigue, retorna None.

# ─── SIN PODA ───────────────────────────────────────────────
def minimax(tablero, depth, es_maximizador):
    ganador = verificar_ganador(tablero)
    if ganador == "X": return 10 - depth  # IA gana
    if ganador == "O": return depth - 10  # humano gana
    if ganador == "empate": return 0

    if es_maximizador:
        mejor = float("-inf")
        for i in range(9):
            if tablero[i] == " ":
                tablero[i] = "X"
                puntaje = minimax(tablero, depth + 1, False)
                tablero[i] = " "
                mejor = max(mejor, puntaje)
        return mejor
    else:
        mejor = float("inf")
        for i in range(9):
            if tablero[i] == " ":
                tablero[i] = "O"
                puntaje = minimax(tablero, depth + 1, True)
                tablero[i] = " "
                mejor = min(mejor, puntaje)
        return mejor

def obtener_mejor_movimiento_sin_poda(tablero):
    historial_pasos = []
    mejor_puntaje = float("-inf")
    mejor_movimiento = None
    nodos_evaluados = 0

    celdas_vacias = [i for i in range(9) if tablero[i] == " "]
    open_list = list(celdas_vacias)
    closed_list = []

    for i in celdas_vacias:
        tablero[i] = "X"
        puntaje = minimax(tablero, 0, False)
        tablero[i] = " "
        nodos_evaluados += 1

        open_list = [x for x in open_list if x != i]
        closed_list.append(i)
        historial_pasos.append((i, list(open_list), list(closed_list)))

        if puntaje > mejor_puntaje:
            mejor_puntaje = puntaje
            mejor_movimiento = i

    return mejor_movimiento, historial_pasos, mejor_puntaje, nodos_evaluados


# ─── CON PODA ALPHA-BETA ────────────────────────────────────
def minimax_alpha_beta(tablero, depth, es_maximizador, alpha, beta):
    ganador = verificar_ganador(tablero)
    if ganador == "X": return 10 - depth  # IA gana
    if ganador == "O": return depth - 10  # humano gana
    if ganador == "empate": return 0

    if es_maximizador:
        mejor = float("-inf")
        for i in range(9):
            if tablero[i] == " ":
                tablero[i] = "X"
                puntaje = minimax_alpha_beta(tablero, depth + 1, False, alpha, beta)
                tablero[i] = " "
                mejor = max(mejor, puntaje)
                alpha = max(alpha, mejor)
                if beta <= alpha:
                    break
        return mejor
    else:
        mejor = float("inf")
        for i in range(9):
            if tablero[i] == " ":
                tablero[i] = "O"
                puntaje = minimax_alpha_beta(tablero, depth + 1, True, alpha, beta)
                tablero[i] = " "
                mejor = min(mejor, puntaje)
                beta = min(beta, mejor)
                if beta <= alpha:
                    break
        return mejor

def obtener_mejor_movimiento_con_poda(tablero):
    historial_pasos = []
    mejor_puntaje = float("-inf")
    mejor_movimiento = None
    nodos_evaluados = 0

    celdas_vacias = [i for i in range(9) if tablero[i] == " "]
    open_list = list(celdas_vacias)
    closed_list = []

    for i in celdas_vacias:
        tablero[i] = "X"
        puntaje = minimax_alpha_beta(tablero, 0, False, float("-inf"), float("inf"))
        tablero[i] = " "
        nodos_evaluados += 1

        open_list = [x for x in open_list if x != i]
        closed_list.append(i)
        historial_pasos.append((i, list(open_list), list(closed_list)))

        if puntaje > mejor_puntaje:
            mejor_puntaje = puntaje
            mejor_movimiento = i

    return mejor_movimiento, historial_pasos, mejor_puntaje, nodos_evaluados