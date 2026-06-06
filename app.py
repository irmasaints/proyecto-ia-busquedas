# app.py
import streamlit as st
from estilos import aplicar_estilos_personalizados, PALETA

from no_informada import buscar_bfs, buscar_dfs
from informada import buscar_greedy, buscar_a_estrella
from local import buscar_hill_climbing, buscar_recocido_simulado

st.set_page_config(page_title="IA Visualizer Academic", layout="wide")
aplicar_estilos_personalizados()

st.title("🧠 Visualizador Matemático de Algoritmos IA")
st.markdown("---")

# --- CONTROL DE LIMPIEZA AUTOMÁTICA EN CAMBIOS DE MENÚ ---
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

# Función para limpiar el estado al cambiar configuraciones o problemas
def limpiar_calculo():
    st.session_state.paso_idx = 0
    st.session_state.historial = []
    st.session_state.camino = []
    st.session_state.calculado = False

# --- SIDEBAR CONFIGURACIÓN ---
st.sidebar.subheader("⚙️ Parámetros del Sistema")
problema = st.sidebar.selectbox("Selecciona el Problema:", ["Laberinto (Frozen Lake)", "Sokoban", "8 Reinas"])

# Si el usuario cambia el problema en el menú, limpiamos la memoria antes de renderizar
if problema != st.session_state.problema_previo:
    limpiar_calculo()
    st.session_state.problema_previo = problema

if problema == "Laberinto (Frozen Lake)":
    algoritmo = st.sidebar.selectbox("Algoritmo de Búsqueda:", ["BFS (Amplitud)", "DFS (Profundidad)"])
    mapa_activo = [["S", "F", "F", "F"], ["F", "H", "F", "H"], ["F", "F", "F", "H"], ["H", "F", "F", "G"]]
    inicio, meta = (0, 0), (3, 3)
elif problema == "Sokoban":
    algoritmo = st.sidebar.selectbox("Algoritmo de Búsqueda:", ["A* (A-Estrella)", "Greedy Best-First"])
    mapa_activo = [["S", "F", "#", "F", "F"], ["F", "F", "#", "F", "G"], ["F", "F", "F", "F", "F"], ["#", "#", "F", "#", "#"]]
    inicio, meta = (0, 0), (1, 4)
else:
    algoritmo = st.sidebar.selectbox("Algoritmo de Búsqueda:", ["Hill Climbing (Escalada)", "Recocido Simulado"])
    mapa_activo = [0, 1, 2, 3, 4, 5, 6, 7]  # Configuración diagonal base
    inicio, meta = None, None

# --- RENDER PRINCIPAL ---
st.markdown(f'<div class="card-info"><h4>Entorno Activo: {problema}</h4><p>Visualización didáctica con conjuntos estructurados y control manual.</p></div>', unsafe_allow_html=True)

# Al dar click calculamos y congelamos los resultados en st.session_state
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
    elif algoritmo == "Hill Climbing (Escalada)":
        st.session_state.camino, st.session_state.historial = buscar_hill_climbing(mapa_activo)
    elif algoritmo == "Recocido Simulado":
        st.session_state.camino, st.session_state.historial = buscar_recocido_simulado(mapa_activo)
    st.session_state.calculado = True

# Renderizado de la matriz gráfica (Soporta laberintos tradicionales y el tablero de ajedrez)
def renderizar(mapa, visitados=None, camino=None, actual=None):
    if visitados is None: visitados = []
    if camino is None: camino = []
    
    # --- ENTORNO ESPECIAL: 8 REINAS (Tablero de Ajedrez) ---
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

    # --- ENTORNO ESTÁNDAR: MATRIZ CUADRÍCULA (Laberinto y Sokoban) ---
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

# --- CONTROL DEL RECORRIDO MANUAL Y ANIMACIÓN ---
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
    es_final = (idx == len(st.session_state.historial) - 1)

    # --- CASO DE RENDERIZADO VERTICAL: 8 REINAS ---
    if problema == "8 Reinas":
        estado_reinas_actual, ataques_actual = st.session_state.historial[idx]
        
        st.subheader("🗺️ Estado Gráfico del Tablero")
        st.markdown(renderizar(mapa_activo, actual=estado_reinas_actual), unsafe_allow_html=True)
        
        if es_final:
            if ataques_actual == 0:
                st.success("👑 ¡Solución perfecta encontrada! 0 ataques mutuos entre reinas.")
            else:
                st.warning(f"⚠️ El algoritmo local terminó y se detuvo en un óptimo local con {ataques_actual} ataques.")
        
        st.markdown("---")
        st.subheader("📋 Bitácora Matemática de Desarrollo")
        st.markdown(f"""
        <div class="box-ejercicio">
            <h4>PASO {idx + 1} — Configuración Activa de Reinas</h4>
            <p class="linea-open">Posición de Reinas (Estructura de columnas): {estado_reinas_actual}</p>
            <p class="linea-closed">💥 Número Total de Parejas en Conflicto / Ataques: {ataques_actual}</p>
            <hr style="border-color:{PALETA['eden']}; margin:10px 0;">
            <p style="font-size:14px; font-family:sans-serif; color:{PALETA['janna']} !important;">
            {"<b>Criterio de Paro Cumplido:</b> El algoritmo local finalizó porque ninguna de las modificaciones adyacentes del vecindario ofrece un mejor resultado." if es_final else "El algoritmo evalúa de forma consecutiva las celdas adyacentes modificando la posición de una reina por columna buscando maximizar su desempeño."}
            </p>
        </div>
        """, unsafe_allow_html=True)

    # --- CASO DE RENDERIZADO HORIZONTAL: LABERINTO O SOKOBAN ---
    else:
        nodo_actual, open_list, closed_list = st.session_state.historial[idx]
        camino_final = st.session_state.camino if es_final else []
        
        col_mapa, col_bitacora = st.columns([1.4, 1.6])
        
        with col_mapa:
            st.subheader("🗺️ Estado Gráfico")
            st.markdown(renderizar(mapa_activo, visitados=closed_list, camino=camino_final, actual=nodo_actual), unsafe_allow_html=True)
            if es_final and st.session_state.camino:
                st.success(f"🏁 Meta encontrada. Camino óptimo completado.")
                
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
    # Estado inicial estático (Antes de presionar el botón de calcular)
    if problema == "8 Reinas":
        # --- DISEÑO VERTICAL LIMPIO PARA LAS REINAS ---
        st.subheader("🗺️ Estado Gráfico del Tablero")
        st.markdown(renderizar(mapa_activo), unsafe_allow_html=True)
        
        st.markdown("---")
        st.subheader("📋 Bitácora Matemática de Desarrollo")
        st.markdown('<div class="box-ejercicio"><h4>Esperando Inicialización...</h4><p>Presiona el botón de arriba para calcular la optimización local del tablero.</p></div>', unsafe_allow_html=True)
    else:
        # --- DISEÑO EN DOS COLUMNAS PARA LABERINTO Y SOKOBAN ---
        col_mapa, col_bitacora = st.columns([1.4, 1.6])
        with col_mapa:
            st.subheader("🗺️ Estado Gráfico")
            st.markdown(renderizar(mapa_activo if mapa_activo else [["S","G"]]), unsafe_allow_html=True)
        with col_bitacora:
            st.subheader("📋 Bitácora Matemática de Desarrollo")
            st.markdown('<div class="box-ejercicio"><h4>Esperando Inicialización...</h4><p>Presiona el botón de arriba para calcular el árbol de búsqueda.</p></div>', unsafe_allow_html=True)