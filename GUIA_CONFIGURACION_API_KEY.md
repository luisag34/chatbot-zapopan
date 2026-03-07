# 🚀 GUÍA PARA CONFIGURAR API KEY EN STREAMLIT CLOUD

## 📋 PASO 1: OBTENER API KEY DE TU CHATBOT

1. **Abre Google AI Studio:**
   ```
   https://makersuite.google.com/app
   ```

2. **Selecciona tu chatbot de Zapopan** (el que ya configuraste)

3. **Haz clic en "Get code"** (botón en la esquina superior derecha)

4. **Busca la API key** - se ve así:
   ```
   AIzaSyAorC3CFB4W5N2N8YLrAVOpOahLzNWFxRs
   ```

5. **Copia la key** completa

## 📋 PASO 2: CONFIGURAR EN STREAMLIT CLOUD

1. **Abre Streamlit Cloud:**
   ```
   https://share.streamlit.io/
   ```

2. **Login con tu cuenta de GitHub** (luisag34)

3. **Selecciona la app** `chatbot-zapopan`

4. **Haz clic en "Settings"** (engranaje ⚙️ en la esquina superior derecha)

5. **Ve a la pestaña "Secrets"**

6. **Pega tu API key** en el formato EXACTO:
   ```toml
   GOOGLE_API_KEY = "AIzaSyAorC3CFB4W5N2N8YLrAVOpOahLzNWFxRs"
   ```

   **IMPORTANTE:**
   - Usa **comillas dobles** `"`
   - **NO** agregues espacios extra
   - **NO** cambies el nombre `GOOGLE_API_KEY`

7. **Haz clic en "Save"**

## 📋 PASO 3: VERIFICAR CONFIGURACIÓN

1. **Espera 1-2 minutos** para que Streamlit actualice

2. **Abre tu app:**
   ```
   https://chatbot-zapopan.streamlit.app/
   ```

3. **Login con:**
   - Usuario: `luis_admin`
   - Contraseña: `ZapopanAdmin2026!`

4. **Haz una consulta de prueba:**
   ```
   "ruido de restaurante por la noche"
   ```

5. **Verifica que aparezca:**
   - ✅ **🤖 Chatbot Zapopan (Google AI Studio)** en la parte inferior
   - ✅ Respuesta **detallada y precisa** (no la respuesta local genérica)

## 🔧 SOLUCIÓN DE PROBLEMAS

### ❌ "No se encontraron regulaciones específicas..."
**Significa:** API key no configurada o incorrecta

**Solución:**
1. Verifica que la key esté en Secrets
2. Verifica formato TOML correcto
3. Prueba la key en AI Studio directamente

### ❌ Error de conexión/timeout
**Significa:** Problemas de red o key inválida

**Solución:**
1. Verifica que la key sea válida
2. Prueba desde otra red
3. Contacta a Doom para debugging

### ❌ App no se actualiza
**Significa:** Streamlit Cloud cache

**Solución:**
1. Espera 5 minutos
2. Refresca con Ctrl+F5
3. Verifica que el commit `d122084` esté desplegado

## 📞 SOPORTE

**Si tienes problemas:**
1. **Toma screenshot** del error
2. **Comparte** (sin mostrar la API key completa)
3. **Doom te ayuda** a diagnosticar

**Recuerda:** Nunca compartas tu API key completa públicamente.

---

**Tiempo estimado:** 5-10 minutos  
**Dificultad:** Baja  
**Riesgo:** Bajo (fallback local garantizado si falla)