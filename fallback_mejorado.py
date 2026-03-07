"""
Sistema de fallback mejorado para chatbot-zapopan
Respuestas locales mejoradas mientras debuggeamos Google AI
"""

import json
import random
from typing import Dict, List
from datetime import datetime

# ============================================================================
# BASE DE CONOCIMIENTO MEJORADA
# ============================================================================

BASE_CONOCIMIENTO_MEJORADA = {
    "ruido": [
        {
            "reglamento": "Reglamento de Policía y Buen Gobierno",
            "articulo": "Artículo 45",
            "contenido": "Prohibición de ruidos y vibraciones que alteren la tranquilidad pública, especialmente entre las 22:00 y 07:00 horas.",
            "dependencia": "Dirección de Inspección y Vigilancia",
            "procedimiento": "Presentar denuncia escrita en ventanilla única con descripción del hecho, horarios y pruebas si las hay.",
            "sancion": "Multa de 50 a 100 UMA (aprox. $5,000 a $10,000 MXN)",
            "contacto": "Tel: 33 3818-2200 ext. 5501 | Email: inspeccion.vigilancia@zapopan.gob.mx"
        },
        {
            "reglamento": "Reglamento de Protección al Medio Ambiente",
            "articulo": "Artículo 28",
            "contenido": "Niveles máximos permisibles de ruido: 55 dB diurno (07:00-22:00), 50 dB nocturno (22:00-07:00) en zona residencial.",
            "dependencia": "Dirección de Medio Ambiente",
            "procedimiento": "Solicitar medición de niveles de ruido por personal autorizado.",
            "sancion": "Multa y posible clausura temporal",
            "contacto": "Tel: 33 3818-2200 ext. 5200"
        }
    ],
    
    "construccion": [
        {
            "reglamento": "Reglamento de Desarrollo Urbano",
            "articulo": "Artículo 67",
            "contenido": "Toda construcción requiere permiso municipal previo. Obras sin permiso son irregulares.",
            "dependencia": "Dirección de Desarrollo Urbano",
            "procedimiento": "Verificar en ventanilla única si existe permiso vigente. Si no, proceder a inspección.",
            "sancion": "Multa de 100 a 500 UMA y posible demolición",
            "contacto": "Tel: 33 3818-2200 ext. 5300"
        }
    ],
    
    "comercio": [
        {
            "reglamento": "Reglamento de Comercio en Vía Pública",
            "articulo": "Artículo 12",
            "contenido": "Prohibido el comercio ambulante sin permiso en zonas no autorizadas.",
            "dependencia": "Dirección de Inspección y Vigilancia",
            "procedimiento": "Reportar con ubicación exacta y fotografía si es posible.",
            "sancion": "Multa y retiro de mercancía",
            "contacto": "Tel: 33 3818-2200 ext. 5502"
        }
    ],
    
    "general": [
        {
            "reglamento": "Ley de Procedimiento Administrativo del Estado de Jalisco",
            "articulo": "Artículo 34",
            "contenido": "Todo ciudadano tiene derecho a presentar quejas y denuncias ante la autoridad municipal.",
            "dependencia": "Dirección de Atención Ciudadana",
            "procedimiento": "Presentar escrito libre en ventanilla única o vía electrónica.",
            "sancion": "N/A",
            "contacto": "Tel: 33 3818-2200 ext. 5000 | Quejas: quejas@zapopan.gob.mx"
        }
    ]
}

# ============================================================================
# DETECTOR DE CATEGORÍAS MEJORADO
# ============================================================================

PALABRAS_CLAVE = {
    "ruido": ["ruido", "sonido", "volumen", "música", "fiesta", "altavoz", "parlante", "escándalo", "bullicio", "estruendo"],
    "construccion": ["construcción", "obra", "edificación", "demolición", "martillo", "taladro", "andamio", "materiales", "obrero"],
    "comercio": ["comercio", "tianguis", "ambulante", "puesto", "venta", "mercado", "producto", "vendedor", "informal"],
    "basura": ["basura", "desechos", "residuos", "inmundicia", "suciedad", "limpieza", "recolección"],
    "estacionamiento": ["estacionamiento", "cajón", "aparcar", "vehículo", "auto", "coche", "bloquear", "acceso"]
}

# ============================================================================
# FUNCIONES PRINCIPALES
# ============================================================================

def detectar_categoria(consulta: str) -> str:
    """Detectar categoría de la consulta"""
    consulta_lower = consulta.lower()
    
    for categoria, palabras in PALABRAS_CLAVE.items():
        for palabra in palabras:
            if palabra in consulta_lower:
                return categoria
    
    return "general"

def buscar_en_fallback(consulta: str) -> List[Dict]:
    """Buscar en base de conocimiento mejorada"""
    categoria = detectar_categoria(consulta)
    
    if categoria in BASE_CONOCIMIENTO_MEJORADA:
        return BASE_CONOCIMIENTO_MEJORADA[categoria]
    else:
        return BASE_CONOCIMIENTO_MEJORADA["general"]

def generar_respuesta_mejorada(consulta: str, resultados: List[Dict]) -> str:
    """Generar respuesta estructurada y profesional"""
    
    respuesta = f"## 📋 **Consulta normativa - Ayuntamiento de Zapopan**\n\n"
    respuesta += f"**Consulta recibida:** \"{consulta}\"\n\n"
    
    if not resultados:
        respuesta += "### ℹ️ **Información general**\n\n"
        respuesta += "No se encontraron regulaciones específicas para tu caso.\n\n"
        respuesta += "**Recomendación:**\n"
        respuesta += "1. Contacta a la **Dirección de Inspección y Vigilancia**\n"
        respuesta += "2. Proporciona detalles específicos (ubicación, horarios, pruebas)\n"
        respuesta += "3. Solicita orientación personalizada\n\n"
        respuesta += "📞 **Contacto:** 33 3818-2200 ext. 5501\n"
        respuesta += "📧 **Email:** inspeccion.vigilancia@zapopan.gob.mx\n"
        
        return respuesta
    
    respuesta += "### 📚 **Regulaciones aplicables identificadas:**\n\n"
    
    for i, reg in enumerate(resultados, 1):
        respuesta += f"#### {i}. {reg['reglamento']}\n"
        respuesta += f"- **Artículo:** {reg['articulo']}\n"
        respuesta += f"- **Contenido:** {reg['contenido']}\n"
        respuesta += f"- **Dependencia responsable:** {reg['dependencia']}\n"
        respuesta += f"- **Procedimiento:** {reg['procedimiento']}\n"
        respuesta += f"- **Sanción aplicable:** {reg['sancion']}\n"
        respuesta += f"- **Contacto:** {reg['contacto']}\n\n"
    
    respuesta += "### ⚖️ **Pasos a seguir:**\n"
    respuesta += "1. **Recopila evidencia** (fotos, videos, testigos)\n"
    respuesta += "2. **Presenta denuncia formal** en ventanilla única\n"
    respuesta += "3. **Solicita inspección** por personal autorizado\n"
    respuesta += "4. **Da seguimiento** al número de folio asignado\n\n"
    
    respuesta += "### ⏰ **Plazos estimados:**\n"
    respuesta += "- **Atención inicial:** 24-48 horas hábiles\n"
    respuesta += "- **Inspección programada:** 3-5 días hábiles\n"
    respuesta += "- **Resolución:** 15-30 días hábiles\n\n"
    
    respuesta += "---\n"
    respuesta += "**Nota:** Esta es una orientación preliminar. Para asesoría legal específica, consulta al área jurídica correspondiente.\n"
    
    return respuesta

def procesar_consulta_fallback_mejorado(consulta: str, usuario: str) -> Dict:
    """Procesar consulta con fallback mejorado"""
    
    # Buscar en base mejorada
    resultados = buscar_en_fallback(consulta)
    
    # Generar respuesta estructurada
    respuesta_texto = generar_respuesta_mejorada(consulta, resultados)
    
    # Registrar para métricas
    registrar_consulta_fallback(consulta, usuario)
    
    return {
        "texto_visible": respuesta_texto,
        "resultados": resultados,
        "categoria": detectar_categoria(consulta),
        "fuente": "fallback_mejorado",
        "usando_ai": False,
        "nota": "Sistema en modo local mejorado - Chatbot AI temporalmente no disponible"
    }

def registrar_consulta_fallback(consulta: str, usuario: str):
    """Registrar consulta para métricas"""
    try:
        registro = {
            "timestamp": datetime.now().isoformat(),
            "usuario": usuario,
            "consulta": consulta,
            "modo": "fallback_mejorado",
            "categoria": detectar_categoria(consulta)
        }
        
        with open("consultas_fallback.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(registro, ensure_ascii=False) + "\n")
    except:
        pass  # Silencioso si falla el registro

# ============================================================================
# INTEGRACIÓN CON APP.PY
# ============================================================================

def procesar_consulta_hibrida(consulta: str, usuario: str, intentar_chatbot: bool = True) -> Dict:
    """
    Procesar consulta híbrida: intentar chatbot primero, luego fallback mejorado
    
    Args:
        consulta: Texto de la consulta
        usuario: Usuario que hace la consulta
        intentar_chatbot: Si debe intentar conectar al chatbot
    
    Returns:
        Dict con respuesta
    """
    
    # Por ahora, siempre usar fallback mejorado hasta que debuggeemos chatbot
    # TODO: Restaurar lógica híbrida cuando chatbot funcione
    
    return procesar_consulta_fallback_mejorado(consulta, usuario)

# ============================================================================
# PRUEBA RÁPIDA
# ============================================================================

if __name__ == "__main__":
    print("🧪 PROBANDO FALLBACK MEJORADO")
    print("=" * 60)
    
    pruebas = [
        "ruido de restaurante por la noche",
        "construcción sin permiso en mi colonia",
        "vendedores ambulantes bloqueando la banqueta",
        "basura acumulada por días"
    ]
    
    for prueba in pruebas:
        print(f"\n🔍 Consulta: '{prueba}'")
        print("-" * 40)
        
        resultado = procesar_consulta_fallback_mejorado(prueba, "test_user")
        
        print(f"✅ Categoría detectada: {resultado['categoria']}")
        print(f"✅ Resultados encontrados: {len(resultado['resultados'])}")
        print(f"✅ Fuente: {resultado['fuente']}")
        
        # Mostrar primer resultado
        if resultado['resultados']:
            reg = resultado['resultados'][0]
            print(f"📋 Primer reglamento: {reg['reglamento']}")
            print(f"   Artículo: {reg['articulo']}")
            print(f"   Dependencia: {reg['dependencia']}")
        
        print(f"\n📝 Respuesta (primeras 200 chars):")
        print(resultado['texto_visible'][:200] + "...")
    
    print("\n" + "=" * 60)
    print("🎯 FALLBACK MEJORADO LISTO PARA INTEGRACIÓN")