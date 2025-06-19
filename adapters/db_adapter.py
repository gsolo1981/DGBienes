import os
import oracledb
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from config.settings import settings
import logging

# Configurar logging para diagnosticar problemas
logger = logging.getLogger(__name__)

# Variables globales para el adaptador
engine = None
SessionLocal = None

def initialize_oracle_adapter():
    """Inicializa el adaptador Oracle solo cuando sea necesario"""
    global engine, SessionLocal
    
    if engine is not None:
        return True  # Ya inicializado
    
    try:
        # Verificar configuración básica
        if not all([settings.DB_HOST, settings.DB_USER, settings.DB_PASS, settings.DB_SERVICE]):
            logger.warning("Configuración Oracle incompleta. Variables faltantes:")
            if not settings.DB_HOST: logger.warning("  - DB_HOST no configurado")
            if not settings.DB_USER: logger.warning("  - DB_USER no configurado") 
            if not settings.DB_PASS: logger.warning("  - DB_PASS no configurado")
            if not settings.DB_SERVICE: logger.warning("  - DB_SERVICE no configurado")
            return False
        
        # Inicializar Oracle Client
        try:
            # Usar la ruta específica que ya tienes configurada
            oracle_client_path = r"C:\oracle\instantclient_23_7"
            if os.path.exists(oracle_client_path):
                oracledb.init_oracle_client(lib_dir=oracle_client_path)
                logger.info(f"Oracle Client inicializado desde: {oracle_client_path}")
            else:
                # Fallback a variable de entorno o ruta por defecto
                oracle_client_path = os.environ.get("ORACLE_CLIENT_LIB_DIR")
                if oracle_client_path and os.path.exists(oracle_client_path):
                    oracledb.init_oracle_client(lib_dir=oracle_client_path)
                    logger.info(f"Oracle Client inicializado desde variable de entorno: {oracle_client_path}")
                else:
                    # Intentar sin especificar ruta (Oracle Client en PATH)
                    oracledb.init_oracle_client()
                    logger.info("Oracle Client inicializado desde PATH del sistema")
                    
        except Exception as e:
            if "DPI-1047" in str(e):
                logger.error("❌ Oracle Client no encontrado. Soluciones:")
                logger.error("  1. Instala Oracle Instant Client 64-bit")
                logger.error("  2. Verifica que existe: C:\\oracle\\instantclient_23_7")
                logger.error("  3. O configura ORACLE_CLIENT_LIB_DIR")
            else:
                logger.error(f"Error inicializando Oracle Client: {e}")
            return False
        
        # Construir DSN
        try:
            dsn = oracledb.makedsn(
                host=settings.DB_HOST,
                port=int(settings.DB_PORT),
                service_name=settings.DB_SERVICE
            )
            logger.info(f"DSN creado: {settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_SERVICE}")
        except Exception as e:
            logger.error(f"Error creando DSN: {e}")
            return False
        
        # Crear engine
        try:
            connection_string = f"oracle+oracledb://{settings.DB_USER}:{settings.DB_PASS}@{dsn}"
            engine = create_engine(connection_string, echo=False)
            SessionLocal = sessionmaker(bind=engine)
            
            # Probar conexión
            with engine.connect() as conn:
                result = conn.execute(text("SELECT 'Oracle conectado' FROM dual"))
                test_result = result.fetchone()[0]
                logger.info(f"✅ Conexión Oracle exitosa: {test_result}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error conectando a Oracle: {e}")
            engine = None
            SessionLocal = None
            return False
            
    except Exception as e:
        logger.error(f"Error general inicializando Oracle adapter: {e}")
        return False

def get_oracle_session():
    """Obtiene una sesión Oracle, inicializando si es necesario"""
    if not initialize_oracle_adapter():
        raise Exception("No se pudo inicializar el adaptador Oracle. Revisa la configuración.")
    
    if SessionLocal is None:
        raise Exception("SessionLocal no disponible. Problema de configuración Oracle.")
    
    return SessionLocal()

def is_oracle_available():
    """Verifica si Oracle está disponible sin lanzar excepciones"""
    return initialize_oracle_adapter()

# Intentar inicialización automática solo si la configuración está completa
if settings.is_configured():
    logger.info("Configuración Oracle detectada. Inicializando adaptador...")
    initialize_oracle_adapter()
else:
    logger.info("Configuración Oracle incompleta. Adaptador en modo lazy loading.")