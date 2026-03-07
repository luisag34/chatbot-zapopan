"""
🏰 Panel de Administración SIMPLE - Sistema de Consulta Normativa Zapopan
Versión sin dependencias externas (sin plotly)
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json
import os
import sys

# Añadir ruta para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(
    page_title="Panel de Administración - Zapopan",
    page_icon="🏰",
    layout="wide"
)

# Verificar autenticación y permisos
if "autenticado" not in st.session_state or not st.session_state.autenticado:
    st.error("🔒 Acceso denegado. Debes iniciar sesión primero.")
    st.stop()

usuario_actual = st.session_state.usuario_actual

# Importar funciones de permisos desde app.py
try:
    from app import (
        es_administrador, 
        puede_gestionar_usuarios,
        USUARIOS_DB,
        ROLES_CONFIG,
        obtener_estadisticas_usuarios
    )
except:
    st.error("❌ Error cargando módulos de seguridad")
    st.stop()

# Verificar que el usuario sea administrador
if not es_administrador(usuario_actual):
    st.error("🚫 Acceso restringido. Solo administradores pueden acceder a este panel.")
    st.info(f"Tu usuario '{usuario_actual}' no tiene permisos de administrador.")
    st.stop()

# Obtener información del usuario actual
usuario_info = USUARIOS_DB.get(usuario_actual, {})
rol_nombre = ROLES_CONFIG.get(usuario_info.get('rol', ''), {}).get('nombre', 'N/A')

# Título principal
st.title("🏰 Panel de Administración - Sistema Normativo Zapopan")
st.markdown(f"**Administrador conectado:** `{usuario_actual}` | **Rol:** {rol_nombre}")
st.markdown("---")

# Pestañas principales
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Dashboard Ejecutivo", 
    "👥 Gestión de Usuarios", 
    "📈 Análisis de Uso", 
    "🔧 Configuración"
])

with tab1:
    st.header("📊 Dashboard Ejecutivo")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Total consultas
        try:
            with open("log_consultas.jsonl", "r", encoding="utf-8") as f:
                consultas = [json.loads(line) for line in f if line.strip()]
            total_consultas = len(consultas)
            st.metric("Total Consultas", total_consultas)
        except:
            st.metric("Total Consultas", 0)
    
    with col2:
        # Usuarios activos
        stats = obtener_estadisticas_usuarios()
        usuarios_activos = stats["usuarios_activos"]
        st.metric("Usuarios Activos", usuarios_activos)
    
    with col3:
        # Consultas hoy
        try:
            hoy = datetime.now().date()
            consultas_hoy = sum(1 for c in consultas if datetime.fromisoformat(c.get('timestamp', '')).date() == hoy)
            st.metric("Consultas Hoy", consultas_hoy)
        except:
            st.metric("Consultas Hoy", 0)
    
    with col4:
        # Tasa de uso
        try:
            tasa_uso = min(100, int((total_consultas / 100) * 100))  # Simplificado
            st.metric("Tasa de Uso", f"{tasa_uso}%")
        except:
            st.metric("Tasa de Uso", "0%")
    
    # Gráfico simple de consultas por día
    st.subheader("📅 Consultas por Día (Últimos 30 días)")
    try:
        if consultas:
            df_consultas = pd.DataFrame(consultas)
            if 'timestamp' in df_consultas.columns:
                df_consultas['fecha'] = pd.to_datetime(df_consultas['timestamp']).dt.date
                df_consultas['fecha'] = pd.to_datetime(df_consultas['fecha'])
                
                # Filtrar últimos 30 días
                fecha_limite = datetime.now() - timedelta(days=30)
                df_reciente = df_consultas[df_consultas['fecha'] >= fecha_limite]
                
                if not df_reciente.empty:
                    consultas_por_dia = df_reciente.groupby('fecha').size().reset_index(name='consultas')
                    
                    # Usar gráfico nativo de Streamlit
                    st.line_chart(consultas_por_dia.set_index('fecha')['consultas'])
                    
                    # Tabla de datos
                    with st.expander("📊 Ver datos detallados"):
                        st.dataframe(consultas_por_dia.sort_values('fecha', ascending=False))
                else:
                    st.info("No hay datos de consultas en los últimos 30 días")
            else:
                st.info("No hay datos de timestamp disponibles")
        else:
            st.info("No hay consultas registradas")
    except Exception as e:
        st.info(f"No hay datos suficientes para gráfico: {e}")

with tab2:
    st.header("👥 Gestión de Usuarios")
    
    # Mostrar tabla de usuarios
    st.subheader("Usuarios del Sistema")
    
    usuarios_lista = []
    for username, info in USUARIOS_DB.items():
        rol_nombre = ROLES_CONFIG.get(info.get('rol', ''), {}).get('nombre', info.get('rol', ''))
        usuarios_lista.append({
            "Usuario": username,
            "Nombre": info.get('nombre_completo', 'N/A'),
            "Email": info.get('email', 'N/A'),
            "Rol": rol_nombre,
            "Área": info.get('area', 'N/A'),
            "Estado": "✅ Activo" if info.get('estado') == 'activo' else "🚫 Bloqueado",
            "Consultas": info.get('consultas_realizadas', 0),
            "Creado": info.get('fecha_creacion', 'N/A'),
            "Último Acceso": info.get('ultimo_acceso', 'N/A')[:19] if info.get('ultimo_acceso') else "Nunca"
        })
    
    usuarios_df = pd.DataFrame(usuarios_lista)
    st.dataframe(usuarios_df, use_container_width=True, hide_index=True)
    
    # Estadísticas
    stats = obtener_estadisticas_usuarios()
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    with col_stat1:
        st.metric("Total Usuarios", stats["total_usuarios"])
    with col_stat2:
        st.metric("Usuarios Activos", stats["usuarios_activos"])
    with col_stat3:
        st.metric("Usuarios Bloqueados", stats["usuarios_bloqueados"])

with tab3:
    st.header("📈 Análisis de Uso")
    
    try:
        if consultas:
            # Análisis por categoría
            st.subheader("📋 Distribución por Categoría")
            categorias = [c.get('categoria_principal', 'Desconocida') for c in consultas]
            df_categorias = pd.DataFrame({'categoria': categorias})
            cat_counts = df_categorias['categoria'].value_counts().reset_index()
            cat_counts.columns = ['categoria', 'count']
            
            # Mostrar como tabla y bar chart
            col_cat1, col_cat2 = st.columns([2, 1])
            
            with col_cat1:
                st.bar_chart(cat_counts.set_index('categoria')['count'])
            
            with col_cat2:
                st.dataframe(cat_counts)
            
            # Análisis por dependencia
            st.subheader("🏢 Dependencias Más Consultadas")
            dependencias = [c.get('dependencia_responsable', 'Desconocida') for c in consultas]
            df_deps = pd.DataFrame({'dependencia': dependencias})
            dep_counts = df_deps['dependencia'].value_counts().head(10).reset_index()
            dep_counts.columns = ['dependencia', 'count']
            
            st.dataframe(dep_counts)
            
        else:
            st.info("No hay datos de consultas para análisis")
    except Exception as e:
        st.info(f"No hay datos suficientes para análisis: {e}")

with tab4:
    st.header("🔧 Configuración del Sistema")
    
    col_config1, col_config2 = st.columns(2)
    
    with col_config1:
        st.subheader("Configuración RAG")
        chunks_recuperar = st.slider("Número de chunks a recuperar", 1, 10, 3)
        umbral_relevancia = st.slider("Umbral de relevancia", 0.0, 1.0, 0.7)
        
        st.subheader("Configuración Gemini")
        temperatura = st.slider("Temperatura", 0.0, 1.0, 0.1, 0.1)
        max_tokens = st.slider("Tokens máximos", 100, 8000, 4000, 100)
        
        if st.button("💾 Guardar Configuración", type="primary"):
            st.success("Configuración guardada (simulación)")
            st.info(f"Temperatura: {temperatura} | Tokens: {max_tokens}")
    
    with col_config2:
        st.subheader("Sistema de Almacenamiento")
        almacenamiento = st.radio(
            "Modo de almacenamiento",
            ["Demo (CSV local)", "Google Sheets", "Base de datos"],
            index=0
        )
        
        st.subheader("Notificaciones")
        notify_risk = st.checkbox("Notificar consultas de riesgo", value=True)
        notify_anomaly = st.checkbox("Notificar uso anómalo", value=True)
        notify_email = st.text_input("Email para notificaciones", value="admin@zapopan.gob.mx")
        
        if st.button("🔄 Reiniciar Sistema", type="secondary"):
            st.warning("Reiniciando sistema... (simulación)")
            st.info("El sistema se reiniciará en 5 segundos")

# Footer
st.markdown("---")
st.caption(f"Panel de Administración • Sistema Normativo Zapopan • Usuario: {usuario_actual} • {datetime.now().strftime('%Y-%m-%d %H:%M')}")

# Nota de seguridad
if usuario_actual == "luis_admin":
    st.sidebar.warning("🏰 **Modo Administrador Supremo Activado**")
    st.sidebar.info("Tienes acceso completo a todas las funcionalidades del sistema.")