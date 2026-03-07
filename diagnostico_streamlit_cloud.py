#!/usr/bin/env python3
"""
DIAGNÓSTICO COMPLETO - POR QUÉ NO FUNCIONA GOOGLE AI STUDIO EN STREAMLIT CLOUD
"""

import os
import sys
import json
import requests

def test_api_key_directamente(api_key: str):
    """Testear API Key directamente con Google AI Studio"""
    print("=" * 70)
    print("🔍 TESTEANDO API KEY DIRECTAMENTE")
    print("=" * 70)
    
    if not api_key:
        print("❌ No hay API Key para probar")
        return False
    
    # Endpoint de prueba
    endpoint = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    url = f"{endpoint}?key={api_key}"
    
    # Payload simple
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": "Responde 'OK' si estás funcionando."}
                ]
            }
        ],
        "generationConfig": {
            "maxOutputTokens": 10
        }
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        print(f"🔗 Probando endpoint: {endpoint}")
        print(f"🔑 API Key: {api_key[:10]}...{api_key[-10:]}")
        
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=10
        )
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API Key FUNCIONA correctamente")
            print(f"📋 Respuesta: {data}")
            return True
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            
            # Análisis de errores comunes
            if response.status_code == 400:
                print("⚠️  Error 400: Bad Request - Posible formato incorrecto del payload")
            elif response.status_code == 403:
                error_data = json.loads(response.text)
                if "leaked" in error_data.get("error", {}).get("message", "").lower():
                    print("🚨 API Key REPORTADA COMO LEAKED (filtrada)")
                    print("   Google bloqueó esta key por seguridad")
                    print("   Necesitas generar una NUEVA API Key")
                else:
                    print("⚠️  Error 403: Permission Denied - API Key inválida o sin permisos")
            elif response.status_code == 404:
                print("⚠️  Error 404: Modelo no encontrado")
                print("   Posiblemente gemini-2.0-flash no está disponible")
            elif response.status_code == 429:
                print("⚠️  Error 429: Rate Limit Exceeded")
                print("   Límite de requests excedido, espera unos minutos")
            else:
                print(f"⚠️  Error desconocido: {response.text[:200]}")
            
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Timeout - El servidor no respondió en 10 segundos")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error - No se pudo conectar al servidor")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def verificar_modelos_disponibles(api_key: str):
    """Verificar qué modelos están disponibles"""
    print("\n" + "=" * 70)
    print("🔍 VERIFICANDO MODELOS DISPONIBLES")
    print("=" * 70)
    
    if not api_key:
        print("❌ No hay API Key para probar modelos")
        return
    
    # Endpoint para listar modelos
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            modelos = data.get("models", [])
            
            print(f"✅ {len(modelos)} modelos disponibles:")
            
            # Filtrar modelos Gemini
            gemini_models = [m for m in modelos if "gemini" in m.get("name", "").lower()]
            
            for model in gemini_models[:10]:  # Mostrar primeros 10
                name = model.get("name", "")
                display_name = model.get("displayName", "")
                version = model.get("version", "")
                print(f"   • {display_name} ({name}) - v{version}")
            
            if len(gemini_models) > 10:
                print(f"   ... y {len(gemini_models) - 10} modelos más")
            
            # Verificar gemini-2.0-flash específicamente
            flash_models = [m for m in gemini_models if "flash" in m.get("name", "").lower()]
            print(f"\n🔍 Modelos 'flash' disponibles: {len(flash_models)}")
            
            for model in flash_models:
                name = model.get("name", "")
                print(f"   • {name}")
                
        else:
            print(f"❌ Error listando modelos: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error verificando modelos: {e}")

def simular_streamlit_cloud_environment():
    """Simular entorno de Streamlit Cloud"""
    print("\n" + "=" * 70)
    print("🔍 SIMULANDO ENTORNO STREAMLIT CLOUD")
    print("=" * 70)
    
    print("📋 Variables de entorno en Streamlit Cloud:")
    print("   1. Streamlit lee secrets de archivo .streamlit/secrets.toml")
    print("   2. Las variables están disponibles en st.secrets")
    print("   3. Formato requerido en secrets.toml:")
    print("""
      GOOGLE_API_KEY = \"tu-api-key-aqui\"
      
      # OPCIONAL: También puedes tener Vertex AI
      VERTEX_AI_PROJECT_ID = \"tu-project-id\"
      VERTEX_AI_LOCATION = \"us-central1\"
      GOOGLE_SERVICE_ACCOUNT_KEY_JSON = \"\"\"{...}\"\"\"
    """)
    
    print("\n🔧 Problemas comunes en Streamlit Cloud:")
    print("   1. **Secrets no se cargan**: Verificar que el archivo .streamlit/secrets.toml existe")
    print("   2. **Formato incorrecto**: Usar comillas simples/dobles correctamente")
    print("   3. **Redeploy necesario**: Después de cambiar Secrets, esperar 3-5 minutos")
    print("   4. **Caché**: Streamlit puede cachear versiones antiguas")
    
    print("\n🎯 Solución rápida:")
    print("   1. Verificar que .streamlit/secrets.toml contiene EXACTAMENTE:")
    print("      GOOGLE_API_KEY = \"tu-nueva-api-key\"")
    print("   2. Esperar 5 minutos después de guardar")
    print("   3. Probar de nuevo")

def diagnosticar_conexion_directa_module():
    """Diagnosticar el módulo de conexión directa"""
    print("\n" + "=" * 70)
    print("🔍 DIAGNOSTICANDO MÓDULO conexion_directa_ai_studio.py")
    print("=" * 70)
    
    try:
        import conexion_directa_ai_studio
        
        print("✅ Módulo cargado correctamente")
        
        # Crear instancia sin API Key
        conexion = conexion_directa_ai_studio.ConexionDirectaAIStudio()
        status = conexion.get_status()
        
        print(f"📊 Estado del módulo:")
        print(f"   Configurado: {status['configured']}")
        print(f"   Tiene API Key: {status['has_api_key']}")
        print(f"   Modelo: {status['model']}")
        print(f"   System Instructions: {status['system_instructions_length']:,} caracteres")
        print(f"   Endpoint: {status['endpoint']}")
        
        # Verificar System Instructions
        try:
            with open("system_instructions_completas_zapopan.txt", "r") as f:
                si = f.read()
                print(f"\n📋 System Instructions cargadas: {len(si):,} caracteres")
                
                # Verificar contenido crítico
                keywords = ["PROTOCOLO DE RESPUESTA", "ANÁLISIS DE SITUACIÓN", "FUENTES"]
                for kw in keywords:
                    if kw in si:
                        print(f"   ✅ \"{kw}\" encontrado")
                    else:
                        print(f"   ❌ \"{kw}\" NO encontrado")
        except:
            print("❌ No se pudo leer system_instructions_completas_zapopan.txt")
        
    except Exception as e:
        print(f"❌ Error cargando módulo: {e}")

def soluciones_recomendadas():
    """Recomendar soluciones basadas en diagnóstico"""
    print("\n" + "=" * 70)
    print("🚀 SOLUCIONES RECOMENDADAS")
    print("=" * 70)
    
    print("🎯 BASADO EN TUS SÍNTOMAS (Sistema en configuración):")
    print("""
    El problema es que `conexion_directa_ai_studio.py` está usando el fallback.
    Esto significa que:
    1. NO está encontrando la API Key en Streamlit Secrets, O
    2. La API Key no funciona, O
    3. Hay error de conexión con Google AI Studio
    """)
    
    print("\n🔧 SOLUCIÓN 1: VERIFICAR SECRETS EN STREAMLIT")
    print("""
    1. Ve a: https://share.streamlit.io/
    2. Selecciona tu app: chatbot-zapopan
    3. Haz clic en Settings (engranaje)
    4. Ve a pestaña Secrets
    5. Verifica que el contenido sea EXACTAMENTE:
    
    GOOGLE_API_KEY = "tu-nueva-api-key-aqui"
    
    (Solo esa línea, sin comillas extras, sin espacios extra)
    """)
    
    print("\n🔧 SOLUCIÓN 2: PROBAR API KEY LOCALMENTE")
    print("""
    1. Ejecuta este diagnóstico con tu API Key:
       python3 diagnostico_streamlit_cloud.py --api-key TU_API_KEY
    
    2. Verifica si la API Key funciona directamente
    
    3. Si funciona localmente pero no en Streamlit:
       - Problema es con Secrets de Streamlit
       - Si no funciona localmente:
       - La API Key está bloqueada o inválida
       - Necesitas generar una NUEVA
    """)
    
    print("\n🔧 SOLUCIÓN 3: ACTIVAR SISTEMA LOCAL DE EMERGENCIA")
    print("""
    Si Google AI Studio tiene problemas persistentes:
    
    1. Usar sistema local con protocolo completo
    2. Respuestas estructuradas (5 pasos)
    3. 100% funcional sin API Key
    4. Listo en 8 minutos
    
    (Doom ya tiene esto preparado)
    """)
    
    print("\n🔧 SOLUCIÓN 4: PROBAR MODELO ALTERNATIVO")
    print("""
    Si gemini-2.0-flash no funciona:
    
    1. Probar gemini-2.5-flash
    2. Probar gemini-2.5-pro
    3. Actualizar endpoint en conexion_directa_ai_studio.py
    """)

def main():
    """Función principal"""
    print("🔧 DIAGNÓSTICO COMPLETO - CHATBOT ZAPOPAN EN STREAMLIT CLOUD")
    print("=" * 70)
    print("PROBLEMA: Sistema muestra '🔧 SISTEMA EN CONFIGURACIÓN' en lugar de respuestas de Google AI Studio")
    print("=" * 70)
    
    # Obtener API Key de argumentos o variable de entorno
    api_key = None
    
    if len(sys.argv) > 1 and sys.argv[1] == "--api-key" and len(sys.argv) > 2:
        api_key = sys.argv[2]
        print(f"🔑 API Key proporcionada por argumento")
    else:
        # Intentar de variable de entorno
        api_key = os.environ.get("GOOGLE_API_KEY")
        if api_key:
            print(f"🔑 API Key obtenida de variable de entorno GOOGLE_API_KEY")
        else:
            print("⚠️  No se proporcionó API Key")
            print("   Usa: python3 diagnostico_streamlit_cloud.py --api-key TU_API_KEY")
    
    # Ejecutar diagnósticos
    if api_key:
        test_api_key_directamente(api_key)
        verificar_modelos_disponibles(api_key)
    
    diagnosticar_conexion_directa_module()
    simular_streamlit_cloud_environment()
    soluciones_recomendadas()
    
    print("\n" + "=" * 70)
    print("🎯 PRÓXIMOS PASOS RECOMENDADOS")
    print("=" * 70)
    
    print("""
    1. ✅ EJECUTAR ESTE DIAGNÓSTICO CON TU API KEY:
       python3 diagnostico_streamlit_cloud.py --api-key "tu-nueva-api-key"
    
    2. 🔍 VERIFICAR RESULTADOS:
       - Si API Key funciona: Problema es Streamlit Secrets
       - Si API Key no funciona: Generar NUEVA API Key
    
    3. ⚡ DECISIÓN RÁPIDA:
       - Si quieres solución INMEDIATA: Activar sistema local
       - Si tienes tiempo: Debuggear Google AI Studio
    
    4. 🏰 CONTACTAR A DOOM:
       Comparte resultados del diagnóstico para siguiente paso
    """)

if __name__ == "__main__":
    main()