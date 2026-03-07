"""
🏰 Panel de Administración - Sistema de Consulta Normativa Zapopan
Panel avanzado solo para administradores con funcionalidades completas
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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
        obtener_estadisticas_usuarios,
        obtener_usuarios_por_rol,
        obtener_usuarios_por_area
    )
except:
    st.error("❌ Error cargando módulos de seguridad")
    st.stop()

# Verificar que el usuario sea administrador
if not es_administrador(usuario_actual):
    st.error("🚫 Acceso restringido. Solo administradores pueden acceder a este panel.")
    st.info(f"Tu usuario '{usuario_actual}' no tiene permisos de administrador.")
    st.stop()

# Título principal
st.title("🏰 Panel de Administración - Sistema Normativo Zapopan")
# Obtener información del usuario actual
usuario_info = USUARIOS_DB.get(usuario_actual, {})
rol_nombre = ROLES_CONFIG.get(usuario_info.get('rol', ''), {}).get('nombre', 'N/A')

st.markdown(f"**Administrador conectado:** `{usuario_actual}` | **Rol:** {rol_nombre}")
st.markdown("---")

# Pestañas principales
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Dashboard Ejecutivo", 
    "👥 Gestión de Usuarios", 
    "📈 Análisis de Uso", 
    "🔧 Configuración", 
    "🔒 Seguridad"
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
    
    # Gráfico de consultas por día
    st.subheader("📅 Consultas por Día (Últimos 30 días)")
    try:
        df_consultas = pd.DataFrame(consultas)
        if 'timestamp' in df_consultas.columns:
            df_consultas['fecha'] = pd.to_datetime(df_consultas['timestamp']).dt.date
            df_consultas['fecha'] = pd.to_datetime(df_consultas['fecha'])
            
            # Filtrar últimos 30 días
            fecha_limite = datetime.now() - timedelta(days=30)
            df_reciente = df_consultas[df_consultas['fecha'] >= fecha_limite]
            
            if not df_reciente.empty:
                consultas_por_dia = df_reciente.groupby('fecha').size().reset_index(name='consultas')
                
                fig = px.line(
                    consultas_por_dia,
                    x='fecha',
                    y='consultas',
                    title='Consultas por Día',
                    markers=True
                )
                fig.update_layout(
                    xaxis_title="Fecha",
                    yaxis_title="Número de Consultas",
                    hovermode='x unified'
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No hay datos de consultas en los últimos 30 días")
        else:
            st.info("No hay datos de timestamp disponibles")
    except Exception as e:
        st.info(f"No hay datos suficientes para gráfico: {e}")

with tab2:
    st.header("👥 Gestión de Usuarios")
    
    # Mostrar tabla de usuarios
    st.subheader("Usuarios del Sistema")
    
    # Crear DataFrame con información de usuarios
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
    
    # Solo el administrador supremo puede gestionar usuarios
    if usuario_actual == "luis_admin":
        st.subheader("🔧 Gestión Avanzada de Usuarios")
        
        col_add, col_edit, col_del = st.columns(3)
        
        with col_add:
            with st.expander("➕ Agregar Nuevo Usuario"):
                nuevo_usuario = st.text_input("Nombre de usuario")
                nuevo_nombre = st.text_input("Nombre completo")
                nuevo_rol = st.selectbox("Rol", ["inspector", "administrador", "demo"])
                nueva_pass = st.text_input("Contraseña", type="password")
                
                if st.button("Crear Usuario", type="primary"):
                    if nuevo_usuario and nueva_pass:
                        st.success(f"Usuario '{nuevo_usuario}' creado (simulación)")
                        st.info("En producción, esto actualizaría la base de datos")
                    else:
                        st.error("Completa todos los campos")
        
        with col_edit:
            with st.expander("✏️ Editar Usuario"):
                usuario_editar = st.selectbox("Seleccionar usuario", list(USUARIOS_DB.keys()))
                if usuario_editar:
                    st.info(f"Editando: {usuario_editar}")
                    nueva_pass_edit = st.text_input("Nueva contraseña", type="password")
                    if st.button("Actualizar Contraseña"):
                        st.success(f"Contraseña actualizada para '{usuario_editar}' (simulación)")
        
        with col_del:
            with st.expander("🗑️ Eliminar Usuario"):
                usuario_eliminar = st.selectbox("Usuario a eliminar", 
                                               [u for u in USUARIOS_DB.keys() if u != "luis_admin"])
                if usuario_eliminar:
                    st.warning(f"⚠️ Eliminar usuario: {usuario_eliminar}")
                    confirmar = st.checkbox("Confirmar eliminación")
                    if confirmar and st.button("Eliminar Usuario", type="secondary"):
                        st.error(f"Usuario '{usuario_eliminar}' eliminado (simulación)")
                        st.info("En producción, esto eliminaría el usuario permanentemente")
    else:
        st.info("ℹ️ Solo el Administrador Supremo puede gestionar usuarios.")

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
            
            fig_cat = px.pie(
                cat_counts,
                values='count',
                names='categoria',
                title='Consultas por Categoría Principal',
                hole=0.3
            )
            st.plotly_chart(fig_cat, use_container_width=True)
            
            # Análisis por dependencia
            st.subheader("🏢 Dependencias Más Consultadas")
            dependencias = [c.get('dependencia_responsable', 'Desconocida') for c in consultas]
            df_deps = pd.DataFrame({'dependencia': dependencias})
            dep_counts = df_deps['dependencia'].value_counts().head(10).reset_index()
            dep_counts.columns = ['dependencia', 'count']
            
            fig_deps = px.bar(
                dep_counts,
                x='count',
                y='dependencia',
                title='Top 10 Dependencias',
                orientation='h'
            )
            fig_deps.update_layout(yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig_deps, use_container_width=True)
            
            # Análisis temporal detallado
            st.subheader("🕒 Patrones de Uso")
            if 'timestamp' in df_consultas.columns:
                df_consultas['hora'] = pd.to_datetime(df_consultas['timestamp']).dt.hour
                horas_counts = df_consultas['hora'].value_counts().sort_index().reset_index()
                horas_counts.columns = ['hora', 'consultas']
                
                fig_horas = px.bar(
                    horas_counts,
                    x='hora',
                    y='consultas',
                    title='Consultas por Hora del Día',
                    labels={'hora': 'Hora', 'consultas': 'Número de Consultas'}
                )
                st.plotly_chart(fig_horas, use_container_width=True)
        else:
            st.info("No hay datos de consultas para análisis")
    except Exception as e:
        st.info(f"No hay datos suficientes para análisis: {e}")

with tab4:
    st.header("🔧 Configuración del Sistema")
    
    col_config1, col_config2 = st.columns(2)
    
    with col_config1:
        st.subheader("Configuración RAG")
        st.slider("Número de chunks a recuperar", 1, 10, 3, key="rag_chunks")
        st.slider("Umbral de relevancia", 0.0, 1.0, 0.7, key="rag_threshold")
        
        st.subheader("Configuración Gemini")
        temperatura = st.slider("Temperatura", 0.0, 1.0, 0.1, 0.1, key="gemini_temp")
        max_tokens = st.slider("Tokens máximos", 100, 8000, 4000, 100, key="gemini_tokens")
        
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
        
        if almacenamiento == "Google Sheets":
            st.text_input("Spreadsheet ID", key="sheets_id")
            st.text_area("Credenciales JSON", key="sheets_creds", height=100)
        
        st.subheader("Notificaciones")
        st.checkbox("Notificar consultas de riesgo", value=True, key="notify_risk")
        st.checkbox("Notificar uso anómalo", value=True, key="notify_anomaly")
        st.text_input("Email para notificaciones", key="notify_email")
        
        if st.button("🔄 Reiniciar Sistema", type="secondary"):
            st.warning("Reiniciando sistema... (simulación)")
            st.info("El sistema se reiniciará en 5 segundos")

with tab5:
    st.header("🔒 Seguridad y Auditoría")
    
    st.subheader("Registro de Auditoría")
    try:
        # Mostrar últimas consultas como registro
        if consultas:
            audit_df = pd.DataFrame(consultas[-20:])  # Últimas 20 consultas
            if 'timestamp' in audit_df.columns and 'usuario_real' in audit_df.columns:
                display_cols = ['timestamp', 'usuario_real', 'categoria_principal', 'dependencia_responsable']
                display_cols = [c for c in display_cols if c in audit_df.columns]
                
                st.dataframe(
                    audit_df[display_cols].sort_values('timestamp', ascending=False),
                    use_container_width=True
                )
            else:
                st.info("No hay datos de auditoría completos")
        else:
            st.info("No hay registros de auditoría")
    except:
        st.info("No hay registros de auditoría disponibles")
    
    st.subheader("Reportes de Seguridad")
    col_rep1, col_rep2 = st.columns(2)
    
    with col_rep1:
        if st.button("📋 Generar Reporte Diario", use_container_width=True):
            st.success("Reporte diario generado (simulación)")
            st.download_button(
                "Descargar Reporte",
                data="Reporte de seguridad - Simulación",
                file_name=f"reporte_seguridad_{datetime.now().strftime('%Y%m%d')}.txt"
            )
    
    with col_rep2:
        if st.button("🔍 Auditoría Completa", use_container_width=True):
            st.success("Auditoría completada (simulación)")
            st.info("No se encontraron vulnerabilidades críticas")
    
    # Solo para administrador supremo
    if usuario_actual == "luis_admin":
        st.subheader("🚨 Acciones Críticas de Seguridad")
        
        with st.expander("Rotación de Credenciales", icon="🔄"):
            st.warning("Esta acción desactivará todas las API Keys actuales")
            if st.button("🔄 Rotar Todas las API Keys", type="secondary"):
                st.error("⚠️ Acción crítica - Requiere confirmación adicional")
                confirm = st.checkbox("Confirmo que quiero rotar todas las API Keys")
                if confirm:
                    st.success("API Keys rotadas (simulación)")
        
        with st.expander("Exportar Todos los Datos", icon="💾"):
            st.info("Exporta todos los datos del sistema para backup")
            if st.button("📦 Exportar Backup Completo", type="primary"):
                st.success("Backup generado (simulación)")
                st.download_button(
                    "Descargar Backup",
                    data="Backup completo del sistema - Simulación",
                    file_name=f"backup_zapopan_{datetime.now().strftime('%Y%m%d_%H%M')}.zip"
                )

# Footer
st.markdown("---")
st.caption(f"Panel de Administración • Sistema Normativo Zapopan • Usuario: {usuario_actual} • {datetime.now().strftime('%Y-%m-%d %H:%M')}")

# Nota de seguridad
if usuario_actual == "luis_admin":
    st.sidebar.warning("🏰 **Modo Administrador Supremo Activado**")
    st.sidebar.info("Tienes acceso completo a todas las funcionalidades del sistema.")