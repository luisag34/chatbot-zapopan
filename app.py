import streamlit as st
import google.generativeai as genai
import json
import pandas as pd
from datetime import datetime

# --- CONFIGURACIÓN DE SEGURIDAD ---
# Para el MVP, definimos los 20 usuarios aquí. 
# Solo quienes estén en esta lista podrán ver el chatbot.
USUARIOS_AUTORIZADOS = {
    "admin_zapopan": "Inspeccion2025",
    "inspector_01": "Zapopan01",
    "inspector_02": "Zapopan02",
    # Puedes seguir agregando hasta los 20
}

# --- CONFIGURACIÓN DE GEMINI ---
# TIP: En Streamlit Cloud, es mejor guardar la API_KEY en "Secrets"
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

def inicializar_chat():
    return genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config={"temperature": 0.1, "top_p": 0.95},
        system_instruction=open("system_instructions.txt", "r").read() # Lee tu archivo TXT
    )

# --- INTERFAZ DE USUARIO ---
st.set_page_config(page_title="Zapopan AI - Inspección", layout="centered")

if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

# --- PANTALLA DE LOGIN ---
if not st.session_state.autenticado:
    st.title("🏛️ Acceso Restringido")
    user = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    if st.button("Ingresar"):
        if user in USUARIOS_AUTORIZADOS and USUARIOS_AUTORIZADOS[user] == password:
            st.session_state.autenticado = True
            st.session_state.usuario_actual = user
            st.rerun()
        else:
            st.error("Credenciales incorrectas")

# --- PANTALLA DEL CHATBOT ---
else:
    st.title(f"🤖 Asistente Normativo - Hola, {st.session_state.usuario_actual}")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Mostrar historial
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Entrada del inspector
    if prompt := st.chat_input("¿Qué situación desea analizar?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            model = inicializar_chat()
            response = model.generate_content(prompt)
            texto_completo = response.text
            
            # SEPARACIÓN LOGICA: Mostramos solo el texto, ocultamos el JSON
            if "---DATASET---" in texto_completo:
                texto_visible = texto_completo.split("---DATASET---")[0]
                json_puro = texto_completo.split("---DATASET---")[1]
            else:
                texto_visible = texto_completo
                json_puro = None

            st.markdown(texto_visible)
            
            # GUARDADO DE DATOS (Simulado para el CSV de auditoría)
            if json_puro:
                try:
                    datos_log = json.loads(json_puro)
                    datos_log["usuario_real"] = st.session_state.usuario_actual
                    # Aquí el sistema guardará una fila en un archivo local
                    # que luego podrás descargar o conectar a Sheets
                    with open("log_consultas.jsonl", "a") as f:
                        f.write(json.dumps(datos_log) + "\n")
                except:
                    pass 

        st.session_state.messages.append({"role": "assistant", "content": texto_visible})
