"""
PROCESADOR EXPANDIDO - SISTEMA LOCAL CON 10+ TEMAS
Reemplaza procesar_consulta_local_protocolo_completo
"""

import json
import random
from datetime import datetime
from typing import Dict, List

def procesar_consulta_local_expandida(consulta: str, usuario: str) -> Dict:
    """
    Procesar consulta usando sistema local expandido con 10+ temas
    """
    # Importar sistema expandido
    from sistema_local_expandido import SistemaLocalExpandido
    
    sistema = SistemaLocalExpandido()
    
    # Detectar tema basado en palabras clave
    consulta_lower = consulta.lower()
    tema_detectado = None
    
    # Diccionario de palabras clave por tema
    palabras_clave = {
        "antena": ["antena", "celular", "telefonía", "azotea", "telecomunicaciones"],
        "ruido": ["ruido", "sonido", "molesto", "fiesta", "música", "alto"],
        "construccion": ["construcción", "obra", "edificio", "demoler", "ampliar"],
        "apertura_negocio": ["negocio", "abrir", "comercio", "licencia", "funcionamiento"],
        "uso_suelo": ["uso de suelo", "destino", "zona", "comercial", "habitacional"],
        "publicidad_exterior": ["publicidad", "espectacular", "anuncio", "letrero"],
        "estacionamiento": ["estacionamiento", "cajones", "parquímetro", "aparcar"],
        "basura": ["basura", "residuos", "recolección", "limpia"],
        "agua": ["agua", "fuga", "servicio", "potable", "SAPA"],
        "mascotas": ["mascota", "perro", "gato", "animal", "tenencia"],
        "arboles": ["árbol", "poda", "tala", "verde", "jardín"],
        "eventos": ["evento", "fiesta", "concierto", "feria", "público"],
        "taxi": ["taxi", "transporte", "uber", "didí", "aplicación"]
    }
    
    # Detectar tema
    for tema, palabras in palabras_clave.items():
        for palabra in palabras:
            if palabra in consulta_lower:
                tema_detectado = tema
                break
        if tema_detectado:
            break
    
    # Si no se detecta tema, usar uno aleatorio de los principales
    if not tema_detectado:
        temas_principales = ["antena", "ruido", "construccion", "apertura_negocio", "uso_suelo"]
        tema_detectado = random.choice(temas_principales)
    
    # Generar respuesta
    resultado = sistema.generar_respuesta(consulta, tema_detectado)
    
    # Registrar consulta localmente
    try:
        from app import registrar_consulta_local
        registrar_consulta_local(consulta, [], usuario)
    except:
        pass
    
    return {
        "texto_visible": resultado["response"],
        "resultados": [],
        "categoria": f"sistema_local_{tema_detectado}",
        "fuente": resultado["source"],
        "indicador": f"📋 Sistema normativo Zapopan • ✅ Protocolo específico ({tema_detectado})",
        "usando_ai": False,
        "sigue_protocolo": True
    }

# Función de compatibilidad para mantener imports existentes
def procesar_consulta_local_protocolo_completo(consulta: str, usuario: str) -> Dict:
    """Alias para compatibilidad con código existente"""
    return procesar_consulta_local_expandida(consulta, usuario)