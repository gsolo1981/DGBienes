# test_hash_sync.py
# Script para probar la sincronización con hash en Bienes_01_BENEFICIARIOS

import os
import sys
import logging
import pandas as pd
from datetime import datetime

# Asegurar que podemos importar los módulos del proyecto
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.sync_service import SyncService
from adapters.db_adapter import get_oracle_session, is_oracle_available
from adapters.sqlserver_adapter import SQLServerAdapter
from config.settings import settings

def setup_logging():
    """Configura logging para la prueba"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('test_hash_sync.log', encoding='utf-8')
        ]
    )

def test_connections():
    """Prueba las conexiones a Oracle y SQL Server"""
    logger = logging.getLogger(__name__)
    
    print("🔍 VERIFICANDO CONEXIONES")
    print("=" * 50)
    
    # Probar Oracle
    try:
        if is_oracle_available():
            oracle_session = get_oracle_session()
            oracle_test = pd.read_sql("SELECT 'Oracle OK' as test FROM dual", oracle_session.bind)
            print(f"✅ Oracle: {oracle_test['test'].iloc[0]}")
            oracle_session.close()
        else:
            print("❌ Oracle: No disponible")
            return False
    except Exception as e:
        print(f"❌ Oracle: Error - {e}")
        return False
    
    # Probar SQL Server
    try:
        sqlserver = SQLServerAdapter()
        if sqlserver.engine:
            result = sqlserver.test_connection()
            if result:
                print(f"✅ SQL Server: {result}")
            else:
                print("❌ SQL Server: Error en conexión")
                return False
        else:
            print("❌ SQL Server: No inicializado")
            return False
    except Exception as e:
        print(f"❌ SQL Server: Error - {e}")
        return False
    
    print("✅ Todas las conexiones OK\n")
    return True

def check_table_structure():
    """Verifica la estructura de la tabla en SQL Server"""
    logger = logging.getLogger(__name__)
    
    print("🔍 VERIFICANDO ESTRUCTURA DE TABLA")
    print("=" * 50)
    
    try:
        sqlserver = SQLServerAdapter()
        
        # Verificar si la tabla existe
        if not sqlserver.table_exists('Bienes_01_BENEFICIARIOS'):
            print("❌ La tabla Bienes_01_BENEFICIARIOS no existe en SQL Server")
            print("   Ejecuta el script DDL primero para crear la tabla")
            return False
        
        print("✅ Tabla Bienes_01_BENEFICIARIOS existe")
        
        # Verificar columnas
        columns = sqlserver.get_table_columns('Bienes_01_BENEFICIARIOS')
        print(f"📊 Columnas encontradas: {len(columns)}")
        
        # Verificar si existe row_hash
        has_hash_column = 'row_hash' in columns['COLUMN_NAME'].values
        
        if has_hash_column:
            print("✅ Columna row_hash existe")
        else:
            print("⚠️  Columna row_hash NO existe")
            print("   Se creará automáticamente durante la sincronización")
        
        print("✅ Estructura de tabla verificada\n")
        return True
        
    except Exception as e:
        print(f"❌ Error verificando estructura: {e}")
        return False

def test_oracle_query():
    """Prueba la consulta Oracle para Bienes_01_BENEFICIARIOS"""
    logger = logging.getLogger(__name__)
    
    print("🔍 PROBANDO CONSULTA ORACLE")
    print("=" * 50)
    
    try:
        # Leer el archivo SQL
        sql_file = os.path.join('sql', 'Bienes', 'Bienes_01_BENEFICIARIOS.sql')
        
        if not os.path.exists(sql_file):
            print(f"❌ No se encuentra el archivo: {sql_file}")
            return None
        
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_content = f.read().strip()
            if sql_content.endswith(';'):
                sql_content = sql_content[:-1]
        
        print(f"✅ Archivo SQL leído: {sql_file}")
        
        # Ejecutar consulta con LIMIT para prueba
        test_query = f"SELECT * FROM ({sql_content}) WHERE ROWNUM <= 5"
        
        oracle_session = get_oracle_session()
        df = pd.read_sql(test_query, oracle_session.bind)
        oracle_session.close()
        
        if df.empty:
            print("⚠️  La consulta no retornó datos")
            return None
        
        print(f"✅ Consulta exitosa: {len(df)} registros de prueba")
        print(f"📊 Columnas: {list(df.columns)}")
        print("\n📋 Muestra de datos:")
        print(df.head().to_string())
        print("")
        
        return df
        
    except Exception as e:
        print(f"❌ Error ejecutando consulta Oracle: {e}")
        return None

def test_hash_generation(sample_df):
    """Prueba la generación de hash"""
    logger = logging.getLogger(__name__)
    
    print("🔍 PROBANDO GENERACIÓN DE HASH")
    print("=" * 50)
    
    try:
        sync_service = SyncService()
        
        # Configuración de campos a excluir
        exclude_fields = ['id', 'row_hash', 'fecha_registro']
        
        # Generar hash para cada registro
        hashes = []
        for _, row in sample_df.iterrows():
            row_dict = row.to_dict()
            hash_value = sync_service.generate_row_hash(row_dict, exclude_fields)
            hashes.append(hash_value)
        
        print(f"✅ Hashes generados para {len(hashes)} registros")
        print("📋 Ejemplos de hash:")
        for i, hash_val in enumerate(hashes[:3]):
            print(f"  Registro {i+1}: {hash_val}")
        
        # Verificar unicidad
        unique_hashes = set(hashes)
        if len(unique_hashes) == len(hashes):
            print(f"✅ Todos los hashes son únicos ({len(unique_hashes)} únicos)")
        else:
            duplicates = len(hashes) - len(unique_hashes)
            print(f"⚠️  Encontrados {duplicates} hashes duplicados")
        
        print("")
        return hashes
        
    except Exception as e:
        print(f"❌ Error generando hashes: {e}")
        return None

def test_full_sync():
    """Prueba la sincronización completa con hash"""
    logger = logging.getLogger(__name__)
    
    print("🔍 EJECUTANDO SINCRONIZACIÓN DE PRUEBA")
    print("=" * 50)
    
    try:
        sync_service = SyncService()
        
        # Sincronizar solo Bienes_01_BENEFICIARIOS
        table_list = ['Bienes_01_BENEFICIARIOS']
        
        # Ejecutar sincronización incremental (con hash)
        total_synced, errors = sync_service.sync_specific_tables(table_list, mode='incremental')
        
        if errors:
            print("❌ Errores durante la sincronización:")
            for error in errors:
                print(f"  - {error}")
            return False
        
        print(f"✅ Sincronización completada: {total_synced} registros")
        
        # Verificar resultado
        sqlserver = SQLServerAdapter()
        
        # Contar registros totales
        count_query = "SELECT COUNT(*) as total FROM [dbo].[Bienes_01_BENEFICIARIOS]"
        result = sqlserver.execute_query(count_query)
        total_records = result['total'].iloc[0]
        
        # Contar registros con hash
        hash_query = """
        SELECT 
            COUNT(*) as total,
            COUNT(row_hash) as with_hash,
            COUNT(DISTINCT row_hash) as unique_hashes
        FROM [dbo].[Bienes_01_BENEFICIARIOS]
        """
        hash_result = sqlserver.execute_query(hash_query)
        stats = hash_result.iloc[0]
        
        print("\n📊 ESTADÍSTICAS FINALES:")
        print(f"Total registros: {stats['total']:,}")
        print(f"Registros con hash: {stats['with_hash']:,}")
        print(f"Hashes únicos: {stats['unique_hashes']:,}")
        
        if stats['total'] == stats['with_hash'] == stats['unique_hashes']:
            print("✅ Todos los registros tienen hash único")
        else:
            print("⚠️  Hay inconsistencias en los hashes")
        
        sync_service.close()
        return True
        
    except Exception as e:
        print(f"❌ Error en sincronización: {e}")
        return False

def test_duplicate_detection():
    """Prueba la detección de duplicados ejecutando dos veces"""
    logger = logging.getLogger(__name__)
    
    print("🔍 PROBANDO DETECCIÓN DE DUPLICADOS")
    print("=" * 50)
    
    try:
        # Contar registros antes
        sqlserver = SQLServerAdapter()
        before_query = "SELECT COUNT(*) as count FROM [dbo].[Bienes_01_BENEFICIARIOS]"
        before_result = sqlserver.execute_query(before_query)
        before_count = before_result['count'].iloc[0]
        
        print(f"📊 Registros antes de segunda sincronización: {before_count:,}")
        
        # Ejecutar segunda sincronización
        sync_service = SyncService()
        table_list = ['Bienes_01_BENEFICIARIOS']
        total_synced, errors = sync_service.sync_specific_tables(table_list, mode='incremental')
        
        # Contar registros después
        after_result = sqlserver.execute_query(before_query)
        after_count = after_result['count'].iloc[0]
        
        print(f"📊 Registros después de segunda sincronización: {after_count:,}")
        print(f"📊 Registros agregados en segunda ejecución: {total_synced}")
        
        if before_count == after_count and total_synced == 0:
            print("✅ PERFECTO: No se agregaron duplicados")
            print("✅ La detección de duplicados funciona correctamente")
        else:
            print("⚠️  PROBLEMA: Se agregaron registros en la segunda ejecución")
            print("   Esto indica que la detección de duplicados no está funcionando")
        
        sync_service.close()
        return before_count == after_count
        
    except Exception as e:
        print(f"❌ Error probando duplicados: {e}")
        return False

def main():
    """Función principal de prueba"""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    print("🧪 PRUEBA DE SINCRONIZACIÓN CON HASH")
    print("=" * 60)
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Entorno: {settings.APP_ENV.upper()}")
    print("=" * 60)
    print("")
    
    # Verificar configuración
    if not settings.is_configured():
        print("❌ ERROR: Configuración incompleta")
        missing = settings.get_missing_config()
        print(f"Variables faltantes: {', '.join(missing)}")
        return False
    
    success = True
    
    # 1. Probar conexiones
    if not test_connections():
        print("❌ FALLO: Problemas de conexión")
        return False
    
    # 2. Verificar estructura de tabla
    if not check_table_structure():
        print("❌ FALLO: Problemas en estructura de tabla")
        return False
    
    # 3. Probar consulta Oracle
    sample_df = test_oracle_query()
    if sample_df is None:
        print("❌ FALLO: Problemas con consulta Oracle")
        return False
    
    # 4. Probar generación de hash
    hashes = test_hash_generation(sample_df)
    if hashes is None:
        print("❌ FALLO: Problemas generando hash")
        return False
    
    # 5. Probar sincronización completa
    if not test_full_sync():
        print("❌ FALLO: Problemas en sincronización")
        return False
    
    # 6. Probar detección de duplicados
    if not test_duplicate_detection():
        print("❌ FALLO: Problemas en detección de duplicados")
        success = False
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 TODAS LAS PRUEBAS EXITOSAS")
        print("✅ La sincronización con hash está funcionando correctamente")
        print("✅ No se crean duplicados en ejecuciones sucesivas")
        print("\n💡 Puedes usar: python main.py --mode sqlserver --sync-mode incremental")
    else:
        print("❌ ALGUNAS PRUEBAS FALLARON")
        print("⚠️  Revisa los logs para más detalles")
    print("=" * 60)
    
    return success

if __name__ == "__main__":
    try:
        success = main()
        exit_code = 0 if success else 1
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n⚠️  Prueba interrumpida por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)
