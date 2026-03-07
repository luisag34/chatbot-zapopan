"""
Dashboard Analítico - Sistema de Consulta Normativa Zapopan
Visualización de métricas e indicadores
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json
import os
import sys

# Manejo de dependencias opcionales (plotly)
try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    st.warning("⚠️ Plotly no está instalado. Los gráficos estarán limitados.")

# Añadir ruta para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(
    page_title="Dashboard Analítico - Zapopan",
    page_icon="📊",
    layout="wide"
)

# Título
st.title("📊 Dashboard Analítico - Sistema de Consulta Normativa")
st.markdown("Visualización de métricas e indicadores del sistema")

# Sidebar para filtros
with st.sidebar:
    st.header("🔍 Filtros")
    
    # Rango de fechas
    st.subheader("Rango de fechas")
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Desde", value=datetime.now() - timedelta(days=30))
    with col2:
        end_date = st.date_input("Hasta", value=datetime.now())
    
    # Categorías
    st.subheader("Categorías")
    show_all_categories = st.checkbox("Mostrar todas las categorías", value=True)
    
    if not show_all_categories:
        categories = st.multiselect(
            "Seleccionar categorías",
            ["construccion", "comercio", "tecnica_medio_ambiente", "espacio_publico", "general"],
            default=["comercio", "construccion"]
        )
    else:
        categories = None
    
    # Actualizar datos
    st.subheader("Actualización")
    if st.button("🔄 Actualizar dashboard", type="primary"):
        st.rerun()

# Función para cargar datos
@st.cache_data(ttl=300)  # Cache por 5 minutos
def load_consultation_data():
    """Cargar datos de consultas desde archivo local o Google Sheets"""
    data = []
    
    # Intentar cargar desde archivo local
    try:
        with open("log_consultas.jsonl", "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    data.append(json.loads(line))
    except FileNotFoundError:
        st.info("📁 No hay datos de consultas disponibles aún")
        return pd.DataFrame()
    
    # Convertir a DataFrame
    if data:
        df = pd.DataFrame(data)
        
        # Convertir timestamp a datetime
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        
        return df
    else:
        return pd.DataFrame()

# Cargar datos
df = load_consultation_data()

if df.empty:
    st.warning("No hay datos disponibles para mostrar. Realiza algunas consultas primero.")
    st.stop()

# Aplicar filtros
if 'timestamp' in df.columns:
    mask = (df['timestamp'].dt.date >= start_date) & (df['timestamp'].dt.date <= end_date)
    df_filtered = df[mask].copy()
else:
    df_filtered = df.copy()

if categories and 'categoria_principal' in df_filtered.columns:
    df_filtered = df_filtered[df_filtered['categoria_principal'].isin(categories)]

# Métricas principales
st.header("📈 Métricas Principales")

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_consultas = len(df_filtered)
    st.metric("Total Consultas", total_consultas)

with col2:
    if 'categoria_principal' in df_filtered.columns and not df_filtered.empty:
        top_category = df_filtered['categoria_principal'].mode()
        top_category_value = top_category[0] if not top_category.empty else "N/A"
        st.metric("Categoría Principal", top_category_value)
    else:
        st.metric("Categoría Principal", "N/A")

with col3:
    if 'dependencia_responsable' in df_filtered.columns and not df_filtered.empty:
        top_dependency = df_filtered['dependencia_responsable'].mode()
        top_dependency_value = top_dependency[0] if not top_dependency.empty else "N/A"
        st.metric("Dependencia Principal", top_dependency_value)
    else:
        st.metric("Dependencia Principal", "N/A")

with col4:
    if 'clasificacion_riesgo' in df_filtered.columns and not df_filtered.empty:
        risk_cases = len(df_filtered[df_filtered['clasificacion_riesgo'] == 'riesgo_inmediato'])
        st.metric("Casos de Riesgo", risk_cases)
    else:
        st.metric("Casos de Riesgo", 0)

# Gráficos
st.header("📊 Visualizaciones")

tab1, tab2, tab3, tab4 = st.tabs(["📅 Temporal", "🏷️ Categorías", "⚖️ Institucional", "⚠️ Riesgo"])

with tab1:
    # Gráfico temporal
    if 'timestamp' in df_filtered.columns and not df_filtered.empty:
        df_filtered['fecha'] = df_filtered['timestamp'].dt.date
        daily_counts = df_filtered.groupby('fecha').size().reset_index(name='consultas')
        
        if PLOTLY_AVAILABLE:
            fig_temporal = px.line(
                daily_counts,
                x='fecha',
                y='consultas',
                title='Consultas por Día',
                markers=True
            )
            fig_temporal.update_layout(
                xaxis_title="Fecha",
                yaxis_title="Número de Consultas",
                hovermode='x unified'
            )
            st.plotly_chart(fig_temporal, use_container_width=True)
        else:
            # Alternativa sin plotly
            st.line_chart(daily_counts.set_index('fecha')['consultas'])
    else:
        st.info("No hay datos temporales disponibles")

with tab2:
    # Gráfico de categorías
    if 'categoria_principal' in df_filtered.columns and not df_filtered.empty:
        category_counts = df_filtered['categoria_principal'].value_counts().reset_index()
        category_counts.columns = ['categoria', 'count']
        
        fig_categories = px.pie(
            category_counts,
            values='count',
            names='categoria',
            title='Distribución por Categoría Principal',
            hole=0.3
        )
        st.plotly_chart(fig_categories, use_container_width=True)
        
        # Tabla de categorías
        with st.expander("Ver detalles por categoría"):
            st.dataframe(
                category_counts.sort_values('count', ascending=False),
                use_container_width=True
            )
    else:
        st.info("No hay datos de categorías disponibles")

with tab3:
    # Gráfico institucional
    if 'dependencia_responsable' in df_filtered.columns and not df_filtered.empty:
        dependency_counts = df_filtered['dependencia_responsable'].value_counts().reset_index()
        dependency_counts.columns = ['dependencia', 'count']
        
        # Limitar a top 10 para mejor visualización
        top_dependencies = dependency_counts.head(10)
        
        fig_dependencies = px.bar(
            top_dependencies,
            x='count',
            y='dependencia',
            title='Top 10 Dependencias Responsables',
            orientation='h'
        )
        fig_dependencies.update_layout(
            yaxis={'categoryorder': 'total ascending'},
            xaxis_title="Número de Consultas",
            yaxis_title="Dependencia"
        )
        st.plotly_chart(fig_dependencies, use_container_width=True)
    else:
        st.info("No hay datos institucionales disponibles")

with tab4:
    # Gráfico de riesgo
    if 'clasificacion_riesgo' in df_filtered.columns and not df_filtered.empty:
        risk_counts = df_filtered['clasificacion_riesgo'].value_counts().reset_index()
        risk_counts.columns = ['riesgo', 'count']
        
        # Mapear nombres más amigables
        risk_mapping = {
            'sin_riesgo': 'Sin Riesgo',
            'riesgo_potencial': 'Riesgo Potencial',
            'riesgo_inmediato': 'Riesgo Inmediato'
        }
        risk_counts['riesgo_label'] = risk_counts['riesgo'].map(risk_mapping)
        risk_counts['riesgo_label'] = risk_counts['riesgo_label'].fillna(risk_counts['riesgo'])
        
        fig_risk = px.bar(
            risk_counts,
            x='riesgo_label',
            y='count',
            title='Distribución por Nivel de Riesgo',
            color='riesgo_label',
            color_discrete_map={
                'Sin Riesgo': '#2E8B57',
                'Riesgo Potencial': '#FFA500',
                'Riesgo Inmediato': '#FF4500'
            }
        )
        fig_risk.update_layout(
            xaxis_title="Nivel de Riesgo",
            yaxis_title="Número de Consultas",
            showlegend=False
        )
        st.plotly_chart(fig_risk, use_container_width=True)
        
        # Mostrar casos de riesgo inmediato
        if 'riesgo_inmediato' in df_filtered['clasificacion_riesgo'].values:
            risk_cases = df_filtered[df_filtered['clasificacion_riesgo'] == 'riesgo_inmediato']
            with st.expander("📋 Ver casos de riesgo inmediato"):
                st.dataframe(
                    risk_cases[['timestamp', 'descripcion_usuario', 'dependencia_responsable']].head(10),
                    use_container_width=True
                )
    else:
        st.info("No hay datos de riesgo disponibles")

# Tabla de datos detallada
st.header("📋 Datos Detallados")

with st.expander("Ver todas las consultas"):
    # Seleccionar columnas para mostrar
    display_columns = [
        'timestamp', 'consulta_id', 'categoria_principal',
        'dependencia_responsable', 'clasificacion_riesgo',
        'tipo_consulta', 'descripcion_usuario'
    ]
    
    # Filtrar columnas disponibles
    available_columns = [col for col in display_columns if col in df_filtered.columns]
    
    if available_columns:
        st.dataframe(
            df_filtered[available_columns].sort_values('timestamp', ascending=False),
            use_container_width=True
        )
    else:
        st.info("No hay columnas disponibles para mostrar")

# Exportar datos
st.header("📥 Exportar Datos")

col_exp1, col_exp2, col_exp3 = st.columns(3)

with col_exp1:
    if st.button("📄 Exportar a CSV"):
        csv = df_filtered.to_csv(index=False, encoding='utf-8')
        st.download_button(
            label="Descargar CSV",
            data=csv,
            file_name=f"consultas_zapopan_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv"
        )

with col_exp2:
    if st.button("📊 Exportar a JSON"):
        json_data = df_filtered.to_json(orient='records', force_ascii=False)
        st.download_button(
            label="Descargar JSON",
            data=json_data,
            file_name=f"consultas_zapopan_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
            mime="application/json"
        )

with col_exp3:
    if st.button("🖨️ Generar Reporte"):
        st.info("""
        **Reporte Generado:**
        
        - Período: {start_date} a {end_date}
        - Total consultas: {total_consultas}
        - Categoría principal: {top_category_value}
        - Dependencia principal: {top_dependency_value}
        - Casos de riesgo: {risk_cases}
        
        *Este es un reporte básico. Para reportes avanzados, contacta al administrador.*
        """.format(
            start_date=start_date,
            end_date=end_date,
            total_consultas=total_consultas,
            top_category_value=top_category_value if 'top_category_value' in locals() else "N/A",
            top_dependency_value=top_dependency_value if 'top_dependency_value' in locals() else "N/A",
            risk_cases=risk_cases if 'risk_cases' in locals() else 0
        ))

# Footer
st.markdown("---")
st.caption("Dashboard Analítico • Sistema de Consulta Normativa Zapopan • v1.0.0 • Actualizado: " + datetime.now().strftime("%Y-%m-%d %H:%M"))