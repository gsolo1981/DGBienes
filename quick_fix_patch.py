# quick_fix_hash.py
# Parche rápido para corregir el error SQL en sync_service.py

import os
import hashlib

def apply_quick_fix():
    """Aplica el parche rápido agregando los métodos necesarios"""
    
    # Código para agregar al final de la clase SyncService
    hash_methods_code = '''
    def _get_hash_tables_by_environment(self):
        """Retorna las tablas que usan hash para sincronización incremental"""
        app_env = settings.APP_ENV.lower()
        
        if app_env == 'bienes':
            return {
                'Bienes_01_BENEFICIARIOS': {
                    'exclude_fields': ['id', 'row_hash', 'fecha_registro']
                }
            }
        elif app_env == 'concesiones':
            return {
                'Concesiones_01_BENEFICIARIOS': {
                    'exclude_fields': ['id', 'row_hash', 'fecha_registro']
                }
            }
        else:
            return {}

    def create_hash_column(self, table_name):
        """Crear columna row_hash si no existe - VERSIÓN CORREGIDA"""
        try:
            clean_table_name = table_name.replace('[', '').replace(']', '')
            
            # Verificar si la columna ya existe - SIN PARÁMETROS
            check_query = f"""
            SELECT COUNT(*) as count
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = '{clean_table_name}' AND COLUMN_NAME = 'row_hash'
            """
            
            result = self.sqlserver.execute_query(check_query)
            exists = result['count'].iloc[0] > 0
            
            if not exists:
                # Agregar columna row_hash usando el engine directamente
                alter_query = f"ALTER TABLE [dbo].[{clean_table_name}] ADD row_hash VARCHAR(64)"
                
                with self.sqlserver.engine.connect() as conn:
                    conn.execute(alter_query)
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
        
        # Convertir a minúsculas para comparación case-insensitive
        exclude_fields = [field.lower() for field in exclude_fields]
        
        # Crear string concatenado de todos los valores, ordenados por nombre de campo
        hash_data = {}
        for key, value in row_data.items():
            if key.lower() not in exclude_fields:
                # Convertir None a string vacío para consistencia
                str_value = str(value).strip() if value is not None else ""
                hash_data[key.lower()] = str_value
        
        # Ordenar por clave para consistencia
        sorted_items = sorted(hash_data.items())
        hash_string = '|'.join([f"{k}:{v}" for k, v in sorted_items])
        
        # Generar hash MD5
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
            
            # Obtener registros sin hash
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
                    row_dict = row.to_dict()
                    new_hash = self.generate_row_hash(row_dict, exclude_fields)
                    
                    update_query = f"""
                    UPDATE [dbo].[{clean_table_name}] 
                    SET row_hash = '{new_hash}' 
                    WHERE id = {row['id']}
                    """
                    
                    conn.execute(update_query)
                    updated_count += 1
                    
                    if updated_count % 1000 == 0:
                        self.logger.info(f"🔄 Procesados {updated_count} registros...")
                
                conn.commit()
            
            self.logger.info(f"✅ Actualizados {updated_count} hashes existentes en {table_name}")
            
        except Exception as e:
            self.logger.error(f"❌ Error actualizando hashes existentes en {table_name}: {e}")
            raise

    def sync_table_with_hash(self, sql_file_path, table_name, source_df):
        """Sincronizar tabla usando hash para evitar duplicados"""
        
        self.logger.info(f"🔄 Sincronizando con HASH: {os.path.basename(sql_file_path)} -> {table_name}")
        
        # Verificar si la tabla existe en SQL Server
        clean_table_name = table_name.replace('[', '').replace(']', '')
        if not self.sqlserver.table_exists(clean_table_name):
            self.logger.warning(f"⏭️  OMITIDA: Tabla {table_name} no existe en SQL Server.")
            return 0, True
        
        # Obtener configuración de hash para esta tabla
        hash_config = self.hash_tables.get(table_name, {})
        exclude_fields = hash_config.get('exclude_fields', ['id', 'row_hash', 'fecha_registro'])
        
        # Crear columna hash si no existe
        self.create_hash_column(table_name)
        
        # Actualizar hashes de registros existentes
        self.update_existing_hashes(table_name, exclude_fields)
        
        # Obtener hashes existentes
        existing_hashes = self.get_existing_hashes(table_name)
        
        # Limpiar DataFrame
        df_clean = self._clean_dataframe_for_sqlserver(source_df.copy())
        
        # Generar hashes para datos nuevos
        new_records = []
        duplicate_count = 0
        
        for _, row in df_clean.iterrows():
            row_dict = row.to_dict()
            new_hash = self.generate_row_hash(row_dict, exclude_fields)
            
            if new_hash in existing_hashes:
                # Es duplicado, ignorar
                duplicate_count += 1
            else:
                # Es nuevo, agregar hash y preparar para insertar
                row_dict['row_hash'] = new_hash
                new_records.append(row_dict)
                existing_hashes.add(new_hash)  # Evitar duplicados en el mismo batch
        
        if not new_records:
            self.logger.info(f"📊 {table_name}: No hay registros nuevos. {duplicate_count} duplicados ignorados.")
            return 0, False
        
        # Convertir a DataFrame y insertar
        df_new = pd.DataFrame(new_records)
        
        try:
            # Insertar solo registros nuevos
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
            self.logger.error(f"❌ Error insertando datos en {table_name}: {e}")
            raise
'''

    print("🔧 APLICANDO PARCHE RÁPIDO PARA ERROR SQL")
    print("=" * 50)
    
    # Leer el archivo sync_service.py actual
    sync_service_path = 'services/sync_service.py'
    
    if not os.path.exists(sync_service_path):
        print(f"❌ No se encuentra {sync_service_path}")
        return False
    
    try:
        # Leer contenido actual
        with open(sync_service_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar si ya tiene el código de hash
        if 'def generate_row_hash(' in content:
            print("⚠️  El archivo ya parece tener métodos de hash")
            print("   Aplicando solo correcciones...")
        
        # Hacer backup
        backup_path = f"{sync_service_path}.backup"
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Backup creado: {backup_path}")
        
        # Agregar import hashlib si no existe
        if 'import hashlib' not in content:
            # Buscar línea de imports
            lines = content.split('\n')
            import_line = -1
            for i, line in enumerate(lines):
                if line.startswith('import ') or line.startswith('from '):
                    import_line = i
            
            if import_line >= 0:
                lines.insert(import_line + 1, 'import hashlib')
                content = '\n'.join(lines)
                print("✅ Agregado: import hashlib")
        
        # Agregar inicialización de hash_tables en __init__
        if 'self.hash_tables = self._get_hash_tables_by_environment()' not in content:
            # Buscar el método __init__
            init_pos = content.find('def __init__(self):')
            if init_pos > 0:
                # Buscar el final del __init__
                lines = content[init_pos:].split('\n')
                for i, line in enumerate(lines):
                    if line.strip() and not line.startswith(' ') and not line.startswith('\t') and i > 0:
                        # Encontró el final del __init__
                        insert_pos = init_pos + len('\n'.join(lines[:i]))
                        content = content[:insert_pos] + '\n        \n        # Configuración de tablas que usan HASH\n        self.hash_tables = self._get_hash_tables_by_environment()\n' + content[insert_pos:]
                        print("✅ Agregada inicialización de hash_tables")
                        break
        
        # Agregar los métodos al final de la clase
        class_end = content.rfind('    def close(self):')
        if class_end > 0:
            # Encontrar el final del método close
            rest_content = content[class_end:]
            method_end = rest_content.find('\n    def ') 
            if method_end == -1:
                # Es el último método
                file_end = content.rfind('\n')
                content = content[:file_end] + hash_methods_code + content[file_end:]
            else:
                insert_pos = class_end + method_end
                content = content[:insert_pos] + hash_methods_code + content[insert_pos:]
        else:
            # Agregar al final del archivo
            content += hash_methods_code
        
        print("✅ Métodos de hash agregados")
        
        # Modificar el método _sync_table para usar hash
        sync_table_pattern = 'def _sync_table(self, sql_file_path, table_name, mode=\'incremental\'):'
        if sync_table_pattern in content:
            # Encontrar y reemplazar el método
            start = content.find(sync_table_pattern)
            if start > 0:
                # Buscar el final del método
                rest = content[start:]
                lines = rest.split('\n')
                indent_level = len(lines[0]) - len(lines[0].lstrip())
                method_lines = [lines[0]]
                
                for i in range(1, len(lines)):
                    line = lines[i]
                    if line.strip() == '':
                        method_lines.append(line)
                        continue
                    
                    current_indent = len(line) - len(line.lstrip())
                    if current_indent <= indent_level and line.strip() and not line.startswith(' ' * (indent_level + 4)):
                        break
                    method_lines.append(line)
                
                # Reemplazar con nueva versión
                new_method = '''    def _sync_table(self, sql_file_path, table_name, mode='incremental'):
        """Sincroniza una tabla individual - versión mejorada con hash"""
        
        file_name = os.path.basename(sql_file_path)
        self.logger.info(f"🔄 Procesando: {file_name} -> {table_name}")
        
        # Verificar si la tabla existe en SQL Server
        clean_table_name = table_name.replace('[', '').replace(']', '')
        if not self.sqlserver.table_exists(clean_table_name):
            self.logger.warning(f"⏭️  OMITIDA: Tabla {table_name} no existe en SQL Server.")
            return 0, True
        
        # Leer y ejecutar el script SQL
        with open(sql_file_path, 'r', encoding='utf-8') as f:
            sql_content = f.read().strip()
            if sql_content.endswith(';'):
                sql_content = sql_content[:-1]
        
        # Verificar si esta tabla usa HASH o FECHA para sincronización incremental
        if hasattr(self, 'hash_tables') and table_name in self.hash_tables:
            # Usar sincronización por HASH
            self.logger.info(f"📊 Usando sincronización por HASH para {table_name}")
            
            # Ejecutar consulta en Oracle para obtener todos los datos
            try:
                oracle_session = self._get_oracle_session()
                df = pd.read_sql_query(sql_content, oracle_session.bind)
            except Exception as e:
                self.logger.error(f"❌ Error ejecutando consulta Oracle: {e}")
                raise
            
            if df.empty:
                self.logger.info(f"📭 No hay datos en Oracle para {table_name}")
                return 0, False
            
            # Limpiar nombres de columnas
            df.columns = [self._clean_column_name(col) for col in df.columns]
            df = df.loc[:, ~df.columns.duplicated(keep='first')]
            df = self._fix_duplicate_columns(df)
            
            # Sincronizar usando hash
            return self.sync_table_with_hash(sql_file_path, table_name, df)
            
        else:
            # Usar sincronización tradicional por FECHA
            self.logger.info(f"📅 Usando sincronización por FECHA para {table_name}")
            
            # Modificar consulta para modo incremental si es necesario
            if mode == 'incremental' and table_name in self.date_columns:
                sql_content = self._add_incremental_filter(sql_content, table_name)
            
            # Ejecutar consulta en Oracle
            try:
                oracle_session = self._get_oracle_session()
                df = pd.read_sql_query(sql_content, oracle_session.bind)
            except Exception as e:
                self.logger.error(f"❌ Error ejecutando consulta Oracle: {e}")
                raise
            
            if df.empty:
                self.logger.info(f"📭 No hay datos nuevos para {table_name}")
                return 0, False
            
            # Limpiar DataFrame
            df.columns = [self._clean_column_name(col) for col in df.columns]
            df = df.loc[:, ~df.columns.duplicated(keep='first')]
            df = self._fix_duplicate_columns(df)
            df = self._clean_dataframe_for_sqlserver(df)
            
            # Insertar datos
            try:
                self.sqlserver.safe_insert(df, clean_table_name, schema='dbo')
                self.logger.info(f"✅ {table_name}: {len(df)} registros sincronizados")
                return len(df), False
            except Exception as e:
                self.logger.error(f"❌ Error sincronizando tabla {table_name}: {e}")
                raise'''
                
                old_method = '\n'.join(method_lines)
                content = content.replace(old_method, new_method)
                print("✅ Método _sync_table actualizado")
        
        # Guardar archivo modificado
        with open(sync_service_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Parche aplicado exitosamente")
        print(f"💾 Backup guardado en: {backup_path}")
        print("")
        print("🎯 PRÓXIMOS PASOS:")
        print("1. Ejecutar script SQL para agregar columna row_hash")
        print("2. Probar: python main.py --mode sqlserver --sync-mode incremental")
        print("")
        
        return True
        
    except Exception as e:
        print(f"❌ Error aplicando parche: {e}")
        return False

if __name__ == "__main__":
    apply_quick_fix()
