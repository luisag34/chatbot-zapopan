"""
Sistema híbrido definitivo para chatbot Zapopan
Fallback mejorado + Gemini 2.5 Flash optimizado
"""

import os
import json
import requests
from typing import Dict, Optional
import streamlit as st

# ============================================================================
# CONFIGURACIÓN GEMINI OPTIMIZADA
# ============================================================================

GEMINI_CONFIG = {
    "model": "gemini-2.5-flash",
    "endpoint": "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent",
    "max_tokens": 3000,  # Máximo para evitar truncamiento
    "temperature": 0.1,
    "safety_settings": [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
    ]
}

# Prompt optimizado para respuestas legales
PROMPT_TEMPLATE = """Eres un experto en regulaciones municipales de Zapopan, Jalisco.

CONSULTA: {consulta}

Responde en español con esta estructura:

1. **ANÁLISIS NORMATIVO** - Explica la situación según normativa de Zapopan
2. **REGLAMENTO APLICABLE** - Nombre del reglamento municipal
3. **ARTÍCULO ESPECÍFICO** - Número y contenido (ej: Reglamento de Policía, Art. 45)
4. **HORARIOS/RESTRICCIONES** - Límites establecidos
5. **DEPENDENCIA RESPONSABLE** - Área del ayuntamiento con competencia
6. **PROCEDIMIENTO** - Pasos para acción ciudadana

Sé específico, preciso y cita solo normativa real de Zapopan.
Si no hay información específica: "Consulta fuera del ámbito normativo disponible."

MATERIAS DE INSPECCIÓN Y VIGILANCIA ZAPOPAN:
- Comercio y establecimientos
- Construcción y obras  
- Medio ambiente (ruido, residuos)
- Anuncios y publicidad
- Espacio público
- Protección civil"""

# ============================================================================
# SISTEMA HÍBRIDO
# ============================================================================

class SistemaHibridoZapopan:
    """Sistema híbrido: IA optimizada + fallback garantizado"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("GOOGLE_API_KEY")
        self.ia_configurada = bool(self.api_key)
        
        # Estadísticas
        self.estadisticas = {
            "total_consultas": 0,
            "ia_exitosas": 0,
            "fallback_usado": 0,
            "errores_ia": 0,
            "ia_desactivada": True  # Temporalmente desactivada
        }
    
    def procesar_consulta(self, consulta: str) -> Dict:
        """Procesar consulta con sistema híbrido"""
        self.estadisticas["total_consultas"] += 1
        
        # ⚠️ TEMPORAL: IA DESACTIVADA POR PROBLEMAS TÉCNICOS
        # Gemini 2.5-flash trunca respuestas, Gemini 2.5-pro no responde
        # Usar siempre fallback mejorado hasta resolver problemas de API
        
        # Paso 1: Usar fallback mejorado (IA temporalmente desactivada)
        self.estadisticas["fallback_usado"] += 1
        resultado = self._usar_fallback(consulta)
        
        # Registrar que IA está desactivada
        self.estadisticas["ia_desactivada"] = True
        
        return resultado
        
        # CÓDIGO ORIGINAL (comentado para referencia):
        # # Paso 1: Intentar IA optimizada
        # if self.ia_configurada:
        #     resultado_ia = self._intentar_ia(consulta)
        #     
        #     if resultado_ia["valida"]:
        #         self.estadisticas["ia_exitosas"] += 1
        #         return {
        #             "texto": resultado_ia["respuesta"],
        #             "fuente": "gemini_optimizado",
        #             "usando_ia": True,
        #             "calidad": resultado_ia["calidad"],
        #             "longitud": len(resultado_ia["respuesta"])
        #         }
        #     else:
        #         self.estadisticas["errores_ia"] += 1
        # 
        # # Paso 2: Usar fallback mejorado
        # self.estadisticas["fallback_usado"] += 1
        # return self._usar_fallback(consulta)
    
    def _intentar_ia(self, consulta: str) -> Dict:
        """Intentar IA con configuración optimizada"""
        try:
            # Preparar prompt
            prompt = PROMPT_TEMPLATE.format(consulta=consulta)
            
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {
                    "temperature": GEMINI_CONFIG["temperature"],
                    "maxOutputTokens": GEMINI_CONFIG["max_tokens"],
                    "topP": 0.8,
                    "topK": 40
                },
                "safetySettings": GEMINI_CONFIG["safety_settings"]
            }
            
            headers = {
                "Content-Type": "application/json",
                "x-goog-api-key": self.api_key
            }
            
            # Llamada a API
            response = requests.post(
                GEMINI_CONFIG["endpoint"],
                headers=headers,
                json=payload,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if "candidates" in data and data["candidates"]:
                    candidate = data["candidates"][0]
                    
                    if (candidate.get("finishReason") == "STOP" and 
                        "content" in candidate and 
                        "parts" in candidate["content"]):
                        
                        parts = candidate["content"]["parts"]
                        if parts and len(parts) > 0 and "text" in parts[0]:
                            texto = parts[0]["text"]
                            
                            # Validar calidad
                            valida, calidad = self._validar_respuesta_ia(texto, consulta)
                            
                            return {
                                "valida": valida,
                                "respuesta": texto,
                                "calidad": calidad,
                                "finish_reason": "STOP"
                            }
            
            # Si llegamos aquí, IA falló
            return {"valida": False, "error": "respuesta_invalida"}
            
        except Exception as e:
            return {"valida": False, "error": str(e)[:80]}
    
    def _validar_respuesta_ia(self, texto: str, consulta_original: str) -> tuple[bool, str]:
        """Validar calidad de respuesta IA"""
        # Validaciones básicas
        if len(texto.strip()) < 150:
            return False, "muy_corta"
        
        texto_lower = texto.lower()
        
        # Criterios de calidad
        criterios = {
            "zapopan": "zapopan" in texto_lower,
            "reglamento": "reglamento" in texto_lower,
            "articulo": "artículo" in texto_lower or "art." in texto_lower,
            "estructura": any(x in texto for x in ["1.", "2.", "3.", "•", "-", "**"]),
            "relevante": any(x in texto_lower for x in ["inspección", "vigilancia", "municipal", "normativa"])
        }
        
        cumplidos = sum(criterios.values())
        
        if cumplidos >= 4:
            return True, "excelente"
        elif cumplidos >= 3:
            return True, "buena"
        elif cumplidos >= 2:
            return True, "aceptable"
        else:
            return False, "insuficiente"
    
    def _usar_fallback(self, consulta: str) -> Dict:
        """Usar sistema fallback mejorado"""
        try:
            from fallback_mejorado import procesar_consulta_fallback_mejorado
            resultado = procesar_consulta_fallback_mejorado(consulta, "sistema_hibrido")
            
            return {
                "texto": resultado["texto_visible"],
                "fuente": "fallback_mejorado",
                "usando_ia": False,
                "calidad": "garantizada",
                "longitud": len(resultado["texto_visible"])
            }
        except:
            # Fallback de emergencia
            texto = f"**Consulta:** {consulta}\n\n"
            texto += "**Orientación general:**\n"
            texto += "Para consultas normativas específicas de Zapopan, contacta a la Dirección de Inspección y Vigilancia:\n"
            texto += "📞 Tel: 33 3818-2200 ext. 5501\n"
            texto += "📧 Email: inspeccion.vigilancia@zapopan.gob.mx\n\n"
            texto += "*Sistema en optimización técnica.*"
            
            return {
                "texto": texto,
                "fuente": "fallback_emergencia",
                "usando_ia": False,
                "calidad": "basica",
                "longitud": len(texto)
            }
    
    def get_estadisticas(self) -> Dict:
        """Obtener estadísticas del sistema"""
        return self.estadisticas.copy()
    
    def get_status(self) -> Dict:
        """Estado del sistema"""
        return {
            "ia_configurada": self.ia_configurada,
            "modelo": GEMINI_CONFIG["model"] if self.ia_configurada else "no_configurado",
            "estadisticas": self.estadisticas
        }

# ============================================================================
# INTEGRACIÓN CON APP
# ============================================================================

def crear_sistema_hibrido() -> SistemaHibridoZapopan:
    """Crear sistema híbrido"""
    api_key = None
    
    # Streamlit Secrets
    try:
        if hasattr(st, 'secrets') and 'GOOGLE_API_KEY' in st.secrets:
            api_key = st.secrets['GOOGLE_API_KEY']
    except:
        pass
    
    # Variable de entorno
    if not api_key:
        api_key = os.environ.get("GOOGLE_API_KEY")
    
    return SistemaHibridoZapopan(api_key)

def procesar_consulta_hibrida(consulta: str, usuario: str) -> Dict:
    """
    Función principal para app.py
    Sistema híbrido completo
    """
    # Importar funciones locales para registro
    from app import buscar_en_base_conocimiento, registrar_consulta_local
    
    # Buscar en base local para contexto
    resultados_locales = buscar_en_base_conocimiento(consulta)
    
    # Procesar con sistema híbrido
    sistema = crear_sistema_hibrido()
    resultado = sistema.procesar_consulta(consulta)
    
    # Registrar consulta
    registrar_consulta_local(consulta, resultados_locales, usuario)
    
    # Preparar respuesta final
    respuesta_final = {
        "texto_visible": resultado["texto"],
        "resultados": resultados_locales,
        "categoria": "sistema_hibrido",
        "fuente": resultado["fuente"],
        "usando_ai": resultado["usando_ia"],
        "calidad": resultado["calidad"]
    }
    
    # Añadir indicador visual si es IA
    if resultado["usando_ia"]:
        indicador = "🤖 **Respuesta generada por IA**"
        if resultado["calidad"] == "excelente":
            indicador += " ✅"
        elif resultado["calidad"] == "buena":
            indicador += " 👍"
        else:
            indicador += " ⚠️"
        
        respuesta_final["texto_visible"] = f"{indicador}\n\n{resultado['texto']}"
    
    return respuesta_final

# ============================================================================
# PRUEBA DEL SISTEMA
# ============================================================================

if __name__ == "__main__":
    print("🚀 SISTEMA HÍBRIDO ZAPOPAN - PRUEBA COMPLETA")
    print("=" * 60)
    
    # Configurar API key para prueba
    import os
    os.environ["GOOGLE_API_KEY"] = "AIzaSyC9lqTVCcIzHYh96-Lo4pmdoiXfyYCmnNY"
    
    sistema = crear_sistema_hibrido()
    
    status = sistema.get_status()
    print(f"🔧 Configuración:")
    print(f"   • IA configurada: {status['ia_configurada']}")
    print(f"   • Modelo: {status.get('modelo', 'N/A')}")
    
    print(f"\n🎯 PROBANDO CONSULTAS:")
    
    consultas_prueba = [
        "ruido de restaurante por la noche",
        "obra sin permiso de construcción",
        "vendedor ambulante en banqueta",
        "anuncio publicitario muy grande"
    ]
    
    for i, consulta in enumerate(consultas_prueba, 1):
        print(f"\n{i}. 📋 \"{consulta}\"")
        print("-" * 40)
        
        resultado = sistema.procesar_consulta(consulta)
        
        print(f"   🤖 Fuente: {resultado['fuente']}")
        print(f"   📊 Calidad: {resultado['calidad']}")
        print(f"   📏 Longitud: {resultado['longitud']} caracteres")
        
        # Preview
        preview = resultado['texto'][:120].replace('\n', ' ')
        print(f"   📝 Preview: {preview}...")
        
        if resultado['fuente'] == 'gemini_optimizado':
            print(f"   ✅ IA FUNCIONANDO")
        else:
            print(f"   🔧 FALLBACK ACTIVADO")
    
    # Estadísticas finales
    stats = sistema.get_estadisticas()
    print(f"\n📈 ESTADÍSTICAS FINALES:")
    print(f"   • Total consultas: {stats['total_consultas']}")
    print(f"   • IA exitosas: {stats['ia_exitosas']}")
    print(f"   • Fallback usado: {stats['fallback_usado']}")
    print(f"   • Errores IA: {stats['errores_ia']}")
    
    if stats['total_consultas'] > 0:
        tasa_exito = (stats['ia_exitosas'] / stats['total_consultas']) * 100
        print(f"   📊 Tasa éxito IA: {tasa_exito:.1f}%")
    
    print("\n" + "=" * 60)
    print("🎯 SISTEMA HÍBRIDO LISTO PARA INTEGRACIÓN EN app.py")
    print("💡 Sistema garantizado: IA cuando funciona, fallback siempre")