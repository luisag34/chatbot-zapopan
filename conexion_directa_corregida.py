"""
CONEXIÓN DIRECTA CORREGIDA A GOOGLE AI STUDIO
Versión corregida con:
1. Modelo gemini-2.5-flash (disponible)
2. Mejor manejo de API Key desde Streamlit Secrets
"""

import os
import json
import requests
from typing import Dict, Optional

def cargar_system_instructions_completas() -> str:
    """Cargar System Instructions completas del archivo"""
    try:
        with open("system_instructions_completas_zapopan.txt", "r", encoding="utf-8") as f:
            return f.read()
    except:
        # Fallback a versión resumida
        return """SISTEMA DE CONSULTA NORMATIVA ZAPOPAN - PROTOCOLO DE RESPUESTA (5 PASOS)"""

class ConexionDirectaCorregida:
    """Conexión directa CORREGIDA al chatbot de Google AI Studio"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Inicializar conexión directa CORREGIDA
        
        Args:
            api_key: API Key de Google AI Studio
        """
        self.api_key = api_key
        
        # USAR MODELO DISPONIBLE según diagnóstico
        # gemini-2.0-flash → DEPRECATED para nuevos usuarios
        # gemini-2.5-flash → DISPONIBLE (según diagnóstico)
        self.model = "gemini-2.5-flash"
        self.endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"
        
        self.system_instructions = cargar_system_instructions_completas()
        
        print(f"🔧 Conexión directa CORREGIDA configurada")
        print(f"   Modelo: {self.model} (disponible)")
        print(f"   API Key: {'✅ Configurada' if self.api_key else '❌ NO configurada'}")
        print(f"   System Instructions: {len(self.system_instructions):,} caracteres")
    
    def is_configured(self) -> bool:
        """Verificar si está configurado"""
        return bool(self.api_key)
    
    def query(self, user_query: str) -> Dict:
        """Consultar Google AI Studio directamente con modelo CORREGIDO"""
        if not self.is_configured():
            return self._fallback_response("API Key no configurada", user_query)
        
        try:
            # Preparar el prompt con System Instructions completas
            full_prompt = f"{self.system_instructions}\n\nCONSULTA DEL USUARIO: {user_query}\n\nRESPONDER SIGUIENDO EXACTAMENTE EL PROTOCOLO DE RESPUESTA (5 pasos)."
            
            # Preparar request para Gemini API con modelo CORREGIDO
            payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": full_prompt}
                        ]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.1,
                    "maxOutputTokens": 2048,  # Suficiente para respuestas completas
                    "topP": 0.8,
                    "topK": 40
                },
                "safetySettings": [
                    {
                        "category": "HARM_CATEGORY_HARASSMENT",
                        "threshold": "BLOCK_NONE"  # Menos restrictivo
                    },
                    {
                        "category": "HARM_CATEGORY_HATE_SPEECH", 
                        "threshold": "BLOCK_NONE"
                    },
                    {
                        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                        "threshold": "BLOCK_NONE"
                    },
                    {
                        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                        "threshold": "BLOCK_NONE"
                    }
                ]
            }
            
            headers = {
                "Content-Type": "application/json"
            }
            
            # URL con API Key - MODELO CORREGIDO
            url = f"{self.endpoint}?key={self.api_key}"
            
            print(f"🔍 Enviando a Google AI Studio: {self.model} (CORREGIDO)")
            
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Extraer texto de respuesta
                if "candidates" in data and len(data["candidates"]) > 0:
                    candidate = data["candidates"][0]
                    if "content" in candidate and "parts" in candidate["content"]:
                        parts = candidate["content"]["parts"]
                        if len(parts) > 0 and "text" in parts[0]:
                            response_text = parts[0]["text"]
                            
                            # Verificar que siga el protocolo
                            sigue_protocolo = self._verificar_protocolo(response_text)
                            
                            return {
                                "response": response_text,
                                "source": "google_ai_studio_corregido",
                                "using_ai": True,
                                "length": len(response_text),
                                "sigue_protocolo": sigue_protocolo,
                                "model": self.model
                            }
                
                # Si no se pudo extraer respuesta
                return self._fallback_response("Error extrayendo respuesta de AI Studio", user_query)
                
            else:
                error_msg = f"Error {response.status_code}: {response.text}"
                print(f"❌ Error AI Studio (corregido): {error_msg}")
                
                # Análisis específico de errores
                if response.status_code == 404:
                    print("⚠️  Error 404: Modelo no encontrado")
                    print(f"   Modelo probado: {self.model}")
                    print("   Posibles soluciones:")
                    print("   1. Probar gemini-flash-latest")
                    print("   2. Probar gemini-2.5-pro")
                    print("   3. Verificar disponibilidad en región")
                
                return self._fallback_response(f"Error AI Studio: {response.status_code}", user_query)
                
        except requests.exceptions.Timeout:
            return self._fallback_response("Timeout consultando AI Studio", user_query)
        except requests.exceptions.ConnectionError:
            return self._fallback_response("Error de conexión con AI Studio", user_query)
        except Exception as e:
            print(f"❌ Error inesperado AI Studio (corregido): {e}")
            return self._fallback_response(f"Error inesperado: {str(e)[:100]}", user_query)
    
    def _verificar_protocolo(self, respuesta: str) -> bool:
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
    
    def _fallback_response(self, error: str, user_query: str) -> Dict:
        """Respuesta de fallback"""
        return {
            "response": f"""🔧 **CONEXIÓN CON CHATBOT ZAPOPAN - CONFIGURACIÓN CORREGIDA**

**Estado:** {error}

**Consulta recibida:** "{user_query}"

**Modelo probado:** {self.model}

**Para consultas sobre antenas de celulares:**
1. **Competencia federal:** Instituto Federal de Telecomunicaciones (IFT)
2. **Competencia municipal:** Verificación de permisos de construcción
3. **Acción recomendada:** Presentar queja en Dirección de Inspección y Vigilancia

**Contacto Inspección y Vigilancia:**
📞 33 3818-2200 ext. 3312, 3313, 3322, 3324
📧 inspeccion.vigilancia@zapopan.gob.mx

*El sistema con protocolo completo de consulta normativa estará disponible en breve.*""",
            "source": "fallback_corregido",
            "using_ai": False,
            "length": 0,
            "sigue_protocolo": False,
            "model": self.model
        }
    
    def get_status(self) -> Dict:
        """Obtener estado de la conexión"""
        return {
            "configured": self.is_configured(),
            "has_api_key": bool(self.api_key),
            "model": self.model,
            "model_disponible": True,  # Según diagnóstico
            "system_instructions_length": len(self.system_instructions),
            "endpoint": self.endpoint
        }

# ============================================================================
# FUNCIÓN PRINCIPAL PARA APP.PY (VERSIÓN FUTURA)
# ============================================================================

def procesar_consulta_corregida_ai_studio(consulta: str, usuario: str) -> Dict:
    """
    Procesar consulta usando conexión directa CORREGIDA a Google AI Studio
    Para usar en app.py después de arreglar problemas
    """
    # Obtener API Key de Secrets de Streamlit
    api_key = None
    
    # IMPORTANTE: En Streamlit Cloud, esto debería funcionar:
    # api_key = st.secrets.get("GOOGLE_API_KEY")
    
    # Para prueba local, usar variable de entorno
    if not api_key:
        api_key = os.environ.get("GOOGLE_API_KEY")
    
    # Inicializar conexión CORREGIDA
    conexion = ConexionDirectaCorregida(api_key)
    
    # Procesar consulta
    resultado = conexion.query(consulta)
    
    # Determinar indicador
    if resultado["using_ai"]:
        if resultado["sigue_protocolo"]:
            indicador = f"🤖 Chatbot Zapopan AI Studio • ✅ Protocolo específico ({resultado['model']})"
        else:
            indicador = f"🤖 Chatbot Zapopan AI Studio • ⚠️ Respuesta básica ({resultado['model']})"
    else:
        indicador = f"🔧 Sistema en configuración • {resultado['model']} en prueba"
    
    return {
        "texto_visible": resultado["response"],
        "resultados": [],
        "categoria": "ai_studio_corregido",
        "fuente": resultado["source"],
        "indicador": indicador,
        "usando_ai": resultado["using_ai"],
        "sigue_protocolo": resultado.get("sigue_protocolo", False)
    }

# ============================================================================
# PRUEBA CON API KEY REAL
# ============================================================================

if __name__ == "__main__":
    print("🔧 PRUEBA CONEXIÓN DIRECTA CORREGIDA")
    print("=" * 60)
    
    # Usar API Key del diagnóstico
    api_key = "AIzaSyBMBqkKa_nSEwc7MNpjDtsp_4SpuD1TxXc"
    
    if not api_key:
        print("⚠️  Configura API Key para prueba:")
        print("   export GOOGLE_API_KEY='tu-api-key'")
        print("   o pasa como argumento")
    
    conexion = ConexionDirectaCorregida(api_key)
    
    status = conexion.get_status()
    print(f"📊 Estado: {status}")
    
    if status["configured"]:
        print("\n🔍 Probando consulta: 'prueba de conexión con modelo corregido'")
        resultado = conexion.query("prueba de conexión con modelo corregido")
        
        print(f"✅ Respuesta recibida: {resultado['using_ai']}")
        print(f"📊 Longitud: {resultado['length']} caracteres")
        print(f"🔍 Sigue protocolo: {resultado['sigue_protocolo']}")
        print(f"🎯 Fuente: {resultado['source']}")
        print(f"🤖 Modelo usado: {resultado['model']}")
        
        if resultado["using_ai"]:
            print("\n🎉 ¡CONEXIÓN CORREGIDA FUNCIONA!")
            print("   El sistema debería dar respuestas idénticas a tu chatbot AI Studio")
            
            print("\n📋 Primeros 500 caracteres de respuesta:")
            print("-" * 60)
            print(resultado["response"][:500] + "...")
            print("-" * 60)
        else:
            print("\n⚠️  Conexión falló, usando fallback")
            print("   Verificar:")
            print("   1. API Key válida")
            print("   2. Modelo disponible")
            print("   3. Quota disponible")
    else:
        print("❌ No configurado - necesita API Key")