import pyodbc
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import pandas as pd
from config.settings import settings
import logging

class SQLServerAdapter:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Verificar configuración antes de intentar conectar
        if not all([settings.SQLSERVER_HOST, settings.SQLSERVER_USER, settings.SQLSERVER_PASS]):
            self.logger.warning("Configuración SQL Server incompleta. Adaptador en modo offline.")
            self.engine = None
            self.SessionLocal = None
            return
            
        try:
            # Configuración de conexión SQL Server
            self.server = settings.SQLSERVER_HOST
            self.database = settings.SQLSERVER_DB
            self.username = settings.SQLSERVER_USER
            self.password = settings.SQLSERVER_PASS
            self.driver = settings.SQLSERVER_DRIVER or '{ODBC Driver 17 for SQL Server}'
            
            # Crear engine de SQLAlchemy
            connection_string = (
                f"mssql+pyodbc://{self.username}:{self.password}@{self.server}/"
                f"{self.database}?driver={self.driver.replace(' ', '+').replace('{', '').replace('}', '')}"
            )
            
            self.engine = create_engine(connection_string, echo=False)
            self.SessionLocal = sessionmaker(bind=self.engine)
            
            self.logger.info("SQL Server adapter inicializado correctamente")
            
        except Exception as e:
            self.logger.error(f"Error inicializando SQL Server adapter: {e}")
            self.engine = None
            self.SessionLocal = None
    
    def get_session(self):
        """Obtiene una nueva sesión de SQLAlchemy"""
        if not self.SessionLocal:
            raise Exception("SQL Server adapter no inicializado correctamente")
        return self.SessionLocal()
    
    def execute_query(self, query, params=None):
        """Ejecuta una consulta SQL y devuelve un DataFrame"""
        if not self.engine:
            raise Exception("SQL Server adapter no inicializado correctamente")
            
        try:
            with self.engine.connect() as conn:
                result = pd.read_sql_query(query, conn)
                return result
        except Exception as e:
            self.logger.error(f"Error ejecutando consulta: {e}")
            self.logger.error(f"Query: {query}")
            raise
    
    def table_exists(self, table_name, schema='dbo'):
        """Verifica si una tabla existe"""
        query = f"""
        SELECT COUNT(*) as count
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_SCHEMA = '{schema}' AND TABLE_NAME = '{table_name}'
        """
        try:
            result = self.execute_query(query)
            return result['count'].iloc[0] > 0
        except Exception as e:
            self.logger.error(f"Error verificando existencia de tabla {table_name}: {e}")
            return False
    
    def get_table_columns(self, table_name, schema='dbo'):
        """Obtiene las columnas de una tabla"""
        query = f"""
        SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_SCHEMA = '{schema}' AND TABLE_NAME = '{table_name}'
        ORDER BY ORDINAL_POSITION
        """
        try:
            return self.execute_query(query)
        except Exception as e:
            self.logger.error(f"Error obteniendo columnas de tabla {table_name}: {e}")
            return None
    
    def truncate_table(self, table_name, schema='dbo'):
        """Trunca una tabla"""
        try:
            query = f"TRUNCATE TABLE [{schema}].[{table_name}]"
            with self.engine.connect() as conn:
                conn.execute(text(query))
                conn.commit()
                self.logger.info(f"Tabla {schema}.{table_name} truncada exitosamente")
        except Exception as e:
            self.logger.error(f"Error truncando tabla {table_name}: {e}")
            raise
    
    def bulk_insert(self, df, table_name, schema='dbo', method='replace'):
        """
        Inserta datos masivamente en una tabla
        method: 'replace', 'append', 'upsert'
        """
        try:
            full_table_name = f"{schema}.{table_name}"
            
            if method == 'replace':
                # Reemplazar todos los datos
                df.to_sql(
                    name=table_name, 
                    con=self.engine, 
                    schema=schema,
                    if_exists='replace', 
                    index=False,
                    method='multi',
                    chunksize=1000
                )
                self.logger.info(f"Datos reemplazados en {full_table_name}: {len(df)} registros")
                
            elif method == 'append':
                # Agregar datos sin verificar duplicados
                df.to_sql(
                    name=table_name, 
                    con=self.engine, 
                    schema=schema,
                    if_exists='append', 
                    index=False,
                    method='multi',
                    chunksize=1000
                )
                self.logger.info(f"Datos agregados a {full_table_name}: {len(df)} registros")
                
            elif method == 'upsert':
                # Método más sofisticado para manejar actualizaciones
                self._upsert_data(df, table_name, schema)
                
        except Exception as e:
            self.logger.error(f"Error insertando datos en {table_name}: {e}")
            raise
    
    def _upsert_data(self, df, table_name, schema='dbo'):
        """
        Implementa lógica de UPSERT (INSERT + UPDATE)
        """
        try:
            # Verificar si la tabla existe
            if self.table_exists(table_name, schema):
                # Si existe, intentar truncar y luego insertar
                try:
                    self.truncate_table(table_name, schema)
                    self.bulk_insert(df, table_name, schema, method='append')
                except Exception as e:
                    self.logger.warning(f"No se pudo truncar {table_name}, intentando reemplazar: {e}")
                    # Si no se puede truncar, usar replace
                    df.to_sql(
                        name=table_name, 
                        con=self.engine, 
                        schema=schema,
                        if_exists='replace', 
                        index=False,
                        method='multi',
                        chunksize=1000
                    )
            else:
                # Si no existe, crear nueva tabla
                df.to_sql(
                    name=table_name, 
                    con=self.engine, 
                    schema=schema,
                    if_exists='replace', 
                    index=False,
                    method='multi',
                    chunksize=1000
                )
                self.logger.info(f"Tabla {table_name} creada con {len(df)} registros")
        except Exception as e:
            self.logger.error(f"Error en upsert de {table_name}: {e}")
            raise
    
    def get_max_date(self, table_name, date_column, schema='dbo'):
        """
        Obtiene la fecha máxima de una columna para sincronización incremental
        """
        try:
            query = f"""
            SELECT MAX([{date_column}]) as max_date
            FROM [{schema}].[{table_name}]
            """
            result = self.execute_query(query)
            max_date = result['max_date'].iloc[0]
            return max_date if pd.notna(max_date) else None
        except Exception as e:
            self.logger.warning(f"No se pudo obtener fecha máxima de {table_name}.{date_column}: {e}")
            return None
    
    def safe_insert(self, df, table_name, schema='dbo'):
        """
        Inserta datos sin truncar - usa INSERT directo con manejo de columnas
        """
        try:
            # Verificar que la tabla existe
            if not self.table_exists(table_name, schema):
                raise Exception(f"Tabla {schema}.{table_name} no existe. Solicitar creación al DBA.")
            
            # Log información del DataFrame antes de insertar
            self.logger.debug(f"Intentando insertar {len(df)} registros en {table_name}")
            self.logger.debug(f"Columnas: {list(df.columns)}")
            
            # Verificar si hay columnas problemáticas
            problematic_cols = [col for col in df.columns if '.' in col or col.lower().endswith('_duplicado_1')]
            if problematic_cols:
                self.logger.warning(f"Columnas problemáticas detectadas: {problematic_cols}")
            
            # Usar pandas to_sql pero con configuración más robusta
            df.to_sql(
                name=table_name, 
                con=self.engine, 
                schema=schema,
                if_exists='append',  # Solo agrega, no trunca
                index=False,
                method=None,  # Usar método por defecto, más confiable
                chunksize=10  # Chunks aún más pequeños para tablas problemáticas
            )
            
            self.logger.info(f"Datos insertados en {schema}.{table_name}: {len(df)} registros")
            
        except Exception as e:
            error_msg = str(e)
            self.logger.error(f"Error insertando datos en {table_name}: {e}")
            
            # Solo intentar método alternativo para errores específicos
            if "Cannot insert the value NULL" in error_msg or "duplicate" in error_msg.lower():
                try:
                    self.logger.info(f"Intentando inserción alternativa para {table_name}...")
                    self._insert_row_by_row(df, table_name, schema)
                except Exception as e2:
                    self.logger.error(f"Error en inserción alternativa: {e2}")
                    # No relanzar error para permitir continuar
            else:
                # Para otros errores, relanzar
                raise e
    
    def _insert_row_by_row(self, df, table_name, schema='dbo'):
        """
        Inserción fila por fila como último recurso - versión simplificada
        """
        try:
            # Obtener nombres de columnas sin duplicados
            columns = list(df.columns)
            columns_str = ', '.join([f"[{col}]" for col in columns])
            placeholders = ', '.join(['?' for _ in columns])
            
            insert_query = f"INSERT INTO [{schema}].[{table_name}] ({columns_str}) VALUES ({placeholders})"
            
            # Insertar fila por fila usando pandas to_sql con chunks muy pequeños
            inserted_count = 0
            try:
                # Intentar inserción directa con chunks de 1 registro
                for i in range(len(df)):
                    single_row = df.iloc[i:i+1]
                    try:
                        single_row.to_sql(
                            name=table_name,
                            con=self.engine,
                            schema=schema,
                            if_exists='append',
                            index=False,
                            method=None,
                            chunksize=1
                        )
                        inserted_count += 1
                    except Exception as e:
                        self.logger.warning(f"Error insertando fila {i}: {e}")
                        continue
                        
            except Exception as e:
                self.logger.error(f"Error en inserción por chunks: {e}")
                
            self.logger.info(f"Inserción fila por fila completada: {inserted_count}/{len(df)} registros insertados")
            
        except Exception as e:
            self.logger.error(f"Error en inserción fila por fila: {e}")
            # No relanzar el error para permitir que continúe la sincronización
    
    def test_connection(self):
        """Prueba la conexión a SQL Server"""
        try:
            query = "SELECT 'SQL Server conectado' as test"
            result = self.execute_query(query)
            return result['test'].iloc[0]
        except Exception as e:
            self.logger.error(f"Error probando conexión SQL Server: {e}")
            return None
    
    def close(self):
        """Cierra la conexión"""
        if hasattr(self, 'engine') and self.engine:
            self.engine.dispose()