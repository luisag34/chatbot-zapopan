"""
Integración simple con Chatbot Zapopan de Google AI Studio
Versión minimalista para deployment rápido
"""

import os
import json
import requests
from typing import Dict, Optional
import streamlit as st

class ChatbotZapopanSimple:
    """Integración simple con chatbot específico"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("GOOGLE_API_KEY")
        self.endpoint = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
        self.is_configured = bool(self.api_key)
    
    def is_available(self) -> bool:
        return self.is_configured
    
    def query(self, user_query: str) -> Dict:
        """Consulta simple al chatbot"""
        if not self.is_available():
            return self._fallback_response("API key no configurada")
        
        try:
            headers = {
                "Content-Type": "application/json",
                "x-goog-api-key": self.api_key
            }
            
            payload = {
                "contents": [{"parts": [{"text": user_query}]}],
                "generationConfig": {
                    "temperature": 0.2,
                    "topP": 0.8,
                    "topK": 40,
                    "maxOutputTokens": 1024,
                }
            }
            
            response = requests.post(
                self.endpoint,
                headers=headers,
                json=payload,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                if "candidates" in data and data["candidates"]:
                    text = data["candidates"][0]["content"]["parts"][0]["text"]
                    return {
                        "success": True,
                        "response": text,
                        "source": "chatbot_zapopan",
                        "using_ai": True
                    }
            
            # Si llegamos aquí, hubo error
            return self._fallback_response(f"Error del chatbot: HTTP {response.status_code}")
            
        except Exception as e:
            return self._fallback_response(f"Error de conexión: {str(e)[:80]}")
    
    def _fallback_response(self, error_msg: str) -> Dict:
        """Respuesta de fallback cuando el chatbot falla"""
        return {
            "success": True,  # Aún así damos respuesta
            "response": f"🔧 **Sistema temporalmente en modo local**\n\n"
                       f"*Nota: El chatbot principal no está disponible ({error_msg}).*\n\n"
                       f"**Consulta procesada con base de conocimiento local.**\n\n"
                       f"Para consultas más precisas, contacta a la Dirección de Inspección y Vigilancia.",
            "source": "local_fallback",
            "using_ai": False
        }

def create_chatbot() -> ChatbotZapopanSimple:
    """Crear instancia del chatbot"""
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
    
    return ChatbotZapopanSimple(api_key)

# Función principal para usar en app.py
def procesar_consulta_con_chatbot(consulta: str, usuario: str):
    """Procesar consulta usando el chatbot de AI Studio"""
    from app import buscar_en_base_conocimiento, registrar_consulta_local
    
    # Crear chatbot
    chatbot = create_chatbot()
    
    # Intentar chatbot primero
    resultado = chatbot.query(consulta)
    
    # Buscar también en base local para contexto/fallback
    resultados_locales = buscar_en_base_conocimiento(consulta)
    
    # Registrar consulta
    registrar_consulta_local(consulta, resultados_locales, usuario)
    
    # Preparar respuesta
    if resultado["using_ai"]:
        return {
            "texto_visible": resultado["response"],
            "resultados": resultados_locales,
            "categoria": "chatbot_ai",
            "fuente": "chatbot_zapopan",
            "usando_ai": True
        }
    else:
        # Fallback a respuesta local
        from app import procesar_consulta_local
        return procesar_consulta_local(consulta, usuario)