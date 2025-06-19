import os
import pandas as pd
import logging
from config.settings import settings

class QueryService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.oracle_session = None
        
    def _get_oracle_session(self):
        """Obtiene sesión Oracle de forma lazy"""
        if self.oracle_session is None:
            from adapters.db_adapter import get_oracle_session, is_oracle_available
            
            if not is_oracle_available():
                raise Exception("Oracle no está disponible. Verifica tu configuración.")
            
            self.oracle_session = get_oracle_session()
        
        return self.oracle_session
    
    def run_queries(self):
        """Ejecuta todas las consultas SQL y genera archivos Excel"""
        self.logger.info("=== Iniciando generación de archivos Excel ===")
        
        try:
            # Verificar Oracle disponible
            session = self._get_oracle_session()
            
            # Resto de tu lógica existente...
            sql_dir = os.path.join(os.path.dirname(__file__), '..', settings.PATH_SQL)
            output_dir = os.path.join(os.path.dirname(__file__), '..', settings.FILE_XLSX)
            
            # Crear directorio de salida si no existe
            os.makedirs(output_dir, exist_ok=True)
            
            total_files = 0
            
            # Recorrer archivos SQL
            for root, dirs, files in os.walk(sql_dir):
                for file in files:
                    if not file.lower().endswith('.sql'):
                        continue
                    
                    try:
                        file_path = os.path.join(root, file)
                        self._process_sql_file(file_path, output_dir, session)
                        total_files += 1
                        
                    except Exception as e:
                        self.logger.error(f"Error procesando {file}: {e}")
            
            self.logger.info(f"✅ Proceso completado: {total_files} archivos generados")
            
        except Exception as e:
            self.logger.error(f"❌ Error en run_queries: {e}")
            raise
        finally:
            if self.oracle_session:
                self.oracle_session.close()
    
    def _process_sql_file(self, sql_file_path, output_dir, session):
        """Procesa un archivo SQL individual"""
        file_name = os.path.basename(sql_file_path)
        excel_name = file_name.replace('.sql', '.xlsx')
        
        self.logger.info(f"Procesando: {file_name}")
        
        # Leer archivo SQL
        with open(sql_file_path, 'r', encoding='utf-8') as f:
            sql_content = f.read().strip()
            if sql_content.endswith(';'):
                sql_content = sql_content[:-1]
        
        # Ejecutar consulta
        df = pd.read_sql_query(sql_content, session.bind)
        
        if df.empty:
            self.logger.warning(f"Sin datos para {file_name}")
            return
        
        # Guardar Excel
        excel_path = os.path.join(output_dir, excel_name)
        df.to_excel(excel_path, index=False, engine='openpyxl')
        
        self.logger.info(f"✅ {excel_name}: {len(df)} registros exportados")