"""
CHATBOT ZAPOPAN - VERSIÓN CORREGIDA
Sin errores de indentación, CSS externo via CDN
"""

import streamlit as st
from datetime import datetime
from procesador_completo import procesar_consulta_local_expandida

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

st.set_page_config(
    page_title="Sistema de Consulta - Dirección de Inspección y Vigilancia",
    page_icon="🏛️",
    layout="wide"
)

# ============================================================================
# SISTEMA DE DISEÑO RESONANT STARK 2026 (CSS INLINE GARANTIZADO)
# ============================================================================

# CSS INLINE COMPLETO - Garantizado que se carga en Streamlit Cloud
st.markdown("""
<style>
/* CSS RESONANT STARK INLINE - 100% garantizado */
:root {
  --rs-primary: #1D4ED8;
  --rs-primary-hover: #1E40AF;
  --rs-secondary: #0F172A;
  --rs-surface: #F8FAFC;
}

/* FONDO Y TIPOGRAFÍA */
.stApp {
  background: #FFFFFF !important;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
  line-height: 1.5 !important;
  color: #0F172A !important;
}

/* HEADERS COMPACTOS */
h1, .stMarkdown h1 {
  font-size: 30px !important;
  font-weight: 700 !important;
  color: #0F172A !important;
  margin: 16px 0 8px 0 !important;
  line-height: 1.2 !important;
}

h2, .stMarkdown h2 {
  font-size: 24px !important;
  font-weight: 600 !important;
  color: #0F172A !important;
  margin: 12px 0 8px 0 !important;
  line-height: 1.3 !important;
}

h3, .stMarkdown h3 {
  font-size: 20px !important;
  font-weight: 600 !important;
  color: #0F172A !important;
  margin: 12px 0 4px 0 !important;
  line-height: 1.4 !important;
}

/* PÁRRAFOS COMPACTOS */
p, .stMarkdown p {
  font-size: 16px !important;
  line-height: 1.5 !important;
  margin: 8px 0 !important;
  color: #374151 !important;
}

/* BOTONES AZULES CON SOMBRA */
.stButton > button {
  background: #1D4ED8 !important;
  color: white !important;
  border: none !important;
  border-radius: 8px !important;
  padding: 12px 24px !important;
  font-size: 16px !important;
  font-weight: 500 !important;
  transition: all 0.2s ease !important;
  cursor: pointer !important;
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05) !important;
}

.stButton > button:hover {
  background: #1E40AF !important;
  transform: translateY(-1px) !important;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
}

/* INPUTS ELEGANTES */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
  background: white !important;
  border: 1px solid #E5E7EB !important;
  border-radius: 8px !important;
  padding: 12px 16px !important;
  font-size: 16px !important;
  color: #0F172A !important;
  transition: all 0.2s ease !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
  border-color: #1D4ED8 !important;
  box-shadow: 0 0 0 3px rgba(29, 78, 216, 0.1) !important;
  outline: none !important;
}

/* CONTAINERS LIMPIOS */
.stContainer, .stExpander {
  background: transparent !important;
  border: none !important;
  padding: 0 !important;
  margin: 16px 0 !important;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
  background: #F8FAFC !important;
  border-right: 1px solid #E5E7EB !important;
}

section[data-testid="stSidebar"] > div {
  padding: 24px !important;
}

/* RESPONSIVE */
@media (max-width: 768px) {
  h1, .stMarkdown h1 { font-size: 24px !important; margin: 12px 0 8px 0 !important; }
  h2, .stMarkdown h2 { font-size: 20px !important; margin: 8px 0 4px 0 !important; }
  h3, .stMarkdown h3 { font-size: 18px !important; margin: 8px 0 4px 0 !important; }
  .stButton > button { padding: 12px 16px !important; font-size: 14px !important; }
  section[data-testid="stSidebar"] { width: 100% !important; max-width: 100% !important; }
}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# FUNCIONES DE AUTENTICACIÓN
# ============================================================================

def verificar_login(usuario: str, password: str) -> bool:
    """Verificar credenciales de usuario"""
    usuarios = {
        "directora_inspeccion": "Zapopan2026!DIV1",
        "subdirector_operativo": "Zapopan2026!DIV2",
        "inspector_jefe": "Zapopan2026!DIV3",
        "inspector_senior": "Zapopan2026!DIV4",
        "inspector_junior": "Zapopan2026!DIV5",
        "analista_normativo": "Zapopan2026!DIV6",
        "coordinador_field": "Zapopan2026!DIV7",
        "supervisor_zona1": "Zapopan2026!Z1",
        "supervisor_zona2": "Zapopan2026!Z2",
        "supervisor_zona3": "Zapopan2026!Z3",
        "tecnico_campo1": "Zapopan2026!TC1",
        "tecnico_campo2": "Zapopan2026!TC2",
        "tecnico_campo3": "Zapopan2026!TC3",
        "administrativo1": "Zapopan2026!AD1",
        "administrativo2": "Zapopan2026!AD2",
        "practicante_derecho": "Zapopan2026!PR1",
        "practicante_ingenieria": "Zapopan2026!PR2",
        "consultor_externo": "Zapopan2026!CE1",
        "ciudadano_verificado": "Zapopan2026!CV1",
        "representante_legal": "Zapopan2026!RL1",
        "administrador_supremo": "AdminSupremo2026!ZAP"
    }
    return usuario in usuarios and usuarios[usuario] == password

def obtener_rol(usuario: str) -> str:
    """Obtener rol del usuario"""
    roles = {
        "directora_inspeccion": "directora",
        "subdirector_operativo": "subdirector",
        "inspector_jefe": "inspector_jefe",
        "inspector_senior": "inspector",
        "inspector_junior": "inspector",
        "analista_normativo": "analista",
        "coordinador_field": "coordinador",
        "supervisor_zona1": "supervisor",
        "supervisor_zona2": "supervisor",
        "supervisor_zona3": "supervisor",
        "tecnico_campo1": "tecnico",
        "tecnico_campo2": "tecnico",
        "tecnico_campo3": "tecnico",
        "administrativo1": "administrativo",
        "administrativo2": "administrativo",
        "practicante_derecho": "practicante",
        "practicante_ingenieria": "practicante",
        "consultor_externo": "consultor",
        "ciudadano_verificado": "ciudadano",
        "representante_legal": "representante",
        "administrador_supremo": "administrador_supremo"
    }
    return roles.get(usuario, "invitado")

def obtener_nombre(usuario: str) -> str:
    """Obtener nombre legible del usuario"""
    nombres = {
        "directora_inspeccion": "Dra. María González",
        "subdirector_operativo": "Lic. Carlos Rodríguez",
        "inspector_jefe": "Ing. Jorge Martínez",
        "inspector_senior": "C. Ana López",
        "inspector_junior": "C. Pedro Sánchez",
        "analista_normativo": "Lic. Laura Ramírez",
        "coordinador_field": "C. Roberto Cruz",
        "supervisor_zona1": "Supervisor Zona 1",
        "supervisor_zona2": "Supervisor Zona 2",
        "supervisor_zona3": "Supervisor Zona 3",
        "tecnico_campo1": "Técnico Campo 1",
        "tecnico_campo2": "Técnico Campo 2",
        "tecnico_campo3": "Técnico Campo 3",
        "administrativo1": "Administrativo 1",
        "administrativo2": "Administrativo 2",
        "practicante_derecho": "Practicante Derecho",
        "practicante_ingenieria": "Practicante Ingeniería",
        "consultor_externo": "Consultor Externo",
        "ciudadano_verificado": "Ciudadano Verificado",
        "representante_legal": "Representante Legal",
        "administrador_supremo": "Administrador Supremo"
    }
    return nombres.get(usuario, usuario)

# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def main():
    """Función principal de la aplicación"""
    
    # Inicializar session state
    if "autenticado" not in st.session_state:
        st.session_state.autenticado = False
        st.session_state.usuario = ""
        st.session_state.rol = ""
        st.session_state.nombre = ""
        st.session_state.historial = []
        st.session_state.resultado_actual = None
        st.session_state.consulta_actual = ""
    
    # ========================================================================
    # PANTALLA DE LOGIN (NO AUTENTICADO)
    # ========================================================================
    if not st.session_state.autenticado:
        st.title("🏛️ Sistema de Consulta")
        st.markdown("**Dirección de Inspección y Vigilancia - Zapopan**")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/7/7d/Zapopan_escudo.svg/1200px-Zapopan_escudo.svg.png", 
                    width=150, caption="Municipio de Zapopan")
        
        with col2:
            st.markdown("#### Iniciar Sesión")
            
            usuario = st.text_input("Usuario", placeholder="Ingresa tu usuario")
            password = st.text_input("Contraseña", type="password", placeholder="Ingresa tu contraseña")
            
            if st.button("Ingresar", type="primary", use_container_width=True):
                if verificar_login(usuario, password):
                    st.session_state.autenticado = True
                    st.session_state.usuario = usuario
                    st.session_state.rol = obtener_rol(usuario)
                    st.session_state.nombre = obtener_nombre(usuario)
                    st.rerun()
                else:
                    st.error("Usuario o contraseña incorrectos")
            
            st.markdown("**Información de acceso:**")
            st.markdown("- Sistema restringido al personal autorizado")
            st.markdown("- Para solicitar acceso, contactar al administrador")
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
        
        # Botón DASHBOARD - SOLO para administrador_supremo
        if st.session_state.rol == "administrador_supremo":
            if st.button("DASHBOARD", use_container_width=True):
                st.info("Funcionalidad de Dashboard en desarrollo")
        
        # Botón APP
        if st.button("APP", use_container_width=True):
            st.info("Aplicación principal activa")
        
        st.markdown("---")
        st.markdown("#### 📋 Historial reciente")
        
        if st.session_state.historial:
            for i, consulta_hist in enumerate(reversed(st.session_state.historial[-5:])):
                st.markdown(f"**{len(st.session_state.historial)-i}.** {consulta_hist[:40]}...")
        else:
            st.markdown("*Sin consultas recientes*")
        
        if st.button("Cerrar sesión", type="secondary", use_container_width=True):
            st.session_state.clear()
            st.rerun()
    
    # Contenido principal
    st.title("🔍 Consulta Normativa")
    st.markdown("Sistema de consulta especializado en normativa municipal de Zapopan")
    
    # Mostrar resultado anterior si existe
    if st.session_state.resultado_actual:
        st.markdown("### 📄 Resultado de tu consulta")
        
        if st.session_state.historial:
            ultima_consulta = st.session_state.historial[-1]
            st.markdown(f"**📝 Tu consulta:** {ultima_consulta}")
            st.markdown("---")
        
        st.markdown(st.session_state.resultado_actual["texto_visible"])
        
        # Mostrar información técnica (solo para administrador_supremo)
        if st.session_state.rol == "administrador_supremo":
            with st.expander("Detalles técnicos (solo administrador)", expanded=False):
                st.json({
                    "categoria": st.session_state.resultado_actual["categoria"],
                    "fuente": st.session_state.resultado_actual["fuente"],
                    "usando_ai": st.session_state.resultado_actual["usando_ai"],
                    "sigue_protocolo": st.session_state.resultado_actual["sigue_protocolo"],
                    "timestamp": datetime.now().isoformat()
                })
        
        st.markdown("---")
        st.markdown("### ")
        st.markdown("*Para nueva consulta, escribe abajo y haz clic en **Consultar***")
    
    # Área de consulta
    st.markdown("### Tu consulta")
    
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
                    resultado = procesar_consulta_local_expandida(consulta, st.session_state.usuario)
                    
                    # Guardar en historial
                    st.session_state.historial.append(consulta)
                    st.session_state.resultado_actual = resultado
                    
                    # Limpiar texto de consulta después de procesar
                    st.session_state.consulta_actual = ""
                    
                    # Forzar rerun para actualizar interfaz y limpiar textarea
                    st.rerun()
            else:
                st.warning("Por favor ingresa una consulta")
    
    with col2:
        if st.button("Limpiar", type="secondary", use_container_width=True):
            st.session_state.consulta_actual = ""
            st.rerun()
    
    # Si no hay resultado, mostrar espacio limpio
    if not st.session_state.resultado_actual:
        st.markdown("---")
        st.markdown("### ")
        st.markdown("*Escribe tu consulta arriba y haz clic en **Consultar***")

# ============================================================================
# EJECUCIÓN
# ============================================================================

if __name__ == "__main__":
    main()