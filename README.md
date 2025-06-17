# Proyecto DGBienes – Exportación de Consultas Oracle a Excel

Este proyecto ejecuta scripts SQL organizados en subdirectorios y exporta sus resultados a un archivo Excel, generando una pestaña por cada script.

---

## 📝 Descripción

- Recorre recursivamente la carpeta `sql/`, incluyendo subcarpetas, para encontrar todos los ficheros `.sql`.
- Ejecuta cada script en una base Oracle usando SQLAlchemy y el driver `python-oracledb` (modo thick).
- Exporta cada resultado a una hoja de un archivo Excel dentro de `output/`, nombrando la pestaña según la ruta relativa del script.

---

## 🚀 Requisitos previos

1. **Python 3.8+**
2. **Oracle Instant Client** (64-bit) instalado y accesible:
   - Añade la carpeta con `oci.dll` a la variable de entorno `PATH`, 
     o especifica su ubicación en `adapters/db_adapter.py`:
     ```python
     oracledb.init_oracle_client(lib_dir=r"C:\ruta\instantclient_xx_xx")
     ```
3. Conexión válida a Oracle (host, puerto, servicio/SID, usuario y contraseña).

---

## 📦 Instalación

```bash
# Clonar o descargar el proyecto
git clone <repo_url> dg-bienes-excel
cd dg-bienes-excel

# Crear y activar entorno virtual (recomendado)
python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows (PowerShell):
.venv\Scripts\Activate.ps1 o 
.venv\Scripts\activate.bat

# Instalar dependencias
pip install -r requirements.txt
```

---

## ⚙️ Configuración

En la raíz del proyecto encontrarás múltiples archivos de entorno (`.env.default`, `.env.sigaf`, `.env.prod`(futuro)), etc.). Cada uno define:

```dotenv
DB_HOST=...
DB_PORT=...
DB_SERVICE=...
DB_USER=...
DB_PASS=...
PATH_SQL=sql       # Carpeta raíz de scripts
FILE_XLSX=NombreSalida
```

### Seleccionar perfil de entorno
También puedes exportar la variable `APP_ENV`:
```bash
#Para SIGAF
$Env:APP_ENV = 'sigaf' # Windows PowerShell
#Para SIGAF Devengados
$Env:APP_ENV = 'sigaf_devengado' # Windows PowerShell
python main.py
#Para SGSIR
$Env:APP_ENV = 'default'
python main.py
```

---

## 📂 Estructura de directorios

```
project_root/
├── adapters/
│   └── db_adapter.py      # Conexión Oracle + SQLAlchemy
├── config/
│   └── settings.py        # Lógica para cargar el .env correcto
├── services/
│   └── query_service.py   # Lógica de ejecución recursiva y exportación
├── sql/                   # Carpeta raíz de scripts
│   ├── beneficiarios/
│   │   └── beneficiarios.sql
│   ├── contratos/
│   │   └── contratos.sql
│   └── ...                # Más subdirectorios con scripts
├── output/                # Carpeta destino de los archivos .xlsx
├── .env.default           # Perfil por defecto (no versionar)
├── .env.sigaf             # Perfil sigaf (no versionar)
├── .env.prod              # Perfil producción (no versionar)
├── main.py                # Punto de entrada y selección de entorno
├── requirements.txt       # Dependencias Python
└── README.md              # Este archivo
```

---

## ▶️ Uso

Con entorno activado:

```bash
# Usar perfil por defecto
python main.py

# Usar perfil SIGAF
python main.py --env sigaf

# Usar perfil default
python main.py --env default
```

- El resultado será `output/<FILE_XLSX>.xlsx`.
- Cada pestaña corresponderá al script SQL con su ruta relativa (subcarpeta_nombre).

---

## 📄 Licencia

Este proyecto está bajo la **licencia MIT**. Ajusta según tus necesidades.
