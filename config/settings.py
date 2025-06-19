import os
from dotenv import load_dotenv

APP_ENV = os.getenv('APP_ENV', 'default').lower()

# Solo cargar .env si existe
env_default_path = '.env.default'
env_specific_path = f'.env.{APP_ENV}'

if os.path.exists(env_default_path):
    load_dotenv(env_default_path)
    print(f"✅ Cargado: {env_default_path}")
else:
    print(f"⚠️  Archivo {env_default_path} no encontrado")

if os.path.exists(env_specific_path) and env_specific_path != env_default_path:
    load_dotenv(env_specific_path, override=True)
    print(f"✅ Cargado: {env_specific_path}")
elif APP_ENV != 'default':
    print(f"⚠️  Archivo {env_specific_path} no encontrado")

class Settings:
    # Configuración Oracle existente
    DB_HOST:   str = os.getenv('DB_HOST', '')
    DB_PORT:   str = os.getenv('DB_PORT', '1521')
    DB_SERVICE:str = os.getenv('DB_SERVICE', '')
    DB_USER:   str = os.getenv('DB_USER', '')
    DB_PASS:   str = os.getenv('DB_PASS', '')
    
    # Configuración SQL Server
    SQLSERVER_HOST: str = os.getenv('SQLSERVER_HOST', '')
    SQLSERVER_DB:   str = os.getenv('SQLSERVER_DB', 'DGBIDB')
    SQLSERVER_USER: str = os.getenv('SQLSERVER_USER', '')
    SQLSERVER_PASS: str = os.getenv('SQLSERVER_PASS', '')
    SQLSERVER_DRIVER: str = os.getenv('SQLSERVER_DRIVER', '{ODBC Driver 17 for SQL Server}')
    
    # Configuración general
    PATH_SQL:  str = os.getenv('PATH_SQL', 'sql')
    FILE_XLSX: str = os.getenv('FILE_XLSX', 'output')
    
    # Configuración de sincronización
    SYNC_MODE: str = os.getenv('SYNC_MODE', 'incremental')  # 'full' o 'incremental'
    SYNC_TO_SQLSERVER: bool = os.getenv('SYNC_TO_SQLSERVER', 'false').lower() == 'true'
    EXPORT_TO_EXCEL: bool = os.getenv('EXPORT_TO_EXCEL', 'true').lower() == 'true'
    
    # Configuración de logging
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    
    # Entorno activo (para configuraciones específicas)
    APP_ENV: str = APP_ENV

    def is_configured(self) -> bool:
        """Verifica si la configuración mínima está presente"""
        return bool(self.DB_HOST and self.DB_USER and self.DB_PASS and self.DB_SERVICE)
    
    def get_missing_config(self) -> list:
        """Retorna lista de configuraciones faltantes"""
        missing = []
        if not self.DB_HOST: missing.append('DB_HOST')
        if not self.DB_USER: missing.append('DB_USER') 
        if not self.DB_PASS: missing.append('DB_PASS')
        if not self.DB_SERVICE: missing.append('DB_SERVICE')
        return missing

settings = Settings()

# Mostrar estado de configuración al cargar
if __name__ != '__main__':  # Solo si no se ejecuta directamente
    if settings.is_configured():
        print(f"✅ Configuración Oracle completa para entorno: {APP_ENV}")
    else:
        print(f"⚠️  Configuración Oracle incompleta para entorno: {APP_ENV}")
        missing = settings.get_missing_config()
        print(f"   Variables faltantes: {', '.join(missing)}")