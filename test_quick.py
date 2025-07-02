# test_quick.py
# Prueba rápida para verificar que la funcionalidad de hash funciona

import os
import sys

def test_hash_functionality():
    """Prueba rápida de funcionalidad de hash"""
    
    print("🧪 PRUEBA RÁPIDA DE HASH")
    print("=" * 40)
    
    try:
        # Importar SyncService
        from services.sync_service import SyncService
        print("✅ SyncService importado correctamente")
        
        # Crear instancia
        sync_service = SyncService()
        print("✅ SyncService instanciado")
        
        # Verificar que tiene métodos de hash
        if hasattr(sync_service, 'generate_row_hash'):
            print("✅ Método generate_row_hash existe")
        else:
            print("❌ Método generate_row_hash NO existe")
            return False
        
        if hasattr(sync_service, 'hash_tables'):
            print("✅ Configuración hash_tables existe")
            print(f"   Tablas configuradas: {list(sync_service.hash_tables.keys())}")
        else:
            print("❌ Configuración hash_tables NO existe")
            return False
        
        # Probar generación de hash
        sample_data = {
            'documento_tipo': 'DNI',
            'documento': '12345678',
            'nombre': 'Juan Pérez',
            'email': 'juan@example.com',
            'activo': 'S'
        }
        
        hash1 = sync_service.generate_row_hash(sample_data)
        hash2 = sync_service.generate_row_hash(sample_data)
        
        if hash1 == hash2:
            print(f"✅ Hash consistente: {hash1[:12]}...")
        else:
            print("❌ Hash NO es consistente")
            return False
        
        # Verificar que cambios generan hash diferente
        sample_data2 = sample_data.copy()
        sample_data2['nombre'] = 'María García'
        hash3 = sync_service.generate_row_hash(sample_data2)
        
        if hash1 != hash3:
            print(f"✅ Cambios detectados: {hash3[:12]}... (diferente)")
        else:
            print("❌ Cambios NO detectados")
            return False
        
        print("\n🎉 TODAS LAS PRUEBAS EXITOSAS")
        print("✅ La funcionalidad de hash está funcionando")
        print("✅ Ya puedes ejecutar la sincronización")
        
        return True
        
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        print("   ¿Ejecutaste el parche quick_fix_hash.py?")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_sql_server_connection():
    """Prueba conexión a SQL Server"""
    print("\n🔍 PROBANDO CONEXIÓN SQL SERVER")
    print("=" * 40)
    
    try:
        from adapters.sqlserver_adapter import SQLServerAdapter
        sqlserver = SQLServerAdapter()
        
        if sqlserver.engine:
            result = sqlserver.test_connection()
            if result:
                print(f"✅ SQL Server: {result}")
                
                # Verificar tabla
                if sqlserver.table_exists('Bienes_01_BENEFICIARIOS'):
                    print("✅ Tabla Bienes_01_BENEFICIARIOS existe")
                    
                    # Verificar columna hash
                    columns = sqlserver.get_table_columns('Bienes_01_BENEFICIARIOS')
                    has_hash = 'row_hash' in columns['COLUMN_NAME'].values if columns is not None else False
                    
                    if has_hash:
                        print("✅ Columna row_hash existe")
                    else:
                        print("⚠️  Columna row_hash NO existe")
                        print("   Ejecuta: add_hash_column.sql")
                    
                    return has_hash
                else:
                    print("❌ Tabla Bienes_01_BENEFICIARIOS NO existe")
                    return False
            else:
                print("❌ SQL Server: Error en conexión")
                return False
        else:
            print("❌ SQL Server: No inicializado")
            return False
            
    except Exception as e:
        print(f"❌ Error SQL Server: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 VERIFICACIÓN RÁPIDA DE INSTALACIÓN")
    print("=" * 50)
    
    # Test 1: Funcionalidad de hash
    hash_ok = test_hash_functionality()
    
    # Test 2: SQL Server
    sql_ok = test_sql_server_connection()
    
    print("\n" + "=" * 50)
    print("📋 RESUMEN:")
    print(f"Funcionalidad Hash: {'✅ OK' if hash_ok else '❌ FALLA'}")
    print(f"SQL Server + Tabla: {'✅ OK' if sql_ok else '❌ FALLA'}")
    
    if hash_ok and sql_ok:
        print("\n🎉 TODO LISTO")
        print("✅ Puedes ejecutar:")
        print("   python main.py --mode sqlserver --sync-mode incremental")
    else:
        print("\n⚠️  FALTA CONFIGURACIÓN")
        if not hash_ok:
            print("1. Ejecutar: python quick_fix_hash.py")
        if not sql_ok:
            print("2. Ejecutar en SQL Server: add_hash_column.sql")
    
    print("=" * 50)
    
    return hash_ok and sql_ok

if __name__ == "__main__":
    main()
