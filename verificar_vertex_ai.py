"""
Script para verificar configuración Vertex AI rápidamente
"""

import os
import json
import sys

def verificar_configuracion():
    print("🔍 VERIFICANDO CONFIGURACIÓN VERTEX AI")
    print("=" * 60)
    
    # Verificar si tenemos módulo Vertex AI
    try:
        from vertex_ai_integration import crear_vertex_ai_chatbot
        print("✅ Módulo Vertex AI importado correctamente")
    except ImportError as e:
        print(f"❌ Error importando módulo Vertex AI: {e}")
        return False
    
    # Crear chatbot
    chatbot = crear_vertex_ai_chatbot()
    status = chatbot.get_status()
    
    print(f"\n📊 ESTADO VERTEX AI:")
    print(f"   • Configurado: {status['configured']}")
    print(f"   • Project ID: {status['project_id']}")
    print(f"   • Location: {status['location']}")
    print(f"   • Access token: {'✅' if status['has_access_token'] else '❌'}")
    print(f"   • Endpoint: {status['endpoint'][:50]}..." if status['endpoint'] else '❌ No configurado')
    
    if status['configured']:
        print(f"\n🎯 ¡VERTEX AI CONFIGURADO CORRECTAMENTE!")
        
        # Probar consulta simple
        print(f"\n🔍 Probando consulta simple...")
        try:
            resultado = chatbot.query("Responde OK si estás funcionando")
            
            print(f"📊 Resultado prueba:")
            print(f"   • Éxito: {resultado['success']}")
            print(f"   • Usando AI: {resultado['using_ai']}")
            print(f"   • Fuente: {resultado['source']}")
            print(f"   • Longitud: {resultado['length']} caracteres")
            
            if resultado['using_ai']:
                print(f"\n✅ ¡VERTEX AI FUNCIONANDO!")
                print(f"💡 Respuesta: {resultado['response'][:100]}...")
                return True
            else:
                print(f"\n⚠️ Vertex AI no respondió, usando fallback")
                print(f"💡 Error: {resultado.get('error', 'N/A')}")
                return False
                
        except Exception as e:
            print(f"❌ Error en prueba: {e}")
            return False
    else:
        print(f"\n❌ Vertex AI no configurado")
        print(f"\n💡 PARA CONFIGURAR:")
        print(f"   1. Ve a https://chatbot-zapopan.streamlit.app/")
        print(f"   2. Manage app → Settings → Secrets")
        print(f"   3. Copia contenido de 'vertex_ai_config_template.toml'")
        print(f"   4. Reemplaza placeholders con tus datos reales")
        print(f"   5. Guarda y espera redeploy (3-5 minutos)")
        return False

def verificar_streamlit_secrets():
    """Verificar formato de secrets.toml"""
    print(f"\n🔍 VERIFICANDO FORMATO SECRETS:")
    
    template_path = "vertex_ai_config_template.toml"
    if os.path.exists(template_path):
        with open(template_path, 'r') as f:
            contenido = f.read()
        
        # Verificar placeholders
        placeholders = [
            "REPLACE_WITH_YOUR_PROJECT_ID",
            "REPLACE_WITH_YOUR_PRIVATE_KEY",
            "REPLACE_WITH_YOUR_PRIVATE_KEY_ID"
        ]
        
        for placeholder in placeholders:
            if placeholder in contenido:
                print(f"   • {placeholder}: ❌ NO REEMPLAZADO")
            else:
                print(f"   • {placeholder}: ✅ REEMPLAZADO")
        
        print(f"\n💡 Template disponible en: {template_path}")
    else:
        print(f"   ❌ Template no encontrado")

def main():
    """Función principal"""
    print("🚀 VERIFICADOR DE CONFIGURACIÓN VERTEX AI")
    print("=" * 60)
    
    # Verificar configuración actual
    config_ok = verificar_configuracion()
    
    # Verificar formato secrets
    verificar_streamlit_secrets()
    
    print("\n" + "=" * 60)
    
    if config_ok:
        print("🎯 ¡SISTEMA LISTO CON VERTEX AI!")
        print("💡 Prueba en: https://chatbot-zapopan.streamlit.app/")
    else:
        print("🔧 SISTEMA CON FALLBACK (Vertex AI no configurado)")
        print("💡 El sistema funciona con respuestas locales")
        print("💡 Configura Vertex AI para respuestas mejoradas")
    
    print("=" * 60)

if __name__ == "__main__":
    main()