"""
Router Semántico Avanzado para denuncias ciudadanas
Basado en la documentación del sistema
"""

import re
from typing import Dict, List, Any, Tuple
from datetime import datetime

class SemanticRouter:
    """Router semántico para clasificar denuncias ciudadanas"""
    
    def __init__(self):
        # Categorías principales
        self.categories = {
            'construccion': {
                'keywords': [
                    'obra', 'construcción', 'edificación', 'ampliación', 'demolición',
                    'barda', 'azotea', 'cimentación', 'excavación', 'remodelación',
                    'material de construcción', 'andamios', 'maquinaria de obra',
                    'antena', 'telecomunicación', 'urbanización', 'fraccionamiento',
                    'uso de suelo', 'licencia de obra', 'permiso de construcción',
                    'edificio', 'casa', 'departamento', 'local comercial'
                ],
                'area': 'ÁREA CONSTRUCCIÓN',
                'dependencias': [
                    'Dirección de Inspección y Vigilancia',
                    'Obras Públicas', 
                    'Ordenamiento del Territorio',
                    'Protección Civil (si hay riesgo)'
                ],
                'reglamentos': [
                    'Reglamento de Construcción',
                    'Reglamento de Urbanización', 
                    'Código Urbano para el Estado de Jalisco'
                ]
            },
            'comercio': {
                'keywords': [
                    'negocio', 'local', 'establecimiento', 'giro', 'licencia',
                    'permiso comercial', 'horario', 'venta', 'alcohol',
                    'bebidas alcohólicas', 'restaurante', 'bar', 'antro',
                    'tienda', 'comercio', 'comercio en vía pública', 'ambulante',
                    'tianguis', 'puesto', 'vendedor', 'mercado',
                    'prestación de servicios', 'evento comercial', 'extensión de giro',
                    'abarrotes', 'farmacia', 'taller', 'oficina'
                ],
                'area': 'ÁREA COMERCIO',
                'dependencias': [
                    'Dirección de Inspección y Vigilancia',
                    'Dirección de Padrón y Licencias',
                    'Dirección de Tianguis y Comercio en Espacios Abiertos',
                    'Consejo Municipal de Giros Restringidos (si hay alcohol)'
                ],
                'reglamentos': [
                    'Reglamento para el Comercio, la Industria y la Prestación de Servicios',
                    'Reglamento de Tianguis y Comercio en Espacios Públicos',
                    'Reglamento del Consejo Municipal de Giros Restringidos',
                    'GirosXAreas 2025'
                ]
            },
            'tecnica_medio_ambiente': {
                'keywords': [
                    'ruido', 'contaminación', 'humo', 'olores', 'residuos',
                    'basura', 'desperdicio', 'descargas', 'emisiones', 'tala',
                    'poda', 'derribo', 'árbol', 'arbolado', 'anuncio',
                    'espectacular', 'publicidad exterior', 'rastro', 'carnicería',
                    'pollería', 'productos cárnicos', 'animales', 'maltrato animal',
                    'sanidad', 'impacto ambiental', 'vibraciones', 'agua',
                    'drenaje', 'alcantarillado', 'aire', 'polvo'
                ],
                'area': 'ÁREA TÉCNICA',
                'dependencias': [
                    'Dirección de Inspección y Vigilancia',
                    'Dirección de Medio Ambiente',
                    'Dirección de Parques y Jardines',
                    'Dirección del Rastro',
                    'Protección Animal o dependencia competente',
                    'Protección Civil (si hay riesgo)',
                    'Padrón y Licencias (si hay comercio involucrado)'
                ],
                'reglamentos': [
                    'Código Ambiental',
                    'Reglamento de Protección al Medio Ambiente',
                    'Reglamento de Residuos',
                    'Reglamento de Arbolado Urbano',
                    'Reglamento de Anuncios',
                    'Reglamento de Rastros',
                    'Reglamento de Protección y Trato Digno a los Animales',
                    'NOM-081-SEMARNAT-1994'
                ]
            },
            'riesgos_proteccion_civil': {
                'keywords': [
                    'riesgo', 'peligro', 'colapso', 'fuga', 'incendio',
                    'explosión', 'cableado riesgoso', 'tanque de gas',
                    'extintores', 'medidas de seguridad', 'evacuación',
                    'sobrecupo', 'salida de emergencia', 'evento masivo inseguro',
                    'inmueble inseguro', 'derrumbe', 'grieta', 'estructura'
                ],
                'area': 'ÁREA TÉCNICA o ÁREA GENERAL con derivación',
                'dependencias': [
                    'Protección Civil',
                    'Dirección de Inspección y Vigilancia',
                    'Obras Públicas',
                    'Comercio o Padrón y Licencias (si hay negocio)'
                ],
                'reglamentos': [
                    'Reglamento de Gestión Integral de Riesgos',
                    'Reglamento para el Comercio, la Industria y la Prestación de Servicios',
                    'Reglamento de Construcción'
                ]
            },
            'espacio_publico': {
                'keywords': [
                    'banqueta', 'calle', 'andador', 'glorieta', 'plaza',
                    'jardín', 'espacio público', 'ocupación indebida',
                    'evento en vía pública', 'instalación temporal',
                    'actividad artística o cultural en espacio público',
                    'parque', 'área verde', 'mobiliario urbano'
                ],
                'area': 'ÁREA COMERCIO o ÁREA GENERAL',
                'dependencias': [
                    'Dirección de Inspección y Vigilancia',
                    'Dirección de Tianguis y Comercio en Espacios Abiertos',
                    'Dirección de Cultura',
                    'Turismo y Centro Histórico',
                    'Ordenamiento del Territorio'
                ],
                'reglamentos': [
                    'Reglamento de Tianguis y Comercio en Espacios Públicos',
                    'Reglamento del Andador 20 de Noviembre',
                    'Reglamento del Jardín del Arte de la Glorieta Chapalita'
                ]
            }
        }
        
        # Categorías NO competencia de Inspección y Vigilancia
        self.non_competence_categories = {
            'seguridad_publica': {
                'keywords': [
                    'robo', 'asalto', 'agresión', 'violencia', 'amenazas',
                    'riña', 'narcomenudeo', 'delito', 'persona armada',
                    'pandilla', 'extorsión', 'secuestro', 'homicidio'
                ],
                'dependencia': 'Comisaría de Seguridad Pública / Fiscalía'
            },
            'servicios_publicos': {
                'keywords': [
                    'bache', 'luminaria', 'alumbrado', 'recolección de basura domiciliaria',
                    'poda de mantenimiento municipal', 'limpieza de calles',
                    'fuga de agua', 'drenaje', 'alcantarillado', 'alcantarilla',
                    'poste', 'cable', 'semáforo', 'señalización'
                ],
                'dependencia': 'Servicios Públicos Municipales / SIAPA / Parques y Jardines'
            }
        }
        
        # Orden de prioridad
        self.priority_order = [
            'riesgos_proteccion_civil',
            'construccion', 
            'comercio',
            'tecnica_medio_ambiente',
            'espacio_publico'
        ]
    
    def classify_query(self, query: str) -> Dict[str, Any]:
        """Clasificar una consulta/demanda ciudadana"""
        query_lower = query.lower()
        
        # 1. Verificar si es NO competencia
        for cat_name, cat_info in self.non_competence_categories.items():
            for keyword in cat_info['keywords']:
                if keyword in query_lower:
                    return {
                        'categoria_principal': cat_name,
                        'categoria_secundaria': None,
                        'area_detectada': 'FUERA DEL ÁMBITO PRINCIPAL DE INSPECCIÓN Y VIGILANCIA',
                        'dependencia_responsable': cat_info['dependencia'],
                        'dependencias_concurrentes': [],
                        'competencia_detectada': 'no_competencia',
                        'tipo_consulta': 'denuncia_ciudadana',
                        'indicador_evento': 'posible_infraccion' if 'seguridad' not in cat_name else 'delito'
                    }
        
        # 2. Calcular scores para cada categoría
        scores = {}
        for cat_name, cat_info in self.categories.items():
            score = 0
            for keyword in cat_info['keywords']:
                if keyword in query_lower:
                    score += 1
            
            # Bonus por múltiples coincidencias
            if score > 0:
                scores[cat_name] = {
                    'score': score,
                    'info': cat_info
                }
        
        # 3. Determinar categoría principal y secundaria
        if not scores:
            # Categoría general si no hay coincidencias
            return {
                'categoria_principal': 'general',
                'categoria_secundaria': None,
                'area_detectada': 'ÁREA GENERAL',
                'dependencia_responsable': 'Dirección de Inspección y Vigilancia',
                'dependencias_concurrentes': [],
                'competencia_detectada': 'por_determinar',
                'tipo_consulta': 'consulta_normativa',
                'indicador_evento': 'consulta_preventiva'
            }
        
        # Ordenar por score y prioridad
        sorted_categories = sorted(
            scores.items(),
            key=lambda x: (x[1]['score'], self.priority_order.index(x[0]) if x[0] in self.priority_order else 99),
            reverse=True
        )
        
        # Categoría principal (la de mayor score/prioridad)
        main_cat_name, main_cat_data = sorted_categories[0]
        main_cat_info = main_cat_data['info']
        
        # Categoría secundaria (la siguiente si existe)
        secondary_cat_name = None
        secondary_cat_info = None
        if len(sorted_categories) > 1:
            secondary_cat_name, secondary_cat_data = sorted_categories[1]
            if secondary_cat_data['score'] >= 1:  # Al menos una coincidencia
                secondary_cat_info = secondary_cat_data['info']
        
        # 4. Determinar competencia
        competencia = 'exclusiva'
        if 'compartida' in query_lower or 'concurrente' in query_lower:
            competencia = 'concurrente'
        elif secondary_cat_name:
            competencia = 'principal_con_secundaria'
        
        # 5. Determinar tipo de consulta
        tipo_consulta = self._determine_query_type(query_lower)
        
        # 6. Determinar indicador de evento
        indicador_evento = self._determine_event_indicator(query_lower)
        
        return {
            'categoria_principal': main_cat_name,
            'categoria_secundaria': secondary_cat_name,
            'area_detectada': main_cat_info['area'],
            'dependencia_responsable': main_cat_info['dependencias'][0],
            'dependencias_concurrentes': main_cat_info['dependencias'][1:] + 
                                        (secondary_cat_info['dependencias'] if secondary_cat_info else []),
            'reglamentos_prioritarios': list(set(main_cat_info['reglamentos'] + 
                                               (secondary_cat_info['reglamentos'] if secondary_cat_info else []))),
            'competencia_detectada': competencia,
            'tipo_consulta': tipo_consulta,
            'indicador_evento': indicador_evento
        }
    
    def _determine_query_type(self, query: str) -> str:
        """Determinar tipo de consulta"""
        if any(word in query for word in ['denunci', 'queja', 'report', 'quej']):
            return 'denuncia_ciudadana'
        elif any(word in query for word in ['puede', 'se puede', 'es posible', 'está permitido']):
            return 'consulta_normativa'
        elif any(word in query for word in ['trámite', 'procedimiento', 'requisito', 'documento']):
            return 'procedimiento_administrativo'
        elif any(word in query for word in ['información', 'dato', 'contacto', 'teléfono']):
            return 'solicitud_informacion'
        else:
            return 'reporte_urbano'
    
    def _determine_event_indicator(self, query: str) -> str:
        """Determinar indicador de evento"""
        if any(word in query for word in ['riesgo', 'peligro', 'urgente', 'inmediat']):
            return 'posible_riesgo_urbano'
        elif any(word in query for word in ['vecino', 'vecina', 'conflicto', 'problema con']):
            return 'posible_conflicto_vecinal'
        elif any(word in query for word in ['siempre', 'constantemente', 'recurrente', 'desde hace']):
            return 'denuncia_recurrente'
        elif any(word in query for word in ['quiero', 'deseo', 'planeo', 'estoy pensando']):
            return 'consulta_preventiva'
        else:
            return 'posible_infraccion'
    
    def generate_structured_data(self, query: str, classification: Dict, 
                                rag_results: List[Dict] = None) -> Dict[str, Any]:
        """Generar datos estructurados para el dataset"""
        from datetime import datetime
        
        # IDs para trazabilidad
        timestamp = datetime.now().isoformat()
        consulta_id = f"Q-{int(datetime.now().timestamp()):08d}"
        sesion_id = f"S-{int(datetime.now().timestamp()):06d}"
        
        # Datos básicos
        structured_data = {
            'timestamp': timestamp,
            'consulta_id': consulta_id,
            'sesion_usuario': sesion_id,
            'descripcion_usuario': query,
            'longitud_consulta': len(query),
            'idioma': 'es',
            
            # Clasificación semántica
            'categoria_principal': classification['categoria_principal'],
            'categoria_secundaria': classification['categoria_secundaria'],
            'area_detectada': classification['area_detectada'],
            'tipo_consulta': classification['tipo_consulta'],
            'indicador_evento': classification['indicador_evento'],
            
            # Clasificación institucional
            'dependencia_responsable': classification['dependencia_responsable'],
            'dependencias_concurrentes': classification['dependencias_concurrentes'],
            'competencia_detectada': classification['competencia_detectada'],
            'nivel_normativo_aplicado': 'municipal',  # Por defecto, se ajusta con RAG
            
            # Datos jurídicos (se llenan con RAG)
            'documentos_consultados': [],
            'articulos_citados': [],
            'ids_juridicos_utilizados': [],
            'reglamentos_prioritarios': classification.get('reglamentos_prioritarios', []),
            
            # Clasificación urbana (se estima)
            'categoria_problema_urbano': self._estimate_urban_problem(query),
            'sector_regulatorio': classification['categoria_principal'],
            'clasificacion_riesgo': self._estimate_risk_level(query),
            'impacto_urbano': self._estimate_urban_impact(query),
            'complejidad_consulta': self._estimate_complexity(query),
            
            # Datos operativos (se llenan después)
            'tiempo_respuesta_segundos': 0,
            'calificacion_sugerida': '',
            'respuesta_generada': ''
        }
        
        # Añadir datos de RAG si están disponibles
        if rag_results:
            # Esto se llenaría con datos reales del RAG
            pass
        
        return structured_data
    
    def _estimate_urban_problem(self, query: str) -> str:
        """Estimar categoría de problema urbano"""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['ruido', 'música', 'sonido', 'volumen', 'alto']):
            return 'ruido_excesivo'
        elif any(word in query_lower for word in ['basura', 'residuo', 'desecho', 'contaminación']):
            return 'residuos'
        elif any(word in query_lower for word in ['obra', 'construcción', 'edificación', 'demolición']):
            return 'obra_sin_licencia'
        elif any(word in query_lower for word in ['anuncio', 'espectacular', 'publicidad', 'cartel']):
            return 'anuncios_irregulares'
        elif any(word in query_lower for word in ['comercio', 'negocio', 'local', 'giro', 'restaurante']):
            return 'comercio_irregular'
        elif any(word in query_lower for word in ['árbol', 'tala', 'poda', 'arbolado']):
            return 'tala_arboles'
        elif any(word in query_lower for word in ['alcohol', 'bar', 'antro', 'licor']):
            return 'venta_alcohol_irregular'
        elif any(word in query_lower for word in ['animal', 'mascota', 'maltrato']):
            return 'maltrato_animal'
        else:
            return 'incumplimiento_normativo'
    
    def _estimate_risk_level(self, query: str) -> str:
        """Estimar nivel de riesgo"""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['riesgo', 'peligro', 'urgente', 'inmediato', 'colapso', 'incendio']):
            return 'riesgo_inmediato'
        elif any(word in query_lower for word in ['posible', 'podría', 'tal vez', 'quizás']):
            return 'riesgo_potencial'
        else:
            return 'sin_riesgo'
    
    def _estimate_urban_impact(self, query: str) -> str:
        """Estimar impacto urbano"""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['muchos', 'varios', 'todos', 'comunidad', 'vecindario']):
            return 'alto'
        elif any(word in query_lower for word in ['algunos', 'varios', 'varias']):
            return 'medio'
        else:
            return 'bajo'
    
    def _estimate_complexity(self, query: str) -> str:
        """Estimar complejidad de la consulta"""
        words = len(query.split())
        
        if words > 50:
            return 'alta'
        elif words > 20:
            return 'media'
        else:
            return 'baja'


# Instancia global para uso en la app
semantic_router = SemanticRouter()

if __name__ == "__main__":
    # Test del router semántico
    router = SemanticRouter()
    
    test_queries = [
        "Un restaurante tiene música muy fuerte hasta la madrugada y además parece vender alcohol fuera de horario",
        "Una obra está invadiendo la banqueta y además no tiene permiso",
        "Un vecino está talando árboles sin autorización",
        "Hay un robo frecuente en mi colonia",
        "Hay un bache grande en la calle principal"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Query: {query}")
        classification = router.classify_query(query)
        print(f"📊 Clasificación:")
        print(f"  Categoría principal: {classification['categoria_principal']}")
        print(f"  Categoría secundaria: {classification['categoria_secundaria']}")
        print(f"  Área: {classification['area_detectada']}")
        print(f"  Dependencia responsable: {classification['dependencia_responsable']}")
        print(f"  Tipo consulta: {classification['tipo_consulta']}")
        print(f"  Indicador evento: {classification['indicador_evento']}")