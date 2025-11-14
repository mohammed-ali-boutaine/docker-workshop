# Base Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copier les fichiers Streamlit
COPY . /app/

# Installer dépendances
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Exposer le port
EXPOSE 8501

# Lancer Streamlit
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
