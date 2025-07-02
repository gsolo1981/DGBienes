# setup_hash_sync.py
# Script de instalación automática para funcionalidad de hash

import os
import sys
import shutil
import logging
from datetime import datetime

def setup_logging():
    """Configurar logging para la instalación"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('setup_hash_sync.log', encoding='utf-8')
        ]
    )

def create_backup():
    """Crear backup del proyecto actual"""
    logger = logging.getLogger(__name__)
    
    print("📦 CREANDO BACKUP DEL PROYECTO")
    print("=" * 50)
    
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_dir = f"backup_antes_hash_{timestamp}"
        
        # Crear directorio de backup
        os.makedirs(backup_dir, exist_ok=True)
        
        # Backup de archivos críticos
        files_to_backup = [
            'services/sync_service.py',
            '.env.bienes',
            'main.py'
        ]
        
        backup_count = 0
        for file_path in files_to_backup:
            if os.path.exists(file_path):
                # Crear directorio en backup si es necesario
                backup_file_path = os.path.join(backup_dir, file_path)
                backup_file_dir = os.path.dirname(backup_file_path)
                os.makedirs(backup_file_dir, exist_ok=True)
                
                # Copiar archivo
                shutil.copy2(file_path, backup_file_path)
                print(f"✅ Backup: {file_path}")
                backup_count += 1
            else:
                print(f"⚠️  Archivo no encontrado: {file_path}")
        
        print(f"✅ Backup completado: {backup_count} archivos en {backup_dir}")
        print("")
        return backup_dir
        
    except Exception as e:
        print(f"❌ Error creando backup: {e}")
        return None

def check_prerequisites():
    """Verificar prerequisitos"""
    logger = logging.getLogger(__name__)
    
    print("🔍 VERIFICANDO PREREQUISITOS")
    print("=" * 50)
    
    checks = {
        'sync_service.py existe': os.path.exists('services/sync_service.py'),
        '.env.bienes existe': os.path.exists('.env.bienes'),
        'main.py existe': os.path.exists('main.py'),
        'directorio sql/Bienes existe': os.path.exists('sql/Bienes'),
        'archivo SQL Beneficiarios existe': os.path.exists('sql/Bienes/Bienes_01_BENEFICIARIOS.sql')
    }
    
    all_ok = True
    for check, status in checks.items():
        icon = "✅" if status else "❌"
        print(f"{icon} {check}")
        if not status:
            all_ok = False
    
    if all_ok:
        print("✅ Todos los prerequisitos cumplidos")
    else:
        print("❌ Faltan prerequisitos. Verifica la estructura del proyecto.")
    
    print("")
    return all_ok

def install_hash_functionality():
    """Instalar la funcionalidad de hash"""
    logger = logging.getLogger(__name__)
    
    print("🔧 INSTALANDO FUNCIONALIDAD DE HASH")
    print("=" * 50)
    
    try:
        # Nota: En un entorno real, aquí copiarías los archivos actualizados
        # Por ahora, solo mostramos las instrucciones
        
        print("📝 Pasos a seguir:")
        print("1. Reemplazar services/sync_service.py con la nueva versión")
        print("2. Ejecutar add_row_hash_column.sql en SQL Server")
        print("3. Ejecutar test_hash_sync.py para verificar")
        print("")
        
        print("✅ Instrucciones de instalación mostradas")
        return True
        
    except Exception as e:
        print(f"❌ Error instalando funcionalidad: {e}")
        return False

def create_sql_script():
    """Crear script SQL para agregar columna hash"""
    logger = logging.getLogger(__name__)
    
    print("📄 CREANDO SCRIPT SQL")
    print("=" * 50)
    
    sql_content = """-- add_row_hash_column.sql
-- Script para agregar la columna row_hash a Bienes_01_BENEFICIARIOS

USE DGBIDB;
GO

-- Verificar si la columna row_hash ya existe
IF NOT EXISTS (
    SELECT 1 
    FROM INFORMATION_SCHEMA.COLUMNS 
    WHERE TABLE_NAME = 'Bienes_01_BENEFICIARIOS' 
    AND COLUMN_NAME = 'row_hash'
)
BEGIN
    -- Agregar la columna row_hash
    ALTER TABLE [dbo].[Bienes_01_BENEFICIARIOS] 
    ADD row_hash VARCHAR(64) NULL;
    
    PRINT '✅ Columna row_hash agregada exitosamente a Bienes_01_BENEFICIARIOS';
    
    -- Crear índice para mejorar performance
    CREATE INDEX IX_Bienes_01_BENEFICIARIOS_row_hash 
    ON [dbo].[Bienes_01_BENEFICIARIOS] (row_hash);
    
    PRINT '✅ Índice IX_Bienes_01_BENEFICIARIOS_row_hash creado exitosamente';
    
END
ELSE
BEGIN
    PRINT '⚠️  La columna row_hash ya existe en Bienes_01_BENEFICIARIOS';
END

-- Verificar el resultado
SELECT 
    COLUMN_NAME,
    DATA_TYPE,
    CHARACTER_MAXIMUM_LENGTH,
    IS_NULLABLE
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_NAME = 'Bienes_01_BENEFICIARIOS' 
  AND COLUMN_NAME = 'row_hash';

-- Mostrar estadísticas
SELECT 
    COUNT(*) as total_registros,
    COUNT(row_hash) as registros_con_hash,
    COUNT(*) - COUNT(row_hash) as registros_sin_hash
FROM [dbo].[Bienes_01_BENEFICIARIOS];

PRINT '🎉 Script completado. La tabla está lista para sincronización con hash.';
"""
    
    try:
        with open('add_row_hash_column.sql', 'w', encoding='utf-8') as f:
            f.write(sql_content)
        
        print("✅ Script SQL creado: add_row_hash_column.sql")
        print("   📋 Ejecutar este script en SQL Server Management Studio")
        print("")
        return True
        
    except Exception as e:
        print(f"❌ Error creando script SQL: {e}")
        return False

def create_test_script():
    """Crear script de prueba"""
    logger = logging.getLogger(__name__)
    
    print("🧪 CREANDO SCRIPT DE PRUEBA")
    print("=" * 50)
    
    # Crear un script de prueba simplificado
    test_content = """# test_simple.py
# Script de prueba simple para verificar hash

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_hash():
    try:
        from services.sync_service import SyncService
        
        print("🔍 Probando funcionalidad de hash...")
        
        sync_service = SyncService()
        
        # Probar generación de hash
        sample_data = {
            'documento_tipo': 'DNI',
            'documento': '12345678',
            'nombre': 'Juan Pérez',
            'email': 'juan@example.com'
        }
        
        hash_value = sync_service.generate_row_hash(sample_data)
        print(f"✅ Hash generado: {hash_value}")
        
        # Verificar que hash es consistente
        hash_value2 = sync_service.generate_row_hash(sample_data)
        if hash_value == hash_value2:
            print("✅ Hash es consistente")
        else:
            print("❌ Hash no es consistente")
            return False
        
        print("✅ Funcionalidad de hash funcionando")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_hash()
    print("=" * 50)
    if success:
        print("🎉 PRUEBA EXITOSA")
        print("✅ Ya puedes ejecutar: python main.py --mode sqlserver --sync-mode incremental")
    else:
        print("❌ PRUEBA FALLÓ")
        print("⚠️  Revisa la instalación")
"""
    
    try:
        with open('test_simple.py', 'w', encoding='utf-8') as f:
            f.write(test_content)
        
        print("✅ Script de prueba creado: test_simple.py")
        print("   📋 Ejecutar: python test_simple.py")
        print("")
        return True
        
    except Exception as e:
        print(f"❌ Error creando script de prueba: {e}")
        return False

def show_next_steps():
    """Mostrar próximos pasos"""
    print("📋 PRÓXIMOS PASOS")
    print("=" * 60)
    print()
    print("1️⃣  EJECUTAR SCRIPT SQL:")
    print("   - Abrir SQL Server Management Studio")
    print("   - Conectar a tu servidor SQL Server")
    print("   - Abrir el archivo: add_row_hash_column.sql")
    print("   - Ejecutar el script")
    print()
    print("2️⃣  ACTUALIZAR CÓDIGO:")
    print("   - Reemplazar services/sync_service.py con la nueva versión")
    print("   - (La nueva versión incluye funcionalidad de hash)")
    print()
    print("3️⃣  PROBAR INSTALACIÓN:")
    print("   python test_simple.py")
    print()
    print("4️⃣  EJECUTAR SINCRONIZACIÓN:")
    print("   set APP_ENV=bienes")
    print("   python main.py --mode sqlserver --sync-mode incremental")
    print()
    print("5️⃣  VERIFICAR RESULTADO:")
    print("   - Primera ejecución: insertará registros")
    print("   - Segunda ejecución: 0 registros (sin duplicados)")
    print()
    print("🎯 OBJETIVO: Sin duplicados en sincronización incremental")
    print("=" * 60)

def main():
    """Función principal"""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    print("🔧 INSTALACIÓN DE SINCRONIZACIÓN CON HASH")
    print("=" * 60)
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()
    
    success = True
    
    # 1. Verificar prerequisitos
    if not check_prerequisites():
        print("❌ No se pueden cumplir los prerequisitos")
        return False
    
    # 2. Crear backup
    backup_dir = create_backup()
    if not backup_dir:
        print("⚠️  No se pudo crear backup, ¿continuar? (y/N): ", end="")
        response = input().strip().lower()
        if response != 'y':
            print("❌ Instalación cancelada")
            return False
    
    # 3. Crear archivos necesarios
    if not create_sql_script():
        success = False
    
    if not create_test_script():
        success = False
    
    # 4. Mostrar próximos pasos
    show_next_steps()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 INSTALACIÓN PREPARADA EXITOSAMENTE")
        print("✅ Archivos creados listos para usar")
        print("📋 Sigue los próximos pasos arriba")
        if backup_dir:
            print(f"💾 Backup guardado en: {backup_dir}")
    else:
        print("❌ PROBLEMAS DURANTE LA PREPARACIÓN")
        print("⚠️  Revisa los errores arriba")
    print("=" * 60)
    
    return success

if __name__ == "__main__":
    try:
        success = main()
        exit_code = 0 if success else 1
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n⚠️  Instalación interrumpida por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)
