# Imagem base leve
FROM python:3.11-slim

# Diretório de trabalho dentro do container
WORKDIR /app

# Impede que o Python gere arquivos .pyc e permite logs em tempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instala dependências de sistema para o Atlas (Certificados SSL)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala as dependências antes do código (aproveita o cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o projeto para o container
COPY . .

# Expõe a porta padrão do Flask
EXPOSE 5000

# Comando para rodar a aplicação
# Nota: 'run:app' assume que seu objeto Flask está no run.py e chama-se 'app'
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]
