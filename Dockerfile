FROM python:3.12-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV ORACLE_HOME=/opt/oracle/instantclient
ENV LD_LIBRARY_PATH=$ORACLE_HOME
ENV PATH=$ORACLE_HOME:$PATH
ENV ORACLE_CLIENT_LIB_DIR=$ORACLE_HOME

# Instalar dependencias del sistema
RUN apt-get update && \
    apt-get install -y \
    curl \
    unzip \
    libaio1 \
    # Dependencias para SQL Server ODBC Driver
    gnupg2 \
    curl \
    apt-transport-https \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Instalar Microsoft ODBC Driver para SQL Server
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Descargar e instalar Oracle Instant Client 21.11
RUN curl -L -o instantclient-basic.zip \
    https://download.oracle.com/otn_software/linux/instantclient/2111000/instantclient-basic-linux.x64-21.11.0.0.0dbru.zip && \
    unzip instantclient-basic.zip -d /opt/oracle && \
    rm instantclient-basic.zip && \
    mv /opt/oracle/instantclient_* $ORACLE_HOME

# Crear carpetas de trabajo
WORKDIR /app
RUN mkdir -p /app/logs /app/output

# Instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY . .

# Configurar permisos
RUN chmod +x /app/main.py

# Comando por defecto
CMD ["python", "main.py", "--mode", "both", "--sync-mode", "incremental"]