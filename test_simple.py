# test_simple.py
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
