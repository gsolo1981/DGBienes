# fix_syntax_error.py
# Corrección rápida para error de sintaxis en sync_service.py

import os
import re

def fix_syntax_error():
    """Corrige el error de sintaxis en sync_service.py"""
    
    print("🔧 CORRIGIENDO ERROR DE SINTAXIS")
    print("=" * 40)
    
    sync_service_path = 'services/sync_service.py'
    
    if not os.path.exists(sync_service_path):
        print(f"❌ No se encuentra {sync_service_path}")
        return False
    
    try:
        # Leer el archivo
        with open(sync_service_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Hacer backup
        backup_path = f"{sync_service_path}.backup_syntax"
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Backup creado: {backup_path}")
        
        # Corregir problemas específicos
        original_content = content
        
        # 1. Corregir nombre de método con asteriscos
        content = re.sub(r'def \*sync\*table\(', 'def _sync_table(', content)
        print("✅ Corregidos asteriscos en nombre de método")
        
        # 2. Corregir posibles problemas de indentación en la línea problemática
        lines = content.split('\n')
        corrected_lines = []
        
        for i, line in enumerate(lines):
            # Buscar la línea problemática
            if 'def _sync_table(' in line:
                # Asegurar indentación correcta (4 espacios para método de clase)
                if not line.startswith('    def'):
                    corrected_line = '    ' + line.lstrip()
                    corrected_lines.append(corrected_line)
                    print(f"✅ Corregida indentación en línea {i+1}")
                else:
                    corrected_lines.append(line)
            else:
                corrected_lines.append(line)
        
        content = '\n'.join(corrected_lines)
        
        # 3. Verificar que no hay otros asteriscos problemáticos
        asterisk_pattern = r'def \*.*?\*'
        if re.search(asterisk_pattern, content):
            print("⚠️  Encontrados otros métodos con asteriscos, corrigiéndolos...")
            content = re.sub(asterisk_pattern, lambda m: m.group(0).replace('*', ''), content)
        
        # 4. Verificar sintaxis básica buscando problemas comunes
        problem_patterns = [
            (r'def \s+\w+\(', 'def '),  # Espacios extra después de def
            (r':\s*\n\s*\n\s*def', ':\n        pass\n\n    def'),  # Métodos vacíos
        ]
        
        for pattern, replacement in problem_patterns:
            if re.search(pattern, content):
                print(f"✅ Corregido patrón problemático: {pattern}")
                content = re.sub(pattern, replacement, content)
        
        # Verificar si hubo cambios
        if content != original_content:
            # Guardar archivo corregido
            with open(sync_service_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ Archivo corregido y guardado")
            print(f"💾 Backup disponible en: {backup_path}")
            
            # Verificar que no hay más problemas obvios
            print("\n🔍 Verificando sintaxis...")
            try:
                compile(content, sync_service_path, 'exec')
                print("✅ Sintaxis básica verificada")
            except SyntaxError as e:
                print(f"⚠️  Aún hay problemas de sintaxis: {e}")
                print(f"   Línea {e.lineno}: {e.text}")
                return False
            
        else:
            print("ℹ️  No se encontraron problemas para corregir")
        
        return True
        
    except Exception as e:
        print(f"❌ Error corrigiendo archivo: {e}")
        return False

def test_import():
    """Prueba si ahora se puede importar SyncService"""
    print("\n🧪 PROBANDO IMPORTACIÓN")
    print("=" * 40)
    
    try:
        # Intentar importar
        import sys
        if 'services.sync_service' in sys.modules:
            del sys.modules['services.sync_service']
        
        from services.sync_service import SyncService
        print("✅ SyncService importado correctamente")
        
        # Crear instancia básica
        sync_service = SyncService()
        print("✅ SyncService instanciado correctamente")
        
        return True
        
    except SyntaxError as e:
        print(f"❌ Error de sintaxis: {e}")
        print(f"   Línea {e.lineno}: {e.text}")
        return False
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def main():
    """Función principal"""
    print("🚑 CORRECCIÓN URGENTE DE ERROR DE SINTAXIS")
    print("=" * 50)
    
    # Corregir error de sintaxis
    if fix_syntax_error():
        # Probar importación
        if test_import():
            print("\n🎉 ERROR CORREGIDO EXITOSAMENTE")
            print("✅ Ya puedes ejecutar:")
            print("   python main.py --mode sqlserver --sync-mode incremental")
        else:
            print("\n⚠️  Archivo corregido pero aún hay problemas")
            print("   Revisa el archivo manualmente")
    else:
        print("\n❌ No se pudo corregir automáticamente")
        print("   Revisa el archivo manualmente")
    
    print("=" * 50)

if __name__ == "__main__":
    main()
