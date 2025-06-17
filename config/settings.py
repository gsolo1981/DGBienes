import os
from dotenv import load_dotenv

"""
# Perfil: 'default' o 'sigaf'
APP_ENV = os.getenv('APP_ENV', 'default').lower()

# Cargo primero el default, luego sobreescribo si hay perfil específico
load_dotenv('.env.default')
env_path = f'.env.{APP_ENV}'
if os.path.exists(env_path):
    load_dotenv(env_path, override=True)
"""

APP_ENV = os.getenv('APP_ENV', 'default').lower()
load_dotenv('.env.default')                      # siempre
load_dotenv(f'.env.{APP_ENV}', override=True)    # solo si APP_ENV está seteado

class Settings:
    DB_HOST:   str = os.getenv('DB_HOST')
    DB_PORT:   str = os.getenv('DB_PORT')
    DB_SERVICE:str = os.getenv('DB_SERVICE')
    DB_USER:   str = os.getenv('DB_USER')
    DB_PASS:   str = os.getenv('DB_PASS')
    PATH_SQL:  str = os.getenv('PATH_SQL', 'sql')
    FILE_XLSX: str = os.getenv('FILE_XLSX', 'output')

settings = Settings()
