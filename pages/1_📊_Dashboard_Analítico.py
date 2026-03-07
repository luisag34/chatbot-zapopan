"""
Dashboard Analítico SIMPLE - Sistema de Consulta Normativa Zapopan
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
    page_title="Dashboard Analítico - Zapopan",
    page_icon="📊",
    layout="wide"
)

# Verificar autenticación
if "autenticado" not in st.session_state or not st.session_state.autenticado:
    st.error("🔒 Acceso denegado. Debes iniciar sesión primero.")
    st.stop()

st.title("📊 Dashboard Analítico - Sistema Normativo Zapopan")
st.markdown("---")

# Cargar datos de consultas
try:
    with open("log_consultas.jsonl", "r", encoding="utf-8") as f:
        consultas = [json.loads(line) for line in f if line.strip()]
    
    if not consultas:
        st.info("📭 No hay datos de consultas registradas aún.")
        st.stop()
    
    df = pd.DataFrame(consultas)
    
    # Convertir timestamp si existe
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    
except Exception as e:
    st.error(f"❌ Error cargando datos: {e}")
    st.info("El dashboard se activará cuando haya consultas registradas.")
    st.stop()

# Filtros
st.sidebar.header("🔍 Filtros")
if 'timestamp' in df.columns:
    fecha_min = df['timestamp'].min().date()
    fecha_max = df['timestamp'].max().date()
    
    fecha_inicio = st.sidebar.date_input(
        "Fecha inicio",
        value=fecha_min,
        min_value=fecha_min,
        max_value=fecha_max
    )
    
    fecha_fin = st.sidebar.date_input(
        "Fecha fin", 
        value=fecha_max,
        min_value=fecha_min,
        max_value=fecha_max
    )
    
    # Filtrar por fecha
    df['fecha'] = df['timestamp'].dt.date
    df_filtrado = df[(df['fecha'] >= fecha_inicio) & (df['fecha'] <= fecha_fin)]
else:
    df_filtrado = df

# Métricas principales
st.header("📈 Métricas Principales")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Consultas", len(df_filtrado))

with col2:
    if 'categoria_principal' in df_filtrado.columns:
        categorias_unicas = df_filtrado['categoria_principal'].nunique()
        st.metric("Categorías Únicas", categorias_unicas)
    else:
        st.metric("Categorías", "N/A")

with col3:
    if 'dependencia_responsable' in df_filtrado.columns:
        dependencias_unicas = df_filtrado['dependencia_responsable'].nunique()
        st.metric("Dependencias", dependencias_unicas)
    else:
        st.metric("Dependencias", "N/A")

with col4:
    if 'usuario_real' in df_filtrado.columns:
        usuarios_unicos = df_filtrado['usuario_real'].nunique()
        st.metric("Usuarios Activos", usuarios_unicos)
    else:
        st.metric("Usuarios", "N/A")

st.markdown("---")

# Pestañas
tab1, tab2, tab3 = st.tabs(["📅 Temporal", "📋 Categorías", "🏢 Dependencias"])

with tab1:
    st.subheader("📅 Consultas por Día")
    
    if 'timestamp' in df_filtrado.columns and not df_filtrado.empty:
        df_filtrado['fecha'] = df_filtrado['timestamp'].dt.date
        daily_counts = df_filtrado.groupby('fecha').size().reset_index(name='consultas')
        
        # Usar gráfico de línea nativo de Streamlit
        st.line_chart(daily_counts.set_index('fecha')['consultas'])
        
        # Tabla de datos
        with st.expander("📊 Ver datos detallados"):
            st.dataframe(daily_counts.sort_values('fecha', ascending=False))
    else:
        st.info("No hay datos temporales disponibles")

with tab2:
    st.subheader("📋 Distribución por Categoría")
    
    if 'categoria_principal' in df_filtrado.columns and not df_filtrado.empty:
        category_counts = df_filtrado['categoria_principal'].value_counts().reset_index()
        category_counts.columns = ['categoria', 'count']
        
        # Mostrar como tabla y bar chart simple
        col_chart, col_table = st.columns([2, 1])
        
        with col_chart:
            st.bar_chart(category_counts.set_index('categoria')['count'])
        
        with col_table:
            st.dataframe(category_counts)
        
        # Estadísticas
        st.metric("Categoría más consultada", category_counts.iloc[0]['categoria'] if not category_counts.empty else "N/A")
    else:
        st.info("No hay datos de categorías disponibles")

with tab3:
    st.subheader("🏢 Dependencias Más Consultadas")
    
    if 'dependencia_responsable' in df_filtrado.columns and not df_filtrado.empty:
        dep_counts = df_filtrado['dependencia_responsable'].value_counts().head(10).reset_index()
        dep_counts.columns = ['dependencia', 'count']
        
        # Mostrar como tabla
        st.dataframe(dep_counts)
        
        # Métricas
        col_met1, col_met2 = st.columns(2)
        with col_met1:
            st.metric("Dependencia principal", dep_counts.iloc[0]['dependencia'] if not dep_counts.empty else "N/A")
        with col_met2:
            st.metric("Consultas a principal", dep_counts.iloc[0]['count'] if not dep_counts.empty else 0)
    else:
        st.info("No hay datos de dependencias disponibles")

# Exportación de datos
st.markdown("---")
st.subheader("📤 Exportación de Datos")

col_exp1, col_exp2 = st.columns(2)

with col_exp1:
    if st.button("📥 Exportar a CSV", width='stretch'):
        csv = df_filtrado.to_csv(index=False)
        st.download_button(
            label="Descargar CSV",
            data=csv,
            file_name=f"consultas_zapopan_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

with col_exp2:
    if st.button("📥 Exportar a JSON", width='stretch'):
        json_data = df_filtrado.to_json(orient='records', force_ascii=False)
        st.download_button(
            label="Descargar JSON",
            data=json_data,
            file_name=f"consultas_zapopan_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json"
        )

# Footer
st.markdown("---")
st.caption(f"Dashboard Analítico • Sistema Normativo Zapopan • {datetime.now().strftime('%Y-%m-%d %H:%M')}")
st.caption("ℹ️ Versión simple sin dependencias externas")