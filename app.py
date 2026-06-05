# app.py
import streamlit as st
from estilos import aplicar_estilos_personalizados, PALETA

from no_informada import buscar_bfs, buscar_dfs
from informada import buscar_greedy, buscar_a_estrella
from adversaria import (
    obtener_mejor_movimiento_sin_poda,
    obtener_mejor_movimiento_con_poda,
    verificar_ganador
)

st.set_page_config(page_title="IA Visualizer Academic", layout="wide")
aplicar_estilos_personalizados()

st.title("🧠 Visualizador Matemático de Algoritmos IA")
st.markdown("---")

# --- SIDEBAR ---
st.sidebar.subheader("⚙️ Parámetros del Sistema")
problema = st.sidebar.selectbox("Selecciona el Problema:", [
    "Laberinto (Frozen Lake)",
    "Sokoban",
    "Gato (Tic-Tac-Toe)"
])

if problema == "Laberinto (Frozen Lake)":
    algoritmo = st.sidebar.selectbox("Algoritmo de Búsqueda:", ["BFS (Amplitud)", "DFS (Profundidad)"])
    mapa_activo = [["S", "F", "F", "F"], ["F", "H", "F", "H"], ["F", "F", "F", "H"], ["H", "F", "F", "G"]]
    inicio, meta = (0, 0), (3, 3)
elif problema == "Sokoban":
    algoritmo = st.sidebar.selectbox("Algoritmo de Búsqueda:", ["A* (A-Estrella)", "Greedy Best-First"])
    mapa_activo = [["S", "F", "#", "F", "F"], ["F", "F", "#", "F", "G"], ["F", "F", "F", "F", "F"], ["#", "#", "F", "#", "#"]]
    inicio, meta = (0, 0), (1, 4)
elif problema == "Gato (Tic-Tac-Toe)":
    algoritmo = st.sidebar.selectbox("Algoritmo de Búsqueda:", [
        "Minimax sin poda",
        "Minimax con poda Alpha-Beta"
    ])
    mapa_activo = None

# --- ESTADOS GLOBALES ---
if "paso_idx" not in st.session_state:
    st.session_state.paso_idx = 0
if "historial" not in st.session_state:
    st.session_state.historial = []
if "camino" not in st.session_state:
    st.session_state.camino = []
if "calculado" not in st.session_state:
    st.session_state.calculado = False
if "tablero_gato" not in st.session_state:
    st.session_state.tablero_gato = [" "] * 9
if "ganador_gato" not in st.session_state:
    st.session_state.ganador_gato = None
if "nodos_evaluados" not in st.session_state:
    st.session_state.nodos_evaluados = 0

def limpiar_calculo():
    st.session_state.paso_idx = 0
    st.session_state.historial = []
    st.session_state.camino = []
    st.session_state.calculado = False

def renderizar(mapa, visitados=None, camino=None, actual=None):
    if visitados is None: visitados = []
    if camino is None: camino = []
    filas, columnas = len(mapa), len(mapa[0])
    html = f"<div style='display: grid; grid-template-columns: repeat({columnas}, 65px); gap: 10px; justify-content: center;'>"
    for r in range(filas):
        for c in range(columnas):
            color = PALETA["janna"]
            icono = ""
            if (r, c) == actual: color, icono = PALETA["bondi_blue"], "🤖"
            elif (r, c) == meta: color, icono = PALETA["san_marino"], "🏆"
            elif mapa[r][c] in ["H", "#"]: color, icono = PALETA["eden"], "🧱"
            elif (r, c) in camino: color, icono = PALETA["sinbad"], "✨"
            elif (r, c) in visitados: color, icono = "#233142", "•"
            font_color = PALETA["fondo_oscuro"] if color == PALETA["janna"] else "white"
            html += f"<div style='width:65px; height:65px; background:{color}; border-radius:10px; display:flex; align-items:center; justify-content:center; color:{font_color}; font-size:20px; font-weight:bold;'>{icono}</div>"
    return html + "</div>"

# --- CARD INFO ---
st.markdown(f'<div class="card-info"><h4>Entorno Activo: {problema}</h4><p>Visualización didáctica con conjuntos estructurados y control manual.</p></div>', unsafe_allow_html=True)


# ================================================================
# BLOQUE DEL GATO
# ================================================================
if problema == "Gato (Tic-Tac-Toe)":
    st.markdown("### 🎮 Tú eres O — La IA es X")
    st.markdown(f"Algoritmo activo: **{algoritmo}**")

    tablero = st.session_state.tablero_gato

    # Si el tablero está vacío, la IA abre el juego como X
    if tablero.count(" ") == 9 and not st.session_state.ganador_gato:
        if algoritmo == "Minimax sin poda":
            mov, pasos, _, nodos = obtener_mejor_movimiento_sin_poda(list(tablero))
        else:
            mov, pasos, _, nodos = obtener_mejor_movimiento_con_poda(list(tablero))
        tablero[mov] = "X"
        st.session_state.tablero_gato = tablero
        st.session_state.historial = pasos
        st.session_state.calculado = True
        st.session_state.nodos_evaluados = nodos

    # Renderizar tablero 3x3
    for fila in range(3):
        cols = st.columns(3)
        for col in range(3):
            i = fila * 3 + col
            with cols[col]:
                contenido = tablero[i]
                deshabilitado = (contenido != " ") or (st.session_state.ganador_gato is not None)
                if st.button(
                    contenido if contenido != " " else str(i + 1),
                    key=f"celda_{i}",
                    disabled=deshabilitado,
                    use_container_width=True
                ):
                    # Jugada del humano (O)
                    tablero[i] = "O"
                    ganador = verificar_ganador(tablero)

                    if not ganador:
                        # Jugada de la IA (X)
                        if algoritmo == "Minimax sin poda":
                            mov, pasos, _, nodos = obtener_mejor_movimiento_sin_poda(list(tablero))
                        else:
                            mov, pasos, _, nodos = obtener_mejor_movimiento_con_poda(list(tablero))

                        if mov is not None:
                            tablero[mov] = "X"
                            st.session_state.historial = pasos
                            st.session_state.calculado = True
                            st.session_state.paso_idx = 0
                            st.session_state.nodos_evaluados = nodos
                            ganador = verificar_ganador(tablero)

                    st.session_state.tablero_gato = tablero
                    st.session_state.ganador_gato = ganador
                    st.rerun()

    st.markdown("---")

    # Resultado
    ganador = st.session_state.ganador_gato
    if ganador == "O":
        st.success("¡Ganaste! 🎉")
    elif ganador == "X":
        st.error("Ganó la IA 🤖")
    elif ganador == "empate":
        st.warning("Empate 🤝")

    # Bitácora
    if st.session_state.calculado and len(st.session_state.historial) > 0:
        st.markdown("---")
        st.markdown("### 📋 Bitácora del último movimiento IA")

        col_btn1, col_btn2, col_txt = st.columns([1, 1, 3])
        with col_btn1:
            if st.button("⬅️ PASO ANTERIOR"):
                if st.session_state.paso_idx > 0:
                    st.session_state.paso_idx -= 1
        with col_btn2:
            if st.button("PASO SIGUIENTE ➡️"):
                if st.session_state.paso_idx < len(st.session_state.historial) - 1:
                    st.session_state.paso_idx += 1
        with col_txt:
            st.markdown(f"<p style='margin-top:10px; font-weight:bold; font-size:18px;'>Paso: {st.session_state.paso_idx + 1} / {len(st.session_state.historial)}</p>", unsafe_allow_html=True)

        idx = st.session_state.paso_idx
        celda_eval, open_list, closed_list = st.session_state.historial[idx]
        str_open   = ", ".join([f"celda {x+1}" for x in open_list])
        str_closed = ", ".join([f"celda {x+1}" for x in closed_list])

        st.markdown(f"""
        <div class="box-ejercicio">
            <h4>PASO {idx + 1} — IA evalúa celda {celda_eval + 1}</h4>
            <p class="linea-open">OPEN (por evaluar): [{str_open if str_open else "vacío"}]</p>
            <p class="linea-closed">CLOSED (evaluadas): [{str_closed}]</p>
            <hr style="border-color:{PALETA['eden']}; margin:10px 0;">
            <p style="font-size:14px; color:{PALETA['janna']} !important;">
                Nodos evaluados en este turno: <b>{st.session_state.nodos_evaluados}</b>
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    if st.button("🔄 Nueva partida"):
        st.session_state.tablero_gato = [" "] * 9
        st.session_state.ganador_gato = None
        st.session_state.historial = []
        st.session_state.calculado = False
        st.session_state.paso_idx = 0
        st.session_state.nodos_evaluados = 0
        st.rerun()

    st.stop()


# ================================================================
# BLOQUE LABERINTO Y SOKOBAN
# ================================================================
if st.button("🧮 CARGAR Y CALCULAR RUTA DEL ALGORITMO"):
    limpiar_calculo()
    if algoritmo == "BFS (Amplitud)":
        st.session_state.camino, st.session_state.historial = buscar_bfs(mapa_activo, inicio, meta)
    elif algoritmo == "DFS (Profundidad)":
        st.session_state.camino, st.session_state.historial = buscar_dfs(mapa_activo, inicio, meta)
    elif algoritmo == "Greedy Best-First":
        st.session_state.camino, st.session_state.historial = buscar_greedy(mapa_activo, inicio, meta)
    elif algoritmo == "A* (A-Estrella)":
        st.session_state.camino, st.session_state.historial = buscar_a_estrella(mapa_activo, inicio, meta)
    st.session_state.calculado = True

if st.session_state.calculado and len(st.session_state.historial) > 0:
    st.markdown("---")
    st.markdown("### 🎛️ Controles del Recorrido Manual")

    col_btn1, col_btn2, col_txt = st.columns([1, 1, 3])
    with col_btn1:
        if st.button("⬅️ PASO ANTERIOR"):
            if st.session_state.paso_idx > 0:
                st.session_state.paso_idx -= 1
    with col_btn2:
        if st.button("PASO SIGUIENTE ➡️"):
            if st.session_state.paso_idx < len(st.session_state.historial) - 1:
                st.session_state.paso_idx += 1
    with col_txt:
        st.markdown(f"<p style='margin-top:10px; font-weight:bold; font-size:18px;'>Paso actual: {st.session_state.paso_idx + 1} / {len(st.session_state.historial)}</p>", unsafe_allow_html=True)

    idx = st.session_state.paso_idx
    nodo_actual, open_list, closed_list = st.session_state.historial[idx]
    es_final = (idx == len(st.session_state.historial) - 1)
    camino_final = st.session_state.camino if es_final else []

    col_mapa, col_bitacora = st.columns([1.4, 1.6])
    with col_mapa:
        st.subheader("🗺️ Estado Gráfico")
        st.markdown(renderizar(mapa_activo, visitados=closed_list, camino=camino_final, actual=nodo_actual), unsafe_allow_html=True)
        if es_final and st.session_state.camino:
            st.success("🏁 Meta encontrada. Camino óptimo completado.")

    with col_bitacora:
        st.subheader("📋 Bitácora Matemática de Desarrollo")
        if algoritmo in ["BFS (Amplitud)", "DFS (Profundidad)"]:
            str_open = ", ".join([f"({r},{c})" for r, c in open_list])
        else:
            str_open = ", ".join([f"({nod[0]},{nod[1]} | v:{val})" for nod, val in open_list])
        str_closed = ", ".join([f"({r},{c})" for r, c in closed_list])

        st.markdown(f"""
        <div class="box-ejercicio">
            <h4>PASO {idx + 1} — Evaluando Nodo {nodo_actual}</h4>
            <p class="linea-open">OPEN: [{str_open}]</p>
            <p class="linea-closed">CLOSED: [{str_closed}]</p>
            <hr style="border-color:{PALETA['eden']}; margin:10px 0;">
            <p style="font-size:14px; font-family:sans-serif; color:{PALETA['janna']} !important;">
            {"<b>¡Meta alcanzada!</b> El proceso de búsqueda termina de forma exitosa." if es_final else "El algoritmo extrae el nodo prioritario de OPEN, analiza sus celdas adyacentes y las añade a la frontera evaluando su costo."}
            </p>
        </div>
        """, unsafe_allow_html=True)
else:
    col_mapa, col_bitacora = st.columns([1.4, 1.6])
    with col_mapa:
        st.subheader("🗺️ Estado Gráfico")
        st.markdown(renderizar(mapa_activo), unsafe_allow_html=True)
    with col_bitacora:
        st.subheader("📋 Bitácora Matemática de Desarrollo")
        st.markdown('<div class="box-ejercicio"><h4>Esperando Inicialización...</h4><p>Presiona el botón de arriba para calcular el árbol de búsqueda.</p></div>', unsafe_allow_html=True)