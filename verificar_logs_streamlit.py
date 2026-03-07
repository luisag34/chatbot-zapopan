"""
Script para verificar logs de Streamlit Cloud
Nota: No podemos acceder directamente a logs de Streamlit Cloud,
pero podemos verificar que la app esté funcionando correctamente.
"""

import requests
import time

def verificar_app_streamlit():
    """Verificar que la app de Streamlit esté funcionando"""
    url = "https://chatbot-zapopan.streamlit.app/"
    
    try:
        print(f"🔍 Probando conexión a: {url}")
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            print("✅ App Streamlit responde correctamente (200 OK)")
            
            # Verificar contenido básico
            if "Streamlit" in response.text:
                print("✅ Contenido Streamlit detectado")
            else:
                print("⚠️  Contenido Streamlit no detectado (puede estar cargando)")
                
            return True
        else:
            print(f"⚠️  App responde con código: {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Timeout - App puede estar iniciando")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Error de conexión - App no disponible")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def verificar_configuracion_local():
    """Verificar configuración local"""
    print("\n🔍 VERIFICANDO CONFIGURACIÓN LOCAL:")
    
    # Verificar archivos críticos
    archivos_criticos = [
        "app.py",
        "vertex_ai_integration.py", 
        "requirements.txt",
        "runtime.txt"
    ]
    
    import os
    for archivo in archivos_criticos:
        if os.path.exists(archivo):
            print(f"✅ {archivo} existe")
        else:
            print(f"❌ {archivo} NO existe")
    
    # Verificar tamaño de app.py
    if os.path.exists("app.py"):
        size = os.path.getsize("app.py")
        print(f"📊 app.py: {size:,} bytes ({size/1024:.1f} KB)")
        
        # Contar líneas
        with open("app.py", "r") as f:
            lineas = f.readlines()
            print(f"📊 Líneas de código: {len(lineas):,}")

if __name__ == "__main__":
    print("=" * 60)
    print("🔧 VERIFICACIÓN DE DEPLOY STREAMLIT")
    print("=" * 60)
    
    verificar_configuracion_local()
    
    print("\n" + "=" * 60)
    print("🌐 VERIFICANDO APP EN STREAMLIT CLOUD")
    print("=" * 60)
    
    # Intentar 3 veces con delay
    for intento in range(1, 4):
        print(f"\n🔍 Intento {intento}/3...")
        if verificar_app_streamlit():
            print("\n🎉 ¡App parece estar funcionando!")
            break
        else:
            if intento < 3:
                print(f"⏳ Esperando 10 segundos antes de reintentar...")
                time.sleep(10)
    else:
        print("\n⚠️  App no responde después de 3 intentos")
        print("   • Puede estar en redeploy")
        print("   • O puede tener problemas de conexión")
        print("   • Verifica manualmente: https://chatbot-zapopan.streamlit.app/")
