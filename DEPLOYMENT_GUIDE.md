# 🚀 Guía de Deployment - Chatbot Zapopan en Streamlit Cloud

## 📋 Requisitos Previos

### 1. Cuentas necesarias:
- ✅ **Streamlit Cloud**: `streamlit.io` (logueado con Google: `luis.aguirre34@gmail.com`)
- ✅ **Google AI Studio**: API Key ya configurada
- ✅ **GitHub**: Repositorio `luisag34/chatbot-zapopan` (privado)

### 2. Archivos del proyecto:
```
chatbot-zapopan/
├── app.py                    # App principal Streamlit
├── pages/1_📊_Dashboard_Analítico.py  # Dashboard
├── rag_engine.py            # Motor RAG
├── semantic_router.py       # Router semántico
├── google_sheets_integration.py  # Integración Google Sheets
├── requirements.txt         # Dependencias
├── .streamlit/
│   ├── config.toml         # Configuración Streamlit
│   └── secrets.toml        # Secrets locales (NO subir a GitHub)
├── system_instructions.txt  # Instrucciones del sistema (43KB+)
├── *.jsonl                 # Datasets RAG (3 archivos)
└── directorio ZPN, IA inspección - Hoja 1.csv
```

## 🚀 Pasos para Deployment en Streamlit Cloud

### Paso 1: Subir a GitHub
```bash
# Ya está en GitHub como repositorio privado
# Verificar que todos los archivos están commitados
```

### Paso 2: Configurar Secrets en Streamlit Cloud

1. Ir a [share.streamlit.io](https://share.streamlit.io)
2. Iniciar sesión con `luis.aguirre34@gmail.com`
3. Click en "New app"
4. Conectar cuenta de GitHub `luisag34`
5. Seleccionar repositorio: `chatbot-zapopan`
6. Branch: `main`
7. Main file path: `app.py`

## ⚠️ **ADVERTENCIA CRÍTICA DE SEGURIDAD**

**NUNCA pongas API Keys reales en archivos que se suban a GitHub.** Google escanea automáticamente repositorios públicos y privados en busca de credenciales expuestas y enviará alertas de seguridad.

**Configurar Secrets (Advanced settings → Secrets):**
```toml
GOOGLE_API_KEY = "REPLACE_WITH_YOUR_API_KEY"

# Opcional: Configuración para Google Sheets (modo producción)
# GOOGLE_SHEETS_CREDENTIALS_JSON = "{\"type\": \"service_account\", ...}"
# GOOGLE_SHEETS_SPREADSHEET_ID = "tu-spreadsheet-id"
```

**⚠️ INSTRUCCIÓN:** Reemplaza `REPLACE_WITH_YOUR_API_KEY` con tu API Key real **SOLO en Streamlit Cloud Secrets**, nunca en archivos del repositorio.

### Paso 3: Configuración de la App

**Main file path:** `app.py`  
**Python version:** 3.9+ (Streamlit Cloud usa 3.9 por defecto)  
**Advanced settings:**
- **Run on save:** ✅ Activado
- **App visibility:** 🔒 Privado (recomendado para datos sensibles)
- **Memory:** 1 GB (suficiente para datasets)

### Paso 4: Desplegar

1. Click en "Deploy"
2. Esperar build (2-3 minutos)
3. Verificar logs de build
4. Acceder a la URL generada

## 🔧 Configuración para Producción

### Google Sheets Real (Opcional)

Para usar Google Sheets real en lugar del modo demo:

1. **Crear credenciales de servicio en Google Cloud Console:**
   - Ir a [console.cloud.google.com](https://console.cloud.google.com)
   - Crear nuevo proyecto o usar existente
   - Habilitar Google Sheets API
   - Crear credenciales de "Service Account"
   - Descargar JSON de credenciales

2. **Crear spreadsheet en Google Sheets:**
   - Crear nueva hoja de cálculo
   - Compartir con el email del service account (ej: `chatbot-zapopan@...iam.gserviceaccount.com`)
   - Dar permisos de "Editor"

3. **Configurar secrets en Streamlit Cloud:**
   ```toml
   GOOGLE_SHEETS_CREDENTIALS_JSON = "{\"type\": \"service_account\", \"project_id\": \"...\", ...}"
   GOOGLE_SHEETS_SPREADSHEET_ID = "1ABC123..."
   ```

### Optimización de Performance

**Para datasets grandes (recomendado):**
1. **Compresión de system_instructions.txt:**
   - Actual: 43KB+ (grande para tokens)
   - Considerar dividir en secciones
   - Usar versiones resumidas para prompts

2. **Cache de RAG:**
   - Los datasets JSONL se cargan en memoria
   - Considerar usar base de datos vectorial (Chroma, Pinecone) para producción

3. **Límites de Streamlit Cloud:**
   - Memoria: 1 GB por defecto
   - Tiempo de ejecución: Sin límite para apps normales
   - Ancho de banda: Generoso para uso normal

## 🐛 Solución de Problemas Comunes

### Error: "ModuleNotFoundError"
```bash
# Verificar requirements.txt incluye:
streamlit
google-generativeai
pandas
gspread
google-auth
oauth2client
plotly
```

### Error: "API Key inválida"
1. Verificar que la API Key de Google AI Studio sea válida
2. Verificar que tenga créditos disponibles
3. Verificar que el modelo `gemini-flash-latest` esté disponible

### Error: "Memory limit exceeded"
1. Reducir tamaño de datasets cargados
2. Usar `RAGEngine` con solo 1 dataset inicialmente
3. Implementar carga lazy de chunks

### Error: "Timeout en Streamlit Cloud"
1. Reducir complejidad de System Instructions
2. Implementar caché con `@st.cache_data`
3. Optimizar búsqueda RAG

## 📊 Monitoreo Post-Deployment

### Métricas a monitorear:
1. **Tiempo de respuesta:** < 10 segundos por consulta
2. **Uso de memoria:** < 800 MB
3. **Consultas por día:** Seguimiento de uso
4. **Errores:** Revisar logs de Streamlit Cloud

### Logs de Streamlit Cloud:
- Acceder a "Manage app" → "Logs"
- Verificar errores en tiempo real
- Monitorear uso de recursos

## 🔄 Actualizaciones Futuras

### Para actualizar la app:
1. Hacer cambios en repositorio local
2. Push a GitHub
3. Streamlit Cloud detecta cambios y redeploy automático

### Consideraciones de escalabilidad:
1. **> 100 consultas/día:** Considerar base de datos vectorial
2. **> 10 usuarios concurrentes:** Optimizar caché
3. **Datos históricos > 1 año:** Implementar archivado

## 📞 Soporte

**Para problemas técnicos:**
1. Revisar logs en Streamlit Cloud
2. Verificar configuración de secrets
3. Probar localmente primero

**Contacto:**
- Streamlit Community: [discuss.streamlit.io](https://discuss.streamlit.io)
- Google AI Studio Support: [ai.google.dev](https://ai.google.dev)

---

**✅ Estado actual del proyecto:** Listo para deployment  
**⏱️ Tiempo estimado deployment:** 10-15 minutos  
**🔒 Seguridad:** Repositorio privado + app privada  
**📈 Escalabilidad:** Arquitectura modular lista para crecimiento  

**¡Sistema completamente funcional con RAG, Router Semántico, Google Sheets y Dashboard!** 🏛️🤖📊