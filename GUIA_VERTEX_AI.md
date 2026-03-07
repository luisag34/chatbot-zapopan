# 🚀 GUÍA DE CONFIGURACIÓN VERTEX AI PARA CHATBOT ZAPOPAN

## 📋 PRERREQUISITOS

1. **Cuenta Google Cloud** con billing habilitado
2. **Project ID** de Google Cloud
3. **Service Account** con permisos de Vertex AI
4. **Vertex AI API** habilitada

## 🔧 PASO 1: CREAR SERVICE ACCOUNT EN GOOGLE CLOUD

### 1.1 Ir a Google Cloud Console
- https://console.cloud.google.com/
- Seleccionar tu proyecto

### 1.2 Crear Service Account
- **IAM & Admin** → **Service Accounts** → **CREATE SERVICE ACCOUNT**
- **Nombre:** `chatbot-zapopan-vertex-ai`
- **ID:** `chatbot-zapopan-vertex-ai`
- **Descripción:** Service account para chatbot Zapopan con Vertex AI

### 1.3 Asignar roles
Agregar estos roles al service account:
- **Vertex AI User** (`roles/aiplatform.user`)
- **Vertex AI Administrator** (`roles/aiplatform.admin`) - opcional pero recomendado

### 1.4 Crear y descargar key
- **Keys** → **ADD KEY** → **Create new key**
- **Tipo:** JSON
- **Descargar** el archivo JSON

## 🔧 PASO 2: HABILITAR APIS NECESARIAS

### 2.1 Habilitar Vertex AI API
- **APIs & Services** → **Library**
- Buscar y habilitar:
  - **Vertex AI API** (`aiplatform.googleapis.com`)
  - **Cloud Resource Manager API** (`cloudresourcemanager.googleapis.com`)

### 2.2 Verificar quotas
- **IAM & Admin** → **Quotas**
- Verificar quotas para:
  - **Vertex AI Text Generation requests per minute**
  - **Vertex AI Text Generation tokens per minute**

## 🔧 PASO 3: CONFIGURAR STREAMLIT SECRETS

### 3.1 Obtener Project ID
- En Google Cloud Console, copiar el **Project ID**
- Ejemplo: `mi-proyecto-123456`

### 3.2 Configurar Streamlit Secrets
En `https://chatbot-zapopan.streamlit.app/` → **Settings** → **Secrets**:

```toml
# Configuración Vertex AI
VERTEX_AI_PROJECT_ID = "tu-project-id-aqui"
VERTEX_AI_LOCATION = "us-central1"  # o "europe-west4", "asia-northeast1"

# Opción A: Service Account Key como JSON string
GOOGLE_SERVICE_ACCOUNT_KEY_JSON = '''
{
  "type": "service_account",
  "project_id": "tu-project-id",
  "private_key_id": "...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "chatbot-zapopan@tu-project-id.iam.gserviceaccount.com",
  "client_id": "...",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/..."
}
'''

# Opción B: Solo API Key (menos segura)
GOOGLE_API_KEY = "AIzaSyC9lqTVCcIzHYh96-Lo4pmdoiXfyYCmnNY"

# Configuración existente
USUARIOS_DB = {...}
```

### 3.3 Formato alternativo (archivo temporal)
Si prefieres no poner el JSON completo en secrets:

```toml
# Solo Project ID y Location
VERTEX_AI_PROJECT_ID = "tu-project-id"
VERTEX_AI_LOCATION = "us-central1"

# Y configurar variable de entorno en deploy
GOOGLE_APPLICATION_CREDENTIALS = "/tmp/service-account-key.json"
```

Luego en el código crear el archivo temporal.

## 🔧 PASO 4: ACTUALIZAR APP.PY

### 4.1 Modificar imports
```python
# En app.py, reemplazar o agregar:
try:
    from vertex_ai_integration import procesar_consulta_vertex_ai
    VERTEX_AI_AVAILABLE = True
except ImportError:
    VERTEX_AI_AVAILABLE = False
```

### 4.2 Modificar función principal
```python
def procesar_consulta_con_chatbot_zapopan(consulta: str, usuario: str):
    """Procesar consulta con Vertex AI primero, luego fallback"""
    
    # Intentar Vertex AI primero
    if VERTEX_AI_AVAILABLE:
        resultado = procesar_consulta_vertex_ai(consulta, usuario)
        if resultado.get("usando_ai", False):
            return resultado
    
    # Fallback al sistema híbrido
    try:
        from chatbot_zapopan_hibrido import procesar_consulta_hibrida
        return procesar_consulta_hibrida(consulta, usuario)
    except ImportError:
        # Último fallback
        return procesar_consulta_local(consulta, usuario)
```

## 🔧 PASO 5: VERIFICAR CONFIGURACIÓN

### 5.1 Probar localmente (opcional)
```bash
# Exportar variables
export GOOGLE_CLOUD_PROJECT="tu-project-id"
export GOOGLE_APPLICATION_CREDENTIALS="/ruta/a/tu-key.json"

# Probar módulo
python3 vertex_ai_integration.py
```

### 5.2 Deploy en Streamlit
- **Commit y push** los cambios
- **Streamlit redeploy** automáticamente
- **Verificar logs** en Streamlit Cloud

## 🚨 SOLUCIÓN DE PROBLEMAS

### ❌ Error: "Vertex AI API not enabled"
- Habilitar Vertex AI API en Google Cloud Console

### ❌ Error: "Permission denied"
- Verificar roles del service account
- Agregar `roles/aiplatform.user`

### ❌ Error: "Quota exceeded"
- Verificar quotas en Google Cloud Console
- Solicitar aumento de quotas si necesario

### ❌ Error: "Invalid project ID"
- Verificar que el Project ID sea correcto
- Probar en Google Cloud Console: `gcloud config get-value project`

## 📊 VENTAJAS DE VERTEX AI VS AI STUDIO

| Característica | AI Studio (Gratuito) | Vertex AI (Empresarial) |
|----------------|---------------------|------------------------|
| **Quotas** | Muy limitadas | Generosas, configurables |
| **Safety filters** | Ultra estrictos | Configurables |
| **Rate limiting** | Bajo | Alto |
| **Soporte** | Básico | Empresarial |
| **Costos** | Gratuito (límites) | ~$1-5/mes uso bajo |
| **Control** | Limitado | Completo |

## 💰 ESTIMACIÓN DE COSTOS

### Uso típico (100 consultas/día):
- **Vertex AI Text Generation:** ~$0.50 - $2.00 USD/mes
- **Depende de:** tokens por consulta, modelo usado

### Modelos disponibles:
- **Gemini 2.0 Flash:** Más económico
- **Gemini 2.5 Pro:** Más caro, mejor calidad
- **Gemini 1.5 Pro/Flash:** Alternativas

## 🎯 PRÓXIMOS PASOS

1. **Configurar Service Account** y descargar key JSON
2. **Actualizar Streamlit Secrets** con Project ID y key
3. **Commit y push** cambios
4. **Probar sistema** en producción
5. **Monitorear costos** primera semana

## 📞 SOPORTE

- **Google Cloud Support:** https://cloud.google.com/support
- **Vertex AI Documentation:** https://cloud.google.com/vertex-ai
- **Streamlit Community:** https://discuss.streamlit.io

---

**Última actualización:** 2026-03-07  
**Por:** Dr. Doom 🏰  
**Estado:** Sistema listo para Vertex AI