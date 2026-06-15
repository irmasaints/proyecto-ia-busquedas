# Equipo 4
# Hernandez Ornelas Mariel
# Sánchez Santos Irma Nayeli
# Maldonado Romero Daniel

import streamlit as st
from estilos import aplicar_estilos_personalizados, PALETA

from no_informada import buscar_bfs, buscar_dfs
from informada import buscar_greedy, buscar_a_estrella, buscar_greedy_sokoban_2cajas, buscar_a_estrella_sokoban_2cajas
from local import buscar_hill_climbing, buscar_recocido_simulado
from adversaria import (
    obtener_mejor_movimiento_sin_poda,
    obtener_mejor_movimiento_con_poda,
    verificar_ganador
)

st.set_page_config(page_title="IA Visualizer Academic", layout="wide")
aplicar_estilos_personalizados()

st.title("🧠 Visualizador de algoritmos de busqueda")
st.markdown("---")

if "paso_idx" not in st.session_state:
    st.session_state.paso_idx = 0
if "historial" not in st.session_state:
    st.session_state.historial = []
if "camino" not in st.session_state:
    st.session_state.camino = []
if "calculado" not in st.session_state:
    st.session_state.calculado = False
if "problema_previo" not in st.session_state:
    st.session_state.problema_previo = "Laberinto (Frozen Lake)"

# Estados exclusivos del Gato
if "tablero_gato" not in st.session_state:
    st.session_state.tablero_gato = [" "] * 9
if "ganador_gato" not in st.session_state:
    st.session_state.ganador_gato = None
if "nodos_evaluados" not in st.session_state:
    st.session_state.nodos_evaluados = 0
if "quien_empieza_gato" not in st.session_state:
    st.session_state.quien_empieza_gato = "IA"
if "quien_empieza_gato_previo" not in st.session_state:
    st.session_state.quien_empieza_gato_previo = "IA"

def limpiar_calculo():
    st.session_state.paso_idx = 0
    st.session_state.historial = []
    st.session_state.camino = []
    st.session_state.calculado = False

def reiniciar_gato():
    st.session_state.tablero_gato = [" "] * 9
    st.session_state.ganador_gato = None
    st.session_state.historial = []
    st.session_state.calculado = False
    st.session_state.paso_idx = 0
    st.session_state.nodos_evaluados = 0

def ejecutar_turno_ia_gato(algoritmo):
    tablero = st.session_state.tablero_gato
    if st.session_state.ganador_gato is not None: return
    if " " not in tablero:
        st.session_state.ganador_gato = verificar_ganador(tablero)
        return

    if algoritmo == "Minimax sin poda":
        mov, pasos, _, nodos = obtener_mejor_movimiento_sin_poda(list(tablero))
    else:
        mov, pasos, _, nodos = obtener_mejor_movimiento_con_poda(list(tablero))

    if mov is not None:
        tablero[mov] = "X"
        st.session_state.tablero_gato = tablero
        st.session_state.historial = pasos
        st.session_state.calculado = True
        st.session_state.paso_idx = 0
        st.session_state.nodos_evaluados = nodos
        st.session_state.ganador_gato = verificar_ganador(tablero)

# --- SIDEBAR CONFIGURACIÓN ---
st.sidebar.subheader("⚙️ Parámetros del Sistema")
problema = st.sidebar.selectbox("Selecciona el Problema:", [
    "Laberinto (Frozen Lake)",
    "Sokoban",
    "8 Reinas",
    "Gato (Tic-Tac-Toe)"
])

if problema != st.session_state.problema_previo:
    limpiar_calculo()
    if st.session_state.problema_previo == "Gato (Tic-Tac-Toe)":
        reiniciar_gato()
    st.session_state.problema_previo = problema

if problema == "Laberinto (Frozen Lake)":
    algoritmo = st.sidebar.selectbox("Algoritmo de Búsqueda:", ["BFS (Amplitud)", "DFS (Profundidad)"])
    mapa_activo = [["S", "F", "F", "F"], ["F", "H", "F", "H"], ["F", "F", "F", "H"], ["H", "F", "F", "G"]]
    inicio, meta = (0, 0), (3, 3)
elif problema == "Sokoban":
    algoritmo = st.sidebar.selectbox("Algoritmo de Búsqueda:", ["A* (A-Estrella)", "Greedy Best-First"])
    # MAPA CONFIGURADO Y OPTIMIZADO PARA MANIOBRAS DE 2 CAJAS (Mariel Original)
    mapa_activo = [
        ["S", "G", "F", "F", "G"],
        ["F", "F", "#", "F", "F"],
        ["F", "F", "F", "F", "F"],
        ["F", "#", "#", "#", "F"],
        ["F", "F", "F", "F", "F"]
    ]
    inicio, meta = ((0, 0), ((2, 1), (2, 3))), ((0, 1), (0, 4))
elif problema == "8 Reinas":
    algoritmo = st.sidebar.selectbox("Algoritmo de Búsqueda:", ["Hill Climbing (Escalada)", "Recocido Simulado"])
    mapa_activo = [0, 1, 2, 3, 4, 5, 6, 7]
    inicio, meta = None, None
elif problema == "Gato (Tic-Tac-Toe)":
    algoritmo = st.sidebar.selectbox("Algoritmo de Búsqueda:", ["Minimax sin poda", "Minimax con poda Alpha-Beta"])
    quien_empieza_gato = st.sidebar.radio("¿Quién empieza la partida?", ["IA", "Usuario"], index=0 if st.session_state.quien_empieza_gato == "IA" else 1)
    st.session_state.quien_empieza_gato = quien_empieza_gato

    if st.session_state.quien_empieza_gato != st.session_state.quien_empieza_gato_previo:
        reiniciar_gato()
        st.session_state.quien_empieza_gato_previo = st.session_state.quien_empieza_gato
        st.rerun()
    mapa_activo = None


# ================================================================
# INTERFAZ DEL GATO
# ================================================================
if problema == "Gato (Tic-Tac-Toe)":
    st.markdown("### 🎮 Tú eres O — La IA es X")
    st.markdown(f"Algoritmo activo: **{algoritmo}**")
    st.markdown(f"Empieza: **{st.session_state.quien_empieza_gato}**")

    st.markdown("""
    <style>
    .tablero-gato div[data-testid="stButton"] button {
        height: 120px !important;
        width: 120px !important;
        font-size: 56px !important;
        font-weight: 900 !important;
        border-radius: 12px !important;
        border: 2px solid #555 !important;
        background-color: #2a2a3e !important;
        color: #aaa !important;
        padding: 0 !important;
    }
    .tablero-gato div[data-testid="stButton"] button:hover:not(:disabled) {
        background-color: #3a3a5a !important;
        cursor: pointer !important;
    }
    </style>
    """, unsafe_allow_html=True)

    if st.session_state.quien_empieza_gato == "IA" and st.session_state.tablero_gato == [" "] * 9:
        ejecutar_turno_ia_gato(algoritmo)

    tablero = st.session_state.tablero_gato
    ganador = st.session_state.ganador_gato

    def estilo_celda(valor):
        if valor == "X": return "X"
        elif valor == "O": return "O"
        return " "

    st.markdown('<div class="tablero-gato">', unsafe_allow_html=True)
    for fila in range(3):
        cols = st.columns([1, 1, 1, 3])
        for col in range(3):
            i = fila * 3 + col
            label = estilo_celda(tablero[i])
            deshabilitado = (tablero[i] != " ") or (ganador is not None)
            with cols[col]:
                if st.button(label, key=f"celda_{i}", disabled=deshabilitado, use_container_width=True):
                    tablero[i] = "O"
                    st.session_state.tablero_gato = tablero
                    st.session_state.ganador_gato = verificar_ganador(tablero)
                    ejecutar_turno_ia_gato(algoritmo)
                    st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style='margin-top:12px; display:flex; gap:20px; font-size:15px;'>
        <span style='background:#1a3a5c; color:#4fc3f7; padding:4px 14px; border-radius:8px; font-weight:bold;'>X = IA</span>
        <span style='background:#3a1a1a; color:#ef9a9a; padding:4px 14px; border-radius:8px; font-weight:bold;'>O = Tú</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    if ganador == "O": st.success("¡Ganaste! 🎉")
    elif ganador == "X": st.error("Ganó la IA 🤖")
    elif ganador == "empate": st.warning("Empate 🤝")

    if st.session_state.calculado and len(st.session_state.historial) > 0:
        st.markdown("---")
        st.markdown("### Controles del Recorrido Manual")
        col_btn1, col_btn2, col_txt = st.columns([1, 1, 3])
        with col_btn1:
            if st.button("⬅️ Paso Anterior"):
                if st.session_state.paso_idx > 0: st.session_state.paso_idx -= 1
        with col_btn2:
            if st.button("Paso Siguiente ➡️"):
                if st.session_state.paso_idx < len(st.session_state.historial) - 1: st.session_state.paso_idx += 1
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
        reiniciar_gato()
        st.rerun()
    st.stop()


# ================================================================
# SIMULADOR MÉTODOS CENTRALES (Laberinto, Sokoban, Reinas)
# ================================================================
if st.button("🧮 Cargar y Calcular Ruta del Algoritmo"):
    limpiar_calculo()
    if algoritmo == "BFS (Amplitud)":
        st.session_state.camino, st.session_state.historial = buscar_bfs(mapa_activo, inicio, meta)
    elif algoritmo == "DFS (Profundidad)":
        st.session_state.camino, st.session_state.historial = buscar_dfs(mapa_activo, inicio, meta)
    elif algoritmo == "Greedy Best-First":
        if problema == "Sokoban":
            st.session_state.camino, st.session_state.historial = buscar_greedy_sokoban_2cajas(mapa_activo, inicio, meta)
        else:
            st.session_state.camino, st.session_state.historial = buscar_greedy(mapa_activo, inicio, meta)
    elif algoritmo == "A* (A-Estrella)":
        if problema == "Sokoban":
            st.session_state.camino, st.session_state.historial = buscar_a_estrella_sokoban_2cajas(mapa_activo, inicio, meta)
        else:
            st.session_state.camino, st.session_state.historial = buscar_a_estrella(mapa_activo, inicio, meta)
    elif algoritmo == "Hill Climbing (Escalada)":
        st.session_state.camino, st.session_state.historial = buscar_hill_climbing(mapa_activo)
    elif algoritmo == "Recocido Simulado":
        st.session_state.camino, st.session_state.historial = buscar_recocido_simulado(mapa_activo)
    st.session_state.calculado = True

def renderizar(mapa, visitados=None, camino=None, actual=None):
    if visitados is None: visitados = []
    if camino is None: camino = []

    if isinstance(mapa, list) and len(mapa) == 8 and all(isinstance(x, int) for x in mapa):
        estado_reinas = actual if actual is not None else mapa
        html = "<div style='display: grid; grid-template-columns: repeat(8, 50px); gap: 4px; justify-content: center; margin-bottom: 20px;'>"
        for r in range(8):
            for c in range(8):
                es_negro = (r + c) % 2 == 1
                color = "#769656" if es_negro else "#eeeed2"
                icono = "👑" if estado_reinas[c] == r else ""
                html += f"<div style='width:50px; height:50px; background:{color}; display:flex; align-items:center; justify-content:center; font-size:24px; border: 1px solid #bdc3c7;'>{icono}</div>"
        return html + "</div>"

    filas, columnas = len(mapa), len(mapa[0])
    
    if problema == "Sokoban" and isinstance(actual, tuple) and isinstance(actual[0], tuple):
        pos_j, pos_cajas = actual
        caja1, caja2 = pos_cajas
        metas_g = [(0, 1), (0, 4)] 
    else:
        pos_j, caja1, caja2 = actual, None, None
        metas_g = [(3, 3)] if problema == "Laberinto (Frozen Lake)" else []

    html = f"<div style='display: grid; grid-template-columns: repeat({columnas}, 65px); gap: 10px; justify-content: center;'>"
    for r in range(filas):
        for c in range(columnas):
            color = PALETA["janna"]
            icono = ""
            
            # CAMBIO DE AVATAR: Colocamos el emoji del operario del almacén en lugar del robot
            if (r, c) == pos_j: color, icono = PALETA["bondi_blue"], "👷‍♂️"
            elif (r, c) == caja1 or (r, c) == caja2: color, icono = "#d97706", "📦"
            elif (r, c) in metas_g: color, icono = PALETA["san_marino"], "🏆"
            elif mapa[r][c] in ["H", "#"]: color, icono = PALETA["eden"], "🧱"
            elif (r, c) in camino: color, icono = PALETA["sinbad"], "✨"
            elif (r, c) in visitados: color, icono = "#233142", "•"
            font_color = PALETA["fondo_oscuro"] if color == PALETA["janna"] else "white"
            html += f"<div style='width:65px; height:65px; background:{color}; border-radius:10px; display:flex; align-items:center; justify-content:center; color:{font_color}; font-size:20px; font-weight:bold;'>{icono}</div>"
    return html + "</div>"

def formatear_nodo(n):
    if isinstance(n, tuple) and len(n) == 2 and isinstance(n[0], tuple) and isinstance(n[1], tuple):
        pos_j, pos_cajas = n
        # Sincronizamos el texto de la bitácora para que muestre el mismo emoji del operario
        return f"👷‍♂️({pos_j[0]+1},{pos_j[1]+1}) 📦[{formatear_nodo(pos_cajas)}]"
    if isinstance(n, tuple) and len(n) == 2 and isinstance(n[0], tuple):
        return " y ".join([f"({c[0]+1},{c[1]+1})" for c in n])
    return f"({n[0]+1},{n[1]+1})"

if st.session_state.calculado and len(st.session_state.historial) > 0:
    st.markdown("---")
    st.markdown("### Controles del Recorrido Manual")

    col_btn1, col_btn2, col_txt = st.columns([1, 1, 3])
    with col_btn1:
        if st.button("⬅️ Paso Anterior"):
            if st.session_state.paso_idx > 0: st.session_state.paso_idx -= 1
    with col_btn2:
        if st.button("Paso Siguiente ➡️"):
            if st.session_state.paso_idx < len(st.session_state.historial) - 1: st.session_state.paso_idx += 1
    with col_txt:
        st.markdown(f"<p style='margin-top:10px; font-weight:bold; font-size:18px;'>Paso actual: {st.session_state.paso_idx + 1} / {len(st.session_state.historial)}</p>", unsafe_allow_html=True)

    idx = st.session_state.paso_idx
    es_final = (idx == len(st.session_state.historial) - 1)

    if problema == "8 Reinas":
        estado_reinas_actual, ataques_actual = st.session_state.historial[idx]
        st.subheader("Estado Gráfico del Tablero")
        st.markdown(renderizar(mapa_activo, actual=estado_reinas_actual), unsafe_allow_html=True)
        if es_final:
            if ataques_actual == 0: st.success("👑 ¡Solución perfecta encontrada! 0 ataques mutuos entre reinas.")
            else: st.warning(f"⚠️ El algoritmo local terminó y se detuvo en un óptimo local con {ataques_actual} ataques.")
        st.markdown("---")
        st.subheader("Desarrollo del Algoritmo")
        st.markdown(f"""
        <div class="box-ejercicio">
            <h4>PASO {idx + 1} — Configuración Activa de Reinas</h4>
            <p class="linea-open">Posición de Reinas (Estructura de columnas): {estado_reinas_actual}</p>
            <p class="linea-closed">💥 Número Total de Parejas en Conflicto / Ataques: {ataques_actual}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        nodo_actual, hijos, open_list, closed_list = st.session_state.historial[idx]
        camino_final = st.session_state.camino if es_final else []

        col_mapa, col_bitacora = st.columns([1.3, 1.7])
        with col_mapa:
            st.markdown(renderizar(mapa_activo, visitados=closed_list, camino=camino_final, actual=nodo_actual), unsafe_allow_html=True)
            if es_final and st.session_state.camino: st.success(f" Meta encontrada.")

        with col_bitacora:
            st.subheader("Desarrollo del Algoritmo")
            nodo_str = formatear_nodo(nodo_actual)
            
            if algoritmo in ["BFS (Amplitud)", "DFS (Profundidad)"]:
                str_hijos = "{" + ", ".join([formatear_nodo(n) for n in hijos]) + "}"
                str_open = "[" + ", ".join([formatear_nodo(n) for n in open_list]) + "]"
            else:
                str_hijos = "{" + ", ".join([f"({formatear_nodo(n)}, h:{v})" for n, v in hijos]) + "}"
                str_open = "[" + ", ".join([f"({formatear_nodo(n)}, h:{v})" for n, v in open_list]) + "]"
            str_closed = "{" + ", ".join([formatear_nodo(n) for n in closed_list]) + "}"
            etiqueta_estructura = "Pila" if algoritmo == "DFS (Profundidad)" else ("Cola" if algoritmo == "BFS (Amplitud)" else "OPEN")
            
            str_ruta = ""
            if es_final and st.session_state.camino:
                if problema == "Sokoban":
                    ruta_formateada = [formatear_nodo(est[1]) for est in st.session_state.camino]
                else:
                    ruta_formateada = [formatear_nodo(n) for n in st.session_state.camino]
                str_ruta = f"<p style='color:{PALETA['sinbad']}; font-weight:bold; margin-top:15px; font-size:16px;'>📍 Ruta encontrada:<br>{' ➔ '.join(ruta_formateada)}</p>"
                
            st.markdown(f"""
            <div class="box-ejercicio">
                <h4 style="margin-bottom: 5px;">S{idx+1} — {nodo_str}</h4>
                <p style="color: #f2e6cf; font-weight: bold; margin-bottom: 5px;">Hijos / Expandidos: {str_hijos if hijos else "Ninguno"}</p>
                <p class="linea-open" style="margin-bottom: 5px;">{etiqueta_estructura}: {str_open}</p>
                <p class="linea-closed" style="margin-bottom: 10px;">Visitados / CLOSED: {str_closed}</p>
                {str_ruta}
            </div>
            """, unsafe_allow_html=True)
else:
    if problema == "8 Reinas":
        st.subheader("Estado Gráfico del Tablero")
        st.markdown(renderizar(mapa_activo), unsafe_allow_html=True)
        st.markdown("---")
        st.subheader("Desarrollo del Algoritmo")
        st.markdown('<div class="box-ejercicio"><h4>Esperando Inicialización...</h4><p>Presiona el botón de arriba para calcular la optimización local del tablero.</p></div>', unsafe_allow_html=True)
    else:
        col_mapa, col_bitacora = st.columns([1.3, 1.7])
        with col_mapa:
            st.markdown(renderizar(mapa_activo if mapa_activo else [["S","G"]]), unsafe_allow_html=True)
        with col_bitacora:
            st.subheader("Desarrollo del Algoritmo")
            st.markdown('<div class="box-ejercicio"><h4>Esperando Inicialización...</h4><p>Presiona el botón de arriba para calcular el árbol de búsqueda.</p></div>', unsafe_allow_html=True)