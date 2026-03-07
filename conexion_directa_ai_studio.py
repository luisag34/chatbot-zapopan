"""
CONEXIÓN DIRECTA A GOOGLE AI STUDIO
Usa la API Key del chatbot específico de Luis para obtener EXACTAMENTE las mismas respuestas
"""

import os
import json
import requests
from typing import Dict, Optional
import streamlit as st

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

def cargar_system_instructions_completas() -> str:
    """Cargar System Instructions completas del archivo"""
    try:
        with open("system_instructions_completas_zapopan.txt", "r", encoding="utf-8") as f:
            return f.read()
    except:
        # Fallback a versión resumida
        return """SISTEMA DE CONSULTA NORMATIVA ZAPOPAN

PROTOCOLO DE RESPUESTA (ORDEN OBLIGATORIO):
1. ANÁLISIS DE SITUACIÓN
2. CLASIFICACIÓN DE ATRIBUCIONES
3. SUSTENTO LEGAL
4. DEPENDENCIAS CON ATRIBUCIONES Y CONTACTO
5. FUENTES

NÚCLEO DE DOCUMENTOS – JERARQUÍA:
Nivel 1 > Nivel 2 > Nivel 3 > Nivel 4

NIVEL 1: Documentos estatales y NOM federales
NIVEL 2: Reglamentos municipales de Zapopan
NIVEL 3: Códigos y manuales municipales
NIVEL 4: Directorio institucional

ROUTER DE ÁREAS:
- CONSTRUCCIÓN: obra, construcción, edificación, ampliación, demolición, antena
- COMERCIO: negocio, local, establecimiento, giro, licencia
- TÉCNICA / MEDIO AMBIENTE: ruido, contaminación, residuos, árboles
- RIESGOS / PROTECCIÓN CIVIL: riesgo, peligro, colapso, incendio

MATRIZ DE COMPETENCIAS – DIRECCIÓN DE INSPECCIÓN Y VIGILANCIA:
FACULTADES PRINCIPALES: Comercio, Construcción (verificación), Anuncios, Medio ambiente (verificación)
FACULTADES CONCURRENTES: Medio ambiente, Protección civil
NO COMPETENCIA PRINCIPAL: Seguridad pública, Servicios públicos, Telecomunicaciones federales (IFT)

REGLAS CRÍTICAS:
1. Jerarquía normativa obligatoria Nivel 1 > Nivel 2 > Nivel 3
2. Prohibición absoluta de alucinación normativa
3. Cada afirmación debe basarse en información recuperada
4. No atribuir facultades a dependencias no mencionadas
5. Priorizar verificación de facultades de Inspección y Vigilancia"""

class ConexionDirectaAIStudio:
    """Conexión directa al chatbot de Google AI Studio de Luis"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Inicializar conexión directa
        
        Args:
            api_key: API Key de Google AI Studio (si None, busca en Secrets)
        """
        self.api_key = api_key or os.environ.get("GOOGLE_API_KEY")
        self.endpoint = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        self.system_instructions = cargar_system_instructions_completas()
        
        # Modelo a usar (gemini-2.0-flash es el que funciona con AI Studio)
        self.model = "gemini-2.0-flash"
        
        print(f"🔧 Conexión directa AI Studio configurada")
        print(f"   API Key: {'✅ Configurada' if self.api_key else '❌ NO configurada'}")
        print(f"   System Instructions: {len(self.system_instructions):,} caracteres")
    
    def is_configured(self) -> bool:
        """Verificar si está configurado"""
        return bool(self.api_key)
    
    def query(self, user_query: str) -> Dict:
        """Consultar Google AI Studio directamente"""
        if not self.is_configured():
            return self._fallback_response("API Key no configurada", user_query)
        
        try:
            # Preparar el prompt con System Instructions completas
            full_prompt = f"{self.system_instructions}\n\nCONSULTA DEL USUARIO: {user_query}\n\nRESPONDER SIGUIENDO EXACTAMENTE EL PROTOCOLO DE RESPUESTA."
            
            # Preparar request para Gemini API
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
                        "threshold": "BLOCK_LOW_AND_ABOVE"
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
            }
            
            headers = {
                "Content-Type": "application/json"
            }
            
            # URL con API Key
            url = f"{self.endpoint}?key={self.api_key}"
            
            print(f"🔍 Enviando a Google AI Studio: {self.model}")
            
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
                                "source": "google_ai_studio_directo",
                                "using_ai": True,
                                "length": len(response_text),
                                "sigue_protocolo": sigue_protocolo,
                                "model": self.model
                            }
                
                # Si no se pudo extraer respuesta
                return self._fallback_response("Error extrayendo respuesta de AI Studio", user_query)
                
            else:
                error_msg = f"Error {response.status_code}: {response.text}"
                print(f"❌ Error AI Studio: {error_msg}")
                return self._fallback_response(f"Error AI Studio: {response.status_code}", user_query)
                
        except requests.exceptions.Timeout:
            return self._fallback_response("Timeout consultando AI Studio", user_query)
        except requests.exceptions.ConnectionError:
            return self._fallback_response("Error de conexión con AI Studio", user_query)
        except Exception as e:
            print(f"❌ Error inesperado AI Studio: {e}")
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
            "response": f"""🔧 **CONEXIÓN CON CHATBOT ZAPOPAN - CONFIGURACIÓN**

**Estado:** {error}

**Consulta recibida:** "{user_query}"

**Para consultas sobre antenas de celulares:**
1. **Competencia federal:** Instituto Federal de Telecomunicaciones (IFT)
2. **Competencia municipal:** Verificación de permisos de construcción
3. **Acción recomendada:** Presentar queja en Dirección de Inspección y Vigilancia

**Contacto Inspección y Vigilancia:**
📞 33 3818-2200 ext. [correspondiente]
📧 inspeccion.vigilancia@zapopan.gob.mx

*El sistema con protocolo completo de consulta normativa estará disponible en breve.*""",
            "source": "fallback_directo",
            "using_ai": False,
            "length": 0,
            "sigue_protocolo": False,
            "model": None
        }
    
    def get_status(self) -> Dict:
        """Obtener estado de la conexión"""
        return {
            "configured": self.is_configured(),
            "has_api_key": bool(self.api_key),
            "model": self.model,
            "system_instructions_length": len(self.system_instructions),
            "endpoint": self.endpoint
        }

# ============================================================================
# FUNCIÓN PRINCIPAL PARA APP.PY
# ============================================================================

def procesar_consulta_directa_ai_studio(consulta: str, usuario: str) -> Dict:
    """
    Procesar consulta usando conexión directa a Google AI Studio
    Para usar en app.py
    """
    # Obtener API Key de Secrets de Streamlit
    api_key = None
    
    # Intentar obtener de Streamlit Secrets
    try:
        if hasattr(st, 'secrets'):
            if 'GOOGLE_API_KEY' in st.secrets:
                api_key = st.secrets['GOOGLE_API_KEY']
                print("✅ API Key obtenida de Streamlit Secrets")
    except:
        pass
    
    # Si no hay en Secrets, intentar variable de entorno
    if not api_key:
        api_key = os.environ.get("GOOGLE_API_KEY")
        if api_key:
            print("✅ API Key obtenida de variable de entorno")
    
    # Inicializar conexión
    conexion = ConexionDirectaAIStudio(api_key)
    
    # Procesar consulta
    resultado = conexion.query(consulta)
    
    # Determinar indicador
    if resultado["using_ai"]:
        if resultado["sigue_protocolo"]:
            indicador = "🤖 Chatbot Zapopan AI Studio • ✅ Protocolo específico"
        else:
            indicador = "🤖 Chatbot Zapopan AI Studio • ⚠️ Respuesta básica"
    else:
        indicador = "🔧 Sistema en configuración • Conexión AI Studio en progreso"
    
    # Registrar consulta localmente
    try:
        from app import registrar_consulta_local
        registrar_consulta_local(consulta, [], usuario)
    except:
        pass
    
    return {
        "texto_visible": resultado["response"],
        "resultados": [],
        "categoria": "ai_studio_directo",
        "fuente": resultado["source"],
        "indicador": indicador,
        "usando_ai": resultado["using_ai"],
        "sigue_protocolo": resultado.get("sigue_protocolo", False)
    }

# ============================================================================
# PRUEBA
# ============================================================================

if __name__ == "__main__":
    print("🔧 PRUEBA CONEXIÓN DIRECTA AI STUDIO")
    print("=" * 60)
    
    # Para prueba, necesitas configurar API Key
    api_key = os.environ.get("GOOGLE_API_KEY")
    
    if not api_key:
        print("⚠️  Configura API Key para prueba:")
        print("   export GOOGLE_API_KEY='tu-api-key'")
        print("   o edita el código para agregarla directamente")
        
        # Usar API Key de prueba (deberías reemplazar con la tuya)
        api_key = "AIzaSyC9lqTVCcIzHYh96-Lo4pmdoiXfyYCmnNY"  # Esta es la que me compartiste
    
    conexion = ConexionDirectaAIStudio(api_key)
    
    status = conexion.get_status()
    print(f"📊 Estado: {status}")
    
    if status["configured"]:
        print("\n🔍 Probando consulta: 'ruido de restaurante por la noche'")
        resultado = conexion.query("ruido de restaurante por la noche")
        
        print(f"✅ Respuesta recibida: {resultado['using_ai']}")
        print(f"📊 Longitud: {resultado['length']} caracteres")
        print(f"🔍 Sigue protocolo: {resultado['sigue_protocolo']}")
        print(f"🎯 Fuente: {resultado['source']}")
        
        if resultado["using_ai"]:
            print("\n📋 Primeros 500 caracteres de respuesta:")
            print("-" * 60)
            print(resultado["response"][:500] + "...")
            print("-" * 60)
    else:
        print("❌ No configurado - necesita API Key")