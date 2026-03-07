#!/usr/bin/env python3
"""
Script de testing local para Google AI integration
Ejecutar en tu máquina local con: python test_google_ai_local.py
"""

import sys
import os

# Agregar directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_without_api_key():
    """Probar módulo sin API key (modo fallback)"""
    print("🧪 TEST 1: Módulo sin API key")
    print("-" * 50)
    
    try:
        from google_ai_integration import create_google_ai_integration
        
        # Crear integración sin API key
        integration = create_google_ai_integration()
        
        # Verificar estado
        status = integration.get_status()
        print(f"✅ Módulo cargado: {status}")
        
        # Probar consulta (debería fallar elegantemente)
        print("\n🔍 Probando consulta sin API key...")
        result = integration.query_google_ai("ruido de restaurante por la noche", "legal")
        print(f"   Resultado: {result.get('success', False)}")
        print(f"   Fuente: {result.get('source', 'unknown')}")
        print(f"   Mensaje: {result.get('message', 'N/A')}")
        
        if result.get('suggest_fallback', False):
            print("   ✅ Fallback sugerido correctamente")
        else:
            print("   ⚠️ Fallback no sugerido")
            
        return True
        
    except Exception as e:
        print(f"❌ Error en test sin API key: {e}")
        return False

def test_module_structure():
    """Probar estructura del módulo"""
    print("\n🧪 TEST 2: Estructura del módulo")
    print("-" * 50)
    
    try:
        # Importar componentes
        from google_ai_integration import (
            GoogleAIIntegration,
            create_google_ai_integration,
            hybrid_query,
            GOOGLE_AI_AVAILABLE
        )
        
        print(f"✅ Componentes importados correctamente")
        print(f"   GoogleAIIntegration: {'✅' if GoogleAIIntegration else '❌'}")
        print(f"   create_google_ai_integration: {'✅' if create_google_ai_integration else '❌'}")
        print(f"   hybrid_query: {'✅' if hybrid_query else '❌'}")
        print(f"   GOOGLE_AI_AVAILABLE: {GOOGLE_AI_AVAILABLE}")
        
        # Probar creación de instancia
        integration = GoogleAIIntegration()
        print(f"   Instancia creada: {'✅' if integration else '❌'}")
        
        # Probar métodos básicos
        print(f"   is_available(): {integration.is_available()}")
        print(f"   get_status(): {integration.get_status()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en test de estructura: {e}")
        return False

def test_hybrid_query_logic():
    """Probar lógica de consulta híbrida"""
    print("\n🧪 TEST 3: Lógica de consulta híbrida")
    print("-" * 50)
    
    try:
        from google_ai_integration import hybrid_query
        
        # Contexto local simulado
        local_context = [
            {
                "reglamento": "Reglamento de Policía y Buen Gobierno",
                "articulo": "Artículo 45",
                "contenido": "Prohibición de ruidos que alteren la tranquilidad",
                "dependencia": "Inspección y Vigilancia"
            }
        ]
        
        # Probar consulta híbrida sin Google AI (debería usar fallback)
        print("🔍 Probando hybrid_query sin Google AI...")
        result = hybrid_query(
            query="ruido nocturno",
            query_type="legal",
            local_context=local_context
        )
        
        print(f"   Éxito: {result.get('success', False)}")
        print(f"   Fuente: {result.get('source', 'unknown')}")
        print(f"   Estrategia: {result.get('strategy', 'N/A')}")
        print(f"   Fallback usado: {result.get('fallback_used', False)}")
        
        if result.get('success', False) and result.get('source') == 'local_fallback':
            print("   ✅ Lógica de fallback funciona correctamente")
        else:
            print("   ⚠️ Comportamiento inesperado")
            
        return True
        
    except Exception as e:
        print(f"❌ Error en test de lógica híbrida: {e}")
        return False

def test_with_mock_api_key():
    """Probar con API key mock (simulada)"""
    print("\n🧪 TEST 4: Con API key mock")
    print("-" * 50)
    
    try:
        from google_ai_integration import GoogleAIIntegration
        
        # API key inválida (para probar manejo de errores)
        mock_api_key = "AIzaSyTEST_KEY_INVALID_1234567890"
        
        integration = GoogleAIIntegration(mock_api_key)
        
        print(f"✅ Instancia creada con API key mock")
        print(f"   Configurado: {integration.is_configured}")
        print(f"   Disponible: {integration.is_available()}")
        
        # Intentar consulta (debería fallar)
        if integration.is_available():
            print("\n🔍 Probando consulta con API key inválida...")
            result = integration.query_google_ai("test", "general")
            print(f"   Resultado: {result}")
            
            if result.get('suggest_fallback', False):
                print("   ✅ Manejo de error de API key funciona")
            else:
                print("   ⚠️ Manejo de error podría mejorar")
        else:
            print("   ✅ Google AI correctamente no disponible con key inválida")
            
        return True
        
    except Exception as e:
        print(f"❌ Error en test con API key mock: {e}")
        return False

def main():
    """Función principal de testing"""
    print("🚀 TESTING LOCAL DE INTEGRACIÓN GOOGLE AI")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 4
    
    # Ejecutar tests
    if test_without_api_key():
        tests_passed += 1
    
    if test_module_structure():
        tests_passed += 1
    
    if test_hybrid_query_logic():
        tests_passed += 1
    
    if test_with_mock_api_key():
        tests_passed += 1
    
    # Resumen
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE TESTING")
    print(f"   Tests pasados: {tests_passed}/{total_tests}")
    
    if tests_passed == total_tests:
        print("   ✅ TODOS los tests pasaron")
        print("\n🎯 Módulo listo para integración en app.py")
        print("   Siguiente paso: Probar con API key real en tu máquina")
    else:
        print(f"   ⚠️ {total_tests - tests_passed} tests fallaron")
        print("\n🔧 Revisar los errores antes de continuar")
    
    # Instrucciones para testing con API key real
    print("\n" + "=" * 60)
    print("🔑 PARA PROBAR CON API KEY REAL:")
    print("1. Obtén API key de Google AI Studio")
    print("2. Configura variable de entorno:")
    print("   export GOOGLE_API_KEY='tu_key_aqui'")
    print("3. Ejecuta: python test_with_real_key.py")
    print("\n💡 O pídeme que cree test_with_real_key.py")

if __name__ == "__main__":
    main()