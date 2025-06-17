FROM python:3.12-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV ORACLE_HOME=/opt/oracle/instantclient
ENV LD_LIBRARY_PATH=$ORACLE_HOME
ENV PATH=$ORACLE_HOME:$PATH
ENV ORACLE_CLIENT_LIB_DIR=$ORACLE_HOME

# Instalar dependencias
RUN apt-get update && \
    apt-get install -y curl unzip libaio1 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Descargar e instalar Oracle Instant Client 21.11
RUN curl -L -o instantclient-basic.zip \
    https://download.oracle.com/otn_software/linux/instantclient/2111000/instantclient-basic-linux.x64-21.11.0.0.0dbru.zip && \
    unzip instantclient-basic.zip -d /opt/oracle && \
    rm instantclient-basic.zip && \
    mv /opt/oracle/instantclient_* $ORACLE_HOME

# Crear carpeta de trabajo
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
