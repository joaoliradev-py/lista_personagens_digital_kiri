# Usar uma imagem Python leve
FROM python:3.11-slim

# Evita que o Python gere arquivos .pyc e permite logs em tempo real
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Define o diretório de trabalho
WORKDIR /app

# Instala dependências do sistema (necessárias para algumas libs de banco de dados)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copia apenas o requirements primeiro para aproveitar o cache do Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código do projeto
COPY . .

# Expõe a porta que o Flask vai rodar (geralmente 5000 ou 8080)
EXPOSE 5000

# Comando para rodar a aplicação usando Gunicorn
# Substitua 'run:app' se o seu objeto Flask estiver em outro lugar
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]
