#!/usr/bin/env python3
"""
Script de diagnóstico para chatbot-zapopan
Ejecutar localmente para verificar configuración
"""

import os
import sys
import json

print("🔍 DIAGNÓSTICO CHATBOT ZAPOPAN")
print("=" * 60)

# ============================================================================
# 1. VERIFICAR VARIABLES DE ENTORNO
# ============================================================================
print("\n1. 📋 VARIABLES DE ENTORNO:")
print("-" * 40)

api_key = os.environ.get("GOOGLE_API_KEY")
print(f"   GOOGLE_API_KEY en entorno: {'✅ SET' if api_key else '❌ NO SET'}")
if api_key:
    print(f"   Longitud: {len(api_key)} caracteres")
    print(f"   Empieza con: {api_key[:10]}...")
    print(f"   Termina con: ...{api_key[-4:]}")

# ============================================================================
# 2. VERIFICAR MÓDULOS
# ============================================================================
print("\n2. 📦 MÓDULOS DISPONIBLES:")
print("-" * 40)

try:
    import streamlit
    print(f"   streamlit: ✅ {streamlit.__version__}")
except ImportError:
    print(f"   streamlit: ❌ No instalado")

try:
    import requests
    print(f"   requests: ✅ {requests.__version__}")
except ImportError:
    print(f"   requests: ❌ No instalado")

try:
    import google.genai
    print(f"   google.genai: ✅ (nueva versión)")
    GENAI_AVAILABLE = "new"
except ImportError:
    try:
        import google.generativeai
        print(f"   google.generativeai: ✅ (deprecated)")
        GENAI_AVAILABLE = "deprecated"
    except ImportError:
        print(f"   google.generativeai: ❌ No instalado")
        GENAI_AVAILABLE = "none"

# ============================================================================
# 3. PROBAR CHATBOT SIMPLE
# ============================================================================
print("\n3. 🤖 PROBAR CHATBOT SIMPLE:")
print("-" * 40)

# Importar nuestro módulo
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from chatbot_zapopan_simple import ChatbotZapopanSimple
    
    chatbot = ChatbotZapopanSimple()
    print(f"   Módulo cargado: ✅")
    print(f"   Chatbot configurado: {chatbot.is_configured}")
    print(f"   Chatbot disponible: {chatbot.is_available()}")
    
    # Probar consulta
    if chatbot.is_available():
        print(f"\n   🔍 Probando consulta con API key...")
        resultado = chatbot.query("Responde 'OK' si estás funcionando.")
        print(f"   Éxito: {resultado['success']}")
        print(f"   Usando AI: {resultado.get('using_ai', False)}")
        print(f"   Fuente: {resultado.get('source', 'N/A')}")
        
        if resultado.get('using_ai'):
            print(f"   ✅ CHATBOT FUNCIONANDO CON IA")
            print(f"   Respuesta: {resultado['response'][:100]}...")
        else:
            print(f"   ⚠️ CHATBOT EN MODO FALLBACK")
            print(f"   Razón: {resultado.get('response', '')[100:200]}...")
    else:
        print(f"   ⚠️ Chatbot no disponible (sin API key)")
        
except Exception as e:
    print(f"   ❌ Error cargando módulo: {e}")

# ============================================================================
# 4. VERIFICAR APP.PY
# ============================================================================
print("\n4. 📄 VERIFICAR app.py:")
print("-" * 40)

try:
    with open("app.py", "r", encoding="utf-8") as f:
        contenido = f.read()
    
    # Buscar importaciones clave
    import_chatbot = "from chatbot_zapopan_simple import" in contenido
    usar_chatbot = "procesar_consulta_con_chatbot_zapopan" in contenido
    
    print(f"   Importa chatbot_zapopan_simple: {'✅' if import_chatbot else '❌'}")
    print(f"   Usa función chatbot: {'✅' if usar_chatbot else '❌'}")
    
    # Contar líneas
    lineas = contenido.count('\n')
    print(f"   Total líneas: {lineas}")
    
except Exception as e:
    print(f"   ❌ Error leyendo app.py: {e}")

# ============================================================================
# 5. VERIFICAR REQUIREMENTS
# ============================================================================
print("\n5. 📦 VERIFICAR requirements.txt:")
print("-" * 40)

try:
    with open("requirements.txt", "r", encoding="utf-8") as f:
        reqs = f.read()
    
    tiene_streamlit = "streamlit" in reqs
    tiene_google_genai = "google-genai" in reqs
    
    print(f"   streamlit en requirements: {'✅' if tiene_streamlit else '❌'}")
    print(f"   google-genai en requirements: {'✅' if tiene_google_genai else '❌'}")
    
    if tiene_google_genai:
        # Extraer versión
        import re
        match = re.search(r'google-genai==([\d.]+)', reqs)
        if match:
            print(f"   Versión google-genai: {match.group(1)}")
    
except Exception as e:
    print(f"   ❌ Error leyendo requirements: {e}")

# ============================================================================
# RESUMEN
# ============================================================================
print("\n" + "=" * 60)
print("📊 RESUMEN DE DIAGNÓSTICO:")
print("-" * 40)

# Evaluar estado
problemas = []

if not api_key:
    problemas.append("❌ NO hay GOOGLE_API_KEY en entorno")
elif not chatbot.is_available() if 'chatbot' in locals() else True:
    problemas.append("⚠️ Chatbot no disponible (¿API key inválida?)")

if GENAI_AVAILABLE == "none":
    problemas.append("⚠️ google-genai no instalado (fallback local)")

if problemas:
    print("   ⚠️ PROBLEMAS IDENTIFICADOS:")
    for p in problemas:
        print(f"   {p}")
else:
    print("   ✅ TODO PARECE CORRECTO EN CONFIGURACIÓN LOCAL")

print("\n💡 RECOMENDACIONES:")
print("1. Ejecuta este script en Streamlit Cloud (si es posible)")
print("2. Verifica logs de Streamlit Cloud para errores")
print("3. Prueba API key directamente con curl:")
print("   curl -X POST https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent \\")
print("     -H 'Content-Type: application/json' \\")
print("     -H 'x-goog-api-key: TU_API_KEY' \\")
print("     -d '{\"contents\":[{\"parts\":[{\"text\":\"test\"}]}]}'")

print("\n🎯 Para debugging remoto, comparte:")
print("   - Screenshot del error")
print("   - Texto EXACTO de respuesta")
print("   - Indicador (🤖 o 📚) que aparece")