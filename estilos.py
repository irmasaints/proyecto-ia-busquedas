
import streamlit as st

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
        .stApp {{
            background-color: {PALETA['fondo_oscuro']};
            color: {PALETA['janna']};
        }}
        
        [data-testid="stHeader"] {{
            background-color: transparent !important;
        }}
        
        .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp p, .stApp li, .stApp span {{
            color: {PALETA['janna']} !important;
        }}
        

        [data-testid="stSidebar"] {{
            background-color: #f1f5f9 !important;
            border-right: 3px solid {PALETA['bondi_blue']};
        }}
        
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, 
        [data-testid="stSidebar"] p, [data-testid="stSidebar"] label, [data-testid="stSidebar"] span {{
            color: {PALETA['eden']} !important;
            font-weight: 800 !important;
        }}
        
        [data-testid="stSidebarHeader"] button svg {{
            color: {PALETA['bondi_blue']} !important;
            fill: {PALETA['bondi_blue']} !important;
        }}


        [data-testid="stSidebar"] div[data-baseweb="select"] {{
            background-color: #ffffff !important;
            border: 2px solid {PALETA['eden']} !important;
            border-radius: 8px !important;
        }}
        [data-testid="stSidebar"] div[data-baseweb="select"] * {{
            color: {PALETA['eden']} !important;
            font-weight: 700 !important;
        }}
        

        div[data-baseweb="menu"] {{
            background-color: #ffffff !important;
            border: 1px solid #e2e8f0 !important;
        }}
        li[data-testid="stSelectboxVirtualDropdownListItem"] {{
            background-color: #ffffff !important;
            color: {PALETA['eden']} !important;
            font-weight: 600 !important;
        }}
        li[data-testid="stSelectboxVirtualDropdownListItem"]:hover {{
            background-color: #f1f5f9 !important;
            color: {PALETA['bondi_blue']} !important;
        }}
        

        div.stButton > button {{
            background-color: {PALETA['bondi_blue']} !important;
            border: 2px solid {PALETA['sinbad']} !important;
            border-radius: 8px !important;
            width: 100% !important;
            padding: 10px !important;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3) !important;
        }}
        
        /* Forzar que CUALQUIER texto dentro del botón sea BLANCO */
        div.stButton > button * {{
            color: #ffffff !important;
            font-weight: 800 !important;
            font-size: 16px !important;
        }}
        
        div.stButton > button:hover {{
            background-color: {PALETA['san_marino']} !important;
        }}
        
        /* 4. Cajas de información */
        .card-info {{
            background-color: {PALETA['eden']};
            padding: 20px;
            border-radius: 12px;
            border-left: 6px solid {PALETA['bondi_blue']};
            margin-bottom: 20px;
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
        .linea-open {{ color: #4ade80 !important; font-weight: bold; font-size: 15px; }}
        .linea-closed {{ color: #f87171 !important; font-weight: bold; font-size: 15px; }}
        </style>
    """, unsafe_allow_html=True)