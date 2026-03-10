"""
SISTEMA LOCAL EXPANDIDO - 10+ TEMAS PARA ZAPOPAN
Reemplaza sistema_local_protocolo_completo.py con base de conocimiento expandida
"""

import json
import random
from datetime import datetime
from typing import Dict, List

class SistemaLocalExpandido:
    """Sistema local expandido con 10+ temas para Zapopan"""
    
    def __init__(self):
        self.base_conocimiento = self._cargar_base_conocimiento_completa()
        self.protocolo_pasos = [
            "ANÁLISIS DE SITUACIÓN",
            "CLASIFICACIÓN DE ATRIBUCIONES", 
            "SUSTENTO LEGAL",
            "DEPENDENCIAS CON ATRIBUCIONES Y CONTACTO",
            "FUENTES"
        ]
        
        print(f"🔧 Sistema local expandido cargado")
        print(f"   Base conocimiento: {len(self.base_conocimiento)} temas")
        print(f"   Temas disponibles: {list(self.base_conocimiento.keys())}")
    
    def _cargar_base_conocimiento_completa(self) -> Dict:
        """Cargar base de conocimiento COMPLETA con 10+ temas"""
        return {
            # TEMAS ORIGINALES
            "antena": self._tema_antena(),
            "ruido": self._tema_ruido(),
            "construccion": self._tema_construccion(),
            
            # TEMAS EXPANDIDOS
            "apertura_negocio": self._tema_apertura_negocio(),
            "uso_suelo": self._tema_uso_suelo(),
            "publicidad_exterior": self._tema_publicidad_exterior(),
            "estacionamiento": self._tema_estacionamiento(),
            "basura": self._tema_basura(),
            "agua": self._tema_agua(),
            "mascotas": self._tema_mascotas(),
            "arboles": self._tema_arboles(),
            "eventos": self._tema_eventos(),
            "taxi": self._tema_taxi(),
        }
    
    def _tema_antena(self) -> Dict:
        return {
            "titulo": "Instalación de antenas de celulares",
            "analisis": """La instalación de una antena de telefonía celular en la azotea de un domicilio particular es una actividad regulada por la normativa estatal y municipal, clasificada jurídicamente como una "Obra Civil para Telecomunicaciones". Para que la instalación sea legal, se requiere licencia municipal previa que garantice seguridad estructural, cumplimiento ambiental y concesión federal del IFT.""",
            "clasificacion": """Facultad compartida: Inspección y Vigilancia verifica permisos; otras dependencias evalúan proyectos estructurales y riesgos.""",
            "sustento": """Reglamento de Construcción Art. 34 (licencia obligatoria), Art. 185 (clausura por obra sin licencia), Código Urbano Art. 295 Bis (cumplimiento normativo).""",
            "dependencias": """Dirección de Inspección y Vigilancia (ext. 3312-3324), Protección Civil (ext. 3778-3783), Atención Ciudadana (ext. 1210-1216).""",
            "fuentes": """Código Urbano para el Estado de Jalisco, Reglamento de Construcción para Zapopan."""
        }
    
    def _tema_ruido(self) -> Dict:
        return {
            "titulo": "Ruido de establecimientos comerciales",
            "analisis": """El ruido excesivo de establecimientos comerciales, especialmente nocturno, afecta salud y tranquilidad. Está regulado con límites máximos permisibles más estrictos de 22:00 a 07:00 horas.""",
            "clasificacion": """Inspección y Vigilancia verifica cumplimiento de límites; Medio Ambiente evalúa impacto acústico; Desarrollo Económico interviene en giros molestos.""",
            "sustento": """Reglamento de Policía Art. 45 (prohibición ruidos molestos), Reglamento Comercio Art. 28 (respeto horarios/ruido), Código Ambiental Art. 67 (límites permisibles).""",
            "dependencias": """Inspección y Vigilancia (ext. 3312-3313), Medio Ambiente (ext. 3510-3512), Desarrollo Económico (ext. 3410-3412).""",
            "fuentes": """Reglamento de Policía, Justicia Cívica y Buen Gobierno; Reglamento para el Comercio; Código Ambiental Municipal."""
        }
    
    def _tema_construccion(self) -> Dict:
        return {
            "titulo": "Permisos para construcción",
            "analisis": """Toda obra de construcción, ampliación o demolición requiere Licencia de Construcción previa que garantice seguridad estructural, cumplimiento reglamentario, imagen urbana y protección civil.""",
            "clasificacion": """Inspección y Vigilancia verifica licencias; Planeación Urbana otorga licencias; Protección Civil evalúa seguridad; Medio Ambiente autoriza aspectos ambientales.""",
            "sustento": """Reglamento de Construcción Art. 34 (licencia obligatoria), Art. 185 (clausura obras sin licencia), Código Urbano Art. 295 (sanciones).""",
            "dependencias": """Planeación Urbana (ext. 3610-3612), Inspección y Vigilancia (ext. 3312-3313), Protección Civil (ext. 3778-3782), Medio Ambiente (ext. 3510-3512).""",
            "fuentes": """Reglamento de Construcción para Zapopan, Código Urbano para Jalisco."""
        }
    
    def _tema_apertura_negocio(self) -> Dict:
        return {
            "titulo": "Requisitos para apertura de negocio",
            "analisis": """La apertura de negocio requiere Licencia de Funcionamiento Municipal, Permiso de Uso de Suelo, dictamen de Protección Civil, autorización ambiental y registro ante Hacienda Municipal según giro comercial.""",
            "clasificacion": """Desarrollo Económico otorga licencias; Inspección y Vigilancia verifica cumplimiento; Protección Civil dictamina seguridad; Medio Ambiente autoriza.""",
            "sustento": """Reglamento Comercio Art. 5 (licencia obligatoria), Art. 42 (clausura sin licencia), Código Fiscal Art. 78 (sanciones).""",
            "dependencias": """Desarrollo Económico (ext. 3410-3412), Inspección y Vigilancia (ext. 3312-3313), Protección Civil (ext. 3778-3782), Medio Ambiente (ext. 3510-3512).""",
            "fuentes": """Reglamento para el Comercio, Código Fiscal Municipal, Ley de Desarrollo Económico de Jalisco."""
        }
    
    def _tema_uso_suelo(self) -> Dict:
        return {
            "titulo": "Consulta sobre uso de suelo",
            "analisis": """El uso de suelo está regulado por Plan de Desarrollo Urbano con destinos específicos (habitacional, comercial, industrial). Cambio de destino requiere Permiso de Uso de Suelo previo.""",
            "clasificacion": """Planeación Urbana otorga permisos; Inspección y Vigilancia verifica compatibilidad; Instituto de Planeación define usos.""",
            "sustento": """Reglamento Construcción Art. 36 (respeto usos suelo), Código Urbano Art. 78 (sanciones cambio no autorizado), Art. 185 (clausura actividades incompatibles).""",
            "dependencias": """Planeación Urbana (ext. 3610-3612), Inspección y Vigilancia (ext. 3312-3313), Instituto Planeación (ext. 3910-3912), Geoportal municipal.""",
            "fuentes": """Plan de Desarrollo Urbano de Zapopan, Código Urbano para Jalisco, Reglamento de Construcción."""
        }
    
    def _tema_publicidad_exterior(self) -> Dict:
        return {
            "titulo": "Publicidad exterior y espectaculares",
            "analisis": """Publicidad exterior visible desde vía pública requiere autorización municipal previa que regule dimensiones, ubicación, seguridad estructural, contenido y plazos para preservar imagen urbana y seguridad vial.""",
            "clasificacion": """Planeación Urbana otorga permisos; Inspección y Vigilancia verifica y remueve irregular; Protección Civil evalúa seguridad; Imagen Urbana evalúa impacto visual.""",
            "sustento": """Reglamento Publicidad Exterior Art. 12 (permiso obligatorio), Art. 45 (remoción sin permiso), Código Urbano Art. 112 (sanciones).""",
            "dependencias": """Planeación Urbana (ext. 3610-3612), Inspección y Vigilancia (ext. 3312-3313), Protección Civil (ext. 3778-3782), Imagen Urbana (ext. 3710-3712).""",
            "fuentes": """Reglamento de Publicidad Exterior para Zapopan, Código Urbano para Jalisco, Reglamento de Imagen Urbana."""
        }
    
    def _tema_estacionamiento(self) -> Dict:
        return {
            "titulo": "Problemas de estacionamiento",
            "analisis": """Estacionamiento irregular en lugares prohibidos (rampas, banquetas, cruces) o incumplimiento de requisitos de cajones en establecimientos comerciales afecta circulación y seguridad.""",
            "clasificacion": """Inspección y Vigilancia verifica requisitos comerciales; Movilidad regula vía pública; Policía aplica sanciones; Desarrollo Económico verifica licencias.""",
            "sustento": """Reglamento Construcción Art. 89 (requisitos estacionamiento), Reglamento Comercio Art. 31 (cumplimiento cajones), Reglamento Vialidad Art. 45 (prohibición estacionamiento irregular).""",
            "dependencias": """Inspección y Vigilancia (ext. 3312-3313), Movilidad y Transporte (ext. 3810-3812), Policía Municipal (ext. 060), Desarrollo Económico (ext. 3410-3412).""",
            "fuentes": """Reglamento de Construcción, Reglamento para el Comercio, Reglamento de Vialidad."""
        }
    
    def _tema_basura(self) -> Dict:
        return {
            "titulo": "Recolección de basura y residuos",
            "analisis": """El servicio de recolección de basura está regulado con horarios, frecuencias y tipos de residuos específicos. Depósito irregular de residuos, falta de recolección o acumulación de basura constituyen infracciones.""",
            "clasificacion": """Servicios Públicos gestiona recolección; Inspección y Vigilancia sanciona depósito irregular; Medio Ambiente regula residuos especiales.""",
            "sustento": """Reglamento de Limpia Art. 12 (horarios recolección), Art. 28 (prohibición depósito irregular), Código Ambiental Art. 45 (gestión residuos).""",
            "dependencias": """Servicios Públicos (ext. 3550-3552), Inspección y Vigilancia (ext. 3312-3313), Medio Ambiente (ext. 3510-3512).""",
            "fuentes": """Reglamento de Limpia Pública de Zapopan, Código Ambiental Municipal."""
        }
    
    def _tema_agua(self) -> Dict:
        return {
            "titulo": "Problemas con servicio de agua",
            "analisis": """El servicio de agua potable está regulado con estándares de calidad, presión y continuidad. Fugas, falta de servicio, problemas de calidad o conexiones irregulares requieren atención específica.""",
            "clasificacion": """SAPA (Sistema de Agua Potable) gestiona servicio; Inspección y Vigilancia verifica conexiones irregulares; Protección Civil atende fugas graves.""",
            "sustento": """Reglamento de Servicios de Agua Potable Art. 15 (calidad agua), Art. 28 (prohibición conexiones irregulares), Art. 42 (obligación reparación fugas).""",
            "dependencias": """SAPA Zapopan (ext. 3650-3652), Inspección y Vigilancia (ext. 3312-3313), Protección Civil (ext. 3778-3782).""",
            "fuentes": """Reglamento de Servicios de Agua Potable de Zapopan."""
        }
    
    def _tema_mascotas(self) -> Dict:
        return {
            "titulo": "Mascotas y animales domésticos",
            "analisis": """La tenencia de mascotas está regulada con obligaciones de registro, vacunación, control y recolección de heces. Animales sueltos, agresivos o que generen molestias constituyen infracciones.""",
            "clasificacion": """Control Animal registra y controla; Inspección y Vigilancia sanciona infracciones; Salud Pública verifica vacunación.""",
            "sustento": """Reglamento de Tenencia Animal Art. 8 (registro obligatorio), Art. 15 (control de animales), Art. 28 (sanciones por molestias).""",
            "dependencias": """Control Animal (ext. 3850-3852), Inspección y Vigilancia (ext. 3312-3313), Salud Pública (ext. 3450-3452).""",
            "fuentes": """Reglamento de Tenencia Animal de Zapopan."""
        }
    
    def _tema_arboles(self) -> Dict:
        return {
            "titulo": "Podas y tala de árboles",
            "analisis": """La poda, tala o trasplante de árboles en áreas públicas o privadas requiere autorización municipal previa que evalúe necesidad, técnica adecuada y reposición según normativa ambiental.""",
            "clasificacion": """Medio Ambiente autoriza podas/talas; Inspección y Vigilancia verifica autorizaciones; Parques y Jardines ejecuta en áreas públicas.""",
            "sustento": """Reglamento Ambiental Art. 34 (autorización poda/tala), Art. 56 (prohibición tala no autorizada), Art. 78 (obligación reposición).""",
            "dependencias": """Medio Ambiente (ext. 3510-3512), Inspección y Vigilancia (ext. 3312-3313), Parques y Jardines (ext. 3750-3752).""",
            "fuentes": """Reglamento Ambiental de Zapopan, Ley del Equilibrio Ecológico de Jalisco."""
        }
    
    def _tema_eventos(self) -> Dict:
        return {
            "titulo": "Permisos para eventos públicos",
            "analisis": """Eventos públicos (fiestas, conciertos, ferias) requieren permiso municipal que garantice seguridad, control de ruido, estacionamiento, protección civil y cumplimiento de horarios.""",
            "clasificacion": """Desarrollo Económico otorga permisos; Inspección y Vigilancia verifica cumplimiento; Protección Civil evalúa seguridad; Movilidad gestiona tránsito.""",
            "sustento": """Reglamento de Eventos Públicos Art. 12 (permiso obligatorio), Art. 28 (condiciones seguridad), Art. 45 (sanciones por incumplimiento).""",
            "dependencias": """Desarrollo Económico (ext. 3410-3412), Inspección y Vigilancia (ext. 3312-3313), Protección Civil (ext. 3778-3782), Movilidad (ext. 3810-3812).""",
            "fuentes": """Reglamento de Eventos Públicos de Zapopan."""
        }
    
    def _tema_taxi(self) -> Dict:
        return {
            "titulo": "Servicio de taxi y transporte",
            "analisis": """El servicio de taxi está regulado con requisitos de licencia, identificación, tarifas y condiciones de vehículos. Taxis irregulares, sobreprecio o mal servicio constituyen infracciones.""",
            "clasificacion": """Movilidad y Transporte regula y otorga licencias; Inspección y Vigilancia verifica cumplimiento; Policía Municipal aplica sanciones.""",
            "sustento": """Reglamento de Transporte Público Art. 15 (licencia obligatoria), Art. 28 (identificación vehículo), Art. 42 (tarifas reguladas