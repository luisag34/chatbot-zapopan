"""
Integración con Google Cloud Vertex AI
Solución profesional para quotas generosas y menos restrictions
"""

import os
import json
import requests
from typing import Dict, Optional
import streamlit as st

# ============================================================================
# CONFIGURACIÓN VERTEX AI
# ============================================================================

class VertexAIChatbot:
    """Chatbot usando Vertex AI (Google Cloud profesional)"""
    
    def __init__(self, project_id: Optional[str] = None, location: str = "us-central1"):
        """
        Inicializar Vertex AI
        
        Args:
            project_id: Google Cloud Project ID
            location: Region (us-central1, europe-west4, etc.)
        """
        self.project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT")
        self.location = location
        self.endpoint = None
        self.access_token = None
        
        # Intentar obtener credenciales
        self._obtener_credenciales()
        
        # Configurar endpoint si tenemos credenciales
        if self.project_id and self.access_token:
            self.endpoint = f"https://{self.location}-aiplatform.googleapis.com/v1/projects/{self.project_id}/locations/{self.location}/publishers/google/models/gemini-2.0-flash:streamGenerateContent"
    
    def _obtener_credenciales(self):
        """Obtener credenciales de Google Cloud"""
        # Opción 1: Variable de entorno con access token
        self.access_token = os.environ.get("GOOGLE_CLOUD_ACCESS_TOKEN")
        
        # Opción 2: Application Default Credentials (ADC)
        if not self.access_token:
            try:
                import google.auth
                import google.auth.transport.requests
                
                # Obtener credenciales ADC
                credentials, project = google.auth.default(
                    scopes=["https://www.googleapis.com/auth/cloud-platform"]
                )
                
                # Obtener access token
                auth_req = google.auth.transport.requests.Request()
                credentials.refresh(auth_req)
                
                self.access_token = credentials.token
                if not self.project_id:
                    self.project_id = project
                    
                print(f"✅ Credenciales ADC obtenidas para proyecto: {self.project_id}")
                
            except ImportError:
                print("⚠️ google-auth library no instalada")
            except Exception as e:
                print(f"⚠️ Error obteniendo credenciales ADC: {e}")
        
        # Opción 3: Service account key file
        if not self.access_token:
            service_account_key_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
            if service_account_key_path and os.path.exists(service_account_key_path):
                try:
                    import google.oauth2.service_account
                    
                    credentials = google.oauth2.service_account.Credentials.from_service_account_file(
                        service_account_key_path,
                        scopes=["https://www.googleapis.com/auth/cloud-platform"]
                    )
                    
                    auth_req = google.auth.transport.requests.Request()
                    credentials.refresh(auth_req)
                    
                    self.access_token = credentials.token
                    
                    # Obtener project_id del archivo de credenciales
                    with open(service_account_key_path, 'r') as f:
                        key_data = json.load(f)
                        if not self.project_id:
                            self.project_id = key_data.get("project_id")
                    
                    print(f"✅ Credenciales service account obtenidas")
                    
                except Exception as e:
                    print(f"⚠️ Error con service account: {e}")
    
    def is_configured(self) -> bool:
        """Verificar si Vertex AI está configurado"""
        return bool(self.project_id and self.access_token and self.endpoint)
    
    def query(self, user_query: str, system_instructions: Optional[str] = None) -> Dict:
        """Consultar Vertex AI"""
        if not self.is_configured():
            return self._fallback_response("Vertex AI no configurado", user_query)
        
        try:
            # Preparar system instructions
            if not system_instructions:
                system_instructions = """Eres un experto en regulaciones municipales de Zapopan, Jalisco.
                
                Responde consultas sobre regulaciones municipales de Zapopan.
                Siempre cita reglamentos y artículos específicos.
                Formato: Reglamento de [Nombre], Art. X
                
                Sé preciso, claro y profesional."""
            
            # Preparar request para Vertex AI
            # Vertex AI usa estructura diferente a AI Studio
            contents = [
                {
                    "role": "user",
                    "parts": [{"text": f"{system_instructions}\n\nConsulta: {user_query}"}]
                }
            ]
            
            # Vertex AI parameters
            parameters = {
                "temperature": 0.1,
                "maxOutputTokens": 2048,  # Vertex AI permite más
                "topP": 0.8,
                "topK": 40
            }
            
            # Safety settings más permisivos en Vertex AI
            safety_settings = [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_LOW_AND_ABOVE"  # Más permisivo que BLOCK_NONE
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH", 
                    "threshold": "BLOCK_LOW_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_LOW_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_LOW_AND_ABOVE"
                }
            ]
            
            payload = {
                "contents": contents,
                "generationConfig": parameters,
                "safetySettings": safety_settings
            }
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.access_token}"
            }
            
            # Usar endpoint de streaming para mejor performance
            stream_endpoint = self.endpoint.replace(":streamGenerateContent", ":generateContent")
            
            print(f"🔍 Enviando a Vertex AI: {stream_endpoint}")
            
            response = requests.post(
                stream_endpoint,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Vertex AI tiene estructura diferente
                if "candidates" in data and data["candidates"]:
                    candidate = data["candidates"][0]
                    
                    if "content" in candidate and "parts" in candidate["content"]:
                        parts = candidate["content"]["parts"]
                        if parts and len(parts) > 0 and "text" in parts[0]:
                            text = parts[0]["text"]
                            
                            # Validar respuesta
                            if self._validar_respuesta(text):
                                return {
                                    "success": True,
                                    "response": text,
                                    "source": "vertex_ai",
                                    "using_ai": True,
                                    "model": "gemini-2.0-flash",
                                    "length": len(text)
                                }
            
            # Si llegamos aquí, hubo error
            error_msg = f"Vertex AI error: {response.status_code}"
            try:
                error_data = response.json()
                if "error" in error_data:
                    error_msg = error_data["error"].get("message", error_msg)
            except:
                pass
            
            return self._fallback_response(error_msg, user_query)
            
        except Exception as e:
            return self._fallback_response(f"Vertex AI exception: {str(e)[:80]}", user_query)
    
    def _validar_respuesta(self, texto: str) -> bool:
        """Validar calidad de respuesta Vertex AI"""
        if len(texto.strip()) < 100:
            return False
        
        texto_lower = texto.lower()
        
        # Criterios mínimos
        tiene_zapopan = "zapopan" in texto_lower
        tiene_reglamento = "reglamento" in texto_lower
        tiene_contenido = len(texto) > 200
        
        return tiene_zapopan and tiene_reglamento and tiene_contenido
    
    def _fallback_response(self, error_msg: str, consulta: str) -> Dict:
        """Fallback al sistema mejorado"""
        try:
            from fallback_mejorado import procesar_consulta_fallback_mejorado
            resultado = procesar_consulta_fallback_mejorado(consulta, "sistema")
            
            return {
                "success": True,
                "response": resultado["texto_visible"],
                "source": "fallback_mejorado",
                "using_ai": False,
                "error": error_msg,
                "length": len(resultado["texto_visible"])
            }
        except:
            # Fallback de emergencia
            texto = f"**Consulta:** {consulta}\n\n"
            texto += "**Orientación:** Contacta a Inspección y Vigilancia de Zapopan.\n"
            texto += "📞 33 3818-2200 ext. 5501\n"
            texto += "📧 inspeccion.vigilancia@zapopan.gob.mx\n\n"
            texto += f"*Nota técnica: {error_msg[:100]}*"
            
            return {
                "success": True,
                "response": texto,
                "source": "fallback_emergencia",
                "using_ai": False,
                "error": error_msg,
                "length": len(texto)
            }
    
    def get_status(self) -> Dict:
        """Obtener estado de Vertex AI"""
        return {
            "configured": self.is_configured(),
            "project_id": self.project_id,
            "location": self.location,
            "has_access_token": bool(self.access_token),
            "endpoint": self.endpoint
        }

# ============================================================================
# FUNCIÓN PRINCIPAL PARA APP
# ============================================================================

def crear_vertex_ai_chatbot() -> VertexAIChatbot:
    """Crear instancia de Vertex AI chatbot"""
    
    # Obtener configuración de Streamlit secrets
    project_id = None
    location = "us-central1"
    
    try:
        if hasattr(st, 'secrets'):
            # Vertex AI secrets
            if 'VERTEX_AI_PROJECT_ID' in st.secrets:
                project_id = st.secrets['VERTEX_AI_PROJECT_ID']
            if 'VERTEX_AI_LOCATION' in st.secrets:
                location = st.secrets['VERTEX_AI_LOCATION']
            
            # Access token directo (opcional)
            if 'GOOGLE_CLOUD_ACCESS_TOKEN' in st.secrets:
                os.environ['GOOGLE_CLOUD_ACCESS_TOKEN'] = st.secrets['GOOGLE_CLOUD_ACCESS_TOKEN']
            
            # Service account key (como JSON string)
            if 'GOOGLE_SERVICE_ACCOUNT_KEY_JSON' in st.secrets:
                # Guardar temporalmente en archivo
                import tempfile
                key_json = st.secrets['GOOGLE_SERVICE_ACCOUNT_KEY_JSON']
                with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                    f.write(key_json)
                    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = f.name
    except:
        pass
    
    # Variables de entorno
    if not project_id:
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    
    return VertexAIChatbot(project_id, location)

def procesar_consulta_vertex_ai(consulta: str, usuario: str) -> Dict:
    """
    Procesar consulta con Vertex AI
    Para usar en app.py
    """
    # Importar funciones locales
    from app import buscar_en_base_conocimiento, registrar_consulta_local
    
    # Buscar en base local
    resultados_locales = buscar_en_base_conocimiento(consulta)
    
    # Intentar Vertex AI
    chatbot = crear_vertex_ai_chatbot()
    
    if chatbot.is_configured():
        resultado = chatbot.query(consulta)
        
        if resultado["using_ai"]:
            # Registrar y retornar
            registrar_consulta_local(consulta, resultados_locales, usuario)
            
            return {
                "texto_visible": resultado["response"],
                "resultados": resultados_locales,
                "categoria": "vertex_ai",
                "fuente": resultado["source"],
                "usando_ai": True,
                "longitud": resultado["length"]
            }
    
    # Fallback al sistema mejorado
    from fallback_mejorado import procesar_consulta_fallback_mejorado
    return procesar_consulta_fallback_mejorado(consulta, usuario)

# ============================================================================
# PRUEBA RÁPIDA
# ============================================================================

if __name__ == "__main__":
    print("🚀 VERTEX AI INTEGRATION TEST")
    print("=" * 60)
    
    # Configurar variables de entorno para prueba
    # NOTA: Necesitas configurar estas variables en tu entorno
    # export GOOGLE_CLOUD_PROJECT="tu-project-id"
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"
    
    chatbot = crear_vertex_ai_chatbot()
    
    status = chatbot.get_status()
    print(f"🔧 Estado Vertex AI:")
    print(f"   • Configurado: {status['configured']}")
    print(f"   • Project ID: {status['project_id']}")
    print(f"   • Location: {status['location']}")
    print(f"   • Access token: {'✅' if status['has_access_token'] else '❌'}")
    print(f"   • Endpoint: {status['endpoint']}")
    
    if status['configured']:
        print(f"\n🎯 Probando consulta...")
        
        consulta = "ruido de restaurante por la noche en Zapopan"
        print(f"📋 Consulta: {consulta}")
        
        resultado = chatbot.query(consulta)
        
        print(f"\n📊 Resultado:")
        print(f"   • Éxito: {resultado['success']}")
        print(f"   • Usando AI: {resultado['using_ai']}")
        print(f"   • Fuente: {resultado['source']}")
        print(f"   • Longitud: {resultado['length']} caracteres")
        
        if resultado['using_ai']:
            print(f"\n🎯 RESPUESTA VERTEX AI (primeras 400 chars):")
            print("=" * 70)
            print(resultado['response'][:400] + ("..." if len(resultado['response']) > 400 else ""))
            print("=" * 70)
            
            # Análisis
            texto = resultado['response'].lower()
            print(f"\n📈 Calidad:")
            print(f"   • Zapopan: {'✅' if 'zapopan' in texto else '❌'}")
            print(f"   • Reglamento: {'✅' if 'reglamento' in texto else '❌'}")
            print(f"   • Artículo: {'✅' if 'artículo' in texto or 'art.' in texto else '❌'}")
            print(f"   • Longitud adecuada: {'✅' if resultado['length'] > 300 else '❌'}")
            
            if 'zapopan' in texto and 'reglamento' in texto and resultado['length'] > 300:
                print(f"\n🎯 ¡VERTEX AI FUNCIONA CORRECTAMENTE!")
            else:
                print(f"\n⚠️ Respuesta mejorable")
        else:
            print(f"\n🔧 Fallback activado: {resultado.get('error', 'N/A')}")
            print(f"📝 Respuesta (primeras 200 chars):")
            print(resultado['response'][:200] + "...")
    else:
        print(f"\n❌ Vertex AI no configurado")
        print(f"💡 Para configurar:")
        print(f"   1. export GOOGLE_CLOUD_PROJECT='tu-project-id'")
        print(f"   2. export GOOGLE_APPLICATION_CREDENTIALS='/path/to/key.json'")
        print(f"   3. Habilitar Vertex AI API en Google Cloud Console")
    
    print("\n" + "=" * 60)
    print("🔧 Módulo Vertex AI listo para integración")