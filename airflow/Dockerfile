# Image officielle d'Apache Airflow
FROM apache/airflow:2.9.1-python3.10

# Définir le répertoire de travail
WORKDIR /opt/airflow

# Copier les DAGs
COPY dags/ /opt/airflow/dags/

# Installer dépendances en tant qu'utilisateur "airflow"
USER airflow
RUN pip install --no-cache-dir pandas sqlalchemy psycopg2-binary

# Commande de démarrage
CMD ["standalone"]
