"""
SISTEMA DE CONSULTA DE LA DIRECCIÓN DE INSPECCIÓN Y VIGILANCIA
Versión profesional 2026 con sistema de diseño institucional moderno
"""

import streamlit as st
import json
from datetime import datetime
from sistema_local_protocolo_completo import procesar_consulta_local_protocolo_completo

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

st.set_page_config(
    page_title="Sistema de Consulta - Dirección de Inspección y Vigilancia",
    page_icon="🏛️",
    layout="wide"
)

# ============================================================================
# SISTEMA DE DISEÑO 2026
# ============================================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
  /* COLORES INSTITUCIONALES 2026 */
  --color-fondo: #0F172A;
  --color-surface: #1E293B;
  --color-primary: #3B82F6;
  --color-primary-hover: #2563EB;
  --color-gobierno: #1D4ED8;
  --color-institucional: #0369A1;
  --color-accent: #10B981;
  --color-alerta: #EF4444;
  --color-advertencia: #F59E0B;
  
  /* ESCALA DE GRISES 2026 */
  --gray-50: #F8FAFC;
  --gray-100: #F1F5F9;
  --gray-200: #E2E8F0;
  --gray-300: #CBD5E1;
  --gray-400: #94A3B8;
  --gray-500: #64748B;
  --gray-600: #475569;
  --gray-700: #334155;
  --gray-800: #1E293B;
  --gray-900: #0F172A;
  
  /* GRADIENTES */
  --gradient-primary: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%);
  --gradient-success: linear-gradient(135deg, #10B981 0%, #34D399 100%);
  
  /* TIPOGRAFÍA FLUID */
  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
  --text-xs: clamp(0.75rem, 0.7rem + 0.25vw, 0.875rem);
  --text-sm: clamp(0.875rem, 0.825rem + 0.25vw, 1rem);
  --text-base: clamp(1rem, 0.95rem + 0.25vw, 1.125rem);
  --text-lg: clamp(1.125rem, 1.05rem + 0.375vw, 1.25rem);
  --text-xl: clamp(1.25rem, 1.15rem + 0.5vw, 1.5rem);
  --text-2xl: clamp(1.5rem, 1.35rem + 0.75vw, 1.875rem);
  --text-3xl: clamp(1.875rem, 1.65rem + 1.125vw, 2.25rem);
  
  /* ESPACIADO 4PX GRID */
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-3: 0.75rem;
  --space-4: 1rem;
  --space-5: 1.25rem;
  --space-6: 1.5rem;
  --space-8: 2rem;
  --space-10: 2.5rem;
  
  /* BORDER RADIUS */
  --radius-sm: 0.375rem;
  --radius-md: 0.5rem;
  --radius-lg: 0.75rem;
  --radius-xl: 1rem;
  
  /* SOMBRAS */
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  --shadow-primary: 0 10px 15px -3px rgba(59, 130, 246, 0.3), 0 4px 6px -2px rgba(59, 130, 246, 0.1);
  
  /* TRANSICIONES */
  --transition-base: 300ms cubic-bezier(0.4, 0, 0.2, 1);
}

/* RESET Y BASE */
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: var(--font-sans); background: var(--color-fondo); color: var(--gray-200); min-height: 100vh; }

/* TÍTULOS CON GRADIENTE */
h1, .stMarkdown h1 { 
  font-size: var(--text-3xl); 
  font-weight: 700; 
  background: var(--gradient-primary); 
  -webkit-background-clip: text; 
  -webkit-text-fill-color: transparent; 
  background-clip: text; 
  margin-bottom: var(--space-4); 
}
h2, .stMarkdown h2 { font-size: var(--text-2xl); color: var(--gray-100); margin-bottom: var(--space-4); }
h3, .stMarkdown h3 { font-size: var(--text-xl); color: var(--gray-200); margin-bottom: var(--space-4); }

/* BOTONES STREAMLIT */
.stButton > button {
  border-radius: var(--radius-lg) !important;
  border: none !important;
  font-family: var(--font-sans) !important;
  font-weight: 600 !important;
  font-size: var(--text-sm) !important;
  padding: var(--space-3) var(--space-6) !important;
  transition: all var(--transition-base) !important;
  min-height: 44px !important;
}
.stButton > button[data-testid="baseButton-primary"] {
  background: var(--gradient-primary) !important;
  color: white !important;
}
.stButton > button[data-testid="baseButton-primary"]:hover {
  transform: translateY(-2px) !important;
  box-shadow: var(--shadow-primary) !important;
}
.stButton > button[data-testid="baseButton-secondary"] {
  background: var(--color-surface) !important;
  color: var(--gray-300) !important;
  border: 1px solid var(--gray-700) !important;
}
.stButton > button[data-testid="baseButton-secondary"]:hover {
  background: var(--gray-800) !important;
  border-color: var(--gray-600) !important;
  transform: translateY(-2px) !important;
}

/* INPUTS STREAMLIT */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
  background: var(--color-surface) !important;
  border: 2px solid var(--gray-700) !important;
  border-radius: var(--radius-lg) !important;
  color: var(--gray-200) !important;
  padding: var(--space-3) var(--space-4) !important;
  font-family: var(--font-sans) !important;
  font-size: var(--text-base) !important;
  transition: all var(--transition-base) !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
  border-color: var(--color-primary) !important;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
  outline: none !important;
}

/* CONTAINERS Y CARDS */
.stContainer, .stExpander, div[data-testid="stVerticalBlock"] > div {
  background: rgba(30, 41, 59, 0.7) !important;
  backdrop-filter: blur(10px);
  border-radius: var(--radius-xl) !important;
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
  padding: var(--space-6) !important;
  margin-bottom: var(--space-4) !important;
  transition: all var(--transition-base) !important;
}
.stContainer:hover, .stExpander:hover {
  border-color: rgba(59, 130, 246, 0.3) !important;
  transform: translateY(-2px);
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
  background: var(--color-fondo) !important;
  border-right: 1px solid var(--gray-800) !important;
}
section[data-testid="stSidebar"] > div {
  padding: var(--space-6) !important;
}

/* ALERTAS */
.stAlert { border-radius: var(--radius-lg) !important; padding: var(--space-4) !important; }
div[data-testid="stAlert"] > div { border-radius: var(--radius-lg) !important; }

/* RESPONSIVE */
@media (max-width: 768px) {
  .stContainer, .stExpander { padding: var(--space-4) !important; border-radius: var(--radius-lg) !important; }
  .stButton > button { padding: var(--space-4) var(--space-6) !important; width: 100% !important; }
  section[data-testid="stSidebar"] { width: 100% !important; max-width: 100% !important; }
  h1, .stMarkdown h1 { font-size: var(--text-2xl) !important; }
  h2, .stMarkdown h2 { font-size: var(--text-xl) !important; }
  h3, .stMarkdown h3 { font-size: var(--text-lg) !important; }
}

/* DARK/LIGHT MODE */
@media (prefers-color-scheme: light) {
  :root {
    --color-fondo: #FFFFFF;
    --color-surface: #F8FAFC;
    --gray-200: #1E293B;
    --gray-300: #334155;
    --gray-700: #94A3B8;
    --gray-800: #64748B;
    --gray-900: #475569;
  }
  .stContainer, .stExpander {
    background: rgba(248, 250, 252, 0.9) !important;
    border: 1px solid rgba(226, 232, 240, 0.8) !important;
  }
}

/* REDUCED MOTION */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# AUTENTICACIÓN
# ============================================================================

USUARIOS_DB = {
    "luis_admin": {"password": "ZapopanAdmin2026!", "rol": "administrador_supremo", "nombre": "Luis Aguirre"},
    "directora_inspeccion": {"password": "Zapopan2026!DIV1", "rol": "directora", "nombre": "María Luisa Vargas"},
    "jefe_comercio": {"password": "Zapopan2026!JCO1", "rol": "jefe_area", "nombre": "Rubén Alejandro Zúñiga"},
    "juridico_01": {"password": "Zapopan2026!JU01", "rol": "area_juridica", "nombre": "Diana Valeria Mendoza"},
    "demo": {"password": "Zapopan2026!AC01", "rol": "demo", "nombre": "Usuario Demo"}
}

def verificar_login(usuario: str, password: str) -> bool:
    """Verificar credenciales"""
    if usuario in USUARIOS_DB:
        return USUARIOS_DB[usuario]["password"] == password
    return False

def obtener_rol(usuario: str) -> str:
    """Obtener rol del usuario"""
    return USUARIOS_DB.get(usuario, {}).get("rol", "demo")

def obtener_nombre(usuario: str) -> str:
    """Obtener nombre del usuario"""
    return USUARIOS_DB.get(usuario, {}).get("nombre", "Usuario")

# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def registrar_consulta_local(consulta: str, resultados: list, usuario: str):
    """Registrar consulta localmente"""
    try:
        registro = {
            "timestamp": datetime.now().isoformat(),
            "usuario": usuario,
            "consulta": consulta,
            "resultados_count": len(resultados),
            "sistema": "local_emergencia"
        }
        
        with open("consultas_local.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(registro, ensure_ascii=False) + "\n")
    except:
        pass

def limpiar_texto_consulta():
    """Limpiar el texto de la consulta en session_state"""
    if "consulta_actual" in st.session_state:
        st.session_state.consulta_actual = ""

# ============================================================================
# INTERFAZ PRINCIPAL
# ============================================================================

def main():
    """Aplicación principal"""
    
    # Inicializar sesión
    if "autenticado" not in st.session_state:
        st.session_state.autenticado = False
        st.session_state.usuario = ""
        st.session_state.rol = ""
        st.session_state.nombre = ""
        st.session_state.historial = []
        st.session_state.consulta_actual = ""
        st.session_state.resultado_actual = None
    
    # ========================================================================
    # PANTALLA DE LOGIN
    # ========================================================================
    
    if not st.session_state.autenticado:
        st.title("Sistema de Consulta de la Dirección de Inspección y Vigilancia")
        st.markdown("### Acceso Restringido - Personal Autorizado")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            with st.container(border=True):
                st.markdown("#### Iniciar Sesión")
                
                usuario = st.text_input("Usuario", placeholder="Ej: directora_inspeccion")
                password = st.text_input("Contraseña", type="password", placeholder="Ej: Zapopan2026!DIV1")
                
                if st.button("Ingresar", type="primary", use_container_width=True):
                    if verificar_login(usuario, password):
                        st.session_state.autenticado = True
                        st.session_state.usuario = usuario
                        st.session_state.rol = obtener_rol(usuario)
                        st.session_state.nombre = obtener_nombre(usuario)
                        st.rerun()
                    else:
                        st.error("Usuario o contraseña incorrectos")
                
                st.markdown("---")
                st.markdown("**Información de acceso:**")
                st.markdown("- Sistema restringido al personal autorizado de la Dirección de Inspección y Vigilancia")
                st.markdown("- Para solicitar acceso, contactar al administrador del sistema")
                st.markdown("- Acceso mediante credenciales institucionales")
        
        return
    
    # ========================================================================
    # PANTALLA PRINCIPAL (AUTENTICADO)
    # ========================================================================
    
    # Sidebar - Columna desplegable izquierda
    with st.sidebar:
        st.markdown(f"### {st.session_state.nombre}")
        st.markdown(f"**Rol:** {st.session_state.rol.replace('_', ' ').title()}")
        st.markdown(f"**Sistema:** Local - Protocolo específico")
        
        st.markdown("---")
        
        # Botón Dashboard - SOLO para administrador_supremo
        if st.session_state.rol == "administrador_supremo":
            if st.button("Dashboard", use_container_width=True):
                st.info("Funcionalidad de Dashboard en desarrollo")
        
        # Botón App
        if st.button("App", use_container_width=True):
            st.info("Aplicación principal activa")
        
        st.markdown("---")
        
        # Historial de consultas recientes (en sidebar como solicitado)
        if st.session_state.historial:
            with st.expander("Historial de consultas recientes", expanded=False):
                for i, consulta in enumerate(reversed(st.session_state.historial[-5:])):
                    st.markdown(f"{i+1}. {consulta[:80]}..." if len(consulta) > 80 else f"{i+1}. {consulta}")
        
        st.markdown("---")
        
        # Botón cerrar sesión
        if st.button("Cerrar Sesión", use_container_width=True):
            st.session_state.autenticado = False
            st.session_state.usuario = ""
            st.session_state.rol = ""
            st.session_state.nombre = ""
            st.session_state.historial = []
            st.session_state.consulta_actual = ""
            st.session_state.resultado_actual = None
            st.rerun()
    
    # Área principal
    st.title("Sistema de Consulta de la Dirección de Inspección y Vigilancia")
    st.markdown(f"### Bienvenido(a), {st.session_state.nombre}")
    
    # Inicializar historial si no existe
    if "historial" not in st.session_state:
        st.session_state.historial = []
    
    # Área de consulta
    st.markdown("### Tu consulta")
    
    # Usar text_input con key para manejar estado
    consulta = st.text_area(
        "Describe tu consulta sobre normativa de Zapopan:",
        value=st.session_state.get("consulta_actual", ""),
        placeholder="Ej: Están colocando una antena de celulares en la azotea de mi vecino...",
        height=100,
        key="consulta_input"
    )
    
    # Actualizar session_state
    st.session_state.consulta_actual = consulta
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        if st.button("Consultar", type="primary", use_container_width=True):
            if consulta.strip():
                with st.spinner("Procesando consulta..."):
                    # Procesar con sistema local
                    resultado = procesar_consulta_local_protocolo_completo(consulta, st.session_state.usuario)
                    
                    # Guardar en historial
                    st.session_state.historial.append(consulta)
                    st.session_state.resultado_actual = resultado
                    
                    # Limpiar texto de consulta después de procesar
                    st.session_state.consulta_actual = ""
                    
                    # Forzar rerun para actualizar interfaz
                    st.rerun()
            else:
                st.warning("Por favor ingresa una consulta")
    
    with col2:
        if st.button("Limpiar", use_container_width=True):
            st.session_state.consulta_actual = ""
            st.session_state.resultado_actual = None
            st.rerun()
    
    # Mostrar resultado si existe
    if st.session_state.get("resultado_actual"):
        resultado = st.session_state.resultado_actual
        
        st.markdown("---")
        st.markdown("### Resultado de la consulta")
        
        # Mostrar la consulta original del usuario
        if st.session_state.historial:
            ultima_consulta = st.session_state.historial[-1]
            with st.container(border=True):
                st.markdown(f"**Tu consulta:** {ultima_consulta}")
        
        # Mostrar respuesta
        st.markdown(resultado["texto_visible"])
        
        # Mostrar información técnica (solo para administrador_supremo)
        if st.session_state.rol == "administrador_supremo":
            with st.expander("Detalles técnicos (solo administrador)", expanded=False):
                st.json({
                    "categoria": resultado["categoria"],
                    "fuente": resultado["fuente"],
                    "usando_ai": resultado["usando_ai"],
                    "sigue_protocolo": resultado["sigue_protocolo"],
                    "timestamp": datetime.now().isoformat()
                })
        
        # Sección de consulta normativa DESPUÉS del resultado
        st.markdown("---")
        st.markdown("### Consulta normativa")
        st.markdown("¿Tienes otra consulta? Utiliza el campo de texto arriba para realizar una nueva consulta.")
    
    # Si no hay resultado, mostrar instrucciones
    else:
        st.markdown("---")
        st.markdown("### Instrucciones de uso")
        st.markdown("""
        1. Escribe tu consulta en el campo de texto superior
        2. Haz clic en **Consultar** para procesar tu solicitud
        3. Revisa el resultado que aparecerá en esta sección
        4. Para una nueva consulta, escribe en el campo de texto y haz clic en **Consultar** nuevamente
        
        **Ejemplos de consultas:**
        - Requisitos para apertura de negocio
        - Permisos para construcción
        - Denuncia por ruido excesivo
        - Consulta sobre uso de suelo
        """)

# ============================================================================
# EJECUCIÓN
# ============================================================================

if __name__ == "__main__":
    main()