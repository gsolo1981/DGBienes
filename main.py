import argparse
import logging
import sys
from services.query_service import QueryService
from services.sync_service import SyncService
from config.settings import settings

def setup_logging():
    """Configura el sistema de logging"""
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('dgbienes.log', encoding='utf-8')
        ]
    )

def list_environments():
    """Lista todos los entornos disponibles"""
    envs = [
        {
            'env': 'default',
            'name': 'Bienes y Concesiones',
            'description': 'Gestión de bienes inmuebles y concesiones',
            'schemas': ['bienes', 'fade2'],
            'active': True
        },
        {
            'env': 'sigaf',
            'name': 'SIGAF',
            'description': 'Sistema Integrado de Gestión Administrativa',
            'schemas': ['slu'],
            'active': True
        },
        {
            'env': 'sigaf_devengado',
            'name': 'SIGAF Devengados',
            'description': 'Módulo de devengados y facturación',
            'schemas': ['slu'],
            'active': True
        }
    ]
    
    print("\n=== ENTORNOS DISPONIBLES ===")
    for env in envs:
        status = "🟢 ACTIVO" if env['active'] else "🔴 INACTIVO"
        print(f"{env['env']:15} | {env['name']:25} | {status}")
        print(f"{'':15} | {env['description']:25} | Schemas: {', '.join(env['schemas'])}")
        print("-" * 80)
    print("\n💡 Para usar un entorno específico:")
    print("   - Ejecuta: set APP_ENV={entorno}  (Windows)")
    print("   - O usa: python main.py --env {entorno}")
    print("\n📋 Comandos útiles:")
    print("   python main.py --info                    # Ver configuración actual")
    print("   python main.py --status                  # Ver estado de sincronización")
    print("   python main.py --mode excel              # Solo generar Excel")
    print("   python main.py --mode both               # Excel + SQL Server")

def show_environment_info():
    """Muestra información del entorno actual"""
    print(f"\n=== INFORMACIÓN DEL ENTORNO ===")
    print(f"Entorno Activo: {settings.APP_ENV.upper()}")
    
    # Verificar configuración Oracle
    oracle_config = "✅ COMPLETA" if settings.is_configured() else "❌ INCOMPLETA"
    print(f"Configuración Oracle: {oracle_config}")
    
    if not settings.is_configured():
        missing = settings.get_missing_config()
        print(f"Variables faltantes: {', '.join(missing)}")
    else:
        print(f"  Host: {settings.DB_HOST}")
        print(f"  Usuario: {settings.DB_USER}")
        print(f"  Servicio: {settings.DB_SERVICE}")
    
    # Configuración SQL Server
    sqlserver_config = "✅ CONFIGURADO" if all([settings.SQLSERVER_HOST, settings.SQLSERVER_USER]) else "❌ INCOMPLETO"
    print(f"Configuración SQL Server: {sqlserver_config}")
    
    if settings.SQLSERVER_HOST and settings.SQLSERVER_USER:
        print(f"  Host: {settings.SQLSERVER_HOST}")
        print(f"  Usuario: {settings.SQLSERVER_USER}")
        print(f"  Base de Datos: {settings.SQLSERVER_DB}")
    
    # Configuración de archivos
    print(f"\nConfiguración de Archivos:")
    print(f"  Carpeta SQL: {settings.PATH_SQL}")
    print(f"  Archivo Excel: {settings.FILE_XLSX}")
    
    # Configuración de sincronización
    print(f"\nConfiguración de Sincronización:")
    print(f"  Modo: {settings.SYNC_MODE}")
    print(f"  SQL Server habilitado: {'✅ SÍ' if settings.SYNC_TO_SQLSERVER else '❌ NO'}")
    print(f"  Excel habilitado: {'✅ SÍ' if settings.EXPORT_TO_EXCEL else '❌ NO'}")

def main():
    parser = argparse.ArgumentParser(description='DGBienes - Exportación y Sincronización Multi-Schema')
    parser.add_argument('--env', type=str, 
                       choices=['default', 'sigaf', 'sigaf_devengado'],
                       help='Perfil de entorno (se puede configurar via APP_ENV también)')
    parser.add_argument('--mode', type=str, choices=['excel', 'sqlserver', 'both'], 
                       default='both', help='Modo de operación')
    parser.add_argument('--sync-mode', type=str, choices=['full', 'incremental'], 
                       default='incremental', help='Modo de sincronización')
    parser.add_argument('--tables', type=str, nargs='*', 
                       help='Sincronizar tablas específicas')
    parser.add_argument('--status', action='store_true', 
                       help='Mostrar estado de sincronización')
    parser.add_argument('--info', action='store_true',
                       help='Mostrar información del entorno actual')
    parser.add_argument('--list-envs', action='store_true',
                       help='Listar entornos disponibles')
    
    args = parser.parse_args()
    
    # Configurar logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Listar entornos disponibles (no requiere DB)
    if args.list_envs:
        list_environments()
        return
    
    # Mostrar información del entorno
    if args.info:
        show_environment_info()
        return
    
    # Verificar configuración básica para otros comandos
    if not settings.is_configured():
        print("❌ ERROR: Configuración Oracle incompleta")
        print("\n🔧 SOLUCIÓN:")
        missing = settings.get_missing_config()
        print(f"Variables faltantes en .env.default: {', '.join(missing)}")
        print("\n💡 Usa 'python main.py --info' para ver detalles")
        return
    
    logger.info(f"=== DGBienes Multi-Schema Iniciado ===")
    logger.info(f"Entorno: {settings.APP_ENV.upper()}")
    logger.info(f"Modo: {args.mode}")
    logger.info(f"Sincronización: {args.sync_mode}")
    
    try:
        # Mostrar estado si se solicita
        if args.status:
            try:
                sync_service = SyncService()
                status = sync_service.get_sync_status()
                
                print(f"\n=== ESTADO DE SINCRONIZACIÓN - {settings.APP_ENV.upper()} ===")
                print(f"Entorno: Bienes y Concesiones")
                print("-" * 60)
                
                for table, info in status.items():
                    if info.get('exists', False):
                        print(f"✅ {table}: {info['count']:,} registros")
                        if info.get('last_update'):
                            print(f"   📅 Última actualización: {info['last_update']}")
                    else:
                        error_msg = info.get('error', 'No existe')
                        print(f"❌ {table}: {error_msg}")
                
                sync_service.close()
            except Exception as e:
                logger.error(f"Error obteniendo estado: {e}")
                print(f"❌ Error verificando estado: {e}")
            return
        
        # Exportación a Excel
        if args.mode in ['excel', 'both'] and settings.EXPORT_TO_EXCEL:
            logger.info(f"Iniciando exportación a Excel para entorno {settings.APP_ENV}...")
            try:
                query_service = QueryService()
                query_service.run_queries()
                logger.info("✅ Exportación a Excel completada")
            except Exception as e:
                logger.error(f"Error en exportación Excel: {e}")
                print(f"❌ Error exportando a Excel: {e}")
        
        # Sincronización a SQL Server
        if args.mode in ['sqlserver', 'both'] and settings.SYNC_TO_SQLSERVER:
            logger.info(f"Iniciando sincronización a SQL Server para entorno {settings.APP_ENV}...")
            try:
                sync_service = SyncService()
                
                if args.tables:
                    # Sincronizar tablas específicas
                    total_synced, errors = sync_service.sync_specific_tables(
                        args.tables, 
                        args.sync_mode
                    )
                else:
                    # Sincronizar todas las tablas del entorno
                    total_synced, errors = sync_service.sync_all_tables(args.sync_mode)
                
                logger.info(f"✅ Sincronización completada: {total_synced:,} registros")
                
                if errors:
                    logger.warning(f"⚠️  Se encontraron {len(errors)} errores durante la sincronización")
                    for error in errors:
                        logger.warning(f"  - {error}")
                
                sync_service.close()
            except Exception as e:
                logger.error(f"Error en sincronización SQL Server: {e}")
                print(f"❌ Error sincronizando a SQL Server: {e}")
        
        logger.info("=== Proceso completado exitosamente ===")
        
    except Exception as e:
        logger.error(f"❌ Error en el proceso principal: {e}")
        logger.error("Para más detalles, revisa el archivo dgbienes.log")
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()