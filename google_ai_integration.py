"""
Módulo de integración con Google AI (Gemini)
Sistema híbrido: Google AI + fallback a base local
"""

import os
import json
from typing import Dict, List, Optional, Tuple
import streamlit as st

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

# Intentar importar Google AI, pero tener fallback si no está disponible
GOOGLE_AI_AVAILABLE = False
try:
    # Intentar nueva versión primero (google.genai)
    import google.genai as genai
    GOOGLE_AI_AVAILABLE = True
    GENAI_VERSION = "new"
except ImportError:
    try:
        # Fallback a versión deprecated (google.generativeai)
        import google.generativeai as genai
        GOOGLE_AI_AVAILABLE = True
        GENAI_VERSION = "deprecated"
    except ImportError:
        st.warning("⚠️ Google AI no está instalado. Usando modo local.")
        genai = None
        GENAI_VERSION = "none"

# ============================================================================
# CLASE PRINCIPAL DE INTEGRACIÓN
# ============================================================================

class GoogleAIIntegration:
    """Integración con Google AI para consultas normativas"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Inicializar con API key (opcional)"""
        self.api_key = api_key or os.environ.get("GOOGLE_API_KEY")
        self.model = None
        self.is_configured = False
        
        if GOOGLE_AI_AVAILABLE and self.api_key:
            self._configure_google_ai()
    
    def _configure_google_ai(self) -> bool:
        """Configurar Google AI con API key"""
        try:
            genai.configure(api_key=self.api_key)
            
            # Usar Gemini 1.5 Flash (rápido y económico)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Configuración de generación
            self.generation_config = {
                "temperature": 0.2,  # Baja temperatura para respuestas precisas
                "top_p": 0.8,
                "top_k": 40,
                "max_output_tokens": 1024,
            }
            
            self.is_configured = True
            return True
            
        except Exception as e:
            st.error(f"❌ Error configurando Google AI: {e}")
            self.is_configured = False
            return False
    
    def is_available(self) -> bool:
        """Verificar si Google AI está disponible y configurado"""
        return GOOGLE_AI_AVAILABLE and self.is_configured
    
    # ========================================================================
    # PROMPTS ESPECIALIZADOS PARA ZAPOPAN
    # ========================================================================
    
    def _create_legal_prompt(self, query: str, context: List[Dict] = None) -> str:
        """Crear prompt especializado para consultas jurídicas"""
        base_prompt = f"""Eres un asistente especializado en regulaciones municipales de Zapopan, Jalisco.

CONTEXTO INSTITUCIONAL:
- Ayuntamiento de Zapopan, Jalisco
- Dirección de Inspección y Vigilancia
- Regulaciones municipales vigentes

CONSULTA DEL USUARIO:
"{query}"

INSTRUCCIONES:
1. Analiza la consulta e identifica las áreas regulatorias relevantes
2. Proporciona información precisa basada en regulaciones municipales
3. Si no conoces una regulación específica, indícalo claramente
4. Mantén un tono profesional y oficial
5. Estructura la respuesta en secciones claras

FORMATO DE RESPUESTA:
- Título: "Análisis de consulta normativa"
- Resumen ejecutivo (2-3 líneas)
- Regulaciones aplicables (lista con artículos)
- Procedimiento recomendado
- Dependencias responsables

RESPONDE EN ESPAÑOL."""

        if context:
            context_text = "\nCONTEXTO ADICIONAL:\n"
            for item in context[:3]:  # Limitar a 3 items de contexto
                context_text += f"- {item.get('reglamento', '')}: {item.get('contenido', '')[:100]}...\n"
            base_prompt += context_text
        
        return base_prompt
    
    def _create_citizen_service_prompt(self, query: str) -> str:
        """Crear prompt para atención ciudadana"""
        return f"""Eres un especialista en atención ciudadana del Ayuntamiento de Zapopan.

CONSULTA CIUDADANA:
"{query}"

OBJETIVO:
Orientar al ciudadano sobre procedimientos, regulaciones y dependencias relevantes.

INSTRUCCIONES:
1. Identifica el tipo de consulta (queja, solicitud, información)
2. Proporciona información clara y accesible
3. Indica pasos concretos a seguir
4. Menciona dependencias específicas
5. Ofrece horarios y contactos cuando sea relevante

TONO:
- Empático pero profesional
- Claro y directo
- Orientado a soluciones

RESPONDE EN ESPAÑOL."""
    
    # ========================================================================
    # FUNCIÓN PRINCIPAL DE CONSULTA
    # ========================================================================
    
    def query_google_ai(self, query: str, query_type: str = "general", 
                       context: List[Dict] = None) -> Dict:
        """
        Consultar a Google AI con fallback integrado
        
        Args:
            query: Texto de la consulta
            query_type: "legal", "citizen", o "general"
            context: Contexto adicional (resultados de búsqueda local)
        
        Returns:
            Dict con respuesta y metadatos
        """
        
        # Si Google AI no está disponible, retornar fallback inmediato
        if not self.is_available():
            return {
                "success": False,
                "source": "fallback",
                "message": "Google AI no disponible",
                "suggest_fallback": True
            }
        
        try:
            # Seleccionar prompt según tipo de consulta
            if query_type == "legal":
                prompt = self._create_legal_prompt(query, context)
            elif query_type == "citizen":
                prompt = self._create_citizen_service_prompt(query)
            else:
                prompt = self._create_legal_prompt(query, context)
            
            # Llamar a Google AI
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config
            )
            
            # Procesar respuesta
            if response and response.text:
                return {
                    "success": True,
                    "source": "google_ai",
                    "response": response.text,
                    "model": "gemini-1.5-flash",
                    "query_type": query_type,
                    "suggest_fallback": False
                }
            else:
                return {
                    "success": False,
                    "source": "google_ai_error",
                    "message": "Respuesta vacía de Google AI",
                    "suggest_fallback": True
                }
                
        except Exception as e:
            # Capturar cualquier error y sugerir fallback
            error_msg = str(e)
            
            # Errores comunes y sus soluciones
            if "API_KEY_INVALID" in error_msg:
                error_msg = "API key de Google AI inválida o expirada"
            elif "quota" in error_msg.lower():
                error_msg = "Límite de cuota alcanzado en Google AI"
            elif "429" in error_msg:
                error_msg = "Demasiadas solicitudes a Google AI"
            
            return {
                "success": False,
                "source": "google_ai_error",
                "message": f"Error en Google AI: {error_msg}",
                "suggest_fallback": True
            }
    
    # ========================================================================
    # FUNCIONES DE UTILIDAD
    # ========================================================================
    
    def get_status(self) -> Dict:
        """Obtener estado de la integración"""
        return {
            "google_ai_available": GOOGLE_AI_AVAILABLE,
            "configured": self.is_configured,
            "api_key_set": bool(self.api_key),
            "model_ready": bool(self.model)
        }
    
    def test_connection(self) -> Tuple[bool, str]:
        """Probar conexión con Google AI"""
        if not self.is_available():
            return False, "Google AI no configurado"
        
        try:
            # Consulta de prueba simple
            test_prompt = "Responde 'OK' si estás funcionando correctamente."
            response = self.model.generate_content(
                test_prompt,
                generation_config={"max_output_tokens": 10}
            )
            
            if response and response.text:
                return True, f"Conexión exitosa: {response.text.strip()}"
            else:
                return False, "Respuesta vacía"
                
        except Exception as e:
            return False, f"Error de conexión: {str(e)}"

# ============================================================================
# FUNCIONES PÚBLICAS
# ============================================================================

def create_google_ai_integration() -> GoogleAIIntegration:
    """Crear instancia de integración con Google AI"""
    
    # Intentar obtener API key de múltiples fuentes
    api_key = None
    
    # 1. Streamlit Secrets
    try:
        if hasattr(st, 'secrets') and 'GOOGLE_API_KEY' in st.secrets:
            api_key = st.secrets['GOOGLE_API_KEY']
    except:
        pass
    
    # 2. Variable de entorno
    if not api_key:
        api_key = os.environ.get("GOOGLE_API_KEY")
    
    # 3. Archivo de configuración local (solo desarrollo)
    if not api_key and os.path.exists(".streamlit/secrets.toml"):
        try:
            import toml
            with open(".streamlit/secrets.toml", "r") as f:
                secrets = toml.load(f)
                api_key = secrets.get("GOOGLE_API_KEY")
        except:
            pass
    
    return GoogleAIIntegration(api_key)

def hybrid_query(query: str, query_type: str = "general", 
                local_context: List[Dict] = None,
                google_ai_integration: GoogleAIIntegration = None) -> Dict:
    """
    Consulta híbrida: intenta Google AI primero, fallback a local
    
    Args:
        query: Texto de consulta
        query_type: Tipo de consulta
        local_context: Contexto local para fallback
        google_ai_integration: Instancia de integración (opcional)
    
    Returns:
        Dict con respuesta combinada
    """
    
    # Crear integración si no se proporciona
    if google_ai_integration is None:
        google_ai_integration = create_google_ai_integration()
    
    # Intentar Google AI primero
    google_ai_result = google_ai_integration.query_google_ai(
        query, query_type, local_context
    )
    
    # Si Google AI tuvo éxito, retornar resultado
    if google_ai_result["success"]:
        return {
            **google_ai_result,
            "strategy": "google_ai_primary",
            "fallback_used": False
        }
    
    # Si Google AI falló pero tenemos contexto local, usarlo
    if local_context and google_ai_result.get("suggest_fallback", False):
        return {
            "success": True,
            "source": "local_fallback",
            "response": _format_local_response(query, local_context),
            "strategy": "google_ai_fallback_to_local",
            "fallback_used": True,
            "google_ai_error": google_ai_result.get("message", "")
        }
    
    # Si no hay nada, retornar error
    return {
        "success": False,
        "source": "no_available_source",
        "message": "No hay fuentes disponibles para responder",
        "strategy": "failed_all_sources"
    }

def _format_local_response(query: str, local_context: List[Dict]) -> str:
    """Formatear respuesta local para consistencia"""
    if not local_context:
        return "No se encontraron regulaciones específicas para tu consulta."
    
    response = f"## 📋 **Resultados de la consulta**\n\n"
    response += f"**Consulta:** {query}\n\n"
    response += "### 📚 **Regulaciones aplicables (modo local):**\n\n"
    
    for i, item in enumerate(local_context[:5], 1):  # Limitar a 5 resultados
        response += f"{i}. **{item.get('reglamento', 'Reglamento')}**\n"
        response += f"   - **Artículo:** {item.get('articulo', 'N/A')}\n"
        response += f"   - **Contenido:** {item.get('contenido', '')}\n"
        response += f"   - **Dependencia:** {item.get('dependencia', 'N/A')}\n\n"
    
    response += "### ⚠️ **Nota:**\n"
    response += "Esta respuesta proviene de la base de conocimiento local. "
    response += "Para análisis más detallado, contacta al área correspondiente."
    
    return response

# ============================================================================
# PRUEBA RÁPIDA (solo si se ejecuta directamente)
# ============================================================================

if __name__ == "__main__":
    print("🔧 Probando módulo de integración Google AI...")
    
    # Crear instancia
    integration = create_google_ai_integration()
    
    # Mostrar estado
    status = integration.get_status()
    print(f"✅ Módulo cargado correctamente")
    print(f"   Google AI disponible: {status['google_ai_available']}")
    print(f"   Configurado: {status['configured']}")
    print(f"   API key configurada: {status['api_key_set']}")
    
    # Probar conexión si está configurado
    if status['configured']:
        success, message = integration.test_connection()
        print(f"   Conexión Google AI: {'✅' if success else '❌'} {message}")
    else:
        print("   ⚠️ Google AI no configurado (sin API key)")
    
    print("\n🎯 Módulo listo para integración en app.py")