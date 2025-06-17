import os
import oracledb
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.settings import settings



# Directorio donde está oci.dll
#oracledb.init_oracle_client(lib_dir=r"C:\oracle\instantclient_23_7")
oracledb.init_oracle_client(lib_dir=os.environ.get("ORACLE_CLIENT_LIB_DIR", "/opt/oracle/instantclient"))

# Construye el DSN con makedsn
dsn = oracledb.makedsn(
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    service_name=settings.DB_SERVICE
)

# Crea el engine usando oracle+oracledb (modo thick)
engine = create_engine(
    f"oracle+oracledb://{settings.DB_USER}:{settings.DB_PASS}@{dsn}",
    echo=False
)
SessionLocal = sessionmaker(bind=engine)