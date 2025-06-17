# Proyecto DGBienes

Este proyecto genera reportes Excel a partir de scripts SQL conectando a distintas bases de datos Oracle. Puede ejecutarse localmente con Docker Compose o desplegarse en Kubernetes.

---

## 🔧 Requisitos

- Docker
- Docker Compose

---

## 🚀 Ejecución local con Docker Compose

### 1. Estructura esperada

Asegurate de tener los siguientes archivos en el root del proyecto:

```
.
├── .env.default
├── .env.sigaf
├── .env.sigaf_devengado
├── Dockerfile
├── docker-compose.yml
├── main.py
├── requirements.txt
├── config/
│   └── settings.py
└── sql/
    ├── Bienes_Concesiones/
    ├── sigaf/
    └── Sigaf_Devengados/
```

### 2. Levantar los servicios

```bash
docker compose up --build
```

Esto construirá y levantará tres contenedores:

- `dgbienes-default`
- `dgbienes-sigaf`
- `dgbienes-sigaf-devengado`

Cada uno se conecta a una base de datos distinta y ejecuta los scripts SQL correspondientes.

Los archivos `.xlsx` generados se guardan en:

```
./output/default/
./output/sigaf/
./output/sigaf_devengado/
```

---

## ⚙️ Configuración por entorno

Cada `.env` define su propia conexión Oracle y carpeta de scripts SQL:

### .env.default
```
PATH_SQL=sql/Bienes_Concesiones
FILE_XLSX=Bienes_Concesiones.xlsx
```

### .env.sigaf
```
PATH_SQL=sql/sigaf
FILE_XLSX=Bienes_Concesiones_Sigaf.xlsx
```

### .env.sigaf_devengado
```
PATH_SQL=sql/Sigaf_Devengados
FILE_XLSX=Sigaf_Devengados.xlsx
```

El archivo `config/settings.py` usa `APP_ENV` para determinar qué `.env` cargar.

---

## ☸️ Despliegue en Kubernetes

Cada entorno se puede desplegar como un `Deployment` + `ConfigMap`.

```bash
kubectl apply -f k8s_yamls/default.yaml
kubectl apply -f k8s_yamls/sigaf.yaml
kubectl apply -f k8s_yamls/sigaf_devengado.yaml
```

---

## 🧪 Debug

- Logs de contenedor:
```bash
docker logs dgbienes-sigaf
```

- Forzar regeneración:
```bash
docker compose build
docker compose up
```

---

## ✍️ Autor

- Gustavo Solomita