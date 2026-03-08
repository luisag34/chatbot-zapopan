"""
SISTEMA DE CONSULTA DE LA DIRECCIÓN DE INSPECCIÓN Y VIGILANCIA
Versión profesional 2026 con sistema de diseño institucional moderno
"""

import streamlit as st
import json
from datetime import datetime
from sistema_local_protocolo_completo import procesar_consulta_local_protocolo_completo


    # ========================================================================
    # ANALYTICS BÁSICO (uso interno)
    # ========================================================================
    
    # Inicializar contadores si no existen
    if "contador_consultas" not in st.session_state:
        st.session_state.contador_consultas = 0
        st.session_state.consultas_por_usuario = {}
        st.session_state.ultima_consulta_hora = None
    
    # Función para registrar consulta
    def registrar_consulta_analytics(usuario, consulta):
        """Registrar métricas básicas de uso"""
        try:
            st.session_state.contador_consultas += 1
            
            if usuario not in st.session_state.consultas_por_usuario:
                st.session_state.consultas_por_usuario[usuario] = 0
            st.session_state.consultas_por_usuario[usuario] += 1
            
            st.session_state.ultima_consulta_hora = datetime.now().isoformat()
            
            # Solo admin puede ver analytics
            if st.session_state.rol == "administrador_supremo":
                with st.sidebar.expander("📊 Analytics (Admin)"):
                    st.metric("Consultas totales", st.session_state.contador_consultas)
                    if st.session_state.consultas_por_usuario:
                        st.write("Consultas por usuario:")
                        for user, count in st.session_state.consultas_por_usuario.items():
                            st.write(f"  • {user}: {count}")
                    if st.session_state.ultima_consulta_hora:
                        st.caption(f"Última consulta: {st.session_state.ultima_consulta_hora[:19]}")
        except:
            pass  # Analytics no debe romper la aplicación
    
    # ============================================================================
# CONFIGURACIÓN
# ============================================================================

st.set_page_config(
    page_title="Sistema de Consulta - Dirección de Inspección y Vigilancia",
    page_icon="🏛️",
    layout="wide"
, layout="wide", initial_sidebar_state="expanded", menu_items=None)

# ============================================================================
# SISTEMA DE DISEÑO 2026
# ============================================================================

st.markdown("""
<style> /* CSS OPTIMIZADO CON CONTRASTE MEJORADO PARA MÓVIL - SISTEMA DE DISEÑO 2026 */

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
  /* COLORES INSTITUCIONALES 2026 - CONTRASTE MEJORADO */
  --color-fondo: #0A1129;           /* Más oscuro para mejor contraste */
  --color-surface: #1A2339;         /* Superficie más clara vs fondo */
  --color-primary: #3B82F6;
  --color-primary-hover: #2563EB;
  --color-gobierno: #1D4ED8;
  --color-institucional: #0369A1;
  --color-accent: #10B981;
  --color-alerta: #EF4444;
  --color-advertencia: #F59E0B;
  
  /* ESCALA DE GRISES 2026 - CONTRASTE OPTIMIZADO */
  --gray-50: #FFFFFF;               /* Blanco puro para máximo contraste */
  --gray-100: #F8FAFC;              /* Casi blanco */
  --gray-200: #F1F5F9;              /* Texto principal - alto contraste */
  --gray-300: #E2E8F0;              /* Texto secundario */
  --gray-400: #CBD5E1;              /* Texto terciario */
  --gray-500: #94A3B8;              /* Placeholders, íconos */
  --gray-600: #64748B;              /* Bordes, separadores */
  --gray-700: #475569;              /* Superficies oscuras */
  --gray-800: #334155;              /* Fondo elementos */
  --gray-900: #1E293B;              /* Fondo principal */
  
  /* COLORES DE TEXTO ESPECÍFICOS PARA ALTO CONTRASTE */
  --text-primary: #FFFFFF;          /* Texto principal - blanco puro */
  --text-secondary: #E2E8F0;        /* Texto secundario */
  --text-muted: #94A3B8;            /* Texto menos importante */
  --text-on-primary: #FFFFFF;       /* Texto sobre botones primarios */
  
  /* GRADIENTES */
  --gradient-primary: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%);
  --gradient-success: linear-gradient(135deg, #10B981 0%, #34D399 100%);
  
  /* TIPOGRAFÍA FLUID */
  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
  --text-xs: clamp(0.75rem, 0.7rem + 0.25vw, 0.875rem);
  --text-sm: clamp(0.875rem, 0.825rem + 0.25vw, 1rem);
  --text-base: clamp(1rem, 0.95rem + 0.25vw, 1.125rem);
  --text-lg: clamp(1.125rem, 1.05rem + 0.375vw, 1.25rem);
  --text-xl: clamp(1.25rem, 1.15rem + 0.5vw, 1.5rem);
  --text-2xl: clamp(1.5rem, 1.35rem + 0.75vw, 1.875rem);
  --text-3xl: clamp(1.875rem, 1.65rem + 1.125vw, 2.25rem);
  
  /* ESPACIADO 4PX GRID */
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-3: 0.75rem;
  --space-4: 1rem;
  --space-5: 1.25rem;
  --space-6: 1.5rem;
  --space-8: 2rem;
  --space-10: 2.5rem;
  
  /* BORDER RADIUS */
  --radius-sm: 0.375rem;
  --radius-md: 0.5rem;
  --radius-lg: 0.75rem;
  --radius-xl: 1rem;
  
  /* SOMBRAS */
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  --shadow-primary: 0 10px 15px -3px rgba(59, 130, 246, 0.3), 0 4px 6px -2px rgba(59, 130, 246, 0.1);
  
  /* TRANSICIONES */
  --transition-base: 300ms cubic-bezier(0.4, 0, 0.2, 1);
}

/* ============================================================================
   RESET Y BASE - CONTRASTE MEJORADO
   ============================================================================ */
* { margin: 0; padding: 0; box-sizing: border-box; }

body { 
  font-family: var(--font-sans); 
  background: var(--color-fondo); 
  color: var(--text-primary); /* BLANCO PURO para máximo contraste */
  min-height: 100vh;
  line-height: 1.6;
}

/* Mejorar contraste de todos los textos Streamlit por defecto */
.stMarkdown, .stText, .stCaption, .stCode {
  color: var(--text-primary) !important;
}

/* ============================================================================
   TÍTULOS CON ALTO CONTRASTE
   ============================================================================ */
h1, .stMarkdown h1 { 
  font-size: var(--text-3xl); 
  font-weight: 700; 
  background: var(--gradient-primary); 
  -webkit-background-clip: text; 
  -webkit-text-fill-color: transparent; 
  background-clip: text; 
  margin-bottom: var(--space-4); 
  line-height: 1.2;
}

h2, .stMarkdown h2 { 
  font-size: var(--text-2xl); 
  color: var(--text-primary) !important; /* BLANCO para alto contraste */
  margin-bottom: var(--space-4); 
  font-weight: 600;
  line-height: 1.3;
}

h3, .stMarkdown h3 { 
  font-size: var(--text-xl); 
  color: var(--text-primary) !important; /* BLANCO para alto contraste */
  margin-bottom: var(--space-4); 
  font-weight: 600;
  line-height: 1.4;
}

/* Texto normal en Streamlit */
.stMarkdown p, .stMarkdown li, .stMarkdown div {
  color: var(--text-primary) !important;
  line-height: 1.6;
}

/* ============================================================================
   BOTONES STREAMLIT - CONTRASTE MEJORADO
   ============================================================================ */
.stButton > button {
  border-radius: var(--radius-lg) !important;
  border: none !important;
  font-family: var(--font-sans) !important;
  font-weight: 600 !important;
  font-size: var(--text-sm) !important;
  padding: var(--space-3) var(--space-6) !important;
  transition: all var(--transition-base) !important;
  min-height: 44px !important; /* Touch target mínimo para móvil */
  color: var(--text-on-primary) !important; /* Texto blanco en botones */
}

/* Botón primario - alto contraste */
.stButton > button[data-testid="baseButton-primary"] {
  background: var(--gradient-primary) !important;
  color: var(--text-on-primary) !important; /* Blanco garantizado */
  font-weight: 700 !important;
}

.stButton > button[data-testid="baseButton-primary"]:hover {
  transform: translateY(-2px) !important;
  box-shadow: var(--shadow-primary) !important;
  filter: brightness(1.1) !important; /* Efecto hover visible */
}

/* Botón secundario - mejor contraste */
.stButton > button[data-testid="baseButton-secondary"] {
  background: var(--color-surface) !important;
  color: var(--text-primary) !important; /* Blanco para contraste */
  border: 2px solid var(--gray-600) !important; /* Borde más visible */
  font-weight: 600 !important;
}

.stButton > button[data-testid="baseButton-secondary"]:hover {
  background: var(--gray-800) !important;
  border-color: var(--color-primary) !important; /* Borde azul en hover */
  transform: translateY(-2px) !important;
  color: var(--text-primary) !important;
}

/* ============================================================================
   INPUTS STREAMLIT - CONTRASTE MEJORADO
   ============================================================================ */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
  background: var(--color-surface) !important;
  border: 2px solid var(--gray-600) !important; /* Borde más visible */
  border-radius: var(--radius-lg) !important;
  color: var(--text-primary) !important; /* Texto blanco */
  padding: var(--space-3) var(--space-4) !important;
  font-family: var(--font-sans) !important;
  font-size: var(--text-base) !important;
  transition: all var(--transition-base) !important;
}

/* Placeholders con mejor contraste */
.stTextInput > div > div > input::placeholder,
.stTextArea > div > div > textarea::placeholder {
  color: var(--text-muted) !important; /* Gris visible pero diferenciado */
  opacity: 0.8 !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
  border-color: var(--color-primary) !important;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.3) !important; /* Sombra más visible */
  outline: none !important;
  background: var(--gray-900) !important; /* Fondo más oscuro en focus */
}

/* ============================================================================
   CONTAINERS Y CARDS - CONTRASTE MEJORADO
   ============================================================================ */
.stContainer, .stExpander, div[data-testid="stVerticalBlock"] > div {
  background: rgba(26, 35, 57, 0.9) !important; /* Más opaco para mejor contraste */
  backdrop-filter: blur(10px);
  border-radius: var(--radius-xl) !important;
  border: 1px solid var(--gray-700) !important; /* Borde más visible */
  padding: var(--space-6) !important;
  margin-bottom: var(--space-4) !important;
  transition: all var(--transition-base) !important;
}

.stContainer:hover, .stExpander:hover {
  border-color: var(--color-primary) !important; /* Borde azul en hover */
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg) !important;
}

/* Texto dentro de containers */
.stContainer .stMarkdown,
.stExpander .stMarkdown,
div[data-testid="stVerticalBlock"] > div .stMarkdown {
  color: var(--text-primary) !important;
}

/* ============================================================================
   SIDEBAR - CONTRASTE MEJORADO
   ============================================================================ */
section[data-testid="stSidebar"] {
  background: var(--color-fondo) !important;
  border-right: 2px solid var(--gray-800) !important; /* Borde más grueso */
}

section[data-testid="stSidebar"] > div {
  padding: var(--space-6) !important;
}

/* Texto en sidebar */
section[data-testid="stSidebar"] .stMarkdown,
section[data-testid="stSidebar"] .stText {
  color: var(--text-primary) !important;
}

/* ============================================================================
   ALERTAS - CONTRASTE MEJORADO
   ============================================================================ */
.stAlert { 
  border-radius: var(--radius-lg) !important; 
  padding: var(--space-4) !important; 
  border: 2px solid transparent !important; /* Borde para destacar */
}

div[data-testid="stAlert"] > div { 
  border-radius: var(--radius-lg) !important; 
  color: var(--text-primary) !important; /* Texto blanco en alertas */
}

/* ============================================================================
   RESPONSIVE - OPTIMIZACIONES ESPECÍFICAS PARA MÓVIL
   ============================================================================ */
@media (max-width: 768px) {
  /* Aumentar contraste y tamaño en móvil */
  body {
    font-size: var(--text-base) !important;
    line-height: 1.7 !important; /* Más espacio entre líneas */
  }
  
  .stContainer, .stExpander { 
    padding: var(--space-4) !important; 
    border-radius: var(--radius-lg) !important;
    background: rgba(26, 35, 57, 0.95) !important; /* Más opaco en móvil */
  }
  
  .stButton > button { 
    padding: var(--space-4) var(--space-6) !important; 
    width: 100% !important;
    min-height: 48px !important; /* Touch target más grande en móvil */
    font-size: var(--text-base) !important; /* Texto más grande */
  }
  
  section[data-testid="stSidebar"] { 
    width: 100% !important; 
    max-width: 100% !important;
    border-right: none !important;
    border-bottom: 2px solid var(--gray-800) !important;
  }
  
  /* Títulos más grandes y con mejor contraste en móvil */
  h1, .stMarkdown h1 { 
    font-size: var(--text-2xl) !important; 
    font-weight: 800 !important; /* Más negrita */
  }
  
  h2, .stMarkdown h2 { 
    font-size: var(--text-xl) !important; 
    font-weight: 700 !important;
    color: var(--text-primary) !important;
  }
  
  h3, .stMarkdown h3 { 
    font-size: var(--text-lg) !important; 
    font-weight: 600 !important;
    color: var(--text-primary) !important;
  }
  
  /* Inputs más grandes en móvil */
  .stTextInput > div > div > input,
  .stTextArea > div > div > textarea {
    padding: var(--space-4) !important;
    font-size: var(--text-base) !important;
    min-height: 48px !important; /* Más alto para fácil tapping */
  }
  
  /* Mejorar contraste de texto en móvil con brillo bajo */
  .stMarkdown p, .stMarkdown li {
    font-weight: 400 !important; /* Peso normal para mejor legibilidad */
    color: var(--text-primary) !important;
  }
}

/* ============================================================================
   CONTRASTE EXTREMO PARA CONDICIONES DE LUZ DIFÍCILES
   ============================================================================ */
@media (max-width: 768px) and (prefers-color-scheme: dark) {
  /* Modo alto contraste para móvil en modo oscuro */
  :root {
    --text-primary: #FFFFFF !important;
    --color-fondo: #000000 !important; /* Negro puro para máximo contraste */
    --color-surface: #111827 !important;
  }
  
  body {
    background: #000000 !important;
    color: #FFFFFF !important;
  }
  
  .stContainer, .stExpander {
    background: #111827 !important;
    border: 2px solid #334155 !important; /* Bordes muy vis </style>
""", unsafe_allow_html=True)