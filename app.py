"""
Sistema de Consulta Normativa Zapopan - VERSIÓN ULTRA-MÍNIMA
Funciona SIN Google AI, SIN plotly, SIN dependencias externas
"""

import streamlit as st
import json
import os
import sys
from datetime import datetime

# ============================================================================
# CONFIGURACIÓN BÁSICA
# ============================================================================

st.set_page_config(
    page_title="Sistema Normativo Zapopan",
    page_icon="🏛️",
    layout="wide"
)

# ============================================================================
# BASE DE DATOS DE USUARIOS (LOCAL)
# ============================================================================

USUARIOS_DB = {
    "luis_admin": {
        "password": "ZapopanAdmin2026!",
        "nombre_completo": "Luis Alberto Aguirre Gómez",
        "email": "luis.aguirre34@gmail.com",
        "rol": "administrador_supremo",
        "area": "Administración Central",
        "estado": "activo"
    },
    "demo": {
        "password": "demo123",
        "nombre_completo": "Usuario de Demostración",
        "email": "demo@zapopan.gob.mx",
        "rol": "demo",
        "area": "Demostración",
        "estado": "activo"
    }
}

ROLES_CONFIG = {
    "administrador_supremo": {
        "nombre": "Administrador Supremo",
        "permisos": ["admin_completo", "gestion_usuarios"]
    },
    "demo": {
        "nombre": "Usuario Demo",
        "permisos": ["consultas_basicas"]
    }
}

# ============================================================================
# FUNCIONES DE AUTENTICACIÓN
# ============================================================================

def autenticar_usuario(usuario: str, password: str) -> bool:
    """Autenticación simple sin dependencias externas"""
    if usuario in USUARIOS_DB:
        return USUARIOS_DB[usuario]["password"] == password
    return False

def obtener_info_usuario(usuario: str):
    """Obtener información de usuario"""
    return USUARIOS_DB.get(usuario)

def es_administrador(usuario: str) -> bool:
    """Verificar si es administrador"""
    info = obtener_info_usuario(usuario)
    return info and info["rol"] == "administrador_supremo"

# ============================================================================
# SISTEMA DE CONSULTAS LOCAL (SIN GOOGLE AI)
# ============================================================================

BASE_DE_CONOCIMIENTO = {
    "ruido": [
        {
            "reglamento": "Reglamento de Policía y Buen Gobierno",
            "articulo": "Artículo 45",
            "contenido": "Queda prohibido generar ruidos o vibraciones que excedan los límites permitidos que alteren la tranquilidad de los vecinos.",
            "dependencia": "Dirección de Inspección y Vigilancia"
        },
        {
            "reglamento": "Reglamento para el Comercio, la Industria y la Prestación de Servicios",
            "articulo": "Artículo 220",
            "contenido": "Los establecimientos comerciales deberán respetar los horarios y niveles de ruido establecidos para no afectar a la comunidad.",
            "dependencia": "Dirección de Inspección y Vigilancia"
        },
        {
            "reglamento": "Reglamento de Protección al Medio Ambiente",
            "articulo": "Artículo 32",
            "contenido": "Se prohíbe la emisión de ruido que supere los 65 decibeles durante el día y 55 decibeles durante la noche en zonas habitacionales.",
            "dependencia": "Dirección de Medio Ambiente"
        }
    ],
    "construcción": [
        {
            "reglamento": "Reglamento de Construcción",
            "articulo": "Artículo 18",
            "contenido": "Toda obra de construcción requiere permiso municipal y debe respetar horarios de 7:00 a 19:00 horas de lunes a viernes.",
            "dependencia": "Dirección de Desarrollo Urbano"
        }
    ],
    "comercio": [
        {
            "reglamento": "Reglamento para el Comercio, la Industria y la Prestación de Servicios",
            "articulo": "Artículo 16",
            "contenido": "Todo establecimiento comercial requiere licencia de funcionamiento expedida por el municipio.",
            "dependencia": "Dirección de Inspección y Vigilancia"
        }
    ]
}

def buscar_en_base_conocimiento(consulta: str):
    """Búsqueda local sin dependencias externas"""
    consulta_lower = consulta.lower()
    resultados = []
    
    # Palabras clave
    palabras_clave = {
        "ruido": ["ruido", "música", "sonido", "volumen", "altavoz", "parlante"],
        "construcción": ["construcción", "obra", "edificación", "demolición"],
        "comercio": ["comercio", "negocio", "restaurante", "bar", "cantina", "giro"]
    }
    
    for categoria, palabras in palabras_clave.items():
        for palabra in palabras:
            if palabra in consulta_lower:
                resultados.extend(BASE_DE_CONOCIMIENTO.get(categoria, []))
                break
    
    # Si no hay resultados, buscar en todos
    if not resultados:
        for categoria in BASE_DE_CONOCIMIENTO.values():
            resultados.extend(categoria)
    
    return resultados[:5]  # Limitar a 5 resultados

def procesar_consulta_local(consulta: str, usuario: str):
    """Procesar consulta sin Google AI"""
    resultados = buscar_en_base_conocimiento(consulta)
    
    if not resultados:
        return {
            "texto_visible": "No se encontraron regulaciones específicas para tu consulta. Por favor, contacta a la Dirección de Inspección y Vigilancia para más información.",
            "resultados": [],
            "categoria": "general"
        }
    
    # Construir respuesta
    respuesta = "## 📋 **Resultados de la consulta**\n\n"
    respuesta += f"**Consulta:** {consulta}\n\n"
    respuesta += "### 📚 **Regulaciones aplicables:**\n\n"
    
    for i, resultado in enumerate(resultados, 1):
        respuesta += f"{i}. **{resultado['reglamento']}**\n"
        respuesta += f"   - **Artículo:** {resultado['articulo']}\n"
        respuesta += f"   - **Contenido:** {resultado['contenido']}\n"
        respuesta += f"   - **Dependencia responsable:** {resultado['dependencia']}\n\n"
    
    respuesta += "### 📞 **Acciones recomendadas:**\n"
    respuesta += "1. **Verificar cumplimiento** de las regulaciones mencionadas\n"
    respuesta += "2. **Contactar a la dependencia** correspondiente para orientación\n"
    respuesta += "3. **Solicitar inspección** si se identifica incumplimiento\n"
    
    # Registrar consulta
    registrar_consulta_local(consulta, resultados, usuario)
    
    return {
        "texto_visible": respuesta,
        "resultados": resultados,
        "categoria": resultados[0]["dependencia"].split()[-1].lower() if resultados else "general"
    }

def registrar_consulta_local(consulta: str, resultados: list, usuario: str):
    """Registrar consulta localmente"""
    try:
        registro = {
            "timestamp": datetime.now().isoformat(),
            "usuario": usuario,
            "consulta": consulta,
            "resultados_count": len(resultados),
            "dependencias": list(set(r["dependencia"] for r in resultados))
        }
        
        # Guardar en archivo local
        with open("consultas_local.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(registro, ensure_ascii=False) + "\n")
    except:
        pass  # Silenciar errores de escritura

# ============================================================================
# INTERFAZ PRINCIPAL
# ============================================================================

def main():
    # Estado de sesión
    if "autenticado" not in st.session_state:
        st.session_state.autenticado = False
        st.session_state.usuario_actual = None
        st.session_state.messages = []
        st.session_state.total_consultas = 0
    
    # ========================================================================
    # PANTALLA DE LOGIN
    # ========================================================================
    if not st.session_state.autenticado:
        st.title("🏛️ Sistema de Consulta Normativa Zapopan")
        st.markdown("---")
        
        st.markdown("""
        ### Sistema de consulta de regulaciones municipales
        
        **Ayuntamiento de Zapopan, Jalisco**
        
        Este sistema permite consultar regulaciones municipales sobre:
        - Ruido y contaminación sonora
        - Construcción y obras
        - Comercio y establecimientos
        - Medio ambiente
        - Espacio público
        
        **🔐 Credenciales de acceso:**
        
        Contacta al administrador del sistema para obtener usuario y contraseña.
        """)
        
        st.markdown("---")
        
        col_login1, col_login2 = st.columns([2, 1])
        
        with col_login1:
            usuario = st.text_input("👤 Usuario", key="login_user")
            password = st.text_input("🔑 Contraseña", type="password", key="login_pass")
        
        with col_login2:
            st.write("")  # Espacio
            st.write("")  # Espacio
            if st.button("🚪 Ingresar", type="primary", width='stretch'):
                if autenticar_usuario(usuario, password):
                    st.session_state.autenticado = True
                    st.session_state.usuario_actual = usuario
                    st.session_state.messages = []
                    st.rerun()
                else:
                    st.error("❌ Credenciales incorrectas")
        
        # Credenciales de prueba (solo en desarrollo)
        with st.expander("🧪 Credenciales de prueba (desarrollo)"):
            st.code("Usuario: luis_admin\nContraseña: ZapopanAdmin2026!")
            st.code("Usuario: demo\nContraseña: demo123")
        
        return
    
    # ========================================================================
    # APLICACIÓN PRINCIPAL (USUARIO AUTENTICADO)
    # ========================================================================
    usuario_actual = st.session_state.usuario_actual
    usuario_info = obtener_info_usuario(usuario_actual)
    
    # Sidebar
    with st.sidebar:
        st.success(f"✅ Conectado como: **{usuario_info['nombre_completo']}**")
        st.info(f"👑 **Rol:** {ROLES_CONFIG[usuario_info['rol']]['nombre']}")
        
        st.markdown("---")
        st.markdown("### 📊 Estadísticas")
        st.metric("Consultas esta sesión", st.session_state.total_consultas)
        
        # Panel de administración (solo para admin)
        if es_administrador(usuario_actual):
            st.markdown("---")
            st.markdown("### 🏰 **PANEL DE ADMINISTRACIÓN**")
            
            with st.expander("👥 Gestión de Usuarios"):
                st.write("**Usuarios del sistema:**")
                for user, info in USUARIOS_DB.items():
                    estado = "✅" if info["estado"] == "activo" else "🚫"
                    st.write(f"{estado} {user} ({info['nombre_completo']})")
            
            with st.expander("📈 Métricas"):
                try:
                    with open("consultas_local.jsonl", "r", encoding="utf-8") as f:
                        lineas = f.readlines()
                    st.metric("Total consultas sistema", len(lineas))
                except:
                    st.metric("Total consultas sistema", 0)
        
        st.markdown("---")
        if st.button("🚪 Cerrar sesión", width='stretch'):
            st.session_state.autenticado = False
            st.session_state.usuario_actual = None
            st.rerun()
    
    # ========================================================================
    # INTERFAZ DE CHAT
    # ========================================================================
    st.title("💬 Consulta Normativa Zapopan")
    st.markdown("---")
    
    # Mostrar historial
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Entrada del usuario
    if prompt := st.chat_input("📝 Describe la situación a consultar (ej: 'ruido de un restaurante por la noche')..."):
        # Agregar mensaje del usuario
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Procesar consulta
        with st.chat_message("assistant"):
            with st.spinner("🔍 Consultando regulaciones..."):
                resultado = procesar_consulta_local(prompt, usuario_actual)
                
                # Mostrar respuesta
                st.markdown(resultado["texto_visible"])
                
                # Actualizar contador
                st.session_state.total_consultas += 1
                
                # Mostrar detalles técnicos solo para admin
                if es_administrador(usuario_actual) and resultado["resultados"]:
                    with st.expander("🔧 Detalles técnicos"):
                        st.json({
                            "categoria": resultado["categoria"],
                            "resultados_encontrados": len(resultado["resultados"]),
                            "dependencias": list(set(r["dependencia"] for r in resultado["resultados"]))
                        })
            
            # Agregar mensaje del asistente
            st.session_state.messages.append({
                "role": "assistant",
                "content": resultado["texto_visible"]
            })
    
    # ========================================================================
    # FOOTER
    # ========================================================================
    st.markdown("---")
    
    col_footer1, col_footer2 = st.columns(2)
    
    with col_footer1:
        st.markdown("### 📚 Áreas de competencia")
        st.markdown("""
        - Ruido y contaminación sonora
        - Construcción y obras
        - Comercio y giros
        - Medio ambiente
        - Espacio público
        """)
    
    with col_footer2:
        st.markdown("### 📞 Dependencias")
        st.markdown("""
        - Inspección y Vigilancia
        - Desarrollo Urbano
        - Medio Ambiente
        - Protección Civil
        """)
    
    st.caption(f"Sistema Normativo Zapopan • Usuario: {usuario_actual} • {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    st.caption("ℹ️ Versión local - Consulta básica de regulaciones")

# ============================================================================
# EJECUCIÓN
# ============================================================================

if __name__ == "__main__":
    main()