"""
Dashboard SIMPLE - Sistema de Consulta Normativa Zapopan
Versión ultra-minimal sin dependencias
"""

import streamlit as st
import json
from datetime import datetime

st.set_page_config(
    page_title="Dashboard - Zapopan",
    page_icon="📊",
    layout="wide"
)

# Verificar autenticación
if "autenticado" not in st.session_state or not st.session_state.autenticado:
    st.error("🔒 Acceso denegado. Debes iniciar sesión primero.")
    st.stop()

st.title("📊 Dashboard Analítico")
st.markdown("---")

# Cargar datos
try:
    with open("consultas_local.jsonl", "r", encoding="utf-8") as f:
        consultas = [json.loads(line) for line in f if line.strip()]
    
    if not consultas:
        st.info("📭 No hay consultas registradas aún.")
        st.stop()
    
except Exception as e:
    st.error(f"❌ Error cargando datos: {e}")
    st.info("El dashboard se activará cuando haya consultas registradas.")
    st.stop()

# Métricas principales
st.header("📈 Métricas Principales")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Consultas", len(consultas))

with col2:
    usuarios_unicos = len(set(c.get("usuario", "") for c in consultas))
    st.metric("Usuarios Únicos", usuarios_unicos)

with col3:
    # Consultas hoy
    hoy = datetime.now().date().isoformat()
    consultas_hoy = sum(1 for c in consultas if c.get("timestamp", "").startswith(hoy))
    st.metric("Consultas Hoy", consultas_hoy)

st.markdown("---")

# Análisis básico
st.header("📋 Análisis de Consultas")

# Por usuario
st.subheader("👥 Consultas por Usuario")
usuarios_counts = {}
for consulta in consultas:
    usuario = consulta.get("usuario", "Desconocido")
    usuarios_counts[usuario] = usuarios_counts.get(usuario, 0) + 1

for usuario, count in sorted(usuarios_counts.items(), key=lambda x: x[1], reverse=True):
    st.write(f"**{usuario}:** {count} consultas")

# Por dependencia
st.subheader("🏢 Dependencias Consultadas")
dependencias_counts = {}
for consulta in consultas:
    deps = consulta.get("dependencias", [])
    for dep in deps:
        dependencias_counts[dep] = dependencias_counts.get(dep, 0) + 1

if dependencias_counts:
    for dep, count in sorted(dependencias_counts.items(), key=lambda x: x[1], reverse=True):
        st.write(f"**{dep}:** {count} referencias")
else:
    st.info("No hay datos de dependencias")

# Timeline simple
st.subheader("📅 Últimas Consultas")
st.write("**Últimas 10 consultas:**")

for i, consulta in enumerate(consultas[-10:][::-1], 1):
    timestamp = consulta.get("timestamp", "")[:16]
    usuario = consulta.get("usuario", "")
    consulta_texto = consulta.get("consulta", "")[:50] + "..." if len(consulta.get("consulta", "")) > 50 else consulta.get("consulta", "")
    
    st.write(f"{i}. **{timestamp}** - *{usuario}*: {consulta_texto}")

# Exportación
st.markdown("---")
st.subheader("📤 Exportar Datos")

if st.button("📥 Exportar a JSON", width='stretch'):
    json_data = json.dumps(consultas, indent=2, ensure_ascii=False)
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