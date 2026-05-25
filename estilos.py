# estilos.py
import streamlit as st

# Paleta de colores oficial
PALETA = {
    "bondi_blue": "#0799b6",
    "san_marino": "#4a6eb0",
    "eden": "#114c5f",
    "sinbad": "#9cd2d3",
    "janna": "#f2e6cf",
    "fondo_oscuro": "#0e1117"
}

def aplicar_estilos_personalizados():
    st.markdown(f"""
        <style>
        /* 1. Fondo general de la aplicación */
        .stApp {{
            background-color: {PALETA['fondo_oscuro']};
            color: {PALETA['janna']};
        }}
        
        /* Asegurar visibilidad de textos en el panel central */
        .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp p, .stApp li, .stApp span {{
            color: {PALETA['janna']} !important;
        }}
        
        /* 2. SIDEBAR CLARO: Fondo gris claro limpio con bordes */
        [data-testid="stSidebar"] {{
            background-color: #e2e8f0 !important;
            border-right: 3px solid {PALETA['bondi_blue']};
        }}
        
        /* Forzar texto de títulos y etiquetas del Sidebar a color Eden (azul oscuro) */
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] h4,
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] span {{
            color: #0c1e2b !important;
            font-weight: 800 !important;
        }}
        
        /* CAJAS DE SELECCIÓN (SELECTBOX) EN EL SIDEBAR */
        [data-testid="stSidebar"] div[data-baseweb="select"] {{
            background-color: #ffffff !important;
            border: 2px solid {PALETA['eden']} !important;
            border-radius: 8px !important;
        }}
        
        /* Texto interno de la opción seleccionada */
        [data-testid="stSidebar"] div[data-baseweb="select"] div {{
            color: #0c1e2b !important;
            font-weight: 600 !important;
        }}
        
        /* --- NUEVO: FORZAR EL MISMO COLOR CLARO AL DESPLEGAR LA LISTA DE OPCIONES --- */
        div[data-baseweb="menu"] {{
            background-color: #ffffff !important;
            border: 1px solid #e2e8f0 !important;
        }}
        
        /* Elementos de la lista desplegada (las opciones interactivas) */
        li[data-testid="stSelectboxVirtualDropdownListItem"] {{
            background-color: #ffffff !important;
            color: #0c1e2b !important;
            font-weight: 600 !important;
        }}
        
        /* Efecto cuando pasas el mouse sobre una opción de la lista */
        li[data-testid="stSelectboxVirtualDropdownListItem"]:hover {{
            background-color: #e2e8f0 !important;
            color: {PALETA['bondi_blue']} !important;
        }}
        
        /* Cambiar color de las flechitas de colapso del menú a Bondi Blue */
        [data-testid="stSidebarHeader"] button svg {{
            color: {PALETA['bondi_blue']} !important;
            fill: {PALETA['bondi_blue']} !important;
        }}
        
        /* 3. BOTONES CENTRALES: Fondo Bondi Blue y letras blancas gruesas */
        div.stButton > button {{
            background-color: {PALETA['bondi_blue']} !important;
            color: #ffffff !important;
            border: 2px solid {PALETA['sinbad']} !important;
            font-weight: 800 !important;
            padding: 12px 20px !important;
            border-radius: 8px !important;
            width: 100% !important;
            font-size: 16px !important;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3) !important;
        }}
        
        /* Efectos Hover y Foco para los botones */
        div.stButton > button:hover, div.stButton > button:active, div.stButton > button:focus {{
            background-color: {PALETA['san_marino']} !important;
            color: #ffffff !important;
            border-color: #ffffff !important;
        }}
        
        /* Contenedores de información y bitácora */
        .card-info {{
            background-color: {PALETA['eden']};
            padding: 20px;
            border-radius: 12px;
            border-left: 6px solid {PALETA['bondi_blue']};
            margin-bottom: 25px;
        }}
        
        .box-ejercicio {{
            background-color: #161b22;
            padding: 20px;
            border-radius: 10px;
            border: 2px solid {PALETA['san_marino']};
            font-family: 'Courier New', Courier, monospace;
            margin-top: 10px;
        }}
        .box-ejercicio h4 {{
            color: {PALETA['bondi_blue']} !important;
            font-family: sans-serif;
            margin-top: 0;
        }}
        .linea-open {{
            color: #4ade80 !important;
            font-weight: bold;
            font-size: 15px;
        }}
        .linea-closed {{
            color: #f87171 !important;
            font-weight: bold;
            font-size: 15px;
        }}
        </style>
    """, unsafe_allow_html=True)