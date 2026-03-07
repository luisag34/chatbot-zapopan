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

# --- CONFIGURACIÓN DE SEGURIDAD ---
USUARIOS_AUTORIZADOS = {
    "admin_zapopan": "Inspeccion2025",
    "inspector_01": "Zapopan01",
    "inspector_02": "Zapopan02",
    "demo": "demo123"  # Usuario de demostración
}

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
        st.success(f"✅ Conectado como: **{st.session_state.usuario_actual}**")
        
        st.markdown("### 📊 Estadísticas")
        if "total_consultas" in st.session_state:
            st.metric("Consultas realizadas", st.session_state.total_consultas)
        
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
        
        **Credenciales de demostración:**  
        👤 Usuario: `demo`  
        🔑 Contraseña: `demo123`
        """)
        
        st.markdown("---")
        
        user = st.text_input("👤 Usuario", key="login_user")
        password = st.text_input("🔑 Contraseña", type="password", key="login_pass")
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🚪 Ingresar", type="primary", use_container_width=True):
                if user in USUARIOS_AUTORIZADOS and USUARIOS_AUTORIZADOS[user] == password:
                    st.session_state.autenticado = True
                    st.session_state.usuario_actual = user
                    st.session_state.messages = []
                    st.session_state.total_consultas = 0
                    st.rerun()
                else:
                    st.error("❌ Credenciales incorrectas")
        
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
