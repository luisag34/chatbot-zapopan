"""
SISTEMA ZAPOPAN DEFINITIVO
Usa EXCLUSIVAMENTE las System Instructions específicas del chatbot de Google AI Studio
"""

import os
import json
import streamlit as st
from typing import Dict, Optional

# ============================================================================
# CONFIGURACIÓN VERTEX AI CON SYSTEM INSTRUCTIONS COMPLETAS
# ============================================================================

def cargar_system_instructions_completas() -> str:
    """
    Cargar las System Instructions completas del archivo compartido
    (4,000+ palabras con arquitectura compleja)
    """
    try:
        # Cargar desde archivo
        with open("system_instructions_completas_zapopan.txt", "r", encoding="utf-8") as f:
            system_instructions = f.read()
        
        print(f"✅ System Instructions cargadas: {len(system_instructions):,} caracteres")
        return system_instructions
    except Exception as e:
        print(f"❌ Error cargando System Instructions: {e}")
        # Fallback a versión resumida
        return """========================================================
SYSTEM INSTRUCTIONS SISTEMA DE CONSULTA NORMATIVA ZAPOPAN
========================================================

########################################################
ARQUITECTURA DEL SISTEMA
########################################################

Eres un sistema de consulta normativa cuya arquitectura se constituye de cuatro apartados:

SISTEMA DE CONSULTA NORMATIVA ZAPOPAN
├── Núcleo de Documentos
├── Router de Áreas
├── Protocolos Especializados
└── Sistema de Auditoría

Esta arquitectura no puede ser modificada ni omitida en ningún momento.

########################################################
PROTOCOLO DE RESPUESTA (ORDEN OBLIGATORIO)
########################################################

Todas las respuestas deben seguir exactamente este orden.

--------------------------------------------------------
1. ANÁLISIS DE SITUACIÓN
--------------------------------------------------------
Explicar qué dicen las normas relevantes.
Indicar cómo se relacionan entre sí los niveles normativos.

Ejemplo conceptual: "El Código Urbano establece la base estatal, mientras que el Reglamento de Construcción de Zapopan detalla la regulación municipal."

--------------------------------------------------------
2. CLASIFICACIÓN DE ATRIBUCIONES
--------------------------------------------------------
Determinar si la situación corresponde a:
• facultad exclusiva de Inspección y Vigilancia
• facultad compartida
• facultad de otra dependencia
• escenario no contemplado

Si no está contemplado indicar: "La normativa actual de Zapopan y el Código Urbano de Jalisco no contemplan el escenario descrito."

--------------------------------------------------------
3. SUSTENTO LEGAL
--------------------------------------------------------
Dividir en:
Fundamento de Inspección y Vigilancia
Fundamento de otras dependencias

Citar SOLO artículos relevantes. Nunca incluir artículos si no son pertinentes.

--------------------------------------------------------
4. DEPENDENCIAS CON ATRIBUCIONES Y CONTACTO
--------------------------------------------------------
Identificar:
• dependencia responsable
• funciones
• datos de contacto

Buscar datos en el directorio institucional.
Si no existen indicar: "Dato de contacto no disponible en el registro actual."

--------------------------------------------------------
5. FUENTES
--------------------------------------------------------
Lista de citas utilizadas.

Ejemplo:
FUENTES
Reglamento de Construcción de Zapopan, Art. 149
Código Urbano de Jalisco, Art. 305
NOM-081-SEMARNAT-1994, numeral 5.3

########################################################
NÚCLEO DE DOCUMENTOS – ESTRUCTURA JERÁRQUICA
########################################################

Los documentos normativos se organizan en cuatro niveles jerárquicos.
En caso de contradicción normativa prevalece el nivel superior.

Jerarquía normativa: Nivel 1 > Nivel 2 > Nivel 3 > Nivel 4

--------------------------------------------------------
NIVEL 1: Documentos estatales y NOM federales
--------------------------------------------------------
Código Urbano para el Estado de Jalisco
Ley del Procedimiento Administrativo del Estado de Jalisco y sus Municipios
NOM-081-SEMARNAT-1994
Reglamento Estatal de Zonificación

--------------------------------------------------------
NIVEL 2: Reglamentos municipales
--------------------------------------------------------
Reglamento de Construcción para el Municipio de Zapopan
Reglamento de Policía, Justicia Cívica y Buen Gobierno de Zapopan
Reglamento de Protección al Medio Ambiente y Equilibrio Ecológico
Reglamento para el Comercio la Industria y la Prestación de Servicios
[15+ reglamentos más]

--------------------------------------------------------
NIVEL 3: Códigos, manuales y documentos municipales
--------------------------------------------------------
Código Ambiental para el Municipio de Zapopan
Manual de Organización de la Dirección de Inspección y Vigilancia

--------------------------------------------------------
NIVEL 4: Directorio institucional
--------------------------------------------------------
directorio ZPN, IA inspección

########################################################
ROUTER DE ÁREAS
########################################################

- CONSTRUCCIÓN: obra, construcción, edificación, ampliación, demolición, barda, azotea, antena, telecomunicación
- COMERCIO: negocio, local, establecimiento, giro, licencia, permiso comercial
- TÉCNICA / MEDIO AMBIENTE: ruido, contaminación, residuos, árboles, anuncios, antenas
- RIESGOS / PROTECCIÓN CIVIL: riesgo, peligro, colapso, incendio, medidas de seguridad
- ESPACIO PÚBLICO: banqueta, calle, andador, plaza, ocupación indebida

########################################################
MATRIZ DE COMPETENCIAS – DIRECCIÓN DE INSPECCIÓN Y VIGILANCIA
########################################################

FACULTADES PRINCIPALES:
• Comercio y establecimientos
• Comercio en vía pública  
• Construcción y obras (verificación en campo)
• Anuncios y publicidad (inspección y medidas de seguridad)
• Medio ambiente y contaminación (verificación y cumplimiento)

FACULTADES CONCURRENTES:
• Medio ambiente (con Dirección de Medio Ambiente)
• Protección civil y riesgos (con Protección Civil)
• Comercio con impacto ambiental o urbano

NO COMPETENCIA PRINCIPAL:
• Seguridad pública (Comisaría de Seguridad Pública)
• Servicios públicos municipales (Dirección de Servicios Públicos)
• Asuntos sociales o asistenciales (DIF municipal)
• Telecomunicaciones federales (IFT)

########################################################
CONVENCIÓN DE CITAS DEL SISTEMA
########################################################

El sistema utiliza la Convención A: cita corta + sección de fuentes.

Las citas dentro del texto utilizan el formato:
Documento, Art. X
Documento, Art. X, Fracc. Y  
Documento, numeral X.X

Ejemplos:
Código Ambiental de Zapopan, Art. 25
Reglamento de Construcción de Zapopan, Art. 149
NOM-081-SEMARNAT-1994, numeral 5.3

Al final de cada respuesta debe existir una sección titulada: FUENTES

########################################################
REGLA CRÍTICA: PROHIBICIÓN ABSOLUTA DE ALUCINACIÓN NORMATIVA
########################################################

El modelo SOLO puede responder utilizando información contenida en los chunks recuperados.
Si la información no aparece en los chunks recuperados:

NO debes inventar normas, artículos o facultades.
Debes indicar explícitamente: "No se encontró fundamento en los documentos normativos disponibles en el sistema."

########################################################
SISTEMA DE AUDITORÍA
########################################################

Cada respuesta debe incluir un bloque de auditoría interno.

Formato:
---AUDIT---
{
  "timestamp": "pendiente",
  "area_identificada": "",
  "tipo_consulta": "",
  "documentos_consultados": [],
  "ids_juridicos_utilizados": [],
  "tiempo_respuesta_segundos": 0,
  "calificacion_sugerida": ""
}

Este bloque permite:
• trazabilidad normativa
• análisis de consultas
• mejora continua del sistema
• auditoría de fundamentos legales

El bloque de auditoría NO debe ser visible para el usuario final.
"""

# ============================================================================
# INTEGRACIÓN CON VERTEX AI
# ============================================================================

class SistemaZapopanDefinitivo:
    """Sistema definitivo que usa EXCLUSIVAMENTE las System Instructions específicas"""
    
    def __init__(self):
        self.system_instructions = cargar_system_instructions_completas()
        self.vertex_ai_available = False
        
        # Intentar cargar Vertex AI
        try:
            from vertex_ai_integration import crear_vertex_ai_chatbot
            self.chatbot = crear_vertex_ai_chatbot()
            self.vertex_ai_available = self.chatbot.is_configured()
        except:
            self.vertex_ai_available = False
    
    def procesar_consulta(self, consulta: str) -> Dict:
        """Procesar consulta usando el protocolo específico"""
        
        # Si Vertex AI está disponible, usarlo con System Instructions completas
        if self.vertex_ai_available:
            try:
                resultado = self.chatbot.query(consulta, self.system_instructions)
                
                if resultado["using_ai"]:
                    return {
                        "texto_visible": resultado["response"],
                        "fuente": "vertex_ai",
                        "indicador": "🚀 Vertex AI • 🔧 Sistema normativo Zapopan (protocolo específico)",
                        "usando_protocolo_especifico": True
                    }
            except Exception as e:
                print(f"❌ Error Vertex AI: {e}")
        
        # Si Vertex AI falla, mostrar mensaje claro
        return {
            "texto_visible": """🔧 **SISTEMA EN CONFIGURACIÓN**

El sistema de consulta normativa con protocolo específico de Zapopan está siendo configurado.

**Para consultas urgentes:**
1. Contactar a la Dirección de Inspección y Vigilancia
2. Presentar denuncia en ventanilla única
3. Solicitar asesoría jurídica del área correspondiente

**Contacto:**
📞 33 3818-2200 ext. [correspondiente]
📧 inspeccion.vigilancia@zapopan.gob.mx

*Sistema volverá a funcionar en breve con el protocolo completo de consulta normativa.*""",
            "fuente": "sistema_local",
            "indicador": "🔧 Sistema en configuración • Protocolo específico en implementación",
            "usando_protocolo_especifico": False
        }
    
    def verificar_protocolo_respuesta(self, respuesta: str) -> bool:
        """Verificar que la respuesta siga el protocolo específico"""
        # Verificar secciones obligatorias
        secciones_obligatorias = [
            "ANÁLISIS DE SITUACIÓN",
            "CLASIFICACIÓN DE ATRIBUCIONES", 
            "SUSTENTO LEGAL",
            "DEPENDENCIAS CON ATRIBUCIONES Y CONTACTO",
            "FUENTES"
        ]
        
        encontradas = 0
        for seccion in secciones_obligatorias:
            if seccion in respuesta:
                encontradas += 1
        
        return encontradas >= 4  # Al menos 4 de 5 secciones

# ============================================================================
# INTEGRACIÓN CON APP.PY
# ============================================================================

def integrar_en_app():
    """Instrucciones para integrar este sistema en app.py"""
    
    return """
INSTRUCCIONES PARA INTEGRAR EN APP.PY:

1. REEMPLAZAR TODO EL SISTEMA ACTUAL:

En app.py, buscar la función que procesa consultas (alrededor de línea 500)
y reemplazarla con:

```python
# ============================================================================
# SISTEMA DEFINITIVO ZAPOPAN (PROTOCOLO ESPECÍFICO)
# ============================================================================

from sistema_zapopan_definitivo import SistemaZapopanDefinitivo

sistema_zapopan = SistemaZapopanDefinitivo()

def procesar_consulta_definitiva(consulta: str, usuario: str) -> Dict:
    \"\"\"Procesar consulta usando el protocolo específico de Zapopan\"\"\"
    resultado = sistema_zapopan.procesar_consulta(consulta)
    
    # Registrar consulta
    registrar_consulta_local(consulta, [], usuario)
    
    return {
        "texto_visible": resultado["texto_visible"],
        "resultados": [],
        "categoria": "sistema_definitivo",
        "fuente": resultado["fuente"],
        "indicador": resultado["indicador"],
        "usando_protocolo_especifico": resultado.get("usando_protocolo_especifico", False)
    }

# En la función principal, reemplazar llamada actual con:
resultado = procesar_consulta_definitiva(consulta, usuario)
```

2. ELIMINAR SISTEMAS ANTERIORES:
- Comentar o eliminar importaciones de: fallback_mejorado, chatbot_zapopan_hibrido
- Mantener solo vertex_ai_integration y sistema_zapopan_definitivo

3. ACTUALIZAR INTERFAZ:
- Mostrar el indicador de resultado["indicador"]
- Resaltar si está usando protocolo específico
"""

# ============================================================================
# PRUEBA DEL SISTEMA
# ============================================================================

if __name__ == "__main__":
    print("🔧 SISTEMA ZAPOPAN DEFINITIVO - PRUEBA")
    print("=" * 60)
    
    sistema = SistemaZapopanDefinitivo()
