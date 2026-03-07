"""
Integración con Google Sheets para chatbot-zapopan
Basado en la documentación de arquitectura
"""

import gspread
from google.oauth2.service_account import Credentials
from typing import Dict, List, Any
import json
import os
from datetime import datetime

class GoogleSheetsIntegration:
    """Gestión de conexión y escritura en Google Sheets"""
    
    def __init__(self, credentials_path: str = None):
        """
        Inicializar conexión a Google Sheets
        
        Args:
            credentials_path: Ruta al archivo JSON de credenciales de servicio
                             Si es None, busca en secrets de Streamlit
        """
        self.credentials_path = credentials_path
        self.client = None
        self.spreadsheet = None
        self.worksheet = None
        
        # Esquema de columnas basado en documentación
        self.column_schema = [
            "timestamp",
            "consulta_id", 
            "sesion_usuario",
            "descripcion_usuario",
            "longitud_consulta",
            "idioma",
            "categoria_principal",
            "categoria_secundaria",
            "area_detectada",
            "tipo_consulta",
            "indicador_evento",
            "dependencia_responsable",
            "dependencias_concurrentes",
            "competencia_detectada",
            "nivel_normativo_aplicado",
            "documentos_consultados",
            "articulos_citados",
            "ids_juridicos_utilizados",
            "reglamentos_prioritarios",
            "categoria_problema_urbano",
            "sector_regulatorio",
            "clasificacion_riesgo",
            "impacto_urbano",
            "complejidad_consulta",
            "tiempo_respuesta_segundos",
            "calificacion_sugerida",
            "respuesta_generada"
        ]
    
    def connect(self, spreadsheet_id: str = None, worksheet_name: str = "consultas_chatbot_zapopan"):
        """
        Conectar a Google Sheets
        
        Args:
            spreadsheet_id: ID de la hoja de cálculo de Google Sheets
            worksheet_name: Nombre de la hoja de trabajo
        """
        try:
            # Determinar credenciales
            if self.credentials_path and os.path.exists(self.credentials_path):
                # Usar archivo de credenciales
                creds = Credentials.from_service_account_file(
                    self.credentials_path,
                    scopes=['https://www.googleapis.com/auth/spreadsheets']
                )
            else:
                # Intentar usar credenciales de entorno/Streamlit
                # Para MVP, usaremos un enfoque simplificado
                print("⚠️ No se encontraron credenciales específicas. Usando modo de demostración.")
                print("ℹ️ En producción, configura las credenciales de servicio de Google Sheets")
                return self._setup_demo_mode()
            
            # Conectar cliente
            self.client = gspread.authorize(creds)
            
            # Abrir spreadsheet
            if spreadsheet_id:
                self.spreadsheet = self.client.open_by_key(spreadsheet_id)
            else:
                # Crear nueva spreadsheet si no existe
                self.spreadsheet = self.client.create("Chatbot Zapopan - Consultas Normativas")
                print(f"✅ Nueva spreadsheet creada: {self.spreadsheet.title}")
                print(f"📋 URL: {self.spreadsheet.url}")
            
            # Obtener o crear worksheet
            try:
                self.worksheet = self.spreadsheet.worksheet(worksheet_name)
                print(f"✅ Worksheet '{worksheet_name}' encontrada")
            except gspread.exceptions.WorksheetNotFound:
                self.worksheet = self.spreadsheet.add_worksheet(
                    title=worksheet_name,
                    rows=1000,
                    cols=len(self.column_schema)
                )
                print(f"✅ Worksheet '{worksheet_name}' creada")
                
                # Escribir encabezados
                self.worksheet.update('A1', [self.column_schema])
                print(f"📝 Encabezados escritos: {len(self.column_schema)} columnas")
            
            print(f"✅ Conectado a Google Sheets: {self.spreadsheet.title}")
            return True
            
        except Exception as e:
            print(f"❌ Error conectando a Google Sheets: {e}")
            return self._setup_demo_mode()
    
    def _setup_demo_mode(self):
        """Configurar modo de demostración (sin Google Sheets real)"""
        print("🔧 Configurando modo de demostración...")
        print("ℹ️ Los datos se guardarán localmente en 'consultas_demo.csv'")
        print("ℹ️ Para usar Google Sheets real, configura credenciales de servicio")
        
        # Crear archivo CSV local para demostración
        import pandas as pd
        df = pd.DataFrame(columns=self.column_schema)
        df.to_csv('consultas_demo.csv', index=False, encoding='utf-8')
        
        self.demo_mode = True
        return True
    
    def append_consultation(self, data: Dict[str, Any]) -> bool:
        """
        Agregar una consulta a Google Sheets
        
        Args:
            data: Diccionario con datos estructurados de la consulta
            
        Returns:
            bool: True si se guardó exitosamente
        """
        try:
            # Preparar fila según esquema de columnas
            row = []
            for column in self.column_schema:
                value = data.get(column, "")
                
                # Procesar listas como texto separado por "|"
                if isinstance(value, list):
                    value = "|".join(str(item) for item in value if item)
                
                # Convertir a string
                row.append(str(value) if value is not None else "")
            
            if hasattr(self, 'demo_mode') and self.demo_mode:
                # Modo demostración: guardar en CSV local
                import pandas as pd
                try:
                    df = pd.read_csv('consultas_demo.csv', encoding='utf-8')
                except:
                    df = pd.DataFrame(columns=self.column_schema)
                
                new_row = pd.DataFrame([row], columns=self.column_schema)
                df = pd.concat([df, new_row], ignore_index=True)
                df.to_csv('consultas_demo.csv', index=False, encoding='utf-8')
                
                print(f"✅ Consulta guardada en modo demo (CSV local)")
                print(f"   ID: {data.get('consulta_id', 'N/A')}")
                print(f"   Categoría: {data.get('categoria_principal', 'N/A')}")
                return True
            
            # Modo real: agregar a Google Sheets
            if self.worksheet:
                # Encontrar la siguiente fila vacía
                next_row = len(self.worksheet.get_all_values()) + 1
                
                # Actualizar la fila
                self.worksheet.update(
                    f'A{next_row}',
                    [row]
                )
                
                print(f"✅ Consulta guardada en Google Sheets")
                print(f"   Fila: {next_row}")
                print(f"   ID: {data.get('consulta_id', 'N/A')}")
                print(f"   URL: {self.spreadsheet.url}")
                return True
            else:
                print("⚠️ No hay conexión a Google Sheets activa")
                return False
                
        except Exception as e:
            print(f"❌ Error guardando consulta: {e}")
            return False
    
    def get_consultation_count(self) -> int:
        """Obtener número total de consultas registradas"""
        try:
            if hasattr(self, 'demo_mode') and self.demo_mode:
                import pandas as pd
                try:
                    df = pd.read_csv('consultas_demo.csv', encoding='utf-8')
                    return len(df)
                except:
                    return 0
            
            if self.worksheet:
                values = self.worksheet.get_all_values()
                # Restar 1 por los encabezados
                return max(0, len(values) - 1)
            return 0
        except:
            return 0
    
    def get_recent_consultations(self, limit: int = 10) -> List[Dict]:
        """Obtener consultas recientes"""
        try:
            if hasattr(self, 'demo_mode') and self.demo_mode:
                import pandas as pd
                try:
                    df = pd.read_csv('consultas_demo.csv', encoding='utf-8')
                    df = df.tail(limit)
                    return df.to_dict('records')
                except:
                    return []
            
            if self.worksheet:
                values = self.worksheet.get_all_values()
                if len(values) <= 1:  # Solo encabezados
                    return []
                
                # Convertir filas a diccionarios
                consultations = []
                headers = values[0]
                
                for row in values[1:][-limit:]:
                    consultation = {}
                    for i, header in enumerate(headers):
                        if i < len(row):
                            value = row[i]
                            # Convertir strings con "|" de vuelta a listas
                            if "|" in value and header in [
                                'dependencias_concurrentes',
                                'documentos_consultados', 
                                'articulos_citados',
                                'ids_juridicos_utilizados',
                                'reglamentos_prioritarios'
                            ]:
                                consultation[header] = [v.strip() for v in value.split("|") if v.strip()]
                            else:
                                consultation[header] = value
                        else:
                            consultation[header] = ""
                    consultations.append(consultation)
                
                return consultations
            return []
        except Exception as e:
            print(f"❌ Error obteniendo consultas recientes: {e}")
            return []
    
    def create_dashboard_sheet(self, sheet_name: str = "dashboard_indicadores"):
        """Crear hoja de dashboard con indicadores"""
        try:
            if hasattr(self, 'demo_mode') and self.demo_mode:
                print("ℹ️ Modo demo: Dashboard se creará localmente")
                return True
            
            if not self.spreadsheet:
                print("⚠️ No hay spreadsheet conectada")
                return False
            
            # Crear o obtener hoja de dashboard
            try:
                dashboard_sheet = self.spreadsheet.worksheet(sheet_name)
                print(f"✅ Hoja de dashboard '{sheet_name}' ya existe")
            except gspread.exceptions.WorksheetNotFound:
                dashboard_sheet = self.spreadsheet.add_worksheet(
                    title=sheet_name,
                    rows=50,
                    cols=10
                )
                print(f"✅ Hoja de dashboard '{sheet_name}' creada")
            
            # Actualizar con indicadores
            self._update_dashboard_indicators(dashboard_sheet)
            
            return True
            
        except Exception as e:
            print(f"❌ Error creando hoja de dashboard: {e}")
            return False
    
    def _update_dashboard_indicators(self, worksheet):
        """Actualizar indicadores en la hoja de dashboard"""
        try:
            # Obtener datos de consultas
            consultations = self.get_recent_consultations(limit=1000)
            
            if not consultations:
                # Datos de ejemplo para dashboard
                indicators = [
                    ["INDICADOR", "VALOR", "DESCRIPCIÓN"],
                    ["Total consultas", "0", "Consultas registradas"],
                    ["Consultas hoy", "0", "Consultas en las últimas 24h"],
                    ["Categoría principal", "N/A", "Categoría más frecuente"],
                    ["Dependencia principal", "N/A", "Dependencia más mencionada"],
                    ["Riesgo inmediato", "0", "Casos con riesgo inmediato"],
                    ["Tiempo promedio", "0s", "Tiempo promedio de respuesta"],
                    ["Última actualización", datetime.now().strftime("%Y-%m-%d %H:%M"), ""]
                ]
            else:
                # Calcular indicadores reales
                import pandas as pd
                df = pd.DataFrame(consultations)
                
                # Convertir timestamps a datetime
                try:
                    df['timestamp_dt'] = pd.to_datetime(df['timestamp'])
                    today = pd.Timestamp.now().normalize()
                    consultations_today = len(df[df['timestamp_dt'] >= today])
                except:
                    consultations_today = 0
                
                # Calcular categoría más frecuente
                if 'categoria_principal' in df.columns:
                    top_category = df['categoria_principal'].mode()
                    top_category = top_category[0] if not top_category.empty else "N/A"
                else:
                    top_category = "N/A"
                
                # Calcular dependencia más frecuente
                if 'dependencia_responsable' in df.columns:
                    top_dependency = df['dependencia_responsable'].mode()
                    top_dependency = top_dependency[0] if not top_dependency.empty else "N/A"
                else:
                    top_dependency = "N/A"
                
                # Calcular casos de riesgo
                if 'clasificacion_riesgo' in df.columns:
                    risk_cases = len(df[df['clasificacion_riesgo'] == 'riesgo_inmediato'])
                else:
                    risk_cases = 0
                
                # Calcular tiempo promedio
                if 'tiempo_respuesta_segundos' in df.columns:
                    try:
                        avg_time = df['tiempo_respuesta_segundos'].astype(float).mean()
                        avg_time_str = f"{avg_time:.1f}s"
                    except:
                        avg_time_str = "N/A"
                else:
                    avg_time_str = "N/A"
                
                indicators = [
                    ["INDICADOR", "VALOR", "DESCRIPCIÓN"],
                    ["Total consultas", str(len(consultations)), "Consultas registradas"],
                    ["Consultas hoy", str(consultations_today), "Consultas en las últimas 24h"],
                    ["Categoría principal", top_category, "Categoría más frecuente"],
                    ["Dependencia principal", top_dependency, "Dependencia más mencionada"],
                    ["Riesgo inmediato", str(risk_cases), "Casos con riesgo inmediato"],
                    ["Tiempo promedio", avg_time_str, "Tiempo promedio de respuesta"],
                    ["Última actualización", datetime.now().strftime("%Y-%m-%d %H:%M"), ""]
                ]
            
            # Actualizar hoja
            worksheet.update('A1', indicators)
            print(f"📊 Dashboard actualizado con {len(indicators)-1} indicadores")
            
        except Exception as e:
            print(f"⚠️ Error actualizando dashboard: {e}")


# Instancia global para uso en la app
sheets_integration = GoogleSheetsIntegration()

if __name__ == "__main__":
    # Test del módulo
    print("🧪 Test Google Sheets Integration")
    print("="*50)
    
    gs = GoogleSheetsIntegration()
    
    # Conectar (en modo demo)
    if gs.connect():
        print("✅ Conexión establecida")
        
        # Datos de prueba
        test_data = {
            "timestamp": datetime.now().isoformat(),
            "consulta_id": "Q-TEST-001",
            "sesion_usuario": "S-TEST-001",
            "descripcion_usuario": "Test de integración Google Sheets",
            "longitud_consulta": 45,
            "idioma": "es",
            "categoria_principal": "comercio",
            "categoria_secundaria": "tecnica_medio_ambiente",
            "area_detectada": "ÁREA COMERCIO",
            "tipo_consulta": "denuncia_ciudadana",
            "indicador_evento": "posible_infraccion",
            "dependencia_responsable": "Dirección de Inspección y Vigilancia",
            "dependencias_concurrentes": ["Dirección de Medio Ambiente", "Dirección de Padrón y Licencias"],
            "competencia_detectada": "concurrente",
            "nivel_normativo_aplicado": "municipal",
            "documentos_consultados": ["Reglamento para el Comercio", "Código Ambiental"],
            "articulos_citados": ["Reglamento Comercio Art. 1", "Código Ambiental Art. 25"],
            "ids_juridicos_utilizados": ["mx|jal|zapopan|reglamento_comercio|art_1"],
            "reglamentos_prioritarios": ["Reglamento para el Comercio", "Código Ambiental"],
            "categoria_problema_urbano": "ruido_excesivo",
            "sector_regulatorio": "comercio",
            "clasificacion_riesgo": "riesgo_potencial",
            "impacto_urbano": "medio",
            "complejidad_consulta": "media",
            "tiempo_respuesta_segundos": 3.2,
            "calificacion_sugerida": "media",
            "respuesta_generada": "Respuesta de prueba generada por el sistema"
        }
        
        # Agregar consulta
        if gs.append_consultation(test_data):
            print("✅ Consulta de prueba guardada")
        
        # Obtener conteo
        count = gs.get_consultation_count()
        print(f"📊 Total consultas: {count}")
        
        # Crear dashboard
        gs.create_dashboard_sheet()
        
        print("\n✅ Test completado exitosamente")
        print("ℹ️ Para usar Google Sheets real:")
        print("   1. Crea credenciales de servicio en Google Cloud Console")
        print("   2. Descarga el archivo JSON")
        print("   3. Configura la ruta en GoogleSheetsIntegration()")
        print("   4. Proporciona el spreadsheet_id en connect()")