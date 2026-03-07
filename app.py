"""
Sistema de Consulta Normativa Zapopan - VERSIÓN ULTRA-MÍNIMA
Funciona SIN Google AI, SIN plotly, SIN dependencias externas
"""

import streamlit as st
import json
import os
import sys
from datetime import datetime

# Importar módulo de fallback mejorado (SIEMPRE disponible)
try:
    from fallback_mejorado import procesar_consulta_hibrida
    FALLBACK_MEJORADO_AVAILABLE = True
except ImportError:
    FALLBACK_MEJORADO_AVAILABLE = False
    st.warning("⚠️ Módulo fallback mejorado no disponible.")

# Sistema híbrido definitivo (fallback garantizado + IA optimizada si funciona)
CHATBOT_MODULE_AVAILABLE = True  # Sistema híbrido siempre disponible

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
    # ========================================================================
    # NIVEL 1: ADMINISTRACIÓN CENTRAL
    # ========================================================================
    "luis_admin": {
        "password": "ZapopanAdmin2026!",
        "nombre_completo": "Luis Alberto Aguirre Gómez",
        "email": "luis.aguirre34@gmail.com",
        "rol": "administrador_supremo",
        "area": "Administración Central",
        "estado": "activo",
        "fecha_creacion": "2026-03-07",
        "ultimo_acceso": None
    },
    
    # ========================================================================
    # NIVEL 2: DIRECCIÓN
    # ========================================================================
    "directora_inspeccion": {
        "password": "Zapopan2026!DIV1",
        "nombre_completo": "María Luisa Vargas",
        "email": "directora.inspeccion@zapopan.gob.mx",
        "rol": "directora",
        "area": "Dirección de Inspección y Vigilancia",
        "estado": "activo",
        "fecha_creacion": "2026-03-07",
        "ultimo_acceso": None
    },
    
    # ========================================================================
    # NIVEL 3: JEFES DE ÁREA
    # ========================================================================
    "jefe_comercio": {
        "password": "Zapopan2026!JCO1",
        "nombre_completo": "Rubén Alejandro Zúñiga",
        "email": "ruben.zuniga@zapopan.gob.mx",
        "rol": "jefe_area",
        "area": "Área de Comercio - Inspección y Vigilancia",
        "estado": "activo",
        "fecha_creacion": "2026-03-07",
        "ultimo_acceso": None
    },
    
    "jefe_atencion": {
        "password": "Zapopan2026!JAT1",
        "nombre_completo": "Adriana [APELLIDO_PENDIENTE]",
        "email": "adriana.atencion@zapopan.gob.mx",
        "rol": "jefe_area",
        "area": "Atención Ciudadana - Inspección y Vigilancia",
        "estado": "activo",
        "fecha_creacion": "2026-03-07",
        "ultimo_acceso": None
    },
    
    "jefe_horarios": {
        "password": "Zapopan2026!JHO1",
        "nombre_completo": "Cornelio González",
        "email": "cornelio.gonzalez@zapopan.gob.mx",
        "rol": "jefe_area",
        "area": "Área de Horarios Especiales - Inspección y Vigilancia",
        "estado": "activo",
        "fecha_creacion": "2026-03-07",
        "ultimo_acceso": None
    },
    
    "jefe_tecnica": {
        "password": "Zapopan2026!JTE1",
        "nombre_completo": "Ignacio Ortiz",
        "email": "ignacio.ortiz@zapopan.gob.mx",
        "rol": "jefe_area",
        "area": "Área Técnica - Inspección y Vigilancia",
        "estado": "activo",
        "fecha_creacion": "2026-03-07",
        "ultimo_acceso": None
    },
    
    "jefe_construccion": {
        "password": "Zapopan2026!JCN1",
        "nombre_completo": "Heriberto Rodríguez",
        "email": "heriberto.rodriguez@zapopan.gob.mx",
        "rol": "jefe_area",
        "area": "Área de Construcción - Inspección y Vigilancia",
        "estado": "activo",
        "fecha_creacion": "2026-03-07",
        "ultimo_acceso": None
    },
    
    # ========================================================================
    # NIVEL 4: JEFES OPERATIVOS (PLACEHOLDERS - COMPLETAR PRÓXIMA SEMANA)
    # ========================================================================
    "jefe_operativo_01": {
        "password": "Zapopan2026!JO01",
        "nombre_completo": "Jefe Operativo 01 (Nombre Pendiente)",
        "email": "jefe.operativo01@zapopan.gob.mx",
        "rol": "jefe_area",
        "area": "Inspección y Vigilancia - Operaciones",
        "estado": "activo",
        "fecha_creacion": "2026-03-07",
        "ultimo_acceso": None,
        "nota": "COMPLETAR: Nombre completo y email real la próxima semana"
    },
    
    "jefe_operativo_02": {
        "password": "Zapopan2026!JO02",
        "nombre_completo": "Jefe Operativo 02 (Nombre Pendiente)",
        "email": "jefe.operativo02@zapopan.gob.mx",
        "rol": "jefe_area",
        "area": "Inspección y Vigilancia - Operaciones",
        "estado": "activo",
        "fecha_creacion": "2026-03-07",
        "ultimo_acceso": None,
        "nota": "COMPLETAR: Nombre completo y email real la próxima semana"
    },
    
    "jefe_operativo_03": {
        "password": "Zapopan2026!JO03",
        "nombre_completo": "Jefe Operativo 03 (Nombre Pendiente)",
        "email": "jefe.operativo03@zapopan.gob.mx",
        "rol": "jefe_area",
        "area": "Inspección y Vigilancia - Operaciones",
        "estado": "activo",
        "fecha_creacion": "2026-03-07",
        "ultimo_acceso": None,
        "nota": "COMPLETAR: Nombre completo y email real la próxima semana"
    },
    
    # ========================================================================
    # NIVEL 5: OPERATIVOS JURÍDICA
    # ========================================================================
    "juridico_01": {
        "password": "Zapopan2026!JU01",
        "nombre_completo": "Diana Valeria Mendoza",
        "email": "diana.mendoza@zapopan.gob.mx",
        "rol": "operativo_juridico",
        "area": "Área Jurídica - Inspección y Vigilancia",
        "estado": "activo",
        "fecha_creacion": "2026-03-07",
        "ultimo_acceso": None
    },
    
    "juridico_02": {
        "password": "Zapopan2026!JU02",
        "nombre_completo": "Diana Montserrat Tellez",
        "email": "diana.tellez@zapopan.gob.mx",
        "rol": "operativo_juridico",
        "area": "Área Jurídica - Inspección y Vigilancia",
        "estado": "activo",
        "fecha_creacion": "2026-03-07",
        "ultimo_acceso": None
    },
    
    "juridico_03": {
        "password": "Zapopan2026!JU03",
        "nombre_completo": "Edgardo [APELLIDO_PENDIENTE]",
        "email": "edgardo.juridico@zapopan.gob.mx",
        "rol": "operativo_juridico",
        "area": "Área Jurídica - Inspección y Vigilancia",
        "estado": "activo",
        "fecha_creacion": "2026-03-07",
        "ultimo_acceso": None
    },
    
    "juridico_04": {
        "password": "Zapopan2026!JU04",
        "nombre_completo": "Operativo Jurídico 04 (Nombre Pendiente)",
        "email": "juridico04@zapopan.gob.mx",
        "rol": "operativo_juridico",
        "area": "Área Jurídica - Inspección y Vigilancia",
        "estado": "activo",
        "fecha_creacion": "2026-03-07",
        "ultimo_acceso": None,
        "nota": "COMPLETAR: Nombre completo y email real la próxima semana"
    },
    
    "juridico_05": {
        "password": "Zapopan2026!JU05",
        "nombre_completo": "Operativo Jurídico 05 (Nombre Pendiente)",
        "email": "juridico05@zapopan.gob.mx",
        "rol": "operativo_juridico",
        "area": "Área Jurídica - Inspección y Vigilancia",
        "estado": "activo",
        "fecha_creacion": "2026-03-07",
        "ultimo_acceso": None,
        "nota": "COMPLETAR: Nombre completo y email real la próxima semana"
    },
    
    # ========================================================================
    # NIVEL 6: OPERATIVOS ATENCIÓN CIUDADANA (PLACEHOLDERS)
    # ========================================================================
    "atencion_01": {
        "password": "Zapopan2026!AC01",
        "nombre_completo": "Operativo Atención 01 (Nombre Pendiente)",
        "email": "atencion01@zapopan.gob.mx",
        "rol": "operativo_atencion",
        "area": "Atención Ciudadana - Inspección y Vigilancia",
        "estado": "activo",
        "fecha_creacion": "2026-03-07",
        "ultimo_acceso": None,
        "nota": "COMPLETAR: Nombre completo y email real la próxima semana"
    },
    
    "atencion_02": {
        "password": "Zapopan2026!AC02",
        "nombre_completo": "Operativo Atención 02 (Nombre Pendiente)",
        "email": "atencion02@zapopan.gob.mx",
        "rol": "operativo_atencion",
        "area": "Atención Ciudadana - Inspección y Vigilancia",
        "estado": "activo",
        "fecha_creacion": "2026-03-07",
        "ultimo_acceso": None,
        "nota": "COMPLETAR: Nombre completo y email real la próxima semana"
    },
    
    "atencion_03": {
        "password": "Zapopan2026!AC03",
        "nombre_completo": "Operativo Atención 03 (Nombre Pendiente)",
        "email": "atencion03@zapopan.gob.mx",
        "rol": "operativo_atencion",
        "area": "Atención Ciudadana - Inspección y Vigilancia",
        "estado": "activo",
        "fecha_creacion": "2026-03-07",
        "ultimo_acceso": None,
        "nota": "COMPLETAR: Nombre completo y email real la próxima semana"
    },
    
    "atencion_04": {
        "password": "Zapopan2026!AC04",
        "nombre_completo": "Operativo Atención 04 (Nombre Pendiente)",
        "email": "atencion04@zapopan.gob.mx",
        "rol": "operativo_atencion",
        "area": "Atención Ciudadana - Inspección y Vigilancia",
        "estado": "activo",
        "fecha_creacion": "2026-03-07",
        "ultimo_acceso": None,
        "nota": "COMPLETAR: Nombre completo y email real la próxima semana"
    },
    
    "atencion_05": {
        "password": "Zapopan2026!AC05",
        "nombre_completo": "Operativo Atención 05 (Nombre Pendiente)",
        "email": "atencion05@zapopan.gob.mx",
        "rol": "operativo_atencion",
        "area": "Atención Ciudadana - Inspección y Vigilancia",
        "estado": "activo",
        "fecha_creacion": "2026-03-07",
        "ultimo_acceso": None,
        "nota": "COMPLETAR: Nombre completo y email real la próxima semana"
    },
    
    # ========================================================================
    # DEMO
    # ========================================================================
    "demo": {
        "password": "demo123",
        "nombre_completo": "Usuario de Demostración",
        "email": "demo@zapopan.gob.mx",
        "rol": "demo",
        "area": "Demostración",
        "estado": "activo",
        "fecha_creacion": "2026-03-06",
        "ultimo_acceso": None
    }
}

ROLES_CONFIG = {
    "administrador_supremo": {
        "nombre": "Administrador Supremo",
        "permisos": ["admin_completo", "gestion_usuarios"],
        "nivel": 100
    },
    "directora": {
        "nombre": "Directora",
        "permisos": ["supervision_general", "reportes", "ver_usuarios"],
        "nivel": 90
    },
    "jefe_area": {
        "nombre": "Jefe de Área",
        "permisos": ["gestion_equipo", "reportes_area", "consultas_avanzadas"],
        "nivel": 80
    },
    "operativo_juridico": {
        "nombre": "Operativo Jurídico",
        "permisos": ["consultas_juridicas", "documentacion", "seguimiento"],
        "nivel": 70
    },
    "operativo_atencion": {
        "nombre": "Operativo Atención Ciudadana",
        "permisos": ["consultas_ciudadanas", "derivacion", "registro"],
        "nivel": 70
    },
    "demo": {
        "nombre": "Usuario Demo",
        "permisos": ["consultas_basicas"],
        "nivel": 10
    }
}

# ============================================================================
# FUNCIONES DE AUTENTICACIÓN
# ============================================================================

def autenticar_usuario(usuario: str, password: str) -> bool:
    """Autenticación simple sin dependencias externas"""
    if usuario in USUARIOS_DB:
        if USUARIOS_DB[usuario]["password"] == password:
            # Registrar último acceso
            from datetime import datetime
            USUARIOS_DB[usuario]["ultimo_acceso"] = datetime.now().isoformat()
            return True
    return False

def obtener_info_usuario(usuario: str):
    """Obtener información de usuario"""
    return USUARIOS_DB.get(usuario)

def es_administrador(usuario: str) -> bool:
    """Verificar si es administrador"""
    info = obtener_info_usuario(usuario)
    return info and info["rol"] == "administrador_supremo"

def cambiar_contrasena(usuario: str, contrasena_actual: str, contrasena_nueva: str) -> bool:
    """Cambiar contraseña de usuario"""
    if usuario not in USUARIOS_DB:
        return False
    
    if USUARIOS_DB[usuario]["password"] != contrasena_actual:
        return False
    
    # Validar seguridad de nueva contraseña
    if len(contrasena_nueva) < 8:
        return False
    
    # Actualizar contraseña
    USUARIOS_DB[usuario]["password"] = contrasena_nueva
    return True

def validar_fortaleza_contrasena(contrasena: str) -> dict:
    """Validar fortaleza de contraseña"""
    validaciones = {
        "longitud_minima": len(contrasena) >= 8,
        "tiene_mayuscula": any(c.isupper() for c in contrasena),
        "tiene_minuscula": any(c.islower() for c in contrasena),
        "tiene_numero": any(c.isdigit() for c in contrasena),
        "tiene_especial": any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in contrasena)
    }
    
    return {
        "valida": all(validaciones.values()),
        "detalles": validaciones
    }

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
    """Procesar consulta sin Google AI (fallback)"""
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

def procesar_consulta_con_chatbot_zapopan(consulta: str, usuario: str):
    """Procesar consulta usando sistema híbrido definitivo"""
    
    # Usar sistema híbrido definitivo (fallback garantizado + IA optimizada si funciona)
    try:
        from chatbot_zapopan_hibrido import procesar_consulta_hibrida
        return procesar_consulta_hibrida(consulta, usuario)
    except ImportError:
        # Fallback al sistema mejorado si no está disponible
        if FALLBACK_MEJORADO_AVAILABLE:
            return procesar_consulta_hibrida(consulta, usuario, intentar_chatbot=False)
        
        # Último fallback
        return procesar_consulta_local(consulta, usuario)

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
        
        # Panel de cambio de contraseña
        st.markdown("---")
        with st.expander("🔐 Cambiar contraseña"):
            contrasena_actual = st.text_input("Contraseña actual", type="password", key="cambiar_actual")
            contrasena_nueva = st.text_input("Nueva contraseña", type="password", key="cambiar_nueva")
            contrasena_confirmar = st.text_input("Confirmar nueva contraseña", type="password", key="cambiar_confirmar")
            
            if st.button("🔄 Cambiar contraseña", width='stretch'):
                if not contrasena_actual or not contrasena_nueva or not contrasena_confirmar:
                    st.error("❌ Todos los campos son obligatorios")
                elif contrasena_nueva != contrasena_confirmar:
                    st.error("❌ Las contraseñas nuevas no coinciden")
                else:
                    validacion = validar_fortaleza_contrasena(contrasena_nueva)
                    if not validacion["valida"]:
                        st.error("❌ La contraseña no cumple con los requisitos de seguridad:")
                        for criterio, cumple in validacion["detalles"].items():
                            icono = "✅" if cumple else "❌"
                            st.write(f"{icono} {criterio.replace('_', ' ').title()}")
                    elif cambiar_contrasena(usuario_actual, contrasena_actual, contrasena_nueva):
                        st.success("✅ Contraseña cambiada exitosamente")
                        st.info("🔒 La próxima vez que ingreses, usa tu nueva contraseña")
                    else:
                        st.error("❌ Contraseña actual incorrecta o usuario no encontrado")
        
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
        
        # Procesar consulta CON CHATBOT ZAPOPAN (si está disponible)
        with st.chat_message("assistant"):
            with st.spinner("🔍 Consultando sistema normativo Zapopan..."):
                resultado = procesar_consulta_con_chatbot_zapopan(prompt, usuario_actual)
                
                # Mostrar respuesta
                st.markdown(resultado["texto_visible"])
                
                # Mostrar indicador de fuente
                fuente = resultado.get("fuente", "")
                calidad = resultado.get("calidad", "")
                
                if fuente == "gemini_optimizado":
                    if calidad == "excelente":
                        st.caption("🤖 Respuesta IA optimizada • ✅ Excelente calidad")
                    elif calidad == "buena":
                        st.caption("🤖 Respuesta IA optimizada • 👍 Buena calidad")
                    elif calidad == "aceptable":
                        st.caption("🤖 Respuesta IA optimizada • ⚠️ Calidad aceptable")
                elif fuente == "fallback_mejorado":
                    st.caption("📋 Sistema normativo Zapopan • 🛡️ Respuesta garantizada")
                else:
                    st.caption("📚 Sistema local • 🔧 Modo básico")
                
                # Actualizar contador
                st.session_state.total_consultas += 1
            
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
    st.caption("🏰 Sistema híbrido definitivo - Fallback garantizado + IA optimizada cuando disponible")

# ============================================================================
# EJECUCIÓN
# ============================================================================

if __name__ == "__main__":
    main()