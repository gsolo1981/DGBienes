#!/usr/bin/env python3
"""
Verificación completa de salud para todas las tablas Bienes
Detecta duplicados, problemas de datos y recomienda acciones
"""
import sys
import logging
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.append(str(Path(__file__).parent))

from adapters.sqlserver_adapter import SQLServerAdapter
from config.settings import settings

def setup_logging():
    """Configura logging básico"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def verify_all_bienes_tables():
    """Verificación completa de todas las tablas Bienes"""
    logger = logging.getLogger(__name__)
    
    logger.info("🏥 VERIFICACIÓN COMPLETA - TODAS LAS TABLAS BIENES")
    logger.info("=" * 60)
    
    tables_config = {
        'Bienes_01_BENEFICIARIOS': {
            'description': 'Beneficiarios del sistema',
            'key_fields': ['documento_tipo', 'documento'],
            'critical_fields': ['nombre', 'documento'],
            'expected_uniqueness': 'documento único por tipo'
        },
        'Bienes_02_CARTERAS': {
            'description': 'Cartera inmobiliaria',
            'key_fields': ['identificacion', 'nrounidad'],
            'critical_fields': ['identificacion', 'circunscripcion', 'seccion'],
            'expected_uniqueness': 'una unidad por identificación'
        },
        'Bienes_03_CONTRATOS': {
            'description': 'Contratos de bienes',
            'key_fields': ['nro', 'documento', 'desde', 'hasta'],
            'critical_fields': ['nro', 'fechafirma', 'documento'],
            'expected_uniqueness': 'un contrato por beneficiario y período'
        },
        'Bienes_04_PLAN_DE_PAGOS': {
            'description': 'Planes de pago',
            'key_fields': ['carpeta', 'documento', 'numero', 'vencimiento'],
            'critical_fields': ['carpeta', 'documento', 'vencimiento'],
            'expected_uniqueness': 'un plan por beneficiario y vencimiento'
        }
    }
    
    try:
        sqlserver = SQLServerAdapter()
        overall_health = True
        total_duplicates = 0
        total_records = 0
        
        for table_name, config in tables_config.items():
            logger.info(f"\n📋 {table_name}")
            logger.info(f"   Descripción: {config['description']}")
            logger.info(f"   Unicidad esperada: {config['expected_uniqueness']}")
            
            if not sqlserver.table_exists(table_name):
                logger.error(f"   ❌ TABLA NO EXISTE")
                overall_health = False
                continue
            
            # Verificar salud general de la tabla
            health_result = verify_table_health(sqlserver, table_name, config)
            
            # Acumular estadísticas
            total_records += health_result['total_records']
            total_duplicates += health_result['duplicates']
            
            if health_result['has_issues']:
                overall_health = False
        
        # Resumen general
        logger.info(f"\n🎯 RESUMEN GENERAL")
        logger.info("=" * 40)
        logger.info(f"Total registros: {total_records:,}")
        logger.info(f"Total duplicados: {total_duplicates:,}")
        
        if overall_health:
            logger.info(f"✅ TODAS LAS TABLAS EN BUEN ESTADO")
            logger.info(f"Recomendación: Ejecutar sincronización normal")
        else:
            logger.warning(f"⚠️  SE ENCONTRARON PROBLEMAS")
            logger.info(f"Recomendación: Ejecutar limpieza antes de sincronizar")
            
            # Comandos recomendados
            logger.info(f"\n📋 COMANDOS RECOMENDADOS:")
            logger.info(f"1. python clean_all_duplicates.py --analyze")
            logger.info(f"2. python clean_all_duplicates.py")
            logger.info(f"3. python verify_tables_health.py")
            logger.info(f"4. python main.py --mode sqlserver --sync-mode incremental")
        
        sqlserver.close()
        return overall_health
        
    except Exception as e:
        logger.error(f"Error verificando tablas: {e}")
        return False

def verify_table_health(sqlserver, table_name, config):
    """Verifica la salud de una tabla específica"""
    logger = logging.getLogger(__name__)
    
    result = {
        'total_records': 0,
        'duplicates': 0,
        'null_criticals': 0,
        'has_issues': False
    }
    
    try:
        # 1. Conteo total de registros
        total_query = f"SELECT COUNT(*) as total FROM [{table_name}]"
        total_records = sqlserver.execute_query(total_query)['total'].iloc[0]
        result['total_records'] = total_records
        logger.info(f"   📊 Total registros: {total_records:,}")
        
        # 2. Verificar duplicados por campos clave
        key_fields = config['key_fields']
        if key_fields:
            dup_count = check_duplicates_by_fields(sqlserver, table_name, key_fields)
            result['duplicates'] = dup_count
            
            if dup_count > 0:
                duplicate_ratio = (dup_count / total_records) * 100
                logger.warning(f"   ❌ Duplicados: {dup_count:,} ({duplicate_ratio:.1f}%)")
                result['has_issues'] = True
            else:
                logger.info(f"   ✅ Sin duplicados por campos clave")
        
        # 3. Verificar campos críticos nulos
        critical_fields = config['critical_fields']
        null_count = check_null_critical_fields(sqlserver, table_name, critical_fields)
        result['null_criticals'] = null_count
        
        if null_count > 0:
            logger.warning(f"   ⚠️  Campos críticos nulos: {null_count:,}")
            result['has_issues'] = True
        else:
            logger.info(f"   ✅ Campos críticos completos")
        
        # 4. Verificaciones específicas por tabla
        specific_issues = check_table_specific_issues(sqlserver, table_name)
        if specific_issues:
            logger.warning(f"   ⚠️  Problemas específicos: {specific_issues}")
            result['has_issues'] = True
        
        # 5. Estado final de la tabla
        if not result['has_issues']:
            logger.info(f"   🎉 TABLA SALUDABLE")
        else:
            logger.warning(f"   🔧 REQUIERE ATENCIÓN")
        
    except Exception as e:
        logger.error(f"   💥 Error verificando {table_name}: {e}")
        result['has_issues'] = True
    
    return result

def check_duplicates_by_fields(sqlserver, table_name, fields):
    """Verifica duplicados por campos específicos"""
    try:
        fields_str = ', '.join(fields)
        
        dup_query = f"""
        WITH duplicates AS (
            SELECT *, ROW_NUMBER() OVER (
                PARTITION BY {fields_str}
                ORDER BY {fields[0]}
            ) as rn
            FROM [{table_name}]
        )
        SELECT COUNT(*) as dup_count
        FROM duplicates 
        WHERE rn > 1
        """
        
        result = sqlserver.execute_query(dup_query)
        return result['dup_count'].iloc[0]
        
    except Exception as e:
        logging.getLogger(__name__).warning(f"Error verificando duplicados: {e}")
        return 0

def check_null_critical_fields(sqlserver, table_name, fields):
    """Verifica campos críticos con valores nulos"""
    try:
        null_conditions = []
        for field in fields:
            null_conditions.append(f"[{field}] IS NULL OR [{field}] = ''")
        
        null_query = f"""
        SELECT COUNT(*) as null_count
        FROM [{table_name}]
        WHERE {' OR '.join(null_conditions)}
        """
        
        result = sqlserver.execute_query(null_query)
        return result['null_count'].iloc[0]
        
    except Exception as e:
        logging.getLogger(__name__).warning(f"Error verificando nulos: {e}")
        return 0

def check_table_specific_issues(sqlserver, table_name):
    """Verificaciones específicas por tabla"""
    issues = []
    
    try:
        if table_name == 'Bienes_01_BENEFICIARIOS':
            # Verificar documentos inválidos
            doc_query = """
            SELECT COUNT(*) as invalid_docs
            FROM [Bienes_01_BENEFICIARIOS]
            WHERE LEN(documento) < 7 OR documento LIKE '%[^0-9]%'
            """
            invalid_docs = sqlserver.execute_query(doc_query)['invalid_docs'].iloc[0]
            if invalid_docs > 0:
                issues.append(f"{invalid_docs} documentos inválidos")
        
        elif table_name == 'Bienes_03_CONTRATOS':
            # Verificar fechas inconsistentes
            date_query = """
            SELECT COUNT(*) as bad_dates
            FROM [Bienes_03_CONTRATOS]
            WHERE desde > hasta OR fechafirma > GETDATE()
            """
            bad_dates = sqlserver.execute_query(date_query)['bad_dates'].iloc[0]
            if bad_dates > 0:
                issues.append(f"{bad_dates} fechas inconsistentes")
        
        elif table_name == 'Bienes_04_PLAN_DE_PAGOS':
            # Verificar montos negativos o fechas futuras irreales
            amount_query = """
            SELECT COUNT(*) as bad_amounts
            FROM [Bienes_04_PLAN_DE_PAGOS]
            WHERE total < 0 OR vencimiento > DATEADD(year, 10, GETDATE())
            """
            bad_amounts = sqlserver.execute_query(amount_query)['bad_amounts'].iloc[0]
            if bad_amounts > 0:
                issues.append(f"{bad_amounts} montos/fechas sospechosas")
        
    except Exception as e:
        issues.append(f"Error verificando: {e}")
    
    return '; '.join(issues) if issues else None

def generate_health_report():
    """Genera un reporte completo de salud"""
    logger = logging.getLogger(__name__)
    
    logger.info("📄 GENERANDO REPORTE DE SALUD COMPLETO")
    logger.info("=" * 50)
    
    # Ejecutar verificación completa
    is_healthy = verify_all_bienes_tables()
    
    # Generar archivo de reporte
    from datetime import datetime
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_file = f"health_report_{timestamp}.log"
    
    try:
        # Re-ejecutar con logging a archivo
        file_handler = logging.FileHandler(report_file, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        
        file_logger = logging.getLogger('health_report')
        file_logger.addHandler(file_handler)
        file_logger.setLevel(logging.INFO)
        
        # Re-ejecutar verificación para el archivo
        verify_all_bienes_tables()
        
        logger.info(f"📄 Reporte guardado en: {report_file}")
        
    except Exception as e:
        logger.warning(f"No se pudo generar archivo de reporte: {e}")
    
    return is_healthy

def main():
    """Función principal"""
    setup_logging()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command in ['--help', '-h']:
            print("""
🏥 VERIFICACIÓN DE SALUD - TODAS LAS TABLAS BIENES

Verifica la integridad y salud de todas las tablas principales:
- Bienes_01_BENEFICIARIOS
- Bienes_02_CARTERAS  
- Bienes_03_CONTRATOS
- Bienes_04_PLAN_DE_PAGOS

COMANDOS:
    python verify_tables_health.py              # Verificación completa
    python verify_tables_health.py --report     # Generar reporte a archivo
    
VERIFICACIONES INCLUIDAS:
- Conteo de registros
- Detección de duplicados por campos clave
- Campos críticos nulos o vacíos
- Validaciones específicas por tabla
- Recomendaciones de acción

INTERPRETACIÓN DE RESULTADOS:
✅ = Sin problemas detectados
⚠️  = Problemas menores que requieren atención  
❌ = Problemas críticos que requieren acción inmediata
🔧 = Tabla requiere mantenimiento

FLUJO RECOMENDADO:
1. python verify_tables_health.py                    # Ver estado general
2. python clean_all_duplicates.py --analyze          # Analizar duplicados
3. python clean_all_duplicates.py                    # Limpiar si necesario
4. python verify_tables_health.py                    # Verificar mejora
            """)
            return
            
        elif command == '--report':
            generate_health_report()
        else:
            logging.getLogger(__name__).error(f"Comando desconocido: {command}")
    else:
        # Verificación estándar
        verify_all_bienes_tables()

if __name__ == '__main__':
    main()