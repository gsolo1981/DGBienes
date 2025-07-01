#!/usr/bin/env python3
"""
Herramienta para contar registros en SQL Server antes/después de sincronización
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

def count_all_tables():
    """Cuenta registros en todas las tablas del entorno"""
    logger = logging.getLogger(__name__)
    
    # Mapeo de tablas por entorno
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
    
    tables = tables_by_env.get(settings.APP_ENV.lower(), [])
    
    if not tables:
        logger.error(f"No hay tablas configuradas para el entorno: {settings.APP_ENV}")
        return
    
    try:
        sqlserver = SQLServerAdapter()
        
        if not sqlserver.engine:
            logger.error("SQL Server no disponible")
            return
        
        logger.info(f"📊 CONTEO DE REGISTROS - ENTORNO: {settings.APP_ENV.upper()}")
        logger.info("=" * 70)
        
        total_records = 0
        existing_tables = 0
        
        for table_name in tables:
            clean_table_name = table_name.replace('[', '').replace(']', '')
            
            try:
                if sqlserver.table_exists(clean_table_name):
                    count_query = f"SELECT COUNT(*) as count FROM [{clean_table_name}]"
                    result = sqlserver.execute_query(count_query)
                    record_count = result['count'].iloc[0]
                    
                    # Formatear nombre para display
                    if 'Bienes_' in clean_table_name:
                        display_name = clean_table_name.replace('Bienes_', '').replace('_', ' ')
                    elif 'Concesiones_' in clean_table_name:
                        display_name = clean_table_name.replace('Concesiones_', '').replace('_', ' ')
                    else:
                        display_name = clean_table_name.replace('_', ' ')
                    
                    logger.info(f"✅ {display_name:30} | {record_count:>8,} registros")
                    total_records += record_count
                    existing_tables += 1
                else:
                    logger.info(f"❌ {clean_table_name:30} | NO EXISTE")
                    
            except Exception as e:
                logger.error(f"❌ {clean_table_name:30} | ERROR: {e}")
        
        logger.info("-" * 70)
        logger.info(f"📋 RESUMEN: {existing_tables} tablas | {total_records:,} registros totales")
        logger.info("=" * 70)
        
        sqlserver.close()
        
    except Exception as e:
        logger.error(f"Error general: {e}")

def count_specific_table(table_name):
    """Cuenta registros en una tabla específica"""
    logger = logging.getLogger(__name__)
    
    try:
        sqlserver = SQLServerAdapter()
        
        clean_table_name = table_name.replace('[', '').replace(']', '')
        
        if sqlserver.table_exists(clean_table_name):
            count_query = f"SELECT COUNT(*) as count FROM [{clean_table_name}]"
            result = sqlserver.execute_query(count_query)
            record_count = result['count'].iloc[0]
            
            logger.info(f"📊 {clean_table_name}: {record_count:,} registros")
            return record_count
        else:
            logger.warning(f"❌ Tabla {clean_table_name} no existe")
            return 0
            
    except Exception as e:
        logger.error(f"Error contando {table_name}: {e}")
        return 0

def compare_before_after():
    """Compara conteos antes y después de una sincronización"""
    logger = logging.getLogger(__name__)
    
    logger.info("📊 COMPARACIÓN ANTES/DESPUÉS DE SINCRONIZACIÓN")
    logger.info("=" * 60)
    logger.info("Ejecuta este script ANTES y DESPUÉS de la sincronización")
    logger.info("para ver las diferencias.")
    logger.info("=" * 60)
    
    count_all_tables()

def show_help():
    """Muestra ayuda del comando"""
    help_text = """
🔧 HERRAMIENTA DE CONTEO DE REGISTROS

USO:
    python count_records.py                    # Contar todas las tablas
    python count_records.py tabla_especifica   # Contar tabla específica
    python count_records.py --help            # Mostrar esta ayuda
    python count_records.py --compare         # Comparar antes/después

EJEMPLOS:
    python count_records.py
    python count_records.py Bienes_02_CARTERAS
    python count_records.py 01_RELACION_BAC_SIGAF

ENTORNOS SOPORTADOS:
    - bienes
    - concesiones  
    - sigaf
    - sigaf_devengado

CONFIGURACIÓN:
    El entorno se configura con la variable APP_ENV en .env.{entorno}
    o se puede especificar: set APP_ENV=bienes
    """
    print(help_text)

def main():
    """Función principal"""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        
        if arg in ['--help', '-h', 'help']:
            show_help()
        elif arg in ['--compare', '-c', 'compare']:
            compare_before_after()
        else:
            # Contar tabla específica
            table_name = sys.argv[1]
            count_specific_table(table_name)
    else:
        # Contar todas las tablas del entorno
        count_all_tables()

if __name__ == '__main__':
    main()