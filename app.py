# app.py
import streamlit as st
from estilos import aplicar_estilos_personalizados, PALETA

from no_informada import buscar_bfs, buscar_dfs
from informada import buscar_greedy, buscar_a_estrella

st.set_page_config(page_title="IA Visualizer Academic", layout="wide")
aplicar_estilos_personalizados()

st.title("🧠 Visualizador Matemático de Algoritmos IA")
st.markdown("---")

# --- SIDEBAR CONFIGURACIÓN ---
st.sidebar.subheader("⚙️ Parámetros del Sistema")
problema = st.sidebar.selectbox("Selecciona el Problema:", ["Laberinto (Frozen Lake)", "Sokoban"])

if problema == "Laberinto (Frozen Lake)":
    algoritmo = st.sidebar.selectbox("Algoritmo de Búsqueda:", ["BFS (Amplitud)", "DFS (Profundidad)"])
    mapa_activo = [["S", "F", "F", "F"], ["F", "H", "F", "H"], ["F", "F", "F", "H"], ["H", "F", "F", "G"]]
    inicio, meta = (0, 0), (3, 3)
else:
    algoritmo = st.sidebar.selectbox("Algoritmo de Búsqueda:", ["A* (A-Estrella)", "Greedy Best-First"])
    mapa_activo = [["S", "F", "#", "F", "F"], ["F", "F", "#", "F", "G"], ["F", "F", "F", "F", "F"], ["#", "#", "F", "#", "#"]]
    inicio, meta = (0, 0), (1, 4)

# --- CONTROL DE ESTADOS GLOBAL DE STREAMLIT ---
if "paso_idx" not in st.session_state:
    st.session_state.paso_idx = 0
if "historial" not in st.session_state:
    st.session_state.historial = []
if "camino" not in st.session_state:
    st.session_state.camino = []
if "calculado" not in st.session_state:
    st.session_state.calculado = False

# Función para limpiar el estado al cambiar configuraciones
def limpiar_calculo():
    st.session_state.paso_idx = 0
    st.session_state.historial = []
    st.session_state.camino = []
    st.session_state.calculado = False

# Renderizado de la matriz gráfica
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
    st.session_state.calculado = True

# Si el algoritmo ya fue procesado, habilitamos la navegación
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

    # Extraer el paso seleccionado de forma segura
    idx = st.session_state.paso_idx
    nodo_actual, open_list, closed_list = st.session_state.historial[idx]
    es_final = (idx == len(st.session_state.historial) - 1)
    camino_final = st.session_state.camino if es_final else []

    col_mapa, col_bitacora = st.columns([1.4, 1.6])
    
    with col_mapa:
        st.subheader("🗺️ Estado Gráfico")
        st.markdown(renderizar(mapa_activo, visitados=closed_list, camino=camino_final, actual=nodo_actual), unsafe_allow_html=True)
        if es_final and st.session_state.camino:
            st.success(f"🏁 Meta encontrada. Camino óptimo completado.")
            
    with col_bitacora:
        st.subheader("📋 Bitácora Matemática de Desarrollo")
        
        # Formatear OPEN dependiendo si el algoritmo maneja pesos (heurísticas) o no
        if algoritmo in ["BFS (Amplitud)", "DFS (Profundidad)"]:
            str_open = ", ".join([f"({r},{c})" for r, c in open_list])
        else:
            # Desestructurar correctamente las tuplas guardadas por Greedy y A*
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
    # Estado inicial estático
    col_mapa, col_bitacora = st.columns([1.4, 1.6])
    with col_mapa:
        st.subheader("🗺️ Estado Gráfico")
        st.markdown(renderizar(mapa_activo if mapa_activo else [["S","G"]]), unsafe_allow_html=True)
    with col_bitacora:
        st.subheader("📋 Bitácora Matemática de Desarrollo")
        st.markdown('<div class="box-ejercicio"><h4>Esperando Inicialización...</h4><p>Presiona el botón de arriba para calcular el árbol de búsqueda.</p></div>', unsafe_allow_html=True)