"""
APP.PY PARA SISTEMA LOCAL DE EMERGENCIA
Versión lista para activar si la API Key falla
"""

import streamlit as st
import json
from datetime import datetime
from sistema_local_protocolo_completo import procesar_consulta_local_protocolo_completo

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

st.set_page_config(
    page_title="Chatbot Normativo Zapopan",
    page_icon="🏛️",
    layout="wide"
)

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
        st.session_state.historial = []
    
    # ========================================================================
    # PANTALLA DE LOGIN
    # ========================================================================
    
    if not st.session_state.autenticado:
        st.title("🏛️ Chatbot Normativo Zapopan")
        st.markdown("### Sistema de Consulta Normativa - Dirección de Inspección y Vigilancia")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            with st.container(border=True):
                st.markdown("#### 🔐 Iniciar Sesión")
                
                usuario = st.text_input("Usuario", placeholder="Ej: directora_inspeccion")
                password = st.text_input("Contraseña", type="password", placeholder="Ej: Zapopan2026!DIV1")
                
                if st.button("🚀 Ingresar", type="primary", use_container_width=True):
                    if verificar_login(usuario, password):
                        st.session_state.autenticado = True
                        st.session_state.usuario = usuario
                        st.session_state.rol = obtener_rol(usuario)
                        st.session_state.nombre = obtener_nombre(usuario)
                        st.rerun()
                    else:
                        st.error("❌ Usuario o contraseña incorrectos")
                
                st.markdown("---")
                st.markdown("**📋 Usuarios disponibles:**")
                st.markdown("- `directora_inspeccion` / `Zapopan2026!DIV1`")
                st.markdown("- `jefe_comercio` / `Zapopan2026!JCO1`")
                st.markdown("- `juridico_01` / `Zapopan2026!JU01`")
                st.markdown("- `demo` / `Zapopan2026!AC01`")
        
        return
    
    # ========================================================================
    # PANTALLA PRINCIPAL (AUTENTICADO)
    # ========================================================================
    
    # Sidebar
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.nombre}")
        st.markdown(f"**Rol:** {st.session_state.rol.replace('_', ' ').title()}")
        st.markdown(f"**Sistema:** 📋 Local • ✅ Protocolo específico")
        
        st.markdown("---")
        
        if st.button("🚪 Cerrar Sesión", use_container_width=True):
            st.session_state.autenticado = False
            st.session_state.usuario = ""
            st.session_state.rol = ""
            st.rerun()
        
        st.markdown("---")
        st.markdown("**ℹ️ Sistema Local de Emergencia**")
        st.markdown("Este sistema genera respuestas con el protocolo completo de Zapopan (5 pasos) usando base de conocimiento local.")
    
    # Área principal
    st.title(f"🏛️ Chatbot Normativo Zapopan")
    st.markdown(f"### 👋 Bienvenido(a), {st.session_state.nombre}")
    
    # Indicador del sistema
    st.caption("📋 Sistema normativo Zapopan • ✅ Protocolo específico (local)")
    
    # Inicializar historial si no existe
    if "historial" not in st.session_state:
        st.session_state.historial = []
    
    # Historial de consultas
    if st.session_state.historial:
        with st.expander("📜 Historial de consultas recientes", expanded=False):
            for i, consulta in enumerate(reversed(st.session_state.historial[-5:])):
                st.markdown(f"{i+1}. {consulta[:80]}...")
    
    # Área de consulta
    st.markdown("### 💬 Consulta normativa")
    
    consulta = st.text_area(
        "Describe tu consulta sobre normativa de Zapopan:",
        placeholder="Ej: Están colocando una antena de celulares en la azotea de mi vecino...",
        height=100
    )
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        if st.button("🔍 Consultar", type="primary", use_container_width=True):
            if consulta.strip():
                with st.spinner("🔍 Procesando consulta..."):
                    # Procesar con sistema local
                    resultado = procesar_consulta_local_protocolo_completo(consulta, st.session_state.usuario)
                    
                    # Guardar en historial
                    st.session_state.historial.append(consulta)
                    
                    # Mostrar resultado
                    st.markdown("---")
                    st.markdown("### 📋 Resultado de la consulta")
                    
                    # Mostrar indicador
                    st.caption(resultado["indicador"])
                    
                    # Mostrar respuesta
                    st.markdown(resultado["texto_visible"])
                    
                    # Mostrar información técnica (solo para admin)
                    if st.session_state.rol == "administrador_supremo":
                        with st.expander("🔧 Detalles técnicos (solo admin)", expanded=False):
                            st.json({
                                "categoria": resultado["categoria"],
                                "fuente": resultado["fuente"],
                                "usando_ai": resultado["usando_ai"],
                                "sigue_protocolo": resultado["sigue_protocolo"]
                            })
            else:
                st.warning("⚠️ Por favor ingresa una consulta")
    
    with col2:
        if st.button("🗑️ Limpiar", use_container_width=True):
            st.rerun()
    
    # Ejemplos de consultas
    st.markdown("---")
    st.markdown("### 💡 Ejemplos de consultas")
    
    ejemplos = [
        "Están colocando una antena de celulares en la azotea de mi vecino",
        "Un restaurante hace mucho ruido por las noches",
        "Mi vecino está construyendo sin permiso municipal",
        "Hay un negocio que vende alcohol sin licencia",
        "Un taller mecánico contamina el aire con humo"
    ]
    
    cols = st.columns(3)
    for i, ejemplo in enumerate(ejemplos):
        with cols[i % 3]:
            if st.button(f"📝 {ejemplo[:30]}...", use_container_width=True):
                st.session_state.ejemplo = ejemplo
                st.rerun()
    
    # Si hay ejemplo pre-cargado
    if "ejemplo" in st.session_state:
        st.text_area("Consulta pre-cargada:", value=st.session_state.ejemplo, height=80)
        if st.button("Usar este ejemplo"):
            consulta = st.session_state.ejemplo
            del st.session_state.ejemplo
            st.rerun()

# ============================================================================
# EJECUCIÓN
# ============================================================================

if __name__ == "__main__":
    main()