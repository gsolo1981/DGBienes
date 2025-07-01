import os
import logging
from typing import Dict, List, Optional
from config.settings import settings

class EnvironmentManager:
    """
    Gestor de configuraciones específicas por entorno/schema
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.current_env = settings.APP_ENV.lower()
        
    def get_environment_info(self) -> Dict:
        """Retorna información del entorno actual"""
        env_configs = {
            'bienes': {
                'name': 'Bienes y Concesiones',
                'description': 'Sistema de gestión de bienes y concesiones',
                'schemas': ['bienes', 'fade'],
                'main_tables': ['Bienes_01_BENEFICIARIOS', 'Concesiones_01_BENEFICIARIOS'],
                'sql_path': 'sql/Bienes',
                'incremental_strategy': 'date_based',
                'priority': 'high'
            },
            'sigaf': {
                'name': 'SIGAF - Sistema Integrado de Gestión',
                'description': 'Sistema Integrado de Gestión Administrativa y Financiera',
                'schemas': ['slu'],
                'main_tables': ['[01_RELACION_BAC_SIGAF]', '[02_SPR_RENGLONES]'],
                'sql_path': 'sql/sigaf',
                'incremental_strategy': 'date_based',
                'priority': 'high'
            },
            'sigaf_devengado': {
                'name': 'SIGAF Devengados',
                'description': 'Módulo de devengados del sistema SIGAF',
                'schemas': ['slu'],
                'main_tables': ['[01_DEVENGADO_v2]'],
                'sql_path': 'sql/Sigaf_Devengados',
                'incremental_strategy': 'date_based',
                'priority': 'medium'
            }
        }
        
        return env_configs.get(self.current_env, {})
    
    def get_sql_files_for_environment(self) -> List[str]:
        """Retorna la lista de archivos SQL para el entorno actual"""
        env_info = self.get_environment_info()
        sql_path = env_info.get('sql_path', settings.PATH_SQL)
        
        sql_files = []
        base_path = os.path.join(os.path.dirname(__file__), '..', sql_path)
        
        if os.path.exists(base_path):
            for root, dirs, files in os.walk(base_path):
                for file in files:
                    if file.lower().endswith('.sql'):
                        sql_files.append(file)
        
        self.logger.info(f"Encontrados {len(sql_files)} archivos SQL para entorno '{self.current_env}'")
        return sql_files
    
    def validate_environment_config(self) -> Dict[str, bool]:
        """Valida la configuración del entorno actual"""
        validation = {
            'oracle_config': False,
            'sqlserver_config': False,
            'sql_files_exist': False,
            'mappings_defined': False
        }
        
        # Validar configuración Oracle
        if all([settings.DB_HOST, settings.DB_USER, settings.DB_PASS, settings.DB_SERVICE]):
            validation['oracle_config'] = True
        
        # Validar configuración SQL Server
        if all([settings.SQLSERVER_HOST, settings.SQLSERVER_USER, settings.SQLSERVER_PASS]):
            validation['sqlserver_config'] = True
        
        # Validar existencia de archivos SQL
        sql_files = self.get_sql_files_for_environment()
        validation['sql_files_exist'] = len(sql_files) > 0
        
        # Validar mapeos definidos
        from services.sync_service import SyncService
        sync_service = SyncService()
        sync_config = sync_service.sync_config
        validation['mappings_defined'] = len(sync_config) > 0
        
        return validation
    
    def get_environment_summary(self) -> str:
        """Retorna un resumen del entorno actual"""
        env_info = self.get_environment_info()
        validation = self.validate_environment_config()
        sql_files = self.get_sql_files_for_environment()
        
        summary = f"""
=== CONFIGURACIÓN DE ENTORNO ===
Entorno Activo: {self.current_env.upper()}
Nombre: {env_info.get('name', 'No definido')}
Descripción: {env_info.get('description', 'No disponible')}

Configuración Oracle: {'✅' if validation['oracle_config'] else '❌'}
- Host: {settings.DB_HOST}
- Usuario: {settings.DB_USER}
- Servicio: {settings.DB_SERVICE}

Configuración SQL Server: {'✅' if validation['sqlserver_config'] else '❌'}
- Host: {settings.SQLSERVER_HOST}
- Base de Datos: {settings.SQLSERVER_DB}
- Usuario: {settings.SQLSERVER_USER}

Archivos SQL: {'✅' if validation['sql_files_exist'] else '❌'}
- Ruta: {env_info.get('sql_path', settings.PATH_SQL)}
- Cantidad: {len(sql_files)}

Mapeos Definidos: {'✅' if validation['mappings_defined'] else '❌'}

Configuración de Sincronización:
- Modo: {settings.SYNC_MODE}
- SQL Server habilitado: {settings.SYNC_TO_SQLSERVER}
- Excel habilitado: {settings.EXPORT_TO_EXCEL}
"""
        return summary
    
    def switch_environment(self, new_env: str) -> bool:
        """
        Cambia el entorno activo (principalmente para testing)
        En producción, esto se hace via variable de entorno APP_ENV
        """
        valid_envs = ['default', 'sigaf', 'sigaf_devengado']
        
        if new_env.lower() not in valid_envs:
            self.logger.error(f"Entorno inválido: {new_env}. Válidos: {valid_envs}")
            return False
        
        self.current_env = new_env.lower()
        self.logger.info(f"Entorno cambiado a: {self.current_env}")
        return True
    
    def get_recommended_sync_strategy(self) -> Dict:
        """Retorna la estrategia de sincronización recomendada por entorno"""
        strategies = {
            'bienes': {
                'initial_load': 'full',
                'daily_sync': 'incremental',
                'batch_size': 1000,
                'retry_attempts': 3,
                'schedule': '0 */6 * * *',  # Cada 6 horas
                'priority_tables': ['Bienes_01_BENEFICIARIOS', 'Bienes_03_CONTRATOS']
            },
            'sigaf': {
                'initial_load': 'full',
                'daily_sync': 'incremental',
                'batch_size': 5000,  # SIGAF maneja más volumen
                'retry_attempts': 5,
                'schedule': '0 */4 * * *',  # Cada 4 horas (más frecuente)
                'priority_tables': ['[01_RELACION_BAC_SIGAF]', '[10_FACTURAS_OP_PAGOS]']
            },
            'sigaf_devengado': {
                'initial_load': 'full',
                'daily_sync': 'incremental',
                'batch_size': 2000,
                'retry_attempts': 3,
                'schedule': '0 */8 * * *',  # Cada 8 horas
                'priority_tables': ['[01_DEVENGADO_v2]']
            }
        }
        
        return strategies.get(self.current_env, strategies['default'])
    
    def log_environment_status(self):
        """Registra el estado del entorno en los logs"""
        self.logger.info(f"=== ESTADO DEL ENTORNO {self.current_env.upper()} ===")
        
        env_info = self.get_environment_info()
        self.logger.info(f"Nombre: {env_info.get('name')}")
        self.logger.info(f"Esquemas Oracle: {env_info.get('schemas', [])}")
        
        validation = self.validate_environment_config()
        for check, status in validation.items():
            status_icon = "✅" if status else "❌"
            self.logger.info(f"{check}: {status_icon}")
        
        strategy = self.get_recommended_sync_strategy()
        self.logger.info(f"Estrategia recomendada: {strategy['daily_sync']}")
        self.logger.info(f"Batch size: {strategy['batch_size']}")
        self.logger.info(f"Programación: {strategy['schedule']}")
        
    def get_environment_specific_filters(self) -> Dict:
        """
        Retorna filtros específicos por entorno para optimizar consultas
        """
        filters = {
            'bienes': {
                # Filtros para Bienes y Concesiones
                'date_range_days': 365,  # Último año por defecto
                'status_filters': ['activo = \'S\''],  # Solo registros activos
                'exclude_test_data': True
            },
            'sigaf': {
                # Filtros para SIGAF
                'date_range_days': 180,  # Últimos 6 meses
                'fiscal_year_filter': 'aa_ocompra >= 2023',
                'entity_filters': ['c_juris = 50'],  # Jurisdicción específica
                'status_filters': ['e_ocompra = \'A\'']  # Solo autorizadas
            },
            'sigaf_devengado': {
                # Filtros para Devengados
                'date_range_days': 90,  # Últimos 3 meses
                'fiscal_year_filter': 'aa_precepcion >= 2023',
                'amount_threshold': 'NVL(i_total,0) > 0',
                'status_filters': ['e_formulario = \'A\'']
            }
        }
        
        return filters.get(self.current_env, {})
    
    @staticmethod
    def list_available_environments() -> List[Dict]:
        """Lista todos los entornos disponibles"""
        return [
            {
                'env': 'bienes',
                'name': 'Bienes ',
                'description': 'Gestión de bienes inmuebles',
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