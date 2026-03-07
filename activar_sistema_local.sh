#!/bin/bash
# SCRIPT PARA ACTIVAR SISTEMA LOCAL DE EMERGENCIA EN 2 MINUTOS

echo "🚀 ACTIVANDO SISTEMA LOCAL DE EMERGENCIA..."
echo "=========================================="

# 1. Reemplazar app.py con versión local
echo "🔧 Reemplazando app.py..."
cp app_local_emergencia.py app.py

# 2. Asegurar que sistema_local_protocolo_completo.py existe
if [ ! -f "sistema_local_protocolo_completo.py" ]; then
    echo "❌ ERROR: sistema_local_protocolo_completo.py no encontrado"
    exit 1
fi

# 3. Hacer commit
echo "📝 Haciendo commit..."
git add app.py sistema_local_protocolo_completo.py
git commit -m "🚨 ACTIVACIÓN SISTEMA LOCAL DE EMERGENCIA - Protocolo completo Zapopan (5 pasos)"

# 4. Hacer push
echo "🚀 Haciendo push a GitHub..."
git push origin main

echo ""
echo "✅ SISTEMA LOCAL ACTIVADO"
echo "========================="
echo "📊 Streamlit redeploy iniciado automáticamente"
echo "⏱️  Tiempo estimado: 3-5 minutos"
echo "🎯 URL: https://chatbot-zapopan.streamlit.app/"
echo ""
echo "🔧 Características del sistema local:"
echo "   • 📋 Protocolo completo (5 pasos)"
echo "   • 🏛️ Respuestas específicas de Zapopan"
echo "   • 🔒 100% local (sin API Key)"
echo "   • ✅ Siempre funciona"
echo ""
echo "👤 Credenciales para probar:"
echo "   • directora_inspeccion / Zapopan2026!DIV1"
echo "   • jefe_comercio / Zapopan2026!JCO1"
echo "   • juridico_01 / Zapopan2026!JU01"
echo ""
echo "💡 Consulta de prueba:"
echo "   \"están colocando una antena de celulares en la azotea de mi vecino\""