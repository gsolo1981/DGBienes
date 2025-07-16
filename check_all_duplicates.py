#!/usr/bin/env python3
"""
Script para verificar duplicados en todas las tablas del sistema
"""
import sys
import logging
from pathlib import Path
import hashlib
import pandas as pd
from datetime import datetime

# Agregar el directorio raíz al path
sys.path.append(str(Path(__file__).parent))

from adapters.sqlserver_adapter import SQLServerAdapter
from services.sync_service import SyncService
from config.settings import settings

def setup_logging():
    """Configura logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def generate_row_hash(row_data, exclude_fields=None):
    """Generar hash MD5 para comparar registros"""
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

def get_table_columns(sqlserver, table_name):
    """Obtiene las columnas de una tabla (excluyendo campos de control)"""
    try:
        clean_table_name = table_name.replace('[', '').replace(']', '')
        
        columns_query = f"""
        SELECT COLUMN_NAME
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_NAME = '{clean_table_name}'
        AND COLUMN_NAME NOT IN ('id', 'row_hash', 'fecha_registro')
        ORDER BY ORDINAL_POSITION
        """
        
        result = sqlserver.execute_query(columns_query)
        return result['COLUMN_NAME'].tolist()
        
    except Exception as e:
        return []

def analyze_table_duplicates(sqlserver, table_name, sync_service):
    """Analiza duplicados en una tabla específica"""
    logger = logging.getLogger(__name__)
    
    clean_table_name = table_name.replace('[', '').replace(']', '')
    
    try:
        # Información básica de la tabla
        count_query = f"SELECT COUNT(*) as count FROM [dbo].[{clean_table_name}]"
        result = sqlserver.execute_query(count_query)
        total_records = result['count'].iloc[0]
        
        if total_records == 0:
            return {
                'table_name': table_name,
                'total_records': 0,
                'unique_records': 0,
                'duplicates': 0,
                'has_hash_column': False,
                'records_with_hash': 0,
                'unique_hashes': 0,
                'status': 'EMPTY',
                'duplicate_groups': 0,
                'error': None
            }
        
        # Verificar si tiene columna row_hash
        check_hash_column = f"""
        SELECT COUNT(*) as count
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_NAME = '{clean_table_name}' AND COLUMN_NAME = 'row_hash'
        """
        result = sqlserver.execute_query(check_hash_column)
        has_hash_column = result['count'].iloc[0] > 0
        
        records_with_hash = 0
        unique_hashes = 0
        
        if has_hash_column:
            hash_stats_query = f"""
            SELECT 
                COUNT(row_hash) as with_hash,
                COUNT(DISTINCT row_hash) as unique_hashes
            FROM [dbo].[{clean_table_name}]
            WHERE row_hash IS NOT NULL AND row_hash != ''
            """
            result = sqlserver.execute_query(hash_stats_query)
            if not result.empty:
                records_with_hash = result['with_hash'].iloc[0]
                unique_hashes = result['unique_hashes'].iloc[0]
        
        # Obtener columnas para análisis de duplicados
        columns = get_table_columns(sqlserver, clean_table_name)
        
        if not columns:
            return {
                'table_name': table_name,
                'total_records': total_records,
                'unique_records': total_records,
                'duplicates': 0,
                'has_hash_column': has_hash_column,
                'records_with_hash': records_with_hash,
                'unique_hashes': unique_hashes,
                'status': 'NO_COLUMNS',
                'duplicate_groups': 0,
                'error': 'No se pudieron obtener columnas'
            }
        
        # Crear consulta para detectar duplicados por contenido
        columns_str = ', '.join([f'[{col}]' for col in columns])
        
        duplicate_analysis_query = f"""
        WITH DuplicateAnalysis AS (
            SELECT 
                {columns_str},
                COUNT(*) as duplicate_count
            FROM [dbo].[{clean_table_name}]
            GROUP BY {columns_str}
            HAVING COUNT(*) > 1
        )
        SELECT 
            COUNT(*) as duplicate_groups,
            SUM(duplicate_count) as total_duplicates,
            SUM(duplicate_count - 1) as records_to_remove
        FROM DuplicateAnalysis
        """
        
        result = sqlserver.execute_query(duplicate_analysis_query)
        
        if not result.empty:
            dup_stats = result.iloc[0]
            duplicate_groups = dup_stats['duplicate_groups'] or 0
            total_duplicates = dup_stats['total_duplicates'] or 0
            records_to_remove = dup_stats['records_to_remove'] or 0
        else:
            duplicate_groups = 0
            total_duplicates = 0
            records_to_remove = 0
        
        # Calcular registros únicos
        unique_records = total_records - records_to_remove
        
        # Determinar estado
        if records_to_remove == 0:
            status = 'CLEAN'
        elif records_to_remove < 100:
            status = 'FEW_DUPLICATES'
        else:
            status = 'MANY_DUPLICATES'
        
        # Verificar si está configurado para hash
        is_hash_configured = table_name in sync_service.hash_tables
        
        return {
            'table_name': table_name,
            'total_records': total_records,
            'unique_records': unique_records,
            'duplicates': records_to_remove,
            'has_hash_column': has_hash_column,
            'records_with_hash': records_with_hash,
            'unique_hashes': unique_hashes,
            'status': status,
            'duplicate_groups': duplicate_groups,
            'is_hash_configured': is_hash_configured,
            'hash_duplicates': records_with_hash - unique_hashes if has_hash_column else 0,
            'error': None
        }
        
    except Exception as e:
        logger.error(f"Error analizando tabla {table_name}: {e}")
        return {
            'table_name': table_name,
            'total_records': 0,
            'unique_records': 0,
            'duplicates': 0,
            'has_hash_column': False,
            'records_with_hash': 0,
            'unique_hashes': 0,
            'status': 'ERROR',
            'duplicate_groups': 0,
            'error': str(e)
        }

def get_all_tables_for_environment():
    """Obtiene todas las tablas según el entorno configurado"""
    
    tables_by_env = {
        'bienes': [
            'Bienes_01_BENEFICIARIOS',
            'Bienes_02_CARTERAS', 
            'Bienes_03_CONTRATOS',
            'Bienes_04_PLAN_DE_PAGOS'
        ],
        'concesiones': [
            'Concesiones_01_BENEFICIARIOS',
            'Concesiones_02_CARTERAS',
            'Concesiones_03_CONTRATOS',
            'Concesiones_04_PLAN_DE_PAGOS'
        ],
        'sigaf': [
            '01_RELACION_BAC_SIGAF',
            '02_SPR_RENGLONES',
            '03_SPR_IMPUTACIONES',
            '04_RPR_SPR_PRD',
            '05_RPR_RENGLONES',
            '06_RPR_IMPUTACIONES',
            '07_PRD_RENGLONES',
            '08_PRD_IMPUTACIONES',
            '09_PRD_FACTURAS',
            '10_FACTURAS_OP_PAGOS',
            '11_RP',
            '12_DRP_RENGLONES',
            '13_DRP_IMPUTACIONES',
            '14_DRP_FACTURAS',
            '15_DRP_FACTURAS_PAGOS',
            '16_PRECIARIO',
            '17_PRECIARIO_IMPUTACIONES',
            '18_PRD_PRECIARIO',
            '19_PRD_PRECIARIO_RENGLONES',
            '20_PRD_PRECIARIO_IMPUTACIONES',
            '21_PRD_PRECIARIO_FACTURAS',
            '22_PAGOS_PRECIARIO',
            '23_UNIDADES_EJECUTORAS',
            '24_PERIODOS_FISCALES',
            '25_ENTES'
        ],
        'sigaf_devengado': [
            '01_DEVENGADO_v2'
        ]
    }
    
    return tables_by_env.get(settings.APP_ENV.lower(), [])

def generate_duplicate_report(results):
    """Genera un reporte consolidado de duplicados"""
    logger = logging.getLogger(__name__)
    
    logger.info("\n" + "="*100)
    logger.info("📊 REPORTE CONSOLIDADO DE DUPLICADOS")
    logger.info("="*100)
    
    # Estadísticas generales
    total_tables = len(results)
    tables_with_duplicates = sum(1 for r in results if r['duplicates'] > 0)
    total_records = sum(r['total_records'] for r in results)
    total_duplicates = sum(r['duplicates'] for r in results)
    tables_with_hash = sum(1 for r in results if r['has_hash_column'])
    tables_with_errors = sum(1 for r in results if r['status'] == 'ERROR')
    
    logger.info(f"📋 Entorno: {settings.APP_ENV.upper()}")
    logger.info(f"📋 Total de tablas analizadas: {total_tables}")
    logger.info(f"📋 Tablas con duplicados: {tables_with_duplicates}")
    logger.info(f"📋 Tablas con errores: {tables_with_errors}")
    logger.info(f"📋 Tablas con columna hash: {tables_with_hash}")
    logger.info(f"📋 Total de registros: {total_records:,}")
    logger.info(f"📋 Total de duplicados: {total_duplicates:,}")
    
    if total_duplicates > 0:
        percentage = (total_duplicates / total_records) * 100
        logger.info(f"📋 Porcentaje de duplicados: {percentage:.2f}%")
    
    # Detalle por tabla
    logger.info("\n" + "="*100)
    logger.info("📋 DETALLE POR TABLA")
    logger.info("="*100)
    
    # Ordenar por cantidad de duplicados (descendente)
    sorted_results = sorted(results, key=lambda x: x['duplicates'], reverse=True)
    
    for result in sorted_results:
        table_name = result['table_name']
        status_icon = {
            'CLEAN': '✅',
            'FEW_DUPLICATES': '⚠️',
            'MANY_DUPLICATES': '❌',
            'EMPTY': '📭',
            'ERROR': '💥',
            'NO_COLUMNS': '❓'
        }.get(result['status'], '❓')
        
        logger.info(f"\n{status_icon} {table_name}")
        logger.info(f"   📊 Registros: {result['total_records']:,}")
        
        if result['total_records'] > 0:
            logger.info(f"   📊 Únicos: {result['unique_records']:,}")
            logger.info(f"   📊 Duplicados: {result['duplicates']:,}")
            
            if result['duplicates'] > 0:
                logger.info(f"   📊 Grupos duplicados: {result['duplicate_groups']:,}")
        
        if result['has_hash_column']:
            logger.info(f"   🔐 Con hash: {result['records_with_hash']:,}")
            logger.info(f"   🔐 Hashes únicos: {result['unique_hashes']:,}")
            
            if result.get('hash_duplicates', 0) > 0:
                logger.info(f"   ⚠️ Hashes duplicados: {result['hash_duplicates']:,}")
        else:
            logger.info(f"   🔐 Sin columna hash")
        
        # Mostrar configuración de hash
        if result.get('is_hash_configured'):
            logger.info(f"   ⚙️ Configurado para hash: ✅")
        else:
            logger.info(f"   ⚙️ Configurado para hash: ❌")
        
        if result['error']:
            logger.info(f"   💥 Error: {result['error']}")
    
    # Recomendaciones
    logger.info("\n" + "="*100)
    logger.info("💡 RECOMENDACIONES")
    logger.info("="*100)
    
    critical_tables = [r for r in results if r['duplicates'] > 1000]
    if critical_tables:
        logger.info("🚨 TABLAS CRÍTICAS (>1000 duplicados):")
        for table in critical_tables:
            logger.info(f"   - {table['table_name']}: {table['duplicates']:,} duplicados")
        logger.info("   💡 Ejecutar limpieza urgente")
    
    moderate_tables = [r for r in results if 100 <= r['duplicates'] <= 1000]
    if moderate_tables:
        logger.info("⚠️ TABLAS CON DUPLICADOS MODERADOS:")
        for table in moderate_tables:
            logger.info(f"   - {table['table_name']}: {table['duplicates']:,} duplicados")
        logger.info("   💡 Planificar limpieza")
    
    few_duplicates = [r for r in results if 1 <= r['duplicates'] < 100]
    if few_duplicates:
        logger.info("📋 TABLAS CON POCOS DUPLICADOS:")
        for table in few_duplicates:
            logger.info(f"   - {table['table_name']}: {table['duplicates']:,} duplicados")
        logger.info("   💡 Limpieza opcional")
    
    # Problemas de configuración
    no_hash_config = [r for r in results if not r.get('is_hash_configured', False) and r['total_records'] > 0]
    if no_hash_config:
        logger.info("⚙️ TABLAS SIN CONFIGURACIÓN HASH:")
        for table in no_hash_config:
            logger.info(f"   - {table['table_name']}")
        logger.info("   💡 Actualizar sync_service.py")
    
    no_hash_column = [r for r in results if not r['has_hash_column'] and r['total_records'] > 0]
    if no_hash_column:
        logger.info("🔐 TABLAS SIN COLUMNA HASH:")
        for table in no_hash_column:
            logger.info(f"   - {table['table_name']}")
        logger.info("   💡 Ejecutar ALTER TABLE para agregar columna")
    
    # Scripts sugeridos
    logger.info("\n" + "="*100)
    logger.info("🔧 SCRIPTS SUGERIDOS")
    logger.info("="*100)
    
    if critical_tables or moderate_tables:
        logger.info("Para limpiar duplicados:")
        logger.info("   python fix_duplicates.py")
    
    if no_hash_column:
        logger.info("Para agregar columnas hash:")
        logger.info("   python setup_hash_columns.py")
    
    if no_hash_config:
        logger.info("Para actualizar configuración:")
        logger.info("   Editar services/sync_service.py")
    
    logger.info("Para sincronización completa:")
    logger.info("   python main.py --mode sqlserver --sync-mode full")

def main():
    """Función principal"""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    start_time = datetime.now()
    
    logger.info("🚀 INICIANDO VERIFICACIÓN DE DUPLICADOS EN TODAS LAS TABLAS")
    logger.info("="*80)
    
    try:
        # Inicializar servicios
        sync_service = SyncService()
        sqlserver = SQLServerAdapter()
        
        if not sqlserver.engine:
            logger.error("❌ SQL Server no disponible")
            return
        
        # Obtener tablas del entorno
        tables = get_all_tables_for_environment()
        
        if not tables:
            logger.error(f"❌ No se encontraron tablas para el entorno: {settings.APP_ENV}")
            return
        
        logger.info(f"📋 Entorno: {settings.APP_ENV.upper()}")
        logger.info(f"📋 Tablas a analizar: {len(tables)}")
        
        # Analizar cada tabla
        results = []
        
        for i, table_name in enumerate(tables, 1):
            logger.info(f"\n🔍 Analizando {i}/{len(tables)}: {table_name}")
            
            result = analyze_table_duplicates(sqlserver, table_name, sync_service)
            results.append(result)
            
            # Mostrar progreso
            if result['status'] == 'CLEAN':
                logger.info(f"   ✅ Limpia: {result['total_records']:,} registros")
            elif result['status'] == 'FEW_DUPLICATES':
                logger.info(f"   ⚠️ Pocos duplicados: {result['duplicates']:,}")
            elif result['status'] == 'MANY_DUPLICATES':
                logger.info(f"   ❌ Muchos duplicados: {result['duplicates']:,}")
            elif result['status'] == 'EMPTY':
                logger.info(f"   📭 Vacía")
            elif result['status'] == 'ERROR':
                logger.info(f"   💥 Error: {result['error']}")
        
        # Generar reporte
        generate_duplicate_report(results)
        
        # Tiempo transcurrido
        end_time = datetime.now()
        duration = end_time - start_time
        
        logger.info(f"\n⏱️ Tiempo transcurrido: {duration}")
        logger.info("="*80)
        logger.info("✅ VERIFICACIÓN COMPLETADA")
        
        sqlserver.close()
        
    except Exception as e:
        logger.error(f"❌ Error en verificación: {e}")
        import traceback
        logger.error(traceback.format_exc())

if __name__ == '__main__':
    main()