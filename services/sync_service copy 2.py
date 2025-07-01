import os
import logging
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from adapters.sqlserver_adapter import SQLServerAdapter
from config.settings import settings

class SyncService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.oracle_session = None
        self.sqlserver = SQLServerAdapter()
        
        # Configuración de sincronización por entorno
        self.sync_config = self._get_sync_config_by_environment()
        
        # Configuración de columnas de fecha para sincronización incremental por entorno
        self.date_columns = self._get_date_columns_by_environment()
        
    def _get_oracle_session(self):
        """Obtiene sesión Oracle de forma lazy"""
        if self.oracle_session is None:
            from adapters.db_adapter import get_oracle_session, is_oracle_available
            
            if not is_oracle_available():
                raise Exception("Oracle no está disponible. Verifica tu configuración.")
            
            self.oracle_session = get_oracle_session()
        
        return self.oracle_session
        
    def _get_sync_config_by_environment(self):
        """Retorna la configuración de mapeo según el entorno activo"""
        app_env = settings.APP_ENV.lower()
        
        if app_env == 'bienes':
            # Esquema Bienes_Concesiones
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
            # Esquema SIGAF
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
            # Esquema SIGAF Devengados
            return {
                '01_DEVENGADO_v2.sql': '[01_DEVENGADO_v2]'
            }
        else:
            self.logger.warning(f"Entorno no reconocido: {app_env}. Usando configuración por defecto.")
            return {}
        
    def _get_date_columns_by_environment(self):
        """Retorna las columnas de fecha según el entorno activo"""
        app_env = settings.APP_ENV.lower()
        
        if app_env == 'bienes':
            # Columnas de fecha para Bienes y Concesiones
            return {
                'Bienes_03_CONTRATOS': 'fechafirma',
                'Bienes_04_PLAN_DE_PAGOS': 'fecha_creacion'
            }
        elif app_env == 'concesiones': 
            return {
                'Concesiones_03_CONTRATOS': 'fechafirma',
                'Concesiones_04_PLAN_DE_PAGOS': 'fecha_creacion'
            }                   
        elif app_env == 'sigaf':
            # Columnas de fecha para SIGAF
            return {
                '[02_SPR_RENGLONES]': 'fh_alta',
                '[03_SPR_IMPUTACIONES]': 'fh_estado',
                '[04_RPR_SPR_PRD]': 'fh_alta',
                '[05_RPR_RENGLONES]': 'fh_autorizacion',
                '[06_RPR_IMPUTACIONES]': 'fh_autorizacion',
                '[07_PRD_RENGLONES]': 'fh_alta',
                '[08_PRD_IMPUTACIONES]': 'fh_autorizacion',
                '[09_PRD_FACTURAS]': 'fhu_actualiz',
                '[10_FACTURAS_OP_PAGOS]': 'f_emision',
                '[11_RP]': 'fh_alta',
                '[12_DRP_RENGLONES]': 'fh_alta',
                '[13_DRP_IMPUTACIONES]': 'fh_alta',
                '[14_DRP_FACTURAS]': 'fh_alta',
                '[15_DRP_FACTURAS_PAGOS]': 'fh_alta',
                '[16_PRECIARIO]': 'fh_alta',
                '[17_PRECIARIO_IMPUTACIONES]': 'fh_estado',
                '[18_PRD_PRECIARIO]': 'fh_alta',
                '[19_PRD_PRECIARIO_RENGLONES]': 'fh_autorizacion',
                '[20_PRD_PRECIARIO_IMPUTACIONES]': 'fh_autorizacion',
                '[21_PRD_PRECIARIO_FACTURAS]': 'fhu_actualiz',
                '[22_PAGOS_PRECIARIO]': 'f_emision'
            }
        elif app_env == 'sigaf_devengado':
            # Columnas de fecha para SIGAF Devengados
            return {
                '[01_DEVENGADO_v2]': 'fh_imputacion'
            }
        else:
            return {}
    
    def sync_all_tables(self, mode='incremental'):
        """
        Sincroniza todas las tablas
        mode: 'full' para carga completa, 'incremental' para solo novedades
        """
        self.logger.info(f"Iniciando sincronización en modo: {mode}")
        
        sql_dir = os.path.join(os.path.dirname(__file__), '..', settings.PATH_SQL)
        
        total_synced = 0
        errors = []
        skipped = []
        
        try:
            # Recorrer recursivamente la carpeta SQL
            for root, dirs, files in os.walk(sql_dir):
                for file in files:
                    if not file.lower().endswith('.sql'):
                        continue
                        
                    try:
                        file_path = os.path.join(root, file)
                        
                        # Obtener nombre de tabla destino
                        table_name = self._get_target_table(file)
                        if not table_name:
                            self.logger.warning(f"No se encontró mapeo para {file}")
                            continue
                        
                        # Sincronizar tabla individual - FIX: manejar correctamente la tupla de retorno
                        result = self._sync_table(file_path, table_name, mode)
                        
                        if result is None:
                            # Error en la sincronización
                            errors.append(f"Error sincronizando {file}: Resultado nulo")
                            continue
                        
                        synced_count, is_skipped = result
                        
                        if is_skipped:
                            skipped.append(f"{file} -> {table_name}")
                        else:
                            total_synced += synced_count
                        
                    except Exception as e:
                        error_msg = f"Error sincronizando {file}: {e}"
                        self.logger.error(error_msg)
                        errors.append(error_msg)
            
            # Resumen final
            self.logger.info(f"Sincronización completada. Total registros: {total_synced}")
            
            if skipped:
                self.logger.info(f"Tablas omitidas (no existen en SQL Server): {len(skipped)}")
                for skip in skipped:
                    self.logger.info(f"  ⏭️  {skip}")
            
            if errors:
                self.logger.warning(f"Errores encontrados: {len(errors)}")
                for error in errors:
                    self.logger.warning(f"  ❌ {error}")
            
            # IMPORTANTE: Siempre devolver una tupla
            return total_synced, errors
            
        except Exception as e:
            # En caso de error general, también devolver tupla
            self.logger.error(f"Error general en sync_all_tables: {e}")
            errors.append(f"Error general: {e}")
            return total_synced, errors
    
    def _diagnose_data_types(self, df, table_name):
        """Diagnostica y reporta tipos de datos problemáticos"""
        self.logger.info(f"=== DIAGNÓSTICO DE TIPOS DE DATOS para {table_name} ===")
        
        for col in df.columns:
            col_type = str(df[col].dtype)
            unique_count = df[col].nunique()
            null_count = df[col].isnull().sum()
            
            # Mostrar muestra de valores
            sample_values = df[col].dropna().head(3).tolist()
            
            self.logger.info(f"Columna: {col}")
            self.logger.info(f"  Tipo: {col_type}")
            self.logger.info(f"  Únicos: {unique_count}, Nulos: {null_count}")
            self.logger.info(f"  Muestra: {sample_values}")
            
            # Detectar posibles problemas de conversión
            if col_type == 'object':
                # Verificar si hay valores que parecen numéricos mezclados con texto
                numeric_like = 0
                text_like = 0
                for val in df[col].dropna():
                    val_str = str(val).strip()
                    if val_str.replace('.', '').replace('-', '').isdigit():
                        numeric_like += 1
                    elif val_str and not val_str.isdigit():
                        text_like += 1
                
                if numeric_like > 0 and text_like > 0:
                    self.logger.warning(f"  ⚠️  PROBLEMA POTENCIAL: Columna {col} mezcla valores numéricos y texto")
                    problematic_values = []
                    for val in df[col].dropna():
                        val_str = str(val).strip()
                        if val_str and not val_str.replace('.', '').replace('-', '').isdigit():
                            problematic_values.append(val)
                            if len(problematic_values) >= 5:
                                break
                    self.logger.warning(f"    Valores problemáticos: {problematic_values}")
    
    def _get_table_schema_mapping(self, table_name):
        """
        Retorna el mapeo de tipos de datos específico por tabla
        """
        schemas = {
            'Bienes_02_CARTERAS': {
                'numeric_int_cols': ['ley', 'circunscripcion', 'seccion', 'manzana', 'parcela', 'nrounidad'],
                'numeric_decimal_cols': ['valuacionfiscal', 'mtstotales', 'mtscubiertos'],
                'varchar_cols': ['barrio', 'identificacion', 'division', 'tipo_unidad', 'piso', 'depto', 
                               'telefono', 'partidaunidad', 'digitoverificador', 'tipoplano'],
                'char_cols': ['nueva', 'habilitado'],
                'exclude_cols': ['id']  # Columnas con IDENTITY que no se deben insertar
            },
            'Bienes_01_BENEFICIARIOS': {
                'varchar_cols': ['documento_tipo', 'documento', 'nombre', 'email', 'emailadicional', 
                               'tipo_persona', 'sexo', 'telefono', 'tipo_domicilio', 'calle', 'piso', 
                               'dpto', 'localidad', 'codigo_postal'],
                'char_cols': ['activo'],
                'datetime_cols': ['fechanacimiento'],
                'exclude_cols': ['id']
            },
            'Bienes_03_CONTRATOS': {
                'numeric_int_cols': ['nro', 'nrounidad'],
                'varchar_cols': ['expediente', 'tipo_contrato', 'tipo_calculo', 'tipo_unidad', 
                               'identificacion', 'descripcion', 'nombre', 'documento'],
                'char_cols': ['vigente', 'principal'],
                'datetime_cols': ['fechafirma', 'desde', 'hasta'],
                'exclude_cols': ['id']
            },
            'Bienes_04_PLAN_DE_PAGOS': {
                'numeric_int_cols': ['carpeta', 'nrounidad', 'numero', 'total', 'cuil', 'legajo'],
                'varchar_cols': ['tipo', 'objetivo_prestacion', 'nombre', 'documento', 'email', 
                               'emailadicional', 'tipo_persona', 'calle', 'identificacion', 
                               'sub_division', 'tipo_contrato', 'tipo_calculo', 'resp_adjudicatatio', 
                               'documento1', 'nro_expediente', 'observaciones', 'observacion', 
                               'estado', 'resp_cumplimiento'],
                'datetime_cols': ['fecha_creacion', 'vencimiento', 'fechabui', 'fechapago'],
                'exclude_cols': ['id']
            }
            # Aquí se pueden agregar más tablas según sea necesario
        }
        return schemas.get(table_name, {})

    def _enhanced_data_cleaning(self, df, table_name):
        """
        Limpieza mejorada de DataFrame para SQL Server con mapeo específico de esquemas
        """
        self.logger.info(f"Iniciando limpieza mejorada de datos para {table_name}")
        df_clean = df.copy()
        
        # Diagnósticar antes de limpiar
        self._diagnose_data_types(df_clean, table_name)
        
        # Obtener esquema específico de la tabla
        schema_mapping = self._get_table_schema_mapping(table_name)
        
        # Excluir columnas que no se deben insertar (como IDENTITY)
        exclude_cols = schema_mapping.get('exclude_cols', [])
        for col in exclude_cols:
            if col in df_clean.columns:
                self.logger.info(f"Eliminando columna {col} (IDENTITY o no insertable)")
                df_clean = df_clean.drop(columns=[col])
        
        # Procesar cada columna según su tipo esperado
        for col in df_clean.columns:
            original_type = str(df_clean[col].dtype)
            self.logger.info(f"Procesando columna: {col} (tipo original: {original_type})")
            
            # Mapeo específico basado en el esquema de la tabla
            if col in schema_mapping.get('numeric_int_cols', []):
                # Columnas que deben ser INT
                self.logger.info(f"  Convirtiendo {col} a INT")
                df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
                df_clean[col] = df_clean[col].fillna(0).astype('int64')
                
            elif col in schema_mapping.get('numeric_decimal_cols', []):
                # Columnas que deben ser DECIMAL
                self.logger.info(f"  Convirtiendo {col} a DECIMAL")
                df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
                df_clean[col] = df_clean[col].fillna(0.0).astype('float64')
                
            elif col in schema_mapping.get('varchar_cols', []):
                # Columnas que deben ser VARCHAR
                self.logger.info(f"  Convirtiendo {col} a VARCHAR")
                df_clean[col] = df_clean[col].fillna('')
                df_clean[col] = df_clean[col].astype(str)
                # Truncar según límites típicos de VARCHAR
                if col in ['barrio', 'tipo_unidad', 'piso', 'depto', 'telefono', 'partidaunidad', 
                          'digitoverificador', 'tipoplano']:
                    df_clean[col] = df_clean[col].str[:50]  # VARCHAR(50)
                else:
                    df_clean[col] = df_clean[col].str[:64]  # VARCHAR(64) para identificacion, division
                    
            elif col in schema_mapping.get('char_cols', []):
                # Columnas que deben ser CHAR(1)
                self.logger.info(f"  Convirtiendo {col} a CHAR(1)")
                df_clean[col] = df_clean[col].fillna('')
                df_clean[col] = df_clean[col].astype(str)
                df_clean[col] = df_clean[col].str[:1]  # Solo el primer carácter
                # Para campos habilitado/activo, asegurar valores válidos
                if col in ['habilitado', 'nueva', 'activo', 'vigente', 'principal']:
                    df_clean[col] = df_clean[col].replace('', 'N')  # Default a 'N' si está vacío
                    
            elif col in schema_mapping.get('datetime_cols', []):
                # Columnas que deben ser DATETIME
                self.logger.info(f"  Convirtiendo {col} a DATETIME")
                df_clean[col] = pd.to_datetime(df_clean[col], errors='coerce')
                df_clean[col] = df_clean[col].fillna(pd.Timestamp('1900-01-01'))
                    
            else:
                # Procesamiento genérico para columnas no mapeadas
                if df_clean[col].dtype == 'object':
                    # Primero, rellenar valores nulos
                    df_clean[col] = df_clean[col].fillna('')
                    df_clean[col] = df_clean[col].astype(str)
                    
                    # Verificar si todos los valores no vacíos son numéricos
                    non_empty_values = df_clean[col][df_clean[col] != ''].copy()
                    
                    if len(non_empty_values) > 0:
                        # Intentar detectar si es realmente numérico
                        numeric_pattern = non_empty_values.str.replace('.', '', regex=False).str.replace('-', '', regex=False).str.isdigit()
                        numeric_percentage = numeric_pattern.sum() / len(non_empty_values)
                        
                        if numeric_percentage > 0.8:  # Si más del 80% son numéricos
                            self.logger.info(f"Columna {col} parece numérica ({numeric_percentage:.1%}), convirtiendo...")
                            try:
                                df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
                                df_clean[col] = df_clean[col].fillna(0)
                                self.logger.info(f"  ✅ Columna {col} convertida a numérica")
                            except Exception as e:
                                self.logger.warning(f"  ❌ No se pudo convertir {col} a numérica: {e}")
                                df_clean[col] = df_clean[col].str[:255]  # Truncar
                        else:
                            # Mantener como string
                            df_clean[col] = df_clean[col].str[:255]  # Truncar strings largos
                            
                elif 'datetime' in original_type:
                    # Para fechas, reemplazar NULL con fecha válida mínima
                    df_clean[col] = df_clean[col].fillna(pd.Timestamp('1900-01-01'))
                    
                elif df_clean[col].dtype in ['int64', 'float64', 'int32', 'float32']:
                    # Para números, reemplazar NULL con 0
                    df_clean[col] = df_clean[col].fillna(0)
                    
                    # Verificar si hay valores infinitos
                    if np.isinf(df_clean[col]).any():
                        self.logger.warning(f"Valores infinitos encontrados en {col}, reemplazando con 0")
                        df_clean[col] = df_clean[col].replace([np.inf, -np.inf], 0)
                    
                elif df_clean[col].dtype == 'bool':
                    # Para booleanos, reemplazar NULL con False
                    df_clean[col] = df_clean[col].fillna(False)
                    
                else:
                    # Para cualquier otro tipo, convertir a string
                    df_clean[col] = df_clean[col].fillna('')
                    df_clean[col] = df_clean[col].astype(str)
                    df_clean[col] = df_clean[col].str[:255]
        
        # Verificación final
        null_count = df_clean.isnull().sum().sum()
        if null_count > 0:
            self.logger.warning(f"Encontrados {null_count} valores NULL después de limpieza, aplicando fillna específico")
            # Rellenar NULLs de forma inteligente según el tipo de columna
            for col in df_clean.columns:
                if df_clean[col].isnull().any():
                    if col in schema_mapping.get('numeric_int_cols', []):
                        df_clean[col] = df_clean[col].fillna(0)
                    elif col in schema_mapping.get('numeric_decimal_cols', []):
                        df_clean[col] = df_clean[col].fillna(0.0)
                    elif col in schema_mapping.get('datetime_cols', []):
                        df_clean[col] = df_clean[col].fillna(pd.Timestamp('1900-01-01'))
                    else:
                        df_clean[col] = df_clean[col].fillna('')
        
        # Verificar tipos finales
        self.logger.info(f"Tipos finales después de limpieza:")
        for col in df_clean.columns:
            self.logger.info(f"  {col}: {df_clean[col].dtype}")
        
        return df_clean
    
    def _fix_duplicate_columns(self, df):
        """
        Renombra columnas duplicadas que persisten y maneja casos especiales
        """
        columns = list(df.columns)
        new_columns = []
        seen = {}
        
        for col in columns:
            # Limpiar nombre base (remover sufijos como .1, .2, etc.)
            base_col = col.split('.')[0] if '.' in col else col
            
            if base_col in seen:
                seen[base_col] += 1
                # Para columnas duplicadas, usar sufijo más claro
                new_col = f"{base_col}_duplicado_{seen[base_col]}"
            else:
                seen[base_col] = 0
                new_col = base_col
            new_columns.append(new_col)
        
        df.columns = new_columns
        
        # Log cambios para debugging
        if len(set(columns)) != len(set(new_columns)):
            changed_cols = [(old, new) for old, new in zip(columns, new_columns) if old != new]
            for old_col, new_col in changed_cols:
                self.logger.info(f"Columna renombrada: {old_col} -> {new_col}")
        
        return df
    
    def _sync_table(self, sql_file_path, table_name, mode='incremental'):
        """Sincroniza una tabla individual"""
        
        self.logger.info(f"Sincronizando: {os.path.basename(sql_file_path)} -> {table_name}")
        
        try:
            # Verificar si la tabla existe en SQL Server antes de proceder
            clean_table_name = table_name.replace('[', '').replace(']', '')
            if not self.sqlserver.table_exists(clean_table_name):
                self.logger.warning(f"⏭️  OMITIDA: Tabla {table_name} no existe en SQL Server. Solicitar creación al DBA.")
                return 0, True  # 0 registros, tabla omitida
            
            # Leer y ejecutar el script SQL
            with open(sql_file_path, 'r', encoding='utf-8') as f:
                sql_content = f.read().strip()
                if sql_content.endswith(';'):
                    sql_content = sql_content[:-1]
            
            # Modificar consulta para modo incremental si es necesario
            if mode == 'incremental' and table_name in self.date_columns:
                sql_content = self._add_incremental_filter(sql_content, table_name)
            
            # Ejecutar consulta en Oracle
            try:
                oracle_session = self._get_oracle_session()
                df = pd.read_sql_query(sql_content, oracle_session.bind)
            except Exception as e:
                self.logger.error(f"Error ejecutando consulta Oracle: {e}")
                return None  # Indicar error
            
            if df.empty:
                self.logger.info(f"No hay datos para sincronizar en {table_name}")
                return 0, False  # 0 registros, no omitida
            
            # Limpiar nombres de columnas para SQL Server
            df.columns = [self._clean_column_name(col) for col in df.columns]
            
            # Eliminar columnas duplicadas manteniendo la primera ocurrencia
            df = df.loc[:, ~df.columns.duplicated(keep='first')]
            
            # Renombrar columnas duplicadas que no se pudieron eliminar
            df = self._fix_duplicate_columns(df)
            
            # Limpieza mejorada de datos
            df = self._enhanced_data_cleaning(df, table_name)
            
            # Insertar datos sin truncar
            try:
                self.sqlserver.safe_insert(df, clean_table_name, schema='dbo')
                self.logger.info(f"✅ {table_name}: {len(df)} registros sincronizados")
                return len(df), False  # registros sincronizados, no omitida
            except Exception as e:
                self.logger.error(f"Error sincronizando tabla {table_name}: {e}")
                return None  # Indicar error
                
        except Exception as e:
            self.logger.error(f"Error general en _sync_table para {table_name}: {e}")
            return None  # Indicar error
    
    def _get_target_table(self, sql_filename):
        """Obtiene el nombre de la tabla destino basado en el archivo SQL"""
        return self.sync_config.get(sql_filename)
    
    def _add_incremental_filter(self, sql_query, table_name):
        """
        Añade filtro incremental basado en la última fecha sincronizada
        """
        date_column = self.date_columns.get(table_name)
        if not date_column:
            return sql_query
        
        # Obtener última fecha sincronizada
        last_sync_date = self.sqlserver.get_max_date(
            table_name.replace('[', '').replace(']', ''), 
            date_column
        )
        
        if last_sync_date:
            # Convertir fecha a formato Oracle
            oracle_date_str = last_sync_date.strftime('%d/%m/%Y')
            
            # Añadir filtro WHERE o AND según corresponda
            if 'WHERE' in sql_query.upper():
                filter_clause = f" AND {date_column} > TO_DATE('{oracle_date_str}', 'DD/MM/YYYY')"
            else:
                filter_clause = f" WHERE {date_column} > TO_DATE('{oracle_date_str}', 'DD/MM/YYYY')"
            
            # Buscar la posición antes de ORDER BY si existe
            order_by_pos = sql_query.upper().find('ORDER BY')
            if order_by_pos != -1:
                sql_query = sql_query[:order_by_pos] + filter_clause + " " + sql_query[order_by_pos:]
            else:
                sql_query += filter_clause
            
            self.logger.info(f"Filtro incremental aplicado: {date_column} > TO_DATE('{oracle_date_str}', 'DD/MM/YYYY')")
        
        return sql_query
    
    def _clean_column_name(self, column_name):
        """Limpia nombres de columnas para SQL Server"""
        # Remover caracteres especiales y espacios
        clean_name = str(column_name).replace(' ', '_').replace('-', '_')
        # SQL Server no permite ciertos caracteres
        invalid_chars = ['[', ']', '(', ')', '.', ',', ';', ':', '!', '@', '#', '$', '%', '^', '&', '*']
        for char in invalid_chars:
            clean_name = clean_name.replace(char, '_')
        return clean_name
    
    def sync_specific_tables(self, table_list, mode='incremental'):
        """Sincroniza tablas específicas"""
        self.logger.info(f"Sincronizando tablas específicas: {table_list}")
        
        total_synced = 0
        errors = []
        
        for table_name in table_list:
            try:
                # Buscar archivo SQL correspondiente
                sql_file = self._find_sql_file_for_table(table_name)
                if not sql_file:
                    errors.append(f"No se encontró archivo SQL para {table_name}")
                    continue
                
                result = self._sync_table(sql_file, table_name, mode)
                if result is not None:
                    synced_count, _ = result
                    total_synced += synced_count
                else:
                    errors.append(f"Error sincronizando {table_name}")
                
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
                # Buscar el archivo recursivamente
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
                
                # Verificar si SQL Server está disponible
                if not self.sqlserver.engine:
                    status[table_name] = {'exists': False, 'error': 'SQL Server no disponible'}
                    continue
                
                # Verificar si la tabla existe
                if not self.sqlserver.table_exists(clean_table_name):
                    status[table_name] = {'exists': False, 'count': 0, 'last_update': None}
                    continue
                
                # Obtener count de registros
                count_query = f"SELECT COUNT(*) as count FROM [{clean_table_name}]"
                result = self.sqlserver.execute_query(count_query)
                record_count = result['count'].iloc[0]
                
                # Obtener última actualización si hay columna de fecha
                last_update = None
                if table_name in self.date_columns:
                    date_column = self.date_columns[table_name]
                    last_update = self.sqlserver.get_max_date(clean_table_name, date_column)
                
                status[table_name] = {
                    'exists': True,
                    'count': record_count,
                    'last_update': last_update
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