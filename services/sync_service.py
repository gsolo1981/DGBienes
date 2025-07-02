import os
import logging
from datetime import datetime, timedelta
import pandas as pd
import hashlib
from adapters.sqlserver_adapter import SQLServerAdapter
from config.settings import settings
from sqlalchemy import text

class SyncService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.oracle_session = None
        self.sqlserver = SQLServerAdapter()
        
        # Configuración de sincronización por entorno
        self.sync_config = self._get_sync_config_by_environment()
        
        # Configuración de columnas de fecha para sincronización incremental por entorno
        self.date_columns = self._get_date_columns_by_environment()
        
        # Configuración de tablas que usan HASH en lugar de fechas
        self.hash_tables = self._get_hash_tables_by_environment()
        
    def _get_oracle_session(self):
        """Obtiene sesión Oracle de forma lazy"""
        if self.oracle_session is None:
            from adapters.db_adapter import get_oracle_session, is_oracle_available
            
            if not is_oracle_available():
                raise Exception("Oracle no está disponible. Verifica tu configuración.")
            
            self.oracle_session = get_oracle_session()
        
        return self.oracle_session
    
    def _get_hash_tables_by_environment(self):
        """Retorna las tablas que usan hash para sincronización incremental"""
        app_env = settings.APP_ENV.lower()
        
        if app_env == 'bienes':
            return {
                'Bienes_01_BENEFICIARIOS': {
                    'exclude_fields': ['id', 'row_hash', 'fecha_registro']
                },
                'Bienes_02_CARTERAS': { 
                    'exclude_fields': ['id', 'row_hash', 'fecha_registro']
                },
                'Bienes_03_CONTRATOS': {  
                    'exclude_fields': ['id', 'row_hash', 'fecha_registro']
                },
                'Bienes_04_PLAN_DE_PAGOS': {  
                    'exclude_fields': ['id', 'row_hash', 'fecha_registro']
                }
            }
        elif app_env == 'concesiones':
            return {
                'Concesiones_01_BENEFICIARIOS': {
                    'exclude_fields': ['id', 'row_hash', 'fecha_registro']
                },
                'Concesiones_02_CARTERAS': { 
                    'exclude_fields': ['id', 'row_hash', 'fecha_registro']
                },
                'Concesiones_03_CONTRATOS': { 
                    'exclude_fields': ['id', 'row_hash', 'fecha_registro']
                },
                'Concesiones_04_PLAN_DE_PAGOS': { 
                    'exclude_fields': ['id', 'row_hash', 'fecha_registro']
                }
            }
        elif app_env == 'sigaf':
            return {
                '01_RELACION_BAC_SIGAF': {
                    'exclude_fields': ['id', 'row_hash', 'fecha_registro']
                },
                '02_SPR_RENGLONES': { 
                    'exclude_fields': ['id', 'row_hash', 'fecha_registro']
                },
                '03_SPR_IMPUTACIONES': { 
                    'exclude_fields': ['id', 'row_hash', 'fecha_registro']
                },
                '04_RPR_SPR_PRD': { 
                    'exclude_fields': ['id', 'row_hash', 'fecha_registro']
                },
                '05_RPR_RENGLONES': { 
                    'exclude_fields': ['id', 'row_hash', 'fecha_registro']
                },
                '06_RPR_IMPUTACIONES': { 
                    'exclude_fields': ['id', 'row_hash', 'fecha_registro']
                },
                '07_PRD_RENGLONES': { 
                    'exclude_fields': ['id', 'row_hash', 'fecha_registro']
                },
                '08_PRD_IMPUTACIONES': { 
                    'exclude_fields': ['id', 'row_hash', 'fecha_registro']
                },
                '09_PRD_FACTURAS': { 
                    'exclude_fields': ['id', 'row_hash', 'fecha_registro']
                },
                '10_FACTURAS_OP_PAGOS': { 
                    'exclude_fields': ['id', 'row_hash', 'fecha_registro']
                },
                '11_RP': { 
                    'exclude_fields': ['id', 'row_hash', 'fecha_registro']
                },
                '12_DRP_RENGLONES': { 
                    'exclude_fields': ['id', 'row_hash', 'fecha_registro']
                },
                '13_DRP_IMPUTACIONES': { 
                    'exclude_fields': ['id', 'row_hash', 'fecha_registro']
                },
                '14_DRP_FACTURAS': { 
                    'exclude_fields': ['id', 'row_hash', 'fecha_registro']
                },
                '15_DRP_FACTURAS_PAGOS': { 
                    'exclude_fields': ['id', 'row_hash', 'fecha_registro']
                },
                '16_PRECIARIO': { 
                    'exclude_fields': ['id', 'row_hash', 'fecha_registro']
                },
                '17_PRECIARIO_IMPUTACIONES': { 
                    'exclude_fields': ['id', 'row_hash', 'fecha_registro']
                },
                '18_PRD_PRECIARIO': { 
                    'exclude_fields': ['id', 'row_hash', 'fecha_registro']
                },
                '19_PRD_PRECIARIO_RENGLONES': { 
                    'exclude_fields': ['id', 'row_hash', 'fecha_registro']
                },
                '20_PRD_PRECIARIO_IMPUTACIONES': { 
                    'exclude_fields': ['id', 'row_hash', 'fecha_registro']
                },
                '21_PRD_PRECIARIO_FACTURAS': { 
                    'exclude_fields': ['id', 'row_hash', 'fecha_registro']
                },
                '22_PAGOS_PRECIARIO': { 
                    'exclude_fields': ['id', 'row_hash', 'fecha_registro']
                },
                '23_UNIDADES_EJECUTORAS': { 
                    'exclude_fields': ['id', 'row_hash', 'fecha_registro']
                },
                '24_PERIODOS_FISCALES': { 
                    'exclude_fields': ['id', 'row_hash', 'fecha_registro']
                },
                '25_ENTES': { 
                    'exclude_fields': ['id', 'row_hash', 'fecha_registro']
                }

            }
        else:
            return {}

        
    def _get_sync_config_by_environment(self):
        """Retorna la configuración de mapeo según el entorno activo"""
        app_env = settings.APP_ENV.lower()
        
        if app_env == 'bienes':
            return {
                'Bienes_01_BENEFICIARIOS.sql': 'Bienes_01_BENEFICIARIOS',
                'Bienes_02_CARTERAS.sql': 'Bienes_02_CARTERAS', 
                'Bienes_03_CONTRATOS.sql': 'Bienes_03_CONTRATOS',
                'Bienes_04_PLAN DE PAGOS.sql': 'Bienes_04_PLAN_DE_PAGOS'
            }
        elif app_env == 'concesiones':
            return {
                'Concesiones_01_BENEFICIARIOS.sql': 'Concesiones_01_BENEFICIARIOS',
                'Concesiones_02_CARTERAS.sql': 'Concesiones_02_CARTERAS',
                'Concesiones_03_CONTRATOS.sql': 'Concesiones_03_CONTRATOS',
                'Concesiones_04_PLAN DE PAGOS.sql': 'Concesiones_04_PLAN_DE_PAGOS'
            }
        elif app_env == 'sigaf':
            return {
                '01_RELACION_BAC_SIGAF.sql': '[01_RELACION_BAC_SIGAF]',
                '02_SPR_RENGLONES.sql': '[02_SPR_RENGLONES]',
                '03_SPR_IMPUTACIONES.sql': '[03_SPR_IMPUTACIONES]',
                '04_RPR_SPR_PRD.sql': '[04_RPR_SPR_PRD]',
                '05_RPR_RENGLONES.sql': '[05_RPR_RENGLONES]',
                '06_RPR_IMPUTACIONES.sql': '[06_RPR_IMPUTACIONES]',
                '07_PRD_RENGLONES.sql': '[07_PRD_RENGLONES]',
                '08_PRD_IMPUTACIONES.sql': '[08_PRD_IMPUTACIONES]',
                '09_PRD_FACTURAS.sql': '[09_PRD_FACTURAS]',
                '10_FACTURAS_OP_PAGOS.sql': '[10_FACTURAS_OP_PAGOS]',
                '11_RP.sql': '[11_RP]',
                '12_DRP_RENGLONES.sql': '[12_DRP_RENGLONES]',
                '13_DRP_IMPUTACIONES.sql': '[13_DRP_IMPUTACIONES]',
                '14_DRP_FACTURAS.sql': '[14_DRP_FACTURAS]',
                '15_DRP_FACTURAS_PAGOS.sql': '[15_DRP_FACTURAS_PAGOS]',
                '16_PRECIARIO.sql': '[16_PRECIARIO]',
                '17_PRECIARIO_IMPUTACIONES.sql': '[17_PRECIARIO_IMPUTACIONES]',
                '18_PRD_PRECIARIO.sql': '[18_PRD_PRECIARIO]',
                '19_PRD_PRECIARIO_RENGLONES.sql': '[19_PRD_PRECIARIO_RENGLONES]',
                '20_PRD_PRECIARIO_IMPUTACIONES.sql': '[20_PRD_PRECIARIO_IMPUTACIONES]',
                '21_PRD_PRECIARIO_FACTURAS.sql': '[21_PRD_PRECIARIO_FACTURAS]',
                '22_PAGOS_PRECIARIO.sql': '[22_PAGOS_PRECIARIO]',
                '23_UNIDADES_EJECUTORAS.sql': '[23_UNIDADES_EJECUTORAS]',
                '24_PERIODOS_FISCALES.sql': '[24_PERIODOS_FISCALES]',
                '25_ENTES.sql': '[25_ENTES]'
            }
        elif app_env == 'sigaf_devengado':
            return {
                '01_DEVENGADO_v2.sql': '[01_DEVENGADO_v2]'
            }
        else:
            self.logger.warning(f"Entorno no reconocido: {app_env}. Usando configuración por defecto.")
            return {}
        
    
    def _get_date_columns_by_environment(self):
        """Retorna las columnas de fecha según el entorno activo"""
        app_env = settings.APP_ENV.lower()
        
        if  app_env == 'sigaf_devengado':
            return {
                '[01_DEVENGADO_v2]': 'fh_imputacion'
            }
        else:
            return {}




    
    def create_hash_column(self, table_name):
        """Crear columna row_hash si no existe"""
        try:
            clean_table_name = table_name.replace('[', '').replace(']', '')
            
            check_query = f"""
            SELECT COUNT(*) as count
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = '{clean_table_name}' AND COLUMN_NAME = 'row_hash'
            """
            
            result = self.sqlserver.execute_query(check_query)
            exists = result['count'].iloc[0] > 0
            
            if not exists:
                alter_query = f"ALTER TABLE [dbo].[{clean_table_name}] ADD row_hash VARCHAR(64)"
                
                with self.sqlserver.engine.connect() as conn:
                    conn.execute(text(alter_query))
                    conn.commit()
                
                self.logger.info(f"✅ Columna row_hash agregada a {table_name}")
            else:
                self.logger.info(f"✅ Columna row_hash ya existe en {table_name}")
                
        except Exception as e:
            self.logger.error(f"❌ Error creando columna hash en {table_name}: {e}")
            raise

    def generate_row_hash(self, row_data, exclude_fields=None):
        """Generar hash MD5 de todos los campos de datos"""
        if exclude_fields is None:
            exclude_fields = ['id', 'row_hash', 'fecha_registro']
        
        exclude_fields = [field.lower() for field in exclude_fields]
        
        hash_data = {}
        for key, value in row_data.items():
            if key.lower() not in exclude_fields:
                str_value = str(value).strip() if value is not None else ""
                hash_data[key.lower()] = str_value
        
        sorted_items = sorted(hash_data.items())
        hash_string = '|'.join([f"{k}:{v}" for k, v in sorted_items])
        
        return hashlib.md5(hash_string.encode('utf-8')).hexdigest()

    def get_existing_hashes(self, table_name):
        """Obtener todos los hashes existentes"""
        try:
            clean_table_name = table_name.replace('[', '').replace(']', '')
            
            query = f"""
            SELECT row_hash, COUNT(*) as count
            FROM [dbo].[{clean_table_name}] 
            WHERE row_hash IS NOT NULL AND row_hash != ''
            GROUP BY row_hash
            """
            
            df = self.sqlserver.execute_query(query)
            existing_hashes = set(df['row_hash'].tolist())
            
            self.logger.info(f"📊 Encontrados {len(existing_hashes)} hashes únicos existentes en {table_name}")
            return existing_hashes
            
        except Exception as e:
            self.logger.error(f"❌ Error obteniendo hashes existentes de {table_name}: {e}")
            return set()

    def update_existing_hashes(self, table_name, exclude_fields=None):
        """Actualizar hashes para registros existentes que no los tienen"""
        try:
            clean_table_name = table_name.replace('[', '').replace(']', '')
            
            query = f"""
            SELECT * FROM [dbo].[{clean_table_name}] 
            WHERE row_hash IS NULL OR row_hash = ''
            """
            
            df = self.sqlserver.execute_query(query)
            
            if df.empty:
                self.logger.info(f"✅ Todos los registros existentes ya tienen hash en {table_name}")
                return
            
            self.logger.info(f"🔄 Actualizando hashes para {len(df)} registros existentes en {table_name}...")
            
            updated_count = 0
            
            with self.sqlserver.engine.connect() as conn:
                for _, row in df.iterrows():
                    try:
                        row_dict = row.to_dict()
                        new_hash = self.generate_row_hash(row_dict, exclude_fields)
                        
                        update_query = text("""
                        UPDATE [dbo].[{table_name}] 
                        SET row_hash = :hash_value 
                        WHERE id = :row_id
                        """.format(table_name=clean_table_name))
                        
                        conn.execute(update_query, {
                            'hash_value': new_hash,
                            'row_id': row['id']
                        })
                        
                        updated_count += 1
                        
                        if updated_count % 100 == 0:
                            self.logger.info(f"🔄 Procesados {updated_count} registros...")
                            conn.commit()
                            
                    except Exception as e:
                        self.logger.warning(f"Error en registro ID {row.get('id', 'N/A')}: {e}")
                        continue
                
                conn.commit()
            
            self.logger.info(f"✅ Actualizados {updated_count} hashes existentes en {table_name}")
            
        except Exception as e:
            self.logger.error(f"❌ Error actualizando hashes existentes en {table_name}: {e}")
            raise

    def sync_table_with_hash(self, sql_file_path, table_name, source_df):
        """Sincronizar tabla usando hash para evitar duplicados"""
        
        self.logger.info(f"🔄 Sincronizando con HASH: {table_name}")
        
        clean_table_name = table_name.replace('[', '').replace(']', '')
        if not self.sqlserver.table_exists(clean_table_name):
            self.logger.warning(f"⏭️ OMITIDA: Tabla {table_name} no existe en SQL Server.")
            return 0, True
        
        try:
            hash_config = self.hash_tables.get(table_name, {})
            exclude_fields = hash_config.get('exclude_fields', ['id', 'row_hash', 'fecha_registro'])
            
            self.create_hash_column(table_name)
            self.update_existing_hashes(table_name, exclude_fields)
            existing_hashes = self.get_existing_hashes(table_name)
            
            df_clean = self._clean_dataframe_for_sqlserver(source_df.copy())
            
            new_records = []
            duplicate_count = 0
            
            for _, row in df_clean.iterrows():
                row_dict = row.to_dict()
                new_hash = self.generate_row_hash(row_dict, exclude_fields)
                
                if new_hash in existing_hashes:
                    duplicate_count += 1
                else:
                    row_dict['row_hash'] = new_hash
                    new_records.append(row_dict)
                    existing_hashes.add(new_hash)
            
            if not new_records:
                self.logger.info(f"📊 {table_name}: No hay registros nuevos. {duplicate_count} duplicados ignorados.")
                return 0, False
            
            df_new = pd.DataFrame(new_records)
            self.sqlserver.safe_insert(df_new, clean_table_name, schema='dbo')
            
            self.logger.info(f"""
            ✅ SINCRONIZACIÓN COMPLETADA - {table_name}
            ==========================================
            Registros fuente: {len(df_clean)}
            Registros insertados: {len(df_new)}
            Duplicados ignorados: {duplicate_count}
            ==========================================
            """)
            
            return len(df_new), False
            
        except Exception as e:
            self.logger.error(f"❌ Error en sincronización con hash para {table_name}: {e}")
            raise
    
    def sync_all_tables(self, mode='incremental'):
        """Sincroniza todas las tablas"""
        self.logger.info(f"🚀 Iniciando sincronización en modo: {mode}")
        
        sql_dir = os.path.join(os.path.dirname(__file__), '..', settings.PATH_SQL)
        
        total_synced = 0
        errors = []
        skipped = []
        
        for root, dirs, files in os.walk(sql_dir):
            for file in files:
                if not file.lower().endswith('.sql'):
                    continue
                    
                try:
                    file_path = os.path.join(root, file)
                    
                    table_name = self._get_target_table(file)
                    if not table_name:
                        self.logger.warning(f"⚠️ No se encontró mapeo para {file}")
                        continue
                    
                    synced_count, is_skipped = self._sync_table(file_path, table_name, mode)
                    
                    if is_skipped:
                        skipped.append(f"{file} -> {table_name}")
                    else:
                        total_synced += synced_count
                    
                except Exception as e:
                    error_msg = f"Error sincronizando {file}: {e}"
                    self.logger.error(error_msg)
                    errors.append(error_msg)
        
        self.logger.info(f"""
        ==========================================
        🎉 SINCRONIZACIÓN COMPLETADA
        ==========================================
        Total registros sincronizados: {total_synced:,}
        Tablas omitidas: {len(skipped)}
        Errores: {len(errors)}
        ==========================================
        """)
        
        if skipped:
            self.logger.info(f"📋 Tablas omitidas (no existen en SQL Server):")
            for skip in skipped:
                self.logger.info(f"  ⏭️ {skip}")
        
        if errors:
            self.logger.warning(f"⚠️ Errores encontrados:")
            for error in errors:
                self.logger.warning(f"  ❌ {error}")
        
        return total_synced, errors
    
    def _fix_duplicate_columns(self, df):
        """Renombra columnas duplicadas que persisten"""
        columns = list(df.columns)
        new_columns = []
        seen = {}
        
        for col in columns:
            base_col = col.split('.')[0] if '.' in col else col
            
            if base_col in seen:
                seen[base_col] += 1
                new_col = f"{base_col}_duplicado_{seen[base_col]}"
            else:
                seen[base_col] = 0
                new_col = base_col
            new_columns.append(new_col)
        
        df.columns = new_columns
        
        if len(set(columns)) != len(set(new_columns)):
            changed_cols = [(old, new) for old, new in zip(columns, new_columns) if old != new]
            for old_col, new_col in changed_cols:
                self.logger.info(f"🔄 Columna renombrada: {old_col} -> {new_col}")
        
        return df
    
    def _clean_dataframe_for_sqlserver(self, df):
        """Limpieza robusta de DataFrame para SQL Server"""
        df_clean = df.copy()
        
        for col in df_clean.columns:
            if df_clean[col].dtype == 'object':
                df_clean[col] = df_clean[col].fillna('')
                df_clean[col] = df_clean[col].astype(str)
                df_clean[col] = df_clean[col].str[:255]
            elif 'datetime' in str(df_clean[col].dtype):
                df_clean[col] = df_clean[col].fillna(pd.Timestamp('1900-01-01'))
            elif df_clean[col].dtype in ['int64', 'float64', 'int32', 'float32']:
                df_clean[col] = df_clean[col].fillna(0)
            elif df_clean[col].dtype == 'bool':
                df_clean[col] = df_clean[col].fillna(False)
            else:
                df_clean[col] = df_clean[col].fillna('')
                df_clean[col] = df_clean[col].astype(str)
                df_clean[col] = df_clean[col].str[:255]
        
        null_count = df_clean.isnull().sum().sum()
        if null_count > 0:
            self.logger.warning(f"⚠️ Encontrados {null_count} valores NULL después de limpieza, aplicando fillna global")
            df_clean = df_clean.fillna('')
        
        return df_clean
    
    def _sync_table(self, sql_file_path, table_name, mode='incremental'):
        """Sincroniza una tabla individual"""
        
        file_name = os.path.basename(sql_file_path)
        self.logger.info(f"🔄 Procesando: {file_name} -> {table_name}")
        
        clean_table_name = table_name.replace('[', '').replace(']', '')
        if not self.sqlserver.table_exists(clean_table_name):
            self.logger.warning(f"⏭️ OMITIDA: Tabla {table_name} no existe en SQL Server.")
            return 0, True
        
        with open(sql_file_path, 'r', encoding='utf-8') as f:
            sql_content = f.read().strip()
            if sql_content.endswith(';'):
                sql_content = sql_content[:-1]
        
        if hasattr(self, 'hash_tables') and table_name in self.hash_tables:
            self.logger.info(f"📊 Usando sincronización por HASH para {table_name}")
            
            try:
                oracle_session = self._get_oracle_session()
                df = pd.read_sql_query(sql_content, oracle_session.bind)
            except Exception as e:
                self.logger.error(f"❌ Error ejecutando consulta Oracle: {e}")
                raise
            
            if df.empty:
                self.logger.info(f"📭 No hay datos en Oracle para {table_name}")
                return 0, False
            
            df.columns = [self._clean_column_name(col) for col in df.columns]
            df = df.loc[:, ~df.columns.duplicated(keep='first')]
            df = self._fix_duplicate_columns(df)
            
            return self.sync_table_with_hash(sql_file_path, table_name, df)
            
        else:
            self.logger.info(f"📅 Usando sincronización por FECHA para {table_name}")
            
            if mode == 'incremental' and table_name in self.date_columns:
                sql_content = self._add_incremental_filter(sql_content, table_name)
            
            try:
                oracle_session = self._get_oracle_session()
                df = pd.read_sql_query(sql_content, oracle_session.bind)
            except Exception as e:
                self.logger.error(f"❌ Error ejecutando consulta Oracle: {e}")
                raise
            
            if df.empty:
                self.logger.info(f"📭 No hay datos nuevos para {table_name}")
                return 0, False
            
            df.columns = [self._clean_column_name(col) for col in df.columns]
            df = df.loc[:, ~df.columns.duplicated(keep='first')]
            df = self._fix_duplicate_columns(df)
            df = self._clean_dataframe_for_sqlserver(df)
            
            try:
                self.sqlserver.safe_insert(df, clean_table_name, schema='dbo')
                self.logger.info(f"✅ {table_name}: {len(df)} registros sincronizados")
                return len(df), False
            except Exception as e:
                self.logger.error(f"❌ Error sincronizando tabla {table_name}: {e}")
                raise
    
    def _get_target_table(self, sql_filename):
        """Obtiene el nombre de la tabla destino basado en el archivo SQL"""
        return self.sync_config.get(sql_filename)
    
    def _add_incremental_filter(self, sql_query, table_name):
        """Añade filtro incremental basado en la última fecha sincronizada"""
        date_column = self.date_columns.get(table_name)
        if not date_column:
            return sql_query
        
        last_sync_date = self.sqlserver.get_max_date(
            table_name.replace('[', '').replace(']', ''), 
            date_column
        )
        
        if last_sync_date:
            oracle_date_str = last_sync_date.strftime('%d/%m/%Y')
            
            if 'WHERE' in sql_query.upper():
                filter_clause = f" AND {date_column} > TO_DATE('{oracle_date_str}', 'DD/MM/YYYY')"
            else:
                filter_clause = f" WHERE {date_column} > TO_DATE('{oracle_date_str}', 'DD/MM/YYYY')"
            
            order_by_pos = sql_query.upper().find('ORDER BY')
            if order_by_pos != -1:
                sql_query = sql_query[:order_by_pos] + filter_clause + " " + sql_query[order_by_pos:]
            else:
                sql_query += filter_clause
            
            self.logger.info(f"📅 Filtro incremental aplicado: {date_column} > TO_DATE('{oracle_date_str}', 'DD/MM/YYYY')")
        
        return sql_query
    
    def _clean_column_name(self, column_name):
        """Limpia nombres de columnas para SQL Server"""
        clean_name = str(column_name).replace(' ', '_').replace('-', '_')
        invalid_chars = ['[', ']', '(', ')', '.', ',', ';', ':', '!', '@', '#', '$', '%', '^', '&', '*']
        for char in invalid_chars:
            clean_name = clean_name.replace(char, '_')
        return clean_name
    
    def sync_specific_tables(self, table_list, mode='incremental'):
        """Sincroniza tablas específicas"""
        self.logger.info(f"🎯 Sincronizando tablas específicas: {table_list}")
        
        total_synced = 0
        errors = []
        
        for table_name in table_list:
            try:
                sql_file = self._find_sql_file_for_table(table_name)
                if not sql_file:
                    errors.append(f"No se encontró archivo SQL para {table_name}")
                    continue
                
                synced_count, is_skipped = self._sync_table(sql_file, table_name, mode)
                
                if not is_skipped:
                    total_synced += synced_count
                
            except Exception as e:
                error_msg = f"Error sincronizando {table_name}: {e}"
                errors.append(error_msg)
                self.logger.error(error_msg)
        
        return total_synced, errors
    
    def _find_sql_file_for_table(self, table_name):
        """Encuentra el archivo SQL correspondiente a una tabla"""
        for sql_file, mapped_table in self.sync_config.items():
            if mapped_table == table_name:
                sql_dir = os.path.join(os.path.dirname(__file__), '..', settings.PATH_SQL)
                for root, dirs, files in os.walk(sql_dir):
                    if sql_file in files:
                        return os.path.join(root, sql_file)
        return None
    
    def get_sync_status(self):
        """Obtiene el estado de sincronización de todas las tablas"""
        status = {}
        
        for sql_file, table_name in self.sync_config.items():
            try:
                clean_table_name = table_name.replace('[', '').replace(']', '')
                
                if not self.sqlserver.engine:
                    status[table_name] = {'exists': False, 'error': 'SQL Server no disponible'}
                    continue
                
                if not self.sqlserver.table_exists(clean_table_name):
                    status[table_name] = {'exists': False, 'count': 0, 'last_update': None}
                    continue
                
                count_query = f"SELECT COUNT(*) as count FROM [{clean_table_name}]"
                result = self.sqlserver.execute_query(count_query)
                record_count = result['count'].iloc[0]
                
                hash_info = None
                if table_name in self.hash_tables:
                    try:
                        hash_query = f"""
                        SELECT 
                            COUNT(*) as total_records,
                            COUNT(row_hash) as records_with_hash,
                            COUNT(DISTINCT row_hash) as unique_hashes
                        FROM [{clean_table_name}]
                        """
                        hash_result = self.sqlserver.execute_query(hash_query)
                        hash_info = hash_result.iloc[0].to_dict()
                    except:
                        hash_info = None
                
                last_update = None
                if table_name in self.date_columns:
                    date_column = self.date_columns[table_name]
                    last_update = self.sqlserver.get_max_date(clean_table_name, date_column)
                
                status[table_name] = {
                    'exists': True,
                    'count': record_count,
                    'last_update': last_update,
                    'hash_info': hash_info,
                    'sync_method': 'hash' if table_name in self.hash_tables else 'date'
                }
                
            except Exception as e:
                status[table_name] = {'exists': False, 'error': str(e)}
        
        return status
    
    def close(self):
        """Cierra todas las conexiones"""
        if self.oracle_session:
            self.oracle_session.close()
        if self.sqlserver:
            self.sqlserver.close()