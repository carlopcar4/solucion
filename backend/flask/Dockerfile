FROM python:3.11-slim

# 1) Instalar dependencias de sistema para Docker-CLI y docker-compose
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    gnupg2 \
    lsb-release \
    python3-pip \
    python3-setuptools \
    python3-wheel && \
    rm -rf /var/lib/apt/lists/*

# 2) Instalar docker CLI
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        lsb-release && \
    mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://download.docker.com/linux/debian/gpg | \
        gpg --dearmor -o /etc/apt/keyrings/docker.gpg && \
    echo \
        "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
        https://download.docker.com/linux/debian \
        $(lsb_release -cs) stable" | \
        tee /etc/apt/sources.list.d/docker.list > /dev/null && \
    apt-get update && \
    apt-get install -y --no-install-recommends docker-ce-cli && \
    rm -rf /var/lib/apt/lists/*

# 3) Instalar docker-compose (v1) descargándolo desde GitHub
#    (aquí tomamos la versión 1.29.2 como ejemplo; ajusta si quieres otra):
RUN curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-linux-x86_64" \
    -o /usr/local/bin/docker-compose && \
    chmod +x /usr/local/bin/docker-compose

WORKDIR /app

# 4) Copiar e instalar dependencias Python (incluyendo flask-cors)
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 5) Copiar el resto de tu aplicación Flask
COPY . /app


EXPOSE 4001
CMD ["python", "app.py"]
