"""
Módulo de integración con Chatbot Zapopan de Google AI Studio
Conecta directamente al chatbot específico que Luis ya configuró
"""

import os
import json
from typing import Dict, Optional
import streamlit as st

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

class ChatbotZapopanIntegration:
    """Integración con chatbot específico de Google AI Studio"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Inicializar con API key del chatbot"""
        self.api_key = api_key or os.environ.get("GOOGLE_API_KEY")
        self.endpoint = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
        self.is_configured = bool(self.api_key)
        
    def is_available(self) -> bool:
        """Verificar si está configurado"""
        return self.is_configured
    
    def query_chatbot(self, query: str, context: str = "") -> Dict:
        """
        Consultar al chatbot de Google AI Studio
        
        Args:
            query: Consulta del usuario
            context: Contexto adicional (opcional)
        
        Returns:
            Dict con respuesta y metadatos
        """
        
        if not self.is_available():
            return {
                "success": False,
                "source": "not_configured",
                "message": "API key no configurada",
                "suggest_fallback": True
            }
        
        try:
            import requests
            
            # Preparar headers
            headers = {
                "Content-Type": "application/json",
                "x-goog-api-key": self.api_key
            }
            
            # Preparar payload para el chatbot
            # NOTA: Luis debe proporcionar la estructura exacta que usa su chatbot
            payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": query}
                        ]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.2,
                    "topP": 0.8,
                    "topK": 40,
                    "maxOutputTokens": 1024,
                }
            }
            
            # Si hay contexto, agregarlo
            if context:
                # Dependiendo de cómo esté configurado el chatbot
                # Podría necesitar agregarse de forma diferente
                pass
            
            # Llamar a la API
            response = requests.post(
                self.endpoint,
                headers=headers,
                json=payload,
                timeout=30  # 30 segundos timeout
            )
            
            # Procesar respuesta
            if response.status_code == 200:
                response_data = response.json()
                
                # Extraer texto de respuesta
                # NOTA: Estructura puede variar según configuración del chatbot
                if "candidates" in response_data and response_data["candidates"]:
                    text = response_data["candidates"][0]["content"]["parts"][0]["text"]
                    
                    return {
                        "success": True,
                        "source": "chatbot_zapopan",
                        "response": text,
                        "model": "chatbot-zapopan-custom",
                        "raw_response": response_data
                    }
                else:
                    return {
                        "success": False,
                        "source": "chatbot_error",
                        "message": "Respuesta vacía del chatbot",
                        "raw_response": response_data,
                        "suggest_fallback": True
                    }
            
            else:
                # Manejar errores HTTP
                error_msg = f"HTTP {response.status_code}"
                try:
                    error_data = response.json()
                    if "error" in error_data:
                        error_msg = error_data["error"].get("message", error_msg)
                except:
                    pass
                
                return {
                    "success": False,
                    "source": "http_error",
                    "message": f"Error del chatbot: {error_msg}",
                    "status_code": response.status_code,
                    "suggest_fallback": True
                }
                
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "source": "timeout",
                "message": "Timeout al conectar con el chatbot",
                "suggest_fallback": True
            }
            
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "source": "connection_error",
                "message": "Error de conexión con el chatbot",
                "suggest_fallback": True
            }
            
        except Exception as e:
            return {
                "success": False,
                "source": "exception",
                "message": f"Error inesperado: {str(e)[:100]}",
                "suggest_fallback": True
            }
    
    def get_status(self) -> Dict:
        """Obtener estado de la integración"""
        return {
            "configured": self.is_configured,
            "api_key_set": bool(self.api_key),
            "endpoint": self.endpoint
        }
    
    def test_connection(self) -> tuple[bool, str]:
        """Probar conexión con el chatbot"""
        if not self.is_available():
            return False, "API key no configurada"
        
        # Consulta de prueba simple
        test_result = self.query_chatbot("Responde 'OK' si estás funcionando.")
        
        if test_result["success"]:
            return True, f"Conexión exitosa: {test_result['response'][:50]}..."
        else:
            return False, f"Error: {test_result.get('message', 'Desconocido')}"

# ============================================================================
# FUNCIONES PÚBLICAS
# ============================================================================

def create_chatbot_integration() -> ChatbotZapopanIntegration:
    """Crear instancia de integración con el chatbot"""
    
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
    
    return ChatbotZapopanIntegration(api_key)

def hybrid_query_with_fallback(query: str, 
                              chatbot_integration: ChatbotZapopanIntegration = None,
                              fallback_function = None) -> Dict:
    """
    Consulta híbrida: intenta chatbot primero, fallback a función local
    
    Args:
        query: Texto de consulta
        chatbot_integration: Instancia de integración (opcional)
        fallback_function: Función para fallback (debe retornar Dict con "texto_visible")
    
    Returns:
        Dict con respuesta combinada
    """
    
    # Crear integración si no se proporciona
    if chatbot_integration is None:
        chatbot_integration = create_chatbot_integration()
    
    # Intentar chatbot primero
    chatbot_result = chatbot_integration.query_chatbot(query)
    
    # Si chatbot tuvo éxito, retornar resultado
    if chatbot_result["success"]:
        return {
            **chatbot_result,
            "strategy": "chatbot_primary",
            "fallback_used": False,
            "texto_visible": chatbot_result["response"]
        }
    
    # Si chatbot falló pero tenemos fallback function, usarla
    if fallback_function and chatbot_result.get("suggest_fallback", False):
        fallback_result = fallback_function(query)
        
        return {
            "success": True,
            "source": "local_fallback",
            "response": fallback_result.get("texto_visible", "No hay respuesta disponible."),
            "strategy": "chatbot_fallback_to_local",
            "fallback_used": True,
            "chatbot_error": chatbot_result.get("message", ""),
            "texto_visible": fallback_result.get("texto_visible", "No hay respuesta disponible.")
        }
    
    # Si no hay nada, retornar error
    return {
        "success": False,
        "source": "no_available_source",
        "message": "No hay fuentes disponibles para responder",
        "strategy": "failed_all_sources",
        "texto_visible": "Lo siento, el sistema no está disponible en este momento. Por favor, intenta más tarde."
    }

# ============================================================================
# PRUEBA RÁPIDA
# ============================================================================

if __name__ == "__main__":
    print("🔧 Probando módulo de integración Chatbot Zapopan...")
    
    # Crear instancia
    integration = create_chatbot_integration()
    
    # Mostrar estado
    status = integration.get_status()
    print(f"✅ Módulo cargado correctamente")
    print(f"   Configurado: {status['configured']}")
    print(f"   API key configurada: {status['api_key_set']}")
    print(f"   Endpoint: {status['endpoint']}")
    
    # Probar conexión si está configurado
    if status['configured']:
        success, message = integration.test_connection()
        print(f"   Conexión chatbot: {'✅' if success else '❌'} {message}")
    else:
        print("   ⚠️ Chatbot no configurado (sin API key)")
    
    print("\n🎯 Módulo listo para integración en app.py")
    print("💡 NOTA: Necesita información específica del chatbot de Luis")