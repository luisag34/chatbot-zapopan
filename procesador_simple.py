"""
PROCESADOR SIMPLE - SIN IMPORTS COMPLEJOS
Para evitar errores en Streamlit Cloud
"""

import random
from datetime import datetime

def procesar_consulta_local_simple(consulta: str, usuario: str) -> dict:
    """
    Procesar consulta usando sistema simple TODO EN UNO
    """
    # Base de conocimiento simple
    temas = {
        "antena": {
            "titulo": "Instalación de antenas de celulares",
            "analisis": "La instalación de antenas requiere licencia municipal que garantice seguridad estructural y cumplimiento ambiental.",
            "clasificacion": "Inspección y Vigilancia verifica permisos; otras dependencias evalúan proyectos.",
            "sustento": "Reglamento de Construcción Art. 34, Art. 185, Código Urbano Art. 295 Bis.",
            "dependencias": "Inspección y Vigilancia (ext. 3312-3324), Protección Civil (ext. 3778-3783).",
            "fuentes": "Código Urbano para Jalisco, Reglamento de Construcción para Zapopan."
        },
        "ruido": {
            "titulo": "Ruido de establecimientos comerciales",
            "analisis": "Ruido excesivo, especialmente nocturno, está regulado con límites máximos permisibles.",
            "clasificacion": "Inspección y Vigilancia verifica cumplimiento; Medio Ambiente evalúa impacto.",
            "sustento": "Reglamento de Policía Art. 45, Reglamento Comercio Art. 28, Código Ambiental Art. 67.",
            "dependencias": "Inspección y Vigilancia (ext. 3312-3313), Medio Ambiente (ext. 3510-3512).",
            "fuentes": "Reglamento de Policía, Reglamento para el Comercio, Código Ambiental."
        },
        "construccion": {
            "titulo": "Permisos para construcción",
            "analisis": "Toda obra requiere Licencia de Construcción previa que garantice seguridad y cumplimiento.",
            "clasificacion": "Inspección y Vigilancia verifica licencias; Planeación Urbana otorga licencias.",
            "sustento": "Reglamento de Construcción Art. 34, Art. 185, Código Urbano Art. 295.",
            "dependencias": "Planeación Urbana (ext. 3610-3612), Inspección y Vigilancia (ext. 3312-3313).",
            "fuentes": "Reglamento de Construcción para Zapopan, Código Urbano para Jalisco."
        },
        "apertura_negocio": {
            "titulo": "Requisitos para apertura de negocio",
            "analisis": "Apertura requiere Licencia de Funcionamiento Municipal, Permiso de Uso de Suelo y dictámenes.",
            "clasificacion": "Desarrollo Económico otorga licencias; Inspección y Vigilancia verifica.",
            "sustento": "Reglamento Comercio Art. 5, Art. 42, Código Fiscal Art. 78.",
            "dependencias": "Desarrollo Económico (ext. 3410-3412), Inspección y Vigilancia (ext. 3312-3313).",
            "fuentes": "Reglamento para el Comercio, Código Fiscal Municipal."
        }
    }
    
    # Detectar tema
    consulta_lower = consulta.lower()
    tema_detectado = "antena"  # default
    
    if "ruido" in consulta_lower or "sonido" in consulta_lower:
        tema_detectado = "ruido"
    elif "construcción" in consulta_lower or "obra" in consulta_lower:
        tema_detectado = "construccion"
    elif "negocio" in consulta_lower or "abrir" in consulta_lower:
        tema_detectado = "apertura_negocio"
    
    # Obtener tema
    tema = temas.get(tema_detectado, temas["antena"])
    
    # Generar respuesta
    protocolo_pasos = [
        "ANÁLISIS DE SITUACIÓN",
        "CLASIFICACIÓN DE ATRIBUCIONES", 
        "SUSTENTO LEGAL",
        "DEPENDENCIAS CON ATRIBUCIONES Y CONTACTO",
        "FUENTES"
    ]
    
    respuesta = f"""
**{tema['titulo']}**

**1. {protocolo_pasos[0]}**

{tema['analisis']}

**2. {protocolo_pasos[1]}**

{tema['clasificacion']}

**3. {protocolo_pasos[2]}**

{tema['sustento']}

**4. {protocolo_pasos[3]}**

{tema['dependencias']}

**5. {protocolo_pasos[4]}**

{tema['fuentes']}
"""
    
    return {
        "texto_visible": respuesta,
        "resultados": [],
        "categoria": f"sistema_local_{tema_detectado}",
        "fuente": "sistema_local_simple",
        "indicador": f"📋 Sistema normativo Zapopan • ✅ Protocolo específico ({tema_detectado})",
        "usando_ai": False,
        "sigue_protocolo": True
    }

# Alias para compatibilidad
def procesar_consulta_local_expandida(consulta: str, usuario: str) -> dict:
    """Alias para mantener compatibilidad con app.py"""
    return procesar_consulta_local_simple(consulta, usuario)