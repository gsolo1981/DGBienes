#!/usr/bin/env python3
"""
Script para verificar drivers ODBC disponibles en el sistema
"""
import pyodbc

def check_odbc_drivers():
    """Muestra todos los drivers ODBC disponibles"""
    print("🔍 DRIVERS ODBC DISPONIBLES EN TU SISTEMA:")
    print("=" * 60)
    
    try:
        drivers = pyodbc.drivers()
        
        if not drivers:
            print("❌ No se encontraron drivers ODBC")
            return
        
        print(f"📋 Encontrados {len(drivers)} drivers:")
        print()
        
        for i, driver in enumerate(drivers, 1):
            print(f"{i:2d}. {driver}")
            
            # Marcar drivers recomendados para SQL Server
            if 'SQL Server' in driver:
                if 'ODBC Driver' in driver and ('17' in driver or '18' in driver):
                    print("    ✅ RECOMENDADO para SQL Server moderno")
                elif driver == 'SQL Server':
                    print("    ⚠️  Driver básico - funciona pero es antiguo")
                else:
                    print("    ℹ️  Driver SQL Server compatible")
        
        print("\n" + "=" * 60)
        print("💡 RECOMENDACIONES:")
        
        # Buscar drivers recomendados
        modern_drivers = [d for d in drivers if 'ODBC Driver' in d and 'SQL Server' in d]
        basic_driver = 'SQL Server' in drivers
        
        if modern_drivers:
            latest = max(modern_drivers, key=lambda x: x.split()[-3] if len(x.split()) > 3 else '0')
            print(f"✅ USA: SQLSERVER_DRIVER={{{latest}}}")
        elif basic_driver:
            print("⚠️  USA: SQLSERVER_DRIVER={SQL Server}")
            print("   (Funciona, pero considera instalar ODBC Driver 17+)")
        else:
            print("❌ NO hay drivers SQL Server. Necesitas instalar:")
            print("   - ODBC Driver 17 for SQL Server (recomendado)")
            print("   - Desde: https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server")
        
    except Exception as e:
        print(f"❌ Error verificando drivers: {e}")
        print("\n🔧 SOLUCIONES:")
        print("1. Instala pyodbc: pip install pyodbc")
        print("2. Instala ODBC Driver 17 for SQL Server")

def test_sql_server_connection():
    """Test de conexión con diferentes drivers"""
    print("\n🧪 PROBANDO CONEXIONES:")
    print("=" * 60)
    
    # Configuración de prueba (ajusta según tu entorno)
    test_configs = [
        {"driver": "{ODBC Driver 17 for SQL Server}", "name": "ODBC 17"},
        {"driver": "{ODBC Driver 18 for SQL Server}", "name": "ODBC 18"},
        {"driver": "{SQL Server}", "name": "SQL Server básico"},
        {"driver": "{SQL Server Native Client 11.0}", "name": "Native Client 11"},
    ]
    
    server = "10.15.0.28"  # Tu servidor de prueba
    database = "DGBIDB"    # Tu base de datos
    
    print("ℹ️  Solo prueba la disponibilidad del driver, no la conexión real")
    print("   (requeriría credenciales válidas)\n")
    
    for config in test_configs:
        try:
            driver = config["driver"]
            name = config["name"]
            
            # Solo verificar si el driver existe (sin conectar realmente)
            connection_string = f"DRIVER={driver};SERVER={server};DATABASE={database};UID=test;PWD=test"
            
            # Esto fallará por credenciales, pero nos dirá si el driver existe
            try:
                pyodbc.connect(connection_string, timeout=1)
            except pyodbc.Error as e:
                error_code = e.args[0] if e.args else ""
                if error_code == 'IM002':
                    print(f"❌ {name}: Driver NO disponible")
                else:
                    print(f"✅ {name}: Driver disponible (error de conexión esperado)")
            except Exception:
                print(f"✅ {name}: Driver disponible")
                
        except Exception as e:
            print(f"❌ {name}: Error - {e}")

if __name__ == '__main__':
    check_odbc_drivers()
    test_sql_server_connection()