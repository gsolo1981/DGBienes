import os
from adapters.db_adapter import SessionLocal
import pandas as pd
from config.settings import settings

# Directorios del proyecto
this_dir = os.path.dirname(__file__)
BASE_DIR = os.path.abspath(os.path.join(this_dir, '..'))
SQL_DIR = os.path.join(BASE_DIR, settings.PATH_SQL)
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')

class QueryService:
    def __init__(self):
        # Asegura carpeta de salida
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        self.session = SessionLocal()

    def run_queries(self):
        # Nombre y ruta del archivo de Excel
        file_name = settings.FILE_XLSX
        if not file_name.lower().endswith('.xlsx'):
            file_name += '.xlsx'
        output_path = os.path.join(OUTPUT_DIR, file_name)

        # Escribe el Excel
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            for file in os.listdir(SQL_DIR):
                if not file.lower().endswith('.sql'):
                    continue

                path = os.path.join(SQL_DIR, file)
                with open(path, 'r', encoding='utf-8') as f:
                    sql = f.read().strip()
                    if sql.endswith(';'):
                        sql = sql[:-1]

                sheet_name = os.path.splitext(file)[0][:31]
                df = pd.read_sql_query(sql, self.session.bind)
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                print(f"→ Hoja '{sheet_name}' generada ({len(df)} filas)")

        # Cierra sesión y muestra ruta final
        self.session.close()
        print(f"✅ Excel generado en: {output_path}")