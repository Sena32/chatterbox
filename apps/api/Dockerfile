FROM python:3.12-slim

WORKDIR /app

# Dependências do sistema mínimas
RUN apt-get update && apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# Instala dependências Python antes de copiar o código-fonte
# (melhor uso do cache de layers)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código-fonte
COPY . .

# Porta padrão da API
EXPOSE 8000

# Comando padrão (sobrescrito pelo docker-compose para --reload)
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
