"""
SISTEMA DE CONSULTA NORMATIVA ZAPOPAN - App Streamlit
Integración completa: RAG + Router Semántico + Google AI Studio + Auditoría
"""

"""
SISTEMA DE CONSULTA NORMATIVA ZAPOPAN - App Streamlit
Integración completa: RAG + Router Semántico + Google AI Studio + Auditoría
"""

import streamlit as st
import google.generativeai as genai
import json
import pandas as pd
from datetime import datetime
import time
import sys
import os

# --- MÓDULOS DEL SISTEMA ---
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from rag_engine import rag_engine
    from semantic_router import semantic_router
    from google_sheets_integration import sheets_integration
    print("✅ Módulos RAG, Router y Google Sheets cargados correctamente")
except ImportError as e:
    st.error(f"❌ Error cargando módulos: {e}")
    print(f"Error: {e}")

# --- CONFIGURACIÓN DE SEGURIDAD Y ROLES ---
# Base de datos de usuarios (en producción usaría base de datos real)
USUARIOS_DB = {
    # 🏰 ADMINISTRADOR SUPREMO (Luis - Propietario del sistema)
    "luis_admin": {
        "password": "ZapopanAdmin2026!",
        "nombre_completo": "Luis Alberto Aguirre Gómez",
        "email": "luis.aguirre34@gmail.com",
        "rol": "administrador_supremo",
        "area": "Administración Central",
        "fecha_creacion": "2026-03-06",
        "estado": "activo",
        "ultimo_acceso": None,
        "consultas_realizadas": 0
    },
    
    # 👩‍💼 DIRECTORA (ejemplo - Luis asignará credenciales reales)
    "directora_ejemplo": {
        "password": "DirectoraZpn2026!",
        "nombre_completo": "Ejemplo Directora",
        "email": "directora@zapopan.gob.mx",
        "rol": "directora",
        "area": "Dirección General",
        "fecha_creacion": "2026-03-06",
        "estado": "activo",
        "ultimo_acceso": None,
        "consultas_realizadas": 0
    },
    
    # 🧪 USUARIO DEMO
    "demo": {
        "password": "demo123",
        "nombre_completo": "Usuario de Demostración",
        "email": "demo@zapopan.gob.mx",
        "rol": "demo",
        "area": "Demostración",
        "fecha_creacion": "2026-03-06",
        "estado": "activo",
        "ultimo_acceso": None,
        "consultas_realizadas": 0
    }
}

# Diccionario simple para autenticación (compatibilidad)
USUARIOS_AUTORIZADOS = {user: data["password"] for user, data in USUARIOS_DB.items()}

# --- ROLES Y PERMISOS DETALLADOS ---
ROLES_CONFIG = {
    "administrador_supremo": {
        "nombre": "Administrador Supremo",
        "nivel": 100,
        "permisos": [
            "admin_completo",
            "gestion_usuarios_completa",  # Crear, editar, bloquear, eliminar
            "ver_todos_logs",
            "config_sistema_completo",
            "ver_dashboard_ejecutivo",
            "exportar_todos_datos",
            "rotar_credenciales",
            "acceso_panel_admin"
        ],
        "descripcion": "Control total del sistema. Solo para el propietario."
    },
    "directora": {
        "nombre": "Directora",
        "nivel": 90,
        "permisos": [
            "ver_metricas_completas",
            "ver_reportes_ejecutivos",
            "ver_logs_areas",
            "exportar_datos_areas",
            "realizar_consultas_avanzadas",
            "ver_dashboard_ejecutivo",
            "acceso_panel_metricas"
        ],
        "descripcion": "Acceso ejecutivo a todas las métricas y reportes."
    },
    "jefe_area": {
        "nombre": "Jefe de Área",
        "nivel": 80,
        "permisos": [
            "ver_metricas_area",
            "ver_reportes_area",
            "gestion_equipo",
            "realizar_consultas_avanzadas",
            "ver_dashboard_operativo",
            "exportar_datos_area"
        ],
        "descripcion": "Gestión operativa de un área específica."
    },
    "coordinador_operativo": {
        "nombre": "Coordinador Operativo",
        "nivel": 70,
        "permisos": [
            "ver_metricas_operativas",
            "supervisar_consultas",
            "realizar_consultas",
            "ver_dashboard_basico",
            "generar_reportes_diarios"
        ],
        "descripcion": "Supervisión diaria y coordinación operativa."
    },
    "area_juridica": {
        "nombre": "Área Jurídica",
        "nivel": 60,
        "permisos": [
            "consultas_legales_avanzadas",
            "acceso_normativa_completa",
            "ver_consultas_juridicas",
            "realizar_consultas",
            "ver_dashboard_juridico"
        ],
        "descripcion": "Acceso especializado a consultas legales y normativa."
    },
    "atencion_ciudadana": {
        "nombre": "Atención Ciudadana",
        "nivel": 50,
        "permisos": [
            "realizar_consultas_basicas",
            "registrar_consultas_ciudadanas",
            "ver_consultas_propias",
            "ver_dashboard_basico"
        ],
        "descripcion": "Atención a consultas ciudadanas y registro básico."
    },
    "demo": {
        "nombre": "Usuario Demo",
        "nivel": 10,
        "permisos": [
            "realizar_consultas_demo",
            "ver_dashboard_basico"
        ],
        "descripcion": "Acceso limitado para demostraciones y pruebas."
    }
}

# Función para obtener información de usuario
def obtener_info_usuario(username: str):
    """Obtener información completa de un usuario"""
    return USUARIOS_DB.get(username)

# Función para verificar permisos
def tiene_permiso(username: str, permiso: str) -> bool:
    """Verificar si un usuario tiene un permiso específico"""
    user_info = obtener_info_usuario(username)
    if not user_info or user_info["estado"] != "activo":
        return False
    
    rol = user_info["rol"]
    if rol in ROLES_CONFIG:
        return permiso in ROLES_CONFIG[rol]["permisos"]
    return False

def es_administrador(username: str) -> bool:
    """Verificar si un usuario es administrador"""
    user_info = obtener_info_usuario(username)
    if not user_info:
        return False
    return user_info["rol"] in ["administrador_supremo", "directora", "jefe_area"]

def puede_gestionar_usuarios(username: str) -> bool:
    """Verificar si un usuario puede gestionar otros usuarios"""
    return tiene_permiso(username, "gestion_usuarios_completa")

# Funciones para gestión de usuarios
def crear_usuario(username: str, password: str, nombre_completo: str, email: str, rol: str, area: str):
    """Crear un nuevo usuario en el sistema"""
    if username in USUARIOS_DB:
        return False, "El usuario ya existe"
    
    if rol not in ROLES_CONFIG:
        return False, "Rol no válido"
    
    USUARIOS_DB[username] = {
        "password": password,
        "nombre_completo": nombre_completo,
        "email": email,
        "rol": rol,
        "area": area,
        "fecha_creacion": datetime.now().strftime("%Y-%m-%d"),
        "estado": "activo",
        "ultimo_acceso": None,
        "consultas_realizadas": 0
    }
    
    # Actualizar diccionario de autenticación
    USUARIOS_AUTORIZADOS[username] = password
    
    return True, f"Usuario '{username}' creado exitosamente"

def actualizar_usuario(username: str, **kwargs):
    """Actualizar información de un usuario"""
    if username not in USUARIOS_DB:
        return False, "Usuario no encontrado"
    
    # Campos que se pueden actualizar
    campos_permitidos = ["nombre_completo", "email", "rol", "area", "estado", "password"]
    
    for campo, valor in kwargs.items():
        if campo in campos_permitidos:
            if campo == "password":
                # Actualizar también en USUARIOS_AUTORIZADOS
                USUARIOS_AUTORIZADOS[username] = valor
            USUARIOS_DB[username][campo] = valor
    
    return True, f"Usuario '{username}' actualizado"

def bloquear_usuario(username: str):
    """Bloquear acceso de un usuario"""
    return actualizar_usuario(username, estado="bloqueado")

def activar_usuario(username: str):
    """Activar acceso de un usuario"""
    return actualizar_usuario(username, estado="activo")

def eliminar_usuario(username: str):
    """Eliminar un usuario del sistema (solo admin supremo)"""
    if username == "luis_admin":
        return False, "No se puede eliminar al administrador supremo"
    
    if username in USUARIOS_DB:
        del USUARIOS_DB[username]
        if username in USUARIOS_AUTORIZADOS:
            del USUARIOS_AUTORIZADOS[username]
        return True, f"Usuario '{username}' eliminado"
    
    return False, "Usuario no encontrado"

def registrar_acceso(username: str):
    """Registrar último acceso de un usuario"""
    if username in USUARIOS_DB:
        USUARIOS_DB[username]["ultimo_acceso"] = datetime.now().isoformat()
        return True
    return False

def incrementar_consultas(username: str):
    """Incrementar contador de consultas de un usuario"""
    if username in USUARIOS_DB:
        USUARIOS_DB[username]["consultas_realizadas"] += 1
        return True
    return False

def obtener_usuarios_por_rol(rol: str):
    """Obtener todos los usuarios de un rol específico"""
    return {user: info for user, info in USUARIOS_DB.items() if info["rol"] == rol}

def obtener_usuarios_por_area(area: str):
    """Obtener todos los usuarios de un área específica"""
    return {user: info for user, info in USUARIOS_DB.items() if info["area"] == area}

def obtener_estadisticas_usuarios():
    """Obtener estadísticas de usuarios"""
    total = len(USUARIOS_DB)
    activos = sum(1 for info in USUARIOS_DB.values() if info["estado"] == "activo")
    bloqueados = total - activos
    
    # Distribución por rol
    por_rol = {}
    for info in USUARIOS_DB.values():
        rol = info["rol"]
        por_rol[rol] = por_rol.get(rol, 0) + 1
    
    return {
        "total_usuarios": total,
        "usuarios_activos": activos,
        "usuarios_bloqueados": bloqueados,
        "distribucion_por_rol": por_rol
    }

def tiene_permiso(usuario: str, permiso: str) -> bool:
    """Verificar si un usuario tiene un permiso específico"""
    if usuario in ROLES_USUARIOS:
        return permiso in ROLES_USUARIOS[usuario]["permisos"]
    return False

def es_administrador(usuario: str) -> bool:
    """Verificar si un usuario es administrador"""
    if usuario in ROLES_USUARIOS:
        return ROLES_USUARIOS[usuario]["rol"] in ["administrador_supremo", "administrador"]
    return False

# --- CONFIGURACIÓN DE GEMINI ---
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# --- CONFIGURACIÓN DE GOOGLE SHEETS ---
# Nota: Para producción, configura credenciales de servicio de Google Sheets
# en .streamlit/secrets.toml o mediante archivo JSON
SHEETS_CONNECTED = False
try:
    # Intentar conectar a Google Sheets (modo demo por defecto)
    SHEETS_CONNECTED = sheets_integration.connect()
    if SHEETS_CONNECTED:
        st.success("✅ Conectado a sistema de almacenamiento de datos")
    else:
        st.info("🔧 Usando modo de demostración para almacenamiento de datos")
except Exception as e:
    st.warning(f"⚠️ Error conectando a Google Sheets: {e}")
    st.info("El sistema funcionará en modo de demostración")

def inicializar_chat(rag_context: str = ""):
    """Inicializar modelo Gemini con System Instructions y contexto RAG"""
    
    # Leer System Instructions
    with open("system_instructions.txt", "r", encoding="utf-8") as f:
        system_instructions = f.read()
    
    # Combinar con contexto RAG si existe
    if rag_context:
        full_instructions = f"{system_instructions}\n\n{rag_context}"
    else:
        full_instructions = system_instructions
    
    # Usar modelo disponible (gemini-flash-latest es la versión más reciente)
    return genai.GenerativeModel(
        model_name="gemini-flash-latest",
        generation_config={
            "temperature": 0.1,
            "top_p": 0.95,
            "max_output_tokens": 4000
        },
        system_instruction=full_instructions
    )

def procesar_consulta_completa(prompt: str, usuario: str) -> Dict:
    """Procesar consulta completa con RAG, router semántico y Gemini"""
    
    start_time = time.time()
    
    # 1. CLASIFICACIÓN SEMÁNTICA
    st.info("🔍 Analizando consulta...")
    classification = semantic_router.classify_query(prompt)
    
    # 2. BÚSQUEDA RAG
    st.info("📚 Buscando normativa relevante...")
    rag_results = rag_engine.semantic_search(prompt, top_k=5)
    rag_context = rag_engine.get_relevant_context(prompt, top_k=3)
    
    # 3. PREPARAR PROMPT MEJORADO
    enhanced_prompt = f"""
CONSULTA DEL USUARIO: {prompt}

INFORMACIÓN DE CLASIFICACIÓN:
- Categoría principal: {classification['categoria_principal']}
- Categoría secundaria: {classification['categoria_secundaria']}
- Área detectada: {classification['area_detectada']}
- Dependencia responsable: {classification['dependencia_responsable']}
- Tipo de consulta: {classification['tipo_consulta']}

{rag_context}

RESPONDE SEGÚN EL PROTOCOLO ESTABLECIDO EN LAS SYSTEM INSTRUCTIONS.
AL FINAL, INCLUYE EL BLOQUE ---DATASET--- CON LOS DATOS ESTRUCTURADOS.
"""
    
    # 4. LLAMAR A GEMINI
    st.info("🤖 Generando respuesta con IA...")
    model = inicializar_chat(rag_context)
    response = model.generate_content(enhanced_prompt)
    texto_completo = response.text
    
    # 5. EXTRAER Y PROCESAR DATOS ESTRUCTURADOS
    dataset_json = None
    if "---DATASET---" in texto_completo:
        texto_visible = texto_completo.split("---DATASET---")[0]
        json_str = texto_completo.split("---DATASET---")[1].strip()
        
        try:
            # Parsear JSON y enriquecer con datos del router y RAG
            dataset_json = json.loads(json_str)
            
            # Añadir metadatos de clasificación
            dataset_json.update({
                "usuario_real": usuario,
                "categoria_principal": classification['categoria_principal'],
                "categoria_secundaria": classification['categoria_secundaria'],
                "area_detectada": classification['area_detectada'],
                "dependencia_responsable": classification['dependencia_responsable'],
                "dependencias_concurrentes": classification['dependencias_concurrentes'],
                "tipo_consulta": classification['tipo_consulta'],
                "indicador_evento": classification['indicador_evento'],
                "reglamentos_prioritarios": classification.get('reglamentos_prioritarios', []),
                
                # Datos de RAG
                "documentos_consultados": rag_engine.get_documents_consulted(rag_results),
                "articulos_citados": rag_engine.get_articles_cited(rag_results),
                "ids_juridicos_utilizados": rag_engine.extract_legal_ids(rag_results),
                
                # Métricas
                "tiempo_respuesta_segundos": round(time.time() - start_time, 2),
                "longitud_consulta": len(prompt),
                "timestamp": datetime.now().isoformat()
            })
            
            # Guardar en archivo local (backup)
            with open("log_consultas.jsonl", "a", encoding="utf-8") as f:
                f.write(json.dumps(dataset_json, ensure_ascii=False) + "\n")
            
            # Guardar en Google Sheets
            try:
                if 'sheets_integration' in globals():
                    saved = sheets_integration.append_consultation(dataset_json)
                    if saved:
                        st.success("✅ Datos guardados en sistema de análisis")
                    else:
                        st.info("ℹ️ Datos guardados localmente (modo demo)")
                else:
                    st.info("ℹ️ Datos guardados localmente")
            except Exception as e:
                st.warning(f"⚠️ Error guardando en Google Sheets: {e}")
                st.info("Datos guardados localmente como backup")
            
        except json.JSONDecodeError as e:
            st.warning(f"⚠️ Error parseando JSON: {e}")
            texto_visible = texto_completo
            dataset_json = None
    else:
        texto_visible = texto_completo
        dataset_json = None
    
    return {
        "texto_visible": texto_visible,
        "dataset_json": dataset_json,
        "classification": classification,
        "rag_results": rag_results,
        "tiempo_respuesta": round(time.time() - start_time, 2)
    }

# --- INTERFAZ DE USUARIO ---
st.set_page_config(
    page_title="Zapopan AI - Sistema de Consulta Normativa",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar para información del sistema
with st.sidebar:
    st.title("🏛️ Sistema Normativo Zapopan")
    st.markdown("---")
    
    if "autenticado" in st.session_state and st.session_state.autenticado:
        usuario_actual = st.session_state.usuario_actual
        usuario_info = st.session_state.get("usuario_info", {})
        
        # Información del usuario
        st.success(f"✅ Conectado como: **{usuario_info.get('nombre_completo', usuario_actual)}**")
        
        # Mostrar información detallada
        with st.expander("👤 Información de tu cuenta", expanded=False):
            col_info1, col_info2 = st.columns(2)
            with col_info1:
                st.write(f"**Usuario:** {usuario_actual}")
                st.write(f"**Rol:** {ROLES_CONFIG.get(usuario_info.get('rol', ''), {}).get('nombre', 'N/A')}")
                st.write(f"**Área:** {usuario_info.get('area', 'N/A')}")
            with col_info2:
                st.write(f"**Estado:** {usuario_info.get('estado', 'N/A')}")
                st.write(f"**Consultas:** {usuario_info.get('consultas_realizadas', 0)}")
                if usuario_info.get('ultimo_acceso'):
                    st.write(f"**Último acceso:** {usuario_info.get('ultimo_acceso', 'N/A')[:16]}")
        
        st.markdown("### 📊 Estadísticas Personales")
        col_stat1, col_stat2 = st.columns(2)
        with col_stat1:
            if "total_consultas" in st.session_state:
                st.metric("Consultas esta sesión", st.session_state.total_consultas)
        with col_stat2:
            st.metric("Consultas totales", usuario_info.get('consultas_realizadas', 0))
        
        # --- SECCIÓN DE GESTIÓN DE USUARIOS (SOLO PARA ADMINISTRADOR SUPREMO) ---
        if usuario_actual == "luis_admin" and puede_gestionar_usuarios(usuario_actual):
            st.markdown("---")
            st.markdown("### 🏰 **GESTIÓN DE USUARIOS**")
            
            # Pestañas de gestión
            gest_tab1, gest_tab2, gest_tab3 = st.tabs(["👥 Ver Usuarios", "➕ Crear Usuario", "⚙️ Gestionar"])
            
            with gest_tab1:
                st.subheader("📋 Lista Completa de Usuarios")
                
                # Crear DataFrame con todos los usuarios
                usuarios_lista = []
                for username, info in USUARIOS_DB.items():
                    usuarios_lista.append({
                        "Usuario": username,
                        "Nombre Completo": info.get("nombre_completo", ""),
                        "Email": info.get("email", ""),
                        "Rol": ROLES_CONFIG.get(info.get("rol", ""), {}).get("nombre", info.get("rol", "")),
                        "Área": info.get("area", ""),
                        "Estado": info.get("estado", ""),
                        "Consultas": info.get("consultas_realizadas", 0),
                        "Creado": info.get("fecha_creacion", ""),
                        "Último Acceso": info.get("ultimo_acceso", "")[:19] if info.get("ultimo_acceso") else "Nunca"
                    })
                
                df_usuarios = pd.DataFrame(usuarios_lista)
                st.dataframe(df_usuarios, use_container_width=True, hide_index=True)
                
                # Estadísticas
                stats = obtener_estadisticas_usuarios()
                col_stat1, col_stat2, col_stat3 = st.columns(3)
                with col_stat1:
                    st.metric("Total Usuarios", stats["total_usuarios"])
                with col_stat2:
                    st.metric("Usuarios Activos", stats["usuarios_activos"])
                with col_stat3:
                    st.metric("Usuarios Bloqueados", stats["usuarios_bloqueados"])
            
            with gest_tab2:
                st.subheader("➕ Crear Nuevo Usuario")
                
                with st.form("crear_usuario_form"):
                    col_form1, col_form2 = st.columns(2)
                    
                    with col_form1:
                        nuevo_usuario = st.text_input("Nombre de usuario*", help="Sin espacios, minúsculas")
                        nombre_completo = st.text_input("Nombre completo*")
                        email = st.text_input("Email*")
                    
                    with col_form2:
                        rol = st.selectbox(
                            "Rol*",
                            options=list(ROLES_CONFIG.keys()),
                            format_func=lambda x: ROLES_CONFIG[x]["nombre"]
                        )
                        area = st.selectbox(
                            "Área*",
                            options=[
                                "Dirección General",
                                "Inspección y Vigilancia", 
                                "Área Jurídica",
                                "Atención Ciudadana",
                                "Coordinación Operativa",
                                "Administración Central",
                                "Demostración"
                            ]
                        )
                        password = st.text_input("Contraseña*", type="password", help="Mínimo 8 caracteres")
                        confirm_password = st.text_input("Confirmar contraseña*", type="password")
                    
                    submitted = st.form_submit_button("✅ Crear Usuario", type="primary")
                    
                    if submitted:
                        # Validaciones
                        if not all([nuevo_usuario, nombre_completo, email, password, confirm_password]):
                            st.error("Todos los campos marcados con * son obligatorios")
                        elif password != confirm_password:
                            st.error("Las contraseñas no coinciden")
                        elif len(password) < 8:
                            st.error("La contraseña debe tener al menos 8 caracteres")
                        elif nuevo_usuario in USUARIOS_DB:
                            st.error(f"El usuario '{nuevo_usuario}' ya existe")
                        else:
                            success, message = crear_usuario(
                                username=nuevo_usuario,
                                password=password,
                                nombre_completo=nombre_completo,
                                email=email,
                                rol=rol,
                                area=area
                            )
                            if success:
                                st.success(message)
                                st.info(f"**Credenciales asignadas:**\n👤 Usuario: `{nuevo_usuario}`\n🔑 Contraseña: `{password}`")
                                st.warning("⚠️ Guarda estas credenciales. Serán necesarias para el primer acceso.")
                            else:
                                st.error(f"Error: {message}")
            
            with gest_tab3:
                st.subheader("⚙️ Gestionar Usuarios Existentes")
                
                # Seleccionar usuario a gestionar
                usuarios_disponibles = [u for u in USUARIOS_DB.keys() if u != "luis_admin"]
                usuario_gestionar = st.selectbox("Seleccionar usuario a gestionar", usuarios_disponibles)
                
                if usuario_gestionar:
                    info_usuario = USUARIOS_DB[usuario_gestionar]
                    
                    st.markdown(f"**Gestionando:** {info_usuario.get('nombre_completo')} ({usuario_gestionar})")
                    
                    col_acc1, col_acc2, col_acc3 = st.columns(3)
                    
                    with col_acc1:
                        if info_usuario["estado"] == "activo":
                            if st.button("🚫 Bloquear Usuario", use_container_width=True, type="secondary"):
                                success, msg = bloquear_usuario(usuario_gestionar)
                                if success:
                                    st.success(msg)
                                    st.rerun()
                                else:
                                    st.error(msg)
                        else:
                            if st.button("✅ Activar Usuario", use_container_width=True, type="primary"):
                                success, msg = activar_usuario(usuario_gestionar)
                                if success:
                                    st.success(msg)
                                    st.rerun()
                                else:
                                    st.error(msg)
                    
                    with col_acc2:
                        if st.button("🔄 Cambiar Contraseña", use_container_width=True):
                            nueva_pass = st.text_input("Nueva contraseña", type="password", key=f"new_pass_{usuario_gestionar}")
                            confirm_pass = st.text_input("Confirmar", type="password", key=f"confirm_pass_{usuario_gestionar}")
                            if st.button("💾 Guardar", key=f"save_pass_{usuario_gestionar}"):
                                if nueva_pass and nueva_pass == confirm_pass:
                                    success, msg = actualizar_usuario(usuario_gestionar, password=nueva_pass)
                                    if success:
                                        st.success(f"Contraseña actualizada para '{usuario_gestionar}'")
                                    else:
                                        st.error(msg)
                    
                    with col_acc3:
                        if st.button("🗑️ Eliminar Usuario", use_container_width=True, type="secondary"):
                            st.warning(f"⚠️ ¿Eliminar permanentemente a '{usuario_gestionar}'?")
                            confirmar = st.checkbox("Confirmar eliminación permanente")
                            if confirmar:
                                success, msg = eliminar_usuario(usuario_gestionar)
                                if success:
                                    st.error(f"Usuario '{usuario_gestionar}' eliminado permanentemente")
                                    st.rerun()
                                else:
                                    st.error(msg)
                    
                    # Información actual del usuario
                    with st.expander("📋 Ver información detallada"):
                        st.json(info_usuario)
        
        # --- PANEL DE ADMINISTRACIÓN GENERAL (PARA TODOS LOS ADMINS) ---
        elif es_administrador(usuario_actual):
            st.markdown("---")
            st.markdown("### 📊 **PANEL DE ADMINISTRACIÓN**")
            
            admin_tab1, admin_tab2 = st.tabs(["📈 Métricas", "⚙️ Configuración"])
            
            with admin_tab1:
                st.subheader("Métricas del Sistema")
                try:
                    with open("log_consultas.jsonl", "r") as f:
                        lineas = f.readlines()
                    total_consultas = len(lineas)
                    st.metric("Total consultas sistema", total_consultas)
                    
                    if lineas:
                        # Consultas hoy (simplificado)
                        hoy = datetime.now().date()
                        consultas_hoy = 0
                        for linea in lineas[-50:]:  # Revisar últimas 50
                            try:
                                data = json.loads(linea)
                                if 'timestamp' in data:
                                    fecha = datetime.fromisoformat(data['timestamp']).date()
                                    if fecha == hoy:
                                        consultas_hoy += 1
                            except:
                                continue
                        
                        st.metric("Consultas hoy", consultas_hoy)
                        st.metric("Tasa uso", f"{min(100, total_consultas // 10)}%")
                    else:
                        st.info("No hay datos de consultas aún")
                except:
                    st.info("No hay datos de métricas disponibles")
            
            with admin_tab2:
                st.subheader("Configuración del Sistema")
                st.info("Configuración avanzada - Próxima versión")
                if st.button("🔄 Reiniciar motor RAG"):
                    st.success("Motor RAG reiniciado (simulación)")
                if st.button("📊 Actualizar datasets"):
                    st.info("Actualización programada para próxima versión")
        
        st.markdown("---")
        st.markdown("### 🔧 Herramientas")
        if st.button("📥 Exportar datos", help="Descargar registro de consultas"):
            try:
                with open("log_consultas.jsonl", "r") as f:
                    data = f.read()
                st.download_button(
                    label="Descargar JSONL",
                    data=data,
                    file_name=f"consultas_zapopan_{datetime.now().strftime('%Y%m%d')}.jsonl",
                    mime="application/json"
                )
            except:
                st.warning("No hay datos para exportar")
        
        if st.button("🔄 Reiniciar chat"):
            st.session_state.messages = []
            st.rerun()
        
        if st.button("🚪 Cerrar sesión"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    st.markdown("---")
    st.markdown("### ℹ️ Acerca del sistema")
    st.markdown("""
    **Sistema de Consulta Normativa**  
    Ayuntamiento de Zapopan, Jalisco
    
    Versión: 1.0.0  
    Motor: Gemini 1.5 Flash  
    Datasets: 3 conjuntos normativos  
    Actualizado: Marzo 2026
    
    👥 **Usuarios autorizados:**  
    - Personal de Inspección y Vigilancia  
    - Inspectores municipales  
    - Administradores
    """)

# --- PANTALLA DE LOGIN ---
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.title("🏛️ Acceso al Sistema Normativo")
        st.markdown("---")
        
        st.markdown("""
        ### Sistema de Consulta Normativa
        **Ayuntamiento de Zapopan, Jalisco**
        
        Este sistema permite consultar y analizar normativa municipal
        relacionada con inspección, vigilancia y regulación urbana.
        
        **🔐 Credenciales de acceso:**
        
        🏰 **Administrador Supremo (Luis - Control total):**  
        👤 Usuario: `luis_admin`  
        🔑 Contraseña: `ZapopanAdmin2026!`
        
        🧪 **Usuario de demostración (Acceso limitado):**  
        👤 Usuario: `demo`  
        🔑 Contraseña: `demo123`
        
        **👥 Roles disponibles en el sistema:**
        
        1. **👩‍💼 Directora** - Acceso ejecutivo completo
        2. **👨‍💼 Jefes de Área** - Gestión operativa por área  
        3. **👷 Coordinadores Operativos** - Supervisión diaria
        4. **⚖️ Área Jurídica** - Consultas legales especializadas
        5. **📞 Atención Ciudadana** - Registro de consultas ciudadanas
        
        **📋 Para obtener credenciales:**  
        Contacta al administrador supremo (`luis_admin`) para asignar
        usuario y contraseña según tu rol en la organización.
        """)
        
        st.markdown("---")
        
        user = st.text_input("👤 Usuario", key="login_user")
        password = st.text_input("🔑 Contraseña", type="password", key="login_pass")
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🚪 Ingresar", type="primary", use_container_width=True):
                # Verificar credenciales y estado del usuario
                if user in USUARIOS_DB:
                    user_info = USUARIOS_DB[user]
                    
                    # Verificar contraseña
                    if user_info["password"] == password:
                        # Verificar estado del usuario
                        if user_info["estado"] == "activo":
                            # Registrar acceso exitoso
                            registrar_acceso(user)
                            
                            st.session_state.autenticado = True
                            st.session_state.usuario_actual = user
                            st.session_state.usuario_info = user_info
                            st.session_state.messages = []
                            st.session_state.total_consultas = 0
                            st.rerun()
                        else:
                            st.error(f"❌ Usuario **{user}** está **{user_info['estado']}**. Contacta al administrador.")
                    else:
                        st.error("❌ Contraseña incorrecta")
                else:
                    st.error("❌ Usuario no encontrado")
        
        with col_btn2:
            if st.button("🆘 Ayuda", use_container_width=True):
                st.info("""
                **Soporte técnico:**  
                Contacta al administrador del sistema para obtener credenciales.
                
                **Usuarios autorizados:**  
                - Personal de Inspección y Vigilancia  
                - Inspectores municipales  
                - Administradores designados
                """)
    
    # Footer
    st.markdown("---")
    st.caption("Sistema desarrollado para el Ayuntamiento de Zapopan, Jalisco • Versión 1.0.0 • 2026")

# --- PANTALLA PRINCIPAL DEL CHATBOT ---
else:
    # Header principal
    col_header1, col_header2 = st.columns([3, 1])
    
    with col_header1:
        st.title(f"🤖 Asistente Normativo Zapopan")
        st.markdown(f"**Usuario:** {st.session_state.usuario_actual} | **Sistema de Consulta Normativa Integral**")
    
    with col_header2:
        st.metric("Consultas", st.session_state.get("total_consultas", 0))
    
    st.markdown("---")
    
    # Inicializar historial de mensajes
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "total_consultas" not in st.session_state:
        st.session_state.total_consultas = 0
    
    # Mostrar historial de conversación
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Mostrar metadata si existe
            if message.get("metadata"):
                with st.expander("📊 Ver detalles técnicos"):
                    st.json(message["metadata"], expanded=False)
    
    # Entrada del usuario
    if prompt := st.chat_input("📝 Describe la situación a analizar (ej: 'Un restaurante con música fuerte hasta la madrugada')..."):
        # Agregar mensaje del usuario
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Procesar consulta
        with st.chat_message("assistant"):
            with st.spinner("🔍 Analizando situación normativa..."):
                try:
                    # Procesar consulta completa
                    resultado = procesar_consulta_completa(prompt, st.session_state.usuario_actual)
                    
                    # Mostrar respuesta
                    st.markdown(resultado["texto_visible"])
                    
                    # Actualizar contador
                    st.session_state.total_consultas += 1
                    
                    # Mostrar detalles técnicos en expander
                    with st.expander("📈 Ver análisis técnico"):
                        col_tech1, col_tech2 = st.columns(2)
                        
                        with col_tech1:
                            st.markdown("### 🏷️ Clasificación")
                            st.json(resultado["classification"], expanded=False)
                        
                        with col_tech2:
                            st.markdown("### ⚖️ Datos RAG")
                            st.metric("Documentos encontrados", len(resultado["rag_results"]))
                            st.metric("Tiempo respuesta", f"{resultado['tiempo_respuesta']}s")
                        
                        if resultado["dataset_json"]:
                            st.markdown("### 🗃️ Dataset estructurado")
                            st.json(resultado["dataset_json"], expanded=False)
                            
                            # Botón para ver JSON completo
                            if st.button("📋 Copiar JSON al portapapeles"):
                                st.code(json.dumps(resultado["dataset_json"], indent=2, ensure_ascii=False))
                    
                    # Agregar mensaje del asistente con metadata
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": resultado["texto_visible"],
                        "metadata": {
                            "classification": resultado["classification"],
                            "rag_count": len(resultado["rag_results"]),
                            "response_time": resultado["tiempo_respuesta"],
                            "has_dataset": resultado["dataset_json"] is not None
                        }
                    })
                    
                except Exception as e:
                    st.error(f"❌ Error procesando la consulta: {str(e)}")
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"Lo siento, hubo un error procesando tu consulta: {str(e)}"
                    })
    
    # Footer de la app
    st.markdown("---")
    
    col_footer1, col_footer2, col_footer3 = st.columns(3)
    
    with col_footer1:
        st.markdown("### 📚 Recursos")
        st.markdown("""
        - System Instructions
        - Datasets normativos
        - Reglamentos municipales
        - Directorio institucional
        """)
    
    with col_footer2:
        st.markdown("### ⚖️ Áreas de competencia")
        st.markdown("""
        - Construcción y obras
        - Comercio y giros
        - Medio ambiente
        - Espacio público
        - Protección civil
        """)
    
    with col_footer3:
        st.markdown("### 🛠️ Soporte")
        st.markdown("""
        - Manual de usuario
        - Preguntas frecuentes
        - Contacto técnico
        - Reportar problema
        """)
    
    st.caption("Sistema de Consulta Normativa Zapopan • Ayuntamiento de Zapopan, Jalisco • v1.0.0 • 2026")

# Función para tipos (añadida al final)
from typing import Dict, List, Any
