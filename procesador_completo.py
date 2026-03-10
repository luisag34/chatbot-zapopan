"""
PROCESADOR COMPLETO - RESPUESTAS DETALLADAS
Reemplaza procesador_simple.py con respuestas completas
"""

import random
from datetime import datetime

def procesar_consulta_local_completa(consulta: str, usuario: str) -> dict:
    """
    Procesar consulta con respuestas COMPLETAS y DETALLADAS
    """
    # Base de conocimiento COMPLETA
    temas = {
        "antena": {
            "titulo": "Instalación de antenas de celulares",
            "analisis": """La instalación de una antena de telefonía celular en la azotea de un domicilio particular es una actividad regulada por la normativa estatal y municipal, clasificada jurídicamente como una "Obra Civil para Telecomunicaciones". 

Para que la instalación sea legal, el propietario o la empresa de telecomunicaciones debe tramitar y obtener previamente una licencia municipal de construcción/instalación. El proyecto debe cumplir con estrictos lineamientos técnicos de seguridad estructural, protección civil y medio ambiente.

Si la obra se está ejecutando sin licencia municipal vigente, es irregular y está sujeta a suspensión o clausura inmediata por parte de la Dirección de Inspección y Vigilancia.""",
            "clasificacion": """**Facultad de Inspección y Vigilancia:** Tiene competencia directa para acudir al domicilio, requerir la exhibición de la licencia municipal y, en caso de no contar con ella, ordenar la suspensión o clausura inmediata de los trabajos.

**Facultad de otras dependencias:** La Dirección de Permisos y Licencias de Construcción evalúa proyectos estructurales. La Coordinación Municipal de Protección Civil evalúa riesgos estructurales.""",
            "sustento": """**Reglamento de Construcción para el Municipio de Zapopan, Art. 34:** Establece la obligación de tramitar licencia para cualquier obra de construcción o instalación.

**Reglamento de Construcción, Art. 185, Fracc. II:** Faculta para clausurar obras que se ejecuten sin licencia.

**Código Urbano para el Estado de Jalisco, Art. 295 Bis:** Señala que las instalaciones de infraestructura para telecomunicaciones deben cumplir con normatividad municipal en materia de imagen urbana, protección civil y medio ambiente.""",
            "dependencias": """**Dirección de Inspección y Vigilancia Zapopan**
- Teléfono: 33 3818 2200, extensiones 3312, 3313, 3322, 3324
- Función: Verificación de permisos de construcción, clausura de obras irregulares

**Coordinación Municipal de Protección Civil y Bomberos**
- Teléfono: 33 3818 2200, extensiones 3778, 3782, 3783
- Función: Evaluación de riesgos estructurales, seguridad en obras

**Dirección de Atención Ciudadana**
- Teléfono: 33 3818 2200, extensiones 1210, 1216
- Función: Recepción de quejas y seguimiento de trámites""",
            "fuentes": """1. **Código Urbano para el Estado de Jalisco**
2. **Reglamento de Construcción para el Municipio de Zapopan, Jalisco**
3. **Ley Federal de Telecomunicaciones y Radiodifusión**"""
        },
        "ruido": {
            "titulo": "Ruido de establecimientos comerciales",
            "analisis": """El ruido generado por establecimientos comerciales, especialmente durante horarios nocturnos (22:00 a 07:00 horas), constituye una posible falta administrativa regulada por la normativa municipal de Zapopan.

Los establecimientos comerciales tienen la obligación de respetar los límites máximos permisibles de emisión de ruido establecidos en la normativa aplicable. Durante el horario nocturno, los límites son más estrictos para garantizar el descanso de la población.

Si un establecimiento comercial está generando ruido por encima de los límites permitidos, especialmente durante la noche, está incurriendo en una posible infracción administrativa.""",
            "clasificacion": """**Facultad de Inspección y Vigilancia:** Tiene competencia para verificar el cumplimiento de los límites de ruido establecidos en los reglamentos municipales, realizar mediciones de ruido y, en caso de exceder los límites permisibles, imponer sanciones administrativas.

**Facultad de otras dependencias:** La Dirección de Medio Ambiente tiene competencia en materia de contaminación acústica. La Dirección de Desarrollo Económico puede intervenir en casos de giros comerciales que generen molestias a los vecinos.""",
            "sustento": """**Reglamento de Policía, Justicia Cívica y Buen Gobierno de Zapopan, Art. 45:** Prohíbe generar ruidos o sonidos que perturben la tranquilidad de los vecinos, especialmente durante la noche.

**Reglamento para el Comercio la Industria y la Prestación de Servicios, Art. 28:** Establece que los establecimientos comerciales deben respetar los horarios y niveles de ruido permitidos.

**Código Ambiental para el Municipio de Zapopan, Art. 67:** Fija los límites máximos permisibles de emisión de ruido para diferentes zonas y horarios.""",
            "dependencias": """**Dirección de Inspección y Vigilancia Zapopan**
- Teléfono: 33 3818 2200, extensiones 3312, 3313
- Función: Verificación de ruido, mediciones, imposición de sanciones

**Dirección de Medio Ambiente**
- Teléfono: 33 3818 2200, extensiones 3510, 3512
- Función: Evaluación de impacto acústico, estudios ambientales

**Dirección de Desarrollo Económico**
- Teléfono: 33 3818 2200, extensiones 3410, 3412
- Función: Intervención en giros comerciales molestos""",
            "fuentes": """1. **Reglamento de Policía, Justicia Cívica y Buen Gobierno de Zapopan**
2. **Reglamento para el Comercio, la Industria y la Prestación de Servicios**
3. **Código Ambiental para el Municipio de Zapopan**"""
        },
        "construccion": {
            "titulo": "Permisos para construcción",
            "analisis": """Toda obra de construcción, ampliación, modificación o demolición en el municipio de Zapopan requiere la obtención previa de una Licencia de Construcción emitida por la autoridad municipal competente.

La Licencia de Construcción garantiza que el proyecto cumple con normas de seguridad estructural, reglamentos de construcción vigentes, lineamientos de imagen urbana, disposiciones de protección civil y normativas ambientales aplicables.

La ejecución de obras sin licencia constituye una infracción administrativa grave que puede derivar en la suspensión o clausura de los trabajos, además de sanciones económicas.""",
            "clasificacion": """**Facultad de Inspección y Vigilancia:** Verifica que las obras cuenten con Licencia de Construcción vigente y se ejecuten conforme a lo autorizado. Puede ordenar la suspensión o clausura de obras irregulares.

**Facultad de otras dependencias:** La Dirección de Planeación Urbana otorga Licencias de Construcción. La Coordinación de Protección Civil emite dictámenes de seguridad. La Dirección de Medio Ambiente otorga autorizaciones ambientales.""",
            "sustento": """**Reglamento de Construcción para el Municipio de Zapopan, Art. 34:** Establece la obligación de tramitar licencia para cualquier obra de construcción.

**Reglamento de Construcción, Art. 185, Fracc. II:** Faculta para clausurar obras que se ejecuten sin licencia.

**Código Urbano para el Estado de Jalisco, Art. 295:** Establece sanciones por construcción sin licencia.""",
            "dependencias": """**Dirección de Planeación Urbana Zapopan**
- Teléfono: 33 3818 2200, extensiones 3610, 3612
- Función: Otorgamiento de Licencias de Construcción

**Dirección de Inspección y Vigilancia Zapopan**
- Teléfono: 33 3818 2200, extensiones 3312, 3313
- Función: Verificación de obras y licencias

**Coordinación Municipal de Protección Civil**
- Teléfono: 33 3818 2200, extensiones 3778, 3782
- Función: Dictámenes de seguridad estructural

**Dirección de Medio Ambiente**
- Teléfono: 33 3818 2200, extensiones 3510, 3512
- Función: Autorizaciones ambientales para obras""",
            "fuentes": """1. **Reglamento de Construcción para el Municipio de Zapopan**
2. **Código Urbano para el Estado de Jalisco**
3. **Ley de Asentamientos Humanos, Ordenamiento Territorial y Desarrollo Urbano del Estado de Jalisco**"""
        }
    }
    
    # Detectar tema
    consulta_lower = consulta.lower()
    tema_detectado = "antena"  # default
    
    if "ruido" in consulta_lower or "sonido" in consulta_lower or "molesto" in consulta_lower:
        tema_detectado = "ruido"
    elif "construcción" in consulta_lower or "obra" in consulta_lower or "edificio" in consulta_lower:
        tema_detectado = "construccion"
    elif "antena" in consulta_lower or "celular" in consulta_lower or "telefonía" in consulta_lower:
        tema_detectado = "antena"
    
    # Obtener tema
    tema = temas.get(tema_detectado, temas["antena"])
    
    # Generar respuesta COMPLETA
    protocolo_pasos = [
        "ANÁLISIS DE SITUACIÓN",
        "CLASIFICACIÓN DE ATRIBUCIONES", 
        "SUSTENTO LEGAL",
        "DEPENDENCIAS CON ATRIBUCIONES Y CONTACTO",
        "FUENTES"
    ]
    
    respuesta = f"""
**{tema['titulo'].upper()}**

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

---
*Respuesta generada por el Sistema de Consulta Normativa - Dirección de Inspección y Vigilancia Zapopan*
"""
    
    return {
        "texto_visible": respuesta,
        "resultados": [],
        "categoria": f"sistema_local_{tema_detectado}",
        "fuente": "sistema_local_completo",
        "indicador": f"📋 Sistema normativo Zapopan • ✅ Protocolo específico ({tema_detectado})",
        "usando_ai": False,
        "sigue_protocolo": True
    }

# Alias para compatibilidad
def procesar_consulta_local_expandida(consulta: str, usuario: str) -> dict:
    """Alias para mantener compatibilidad con app.py"""
    return procesar_consulta_local_completa(consulta, usuario)