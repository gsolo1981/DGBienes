# 🎯 DGBienes Multi-Schema - Guía Completa

## 📊 **Arquitectura Multi-Schema**

El sistema ahora maneja **3 entornos diferentes** que apuntan a **distintos schemas de Oracle**:

```
┌─────────────────────────────────────────────────────────────────┐
│                        ORACLE DATABASE                         │
├─────────────────────┬─────────────────────┬─────────────────────┤
│   SCHEMA: bienes    │    SCHEMA: slu      │    SCHEMA: slu      │
│   SCHEMA: fade2     │                     │   (devengados)      │
├─────────────────────┼─────────────────────┼─────────────────────┤
│   🏠 BIENES Y       │   💰 SIGAF          │   📋 SIGAF          │
│   CONCESIONES       │   (Principal)       │   DEVENGADOS        │
│                     │                     │                     │
│ • Beneficiarios     │ • Órdenes Compra    │ • Devengados        │
│ • Carteras          │ • Recepciones       │ • Imputaciones      │
│ • Contratos         │ • Facturas          │ • Períodos          │
│ • Planes Pago       │ • Pagos             │                     │
└─────────────────────┴─────────────────────┴─────────────────────┘
            │                     │                     │
            ▼                     ▼                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                      SQL SERVER - DGBIDB                       │
│  📊 Todas las tablas consolidadas en una sola base destino     │
└─────────────────────────────────────────────────────────────────┘
```

## 🔧 **Configuración por Entorno**

### **📁 Estructura de Archivos de Configuración**

```
proyecto/
├── .env.default          # 🏠 Bienes y Concesiones
├── .env.sigaf            # 💰 SIGAF Principal  
├── .env.sigaf_devengado  # 📋 SIGAF Devengados
└── sql/
    ├── Bienes_Concesiones/    # Scripts Bienes
    ├── sigaf/                 # Scripts SIGAF
    └── Sigaf_Devengados/      # Scripts Devengados
```

### **🔑 Variables de Entorno por Schema**

#### **`.env.default` - Bienes y Concesiones**
```bash
# Oracle - Schema Bienes/Concesiones
DB_HOST=oracle-bienes.empresa.com
DB_USER=usuario_bienes
DB_PASS=password_bienes
DB_SERVICE=BIENES_DB

# SQL Server - Destino común
SQLSERVER_HOST=sqlserver.empresa.com
SQLSERVER_DB=DGBIDB
SQLSERVER_USER=dg_user
SQLSERVER_PASS=dg_password

# Configuración específica
PATH_SQL=sql/Bienes_Concesiones
FILE_XLSX=reporte_bienes_concesiones
SYNC_TO_SQLSERVER=true
```

#### **`.env.sigaf` - SIGAF Principal**
```bash
# Oracle - Schema SIGAF
DB_HOST=oracle-sigaf.empresa.com
DB_USER=usuario_sigaf
DB_PASS=password_sigaf
DB_SERVICE=SIGAF_DB

# SQL Server - Mismo destino
SQLSERVER_HOST=sqlserver.empresa.com
SQLSERVER_DB=DGBIDB
SQLSERVER_USER=dg_user
SQLSERVER_PASS=dg_password

# Configuración específica
PATH_SQL=sql/sigaf
FILE_XLSX=reporte_sigaf
SYNC_TO_SQLSERVER=true
```

#### **`.env.sigaf_devengado` - SIGAF Devengados**
```bash
# Oracle - Schema SIGAF (mismo que SIGAF pero diferente usuario/permisos)
DB_HOST=oracle-sigaf.empresa.com
DB_USER=usuario_sigaf_devengados
DB_PASS=password_sigaf_dev
DB_SERVICE=SIGAF_DB

# SQL Server - Mismo destino
SQLSERVER_HOST=sqlserver.empresa.com
SQLSERVER_DB=DGBIDB
SQLSERVER_USER=dg_user
SQLSERVER_PASS=dg_password

# Configuración específica
PATH_SQL=sql/Sigaf_Devengados
FILE_XLSX=reporte_devengados
SYNC_TO_SQLSERVER=true
```

## 🚀 **Comandos por Entorno**

### **🏠 Bienes y Concesiones**
```bash
# Exportar solo Excel
APP_ENV=default python main.py --mode excel

# Sincronización incremental
APP_ENV=default python main.py --mode both --sync-mode incremental

# Carga inicial completa
APP_ENV=default python main.py --mode sqlserver --sync-mode full

# Estado de sincronización
APP_ENV=default python main.py --status
```

### **💰 SIGAF Principal**
```bash
# Sincronización incremental SIGAF
APP_ENV=sigaf python main.py --mode both --sync-mode incremental

# Solo tablas críticas SIGAF
APP_ENV=sigaf python main.py --mode sqlserver --tables "[01_RELACION_BAC_SIGAF]" "[10_FACTURAS_OP_PAGOS]"

# Información del entorno SIGAF
APP_ENV=sigaf python main.py --info
```

### **📋 SIGAF Devengados**
```bash
# Sincronización devengados
APP_ENV=sigaf_devengado python main.py --mode both --sync-mode incremental

# Solo devengados (tabla específica)
APP_ENV=sigaf_devengado python main.py --mode sqlserver --tables "[01_DEVENGADO_v2]"
```

## 🐳 **Docker Multi-Schema**

### **Servicios Principales por Entorno**
```bash
# Ejecutar solo Bienes y Concesiones
docker-compose up dgbienes-bienes

# Ejecutar solo SIGAF
docker-compose up dgbienes-sigaf

# Ejecutar solo Devengados
docker-compose up dgbienes-devengados

# Ejecutar TODOS los entornos secuencialmente
docker-compose --profile all up dgbienes-all-environments
```

### **Servicios de Mantenimiento**
```bash
# Carga inicial completa por entorno
docker-compose --profile manual up dgbienes-bienes-full
docker-compose --profile manual up dgbienes-sigaf-full  
docker-compose --profile manual up dgbienes-devengados-full

# Tablas críticas SIGAF (alta prioridad)
docker-compose --profile priority up dgbienes-sigaf-priority

# Estado general
docker-compose --profile manual up dgbienes-status

# Información de entornos
docker-compose --profile manual up dgbienes-info
```

## 📋 **Mapeo de Tablas por Entorno**

### **🏠 Entorno: Bienes y Concesiones (`default`)**
| Archivo SQL | Tabla SQL Server | Schema Oracle |
|-------------|------------------|---------------|
| `Bienes_01_BENEFICIARIOS.sql` | `Bienes_01_BENEFICIARIOS` | `bienes` |
| `Bienes_02_CARTERAS.sql` | `Bienes_02_CARTERAS` | `bienes` |
| `Bienes_03_CONTRATOS.sql` | `Bienes_03_CONTRATOS` | `bienes` |
| `Bienes_04_PLAN DE PAGOS.sql` | `Bienes_04_PLAN_DE_PAGOS` | `bienes` |
| `Concesiones_01_BENEFICIARIOS.sql` | `Concesiones_01_BENEFICIARIOS` | `fade2` |
| `Concesiones_02_CARTERAS.sql` | `Concesiones_02_CARTERAS` | `fade2` |
| `Concesiones_03_CONTRATOS.sql` | `Concesiones_03_CONTRATOS` | `fade2` |
| `Concesiones_04_PLAN DE PAGOS.sql` | `Concesiones_04_PLAN_DE_PAGOS` | `fade2` |

### **💰 Entorno: SIGAF (`sigaf`)**
| Archivo SQL | Tabla SQL Server | Schema Oracle |
|-------------|------------------|---------------|
| `01_RELACION_BAC_SIGAF.sql` | `[01_RELACION_BAC_SIGAF]` | `slu` |
| `02_SPR_RENGLONES.sql` | `[02_SPR_RENGLONES]` | `slu` |
| `03_SPR_IMPUTACIONES.sql` | `[03_SPR_IMPUTACIONES]` | `slu` |
| `04_RPR_SPR_PRD.sql` | `[04_RPR_SPR_PRD]` | `slu` |
| `05_RPR_RENGLONES.sql` | `[05_RPR_RENGLONES]` | `slu` |
| `06_RPR_IMPUTACIONES.sql` | `[06_RPR_IMPUTACIONES]` | `slu` |
| `07_PRD_RENGLONES.sql` | `[07_PRD_RENGLONES]` | `slu` |
| `08_PRD_IMPUTACIONES.sql` | `[08_PRD_IMPUTACIONES]` | `slu` |
| `09_PRD_FACTURAS.sql` | `[09_PRD_FACTURAS]` | `slu` |
| `10_FACTURAS_OP_PAGOS.sql` | `[10_FACTURAS_OP_PAGOS]` | `slu` |
| ... | ... | `slu` |
| `25_ENTES.sql` | `[25_ENTES]` | `slu` |

### **📋 Entorno: SIGAF Devengados (`sigaf_devengado`)**
| Archivo SQL | Tabla SQL Server | Schema Oracle |
|-------------|------------------|---------------|
| `01_DEVENGADO_v2.sql` | `[01_DEVENGADO_v2]` | `slu` |

## ⏰ **Estrategias de Sincronización por Entorno**

### **🏠 Bienes y Concesiones**
- **Frecuencia**: Cada 6 horas
- **Batch Size**: 1,000 registros
- **Incremental**: Por `fechafirma`, `fecha_creacion`
- **Prioridad**: Alta (datos críticos de beneficiarios)

### **💰 SIGAF Principal**
- **Frecuencia**: Cada 4 horas
- **Batch Size**: 5,000 registros (mayor volumen)
- **Incremental**: Por `fh_alta`, `fh_autorizacion`, `f_emision`
- **Prioridad**: Muy Alta (datos financieros)

### **📋 SIGAF Devengados**
- **Frecuencia**: Cada 8 horas
- **Batch Size**: 2,000 registros
- **Incremental**: Por `fh_imputacion`
- **Prioridad**: Media (datos de reportes)

## 📅 **Programación Automatizada**

### **Crontab Recomendado**
```bash
# Bienes y Concesiones cada 6 horas
0 */6 * * * cd /app && APP_ENV=default python main.py --mode both --sync-mode incremental

# SIGAF cada 4 horas
0 */4 * * * cd /app && APP_ENV=sigaf python main.py --mode both --sync-mode incremental

# Devengados cada 8 horas
0 */8 * * * cd /app && APP_ENV=sigaf_devengado python main.py --mode both --sync-mode incremental

# Sincronización completa semanal (domingos 2:00 AM)
0 2 * * 0 cd /app && APP_ENV=default python main.py --mode sqlserver --sync-mode full
0 3 * * 0 cd /app && APP_ENV=sigaf python main.py --mode sqlserver --sync-mode full
0 4 * * 0 cd /app && APP_ENV=sigaf_devengado python main.py --mode sqlserver --sync-mode full
```

### **Kubernetes CronJobs (Opcional)**
```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: dgbienes-sync-bienes
spec:
  schedule: "0 */6 * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: dgbienes
            image: dgbienes:latest
            env:
            - name: APP_ENV
              value: "default"
            command: ["python", "main.py", "--mode", "both", "--sync-mode", "incremental"]
---
apiVersion: batch/v1
kind: CronJob
metadata:
  name: dgbienes-sync-sigaf
spec:
  schedule: "0 */4 * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: dgbienes
            image: dgbienes:latest
            env:
            - name: APP_ENV
              value: "sigaf"
            command: ["python", "main.py", "--mode", "both", "--sync-mode", "incremental"]
```

## 🔍 **Monitoreo y Troubleshooting**

### **Comandos de Diagnóstico**
```bash
# Listar todos los entornos disponibles
python main.py --list-envs

# Información detallada del entorno actual
APP_ENV=sigaf python main.py --info

# Estado de sincronización por entorno
APP_ENV=default python main.py --status
APP_ENV=sigaf python main.py --status
APP_ENV=sigaf_devengado python main.py --status

# Ver logs específicos por entorno
tail -f dgbienes.log | grep "sigaf"
tail -f dgbienes.log | grep "default"
```

### **Validación de Configuración**
```bash
# Verificar conectividad Oracle por entorno
APP_ENV=default python -c "from adapters.db_adapter import engine; print(engine.execute('SELECT 1 FROM dual').scalar())"
APP_ENV=sigaf python -c "from adapters.db_adapter import engine; print(engine.execute('SELECT 1 FROM dual').scalar())"

# Verificar conectividad SQL Server
python -c "from adapters.sqlserver_adapter import SQLServerAdapter; s=SQLServerAdapter(); print('OK' if s.execute_query('SELECT 1 as test').iloc[0,0]==1 else 'FAIL')"
```

## 🚨 **Escenarios de Recuperación**

### **Problema: Schema Oracle No Disponible**
```bash
# Verificar que entorno específico
APP_ENV=sigaf python main.py --info

# Intentar solo otros entornos mientras se resuelve
APP_ENV=default python main.py --mode both
APP_ENV=sigaf_devengado python main.py --mode both
```

### **Problema: Tablas Desincronizadas**
```bash
# Re-sincronizar entorno específico completo
APP_ENV=sigaf python main.py --mode sqlserver --sync-mode full

# Solo tablas críticas
APP_ENV=sigaf python main.py --mode sqlserver --sync-mode full --tables "[01_RELACION_BAC_SIGAF]" "[10_FACTURAS_OP_PAGOS]"
```

### **Problema: Datos Corruptos**
```bash
# Limpiar y recargar entorno específico
APP_ENV=sigaf python main.py --mode sqlserver --sync-mode full

# Verificar integridad
APP_ENV=sigaf python main.py --status
```

## 📊 **Dashboard de Monitoreo (Propuesta)**

```bash
# Script de monitoreo general
#!/bin/bash
echo "=== ESTADO MULTI-SCHEMA DGBienes ==="
echo "Timestamp: $(date)"
echo ""

for env in default sigaf sigaf_devengado; do
    echo "🔍 Entorno: $env"
    APP_ENV=$env python main.py --status | grep -E "(✅|❌)" | head -5
    echo ""
done

echo "📊 Resumen de logs recientes:"
tail -20 dgbienes.log | grep -E "(ERROR|INFO|WARNING)" | tail -10
```

## 🎯 **Mejores Prácticas Multi-Schema**

### **✅ DO's**
- ✅ Usar variables de entorno específicas por schema
- ✅ Mantener logs separados por entorno cuando sea posible
- ✅ Probar conexiones antes de sincronizaciones masivas
- ✅ Implementar alertas por entorno crítico
- ✅ Documentar permisos específicos por schema Oracle

### **❌ DON'Ts**
- ❌ Mezclar configuraciones entre entornos
- ❌ Ejecutar sincronización completa en horarios pico
- ❌ Ignorar errores de conectividad por schema
- ❌ Usar credenciales compartidas entre esquemas sensibles

## 🔮 **Roadmap de Mejoras**

### **Fase 1: Optimización (Próximas 2 semanas)**
- 🔄 Implementar UPSERT verdadero por registro
- 📊 Dashboard web de monitoreo multi-schema
- 🔔 Alertas específicas por entorno

### **Fase 2: Escalabilidad (Próximo mes)**
- ⚡ Paralelización de sincronización entre schemas
- 🗜️ Compresión de archivos Excel por entorno
- 🔐 Encriptación de datos sensibles por schema

### **Fase 3: Inteligencia (Próximos 3 meses)**
- 🤖 Auto-detección de cambios en esquemas Oracle
- 📈 Predicción de volúmenes de sincronización
- 🎯 Optimización automática de horarios por entorno

---

**¡Tu sistema DGBienes ahora está preparado para manejar múltiples schemas Oracle de forma inteligente y eficiente!** 🎉