# Workshop ETL : Dockerisation d'une application Airflow + FastAPI + Streamlit

## 🎯 Objectif du Workshop

Apprendre à dockeriser une application ETL complète composée de :
- **Airflow** : Orchestration et gestion du pipeline ETL
- **FastAPI** : API REST pour exposer les données
- **Streamlit** : Interface de visualisation des données
- **PostgreSQL** : Base de données relationnelle
- **MongoDB** : Base de données NoSQL

---

## 📋 Prérequis

- Docker et Docker Compose installés
- Connaissances de base en Python
- Éditeur de code (VS Code recommandé)
- Les fichiers sources de l'application (airflow/, fastapi/, streamlit/)

---

## 📁 Structure du Projet à Créer

```
docker-workshop/
│
├── docker-compose.yml          # À créer : orchestration de tous les services
├── airflow/
│   ├── Dockerfile              # À créer : image Airflow personnalisée
│   ├── dags/
│   │   └── etl_dag.py          # Déjà fourni : DAG pour ETL
│   └── data/
│       └── input.csv           # Déjà fourni : données d'entrée
├── fastapi/
│   ├── Dockerfile              # À créer : image FastAPI
│   ├── main.py                 # Déjà fourni : code de l'API
│   └── requirements.txt        # Déjà fourni : dépendances
├── streamlit/
│   ├── Dockerfile              # À créer : image Streamlit
│   ├── app.py                  # Déjà fourni : code de l'app
│   └── requirements.txt        # Déjà fourni : dépendances
└── README.md
```

---

## 🚀 Étape 1 : Créer le Dockerfile pour Airflow

### Objectif
Créer une image Docker personnalisée pour Airflow qui inclut toutes les dépendances nécessaires.

### Instructions

1. Créez le fichier `airflow/Dockerfile`

2. Contenu du Dockerfile :

```dockerfile
# Image de base Airflow
FROM apache/airflow:2.7.3-python3.11

# Passer en mode root pour installer des packages système
USER root

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Revenir à l'utilisateur airflow
USER airflow

# Copier et installer les dépendances Python
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

# Définir le répertoire de travail
WORKDIR /opt/airflow
```

3. Créez le fichier `airflow/requirements.txt` :

```txt
pandas>=2.0.0
psycopg2-binary>=2.9.0
pymongo>=4.0.0
sqlalchemy>=2.0.0
```

### 📝 Points Clés à Expliquer

- **FROM** : Utilise l'image officielle Airflow
- **USER root/airflow** : Changement d'utilisateur pour les permissions
- **RUN apt-get** : Installation de dépendances système
- **COPY requirements.txt** : Copie des dépendances Python
- **WORKDIR** : Définit le répertoire de travail dans le conteneur

---

## 🚀 Étape 2 : Créer le Dockerfile pour FastAPI

### Objectif
Créer une image Docker légère pour l'API FastAPI.

### Instructions

1. Créez le fichier `fastapi/Dockerfile`

2. Contenu du Dockerfile :

```dockerfile
# Image de base Python légère
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les dépendances
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application
COPY . .

# Exposer le port de l'API
EXPOSE 8000

# Commande de démarrage
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

3. Vérifiez que `fastapi/requirements.txt` contient :

```txt
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
psycopg2-binary>=2.9.0
pymongo>=4.0.0
sqlalchemy>=2.0.0
pydantic>=2.0.0
```

### 📝 Points Clés à Expliquer

- **python:3.11-slim** : Image Python légère
- **WORKDIR /app** : Tous les fichiers seront dans /app
- **EXPOSE 8000** : Documente le port utilisé
- **uvicorn --reload** : Recharge automatique en cas de modification

---

## 🚀 Étape 3 : Créer le Dockerfile pour Streamlit

### Objectif
Créer une image Docker pour l'interface de visualisation Streamlit.

### Instructions

1. Créez le fichier `streamlit/Dockerfile`

2. Contenu du Dockerfile :

```dockerfile
# Image de base Python
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les dépendances
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application
COPY . .

# Exposer le port Streamlit
EXPOSE 8501

# Commande de démarrage
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

3. Vérifiez que `streamlit/requirements.txt` contient :

```txt
streamlit>=1.28.0
pandas>=2.0.0
psycopg2-binary>=2.9.0
pymongo>=4.0.0
sqlalchemy>=2.0.0
plotly>=5.17.0
```

### 📝 Points Clés à Expliquer

- **EXPOSE 8501** : Port par défaut de Streamlit
- **--server.address=0.0.0.0** : Permet l'accès depuis l'extérieur du conteneur
- **streamlit run** : Commande pour démarrer l'application

---

## 🚀 Étape 4 : Créer le fichier docker-compose.yml

### Objectif
Orchestrer tous les services et définir leurs interactions.

### Instructions

1. Créez le fichier `docker-compose.yml` à la racine du projet

2. Contenu du docker-compose.yml :

```yaml
version: '3.8'

services:
  # PostgreSQL Database
  postgres:
    image: postgres:15-alpine
    container_name: postgres_db
    environment:
      POSTGRES_USER: airflow
      POSTGRES_PASSWORD: airflow
      POSTGRES_DB: airflow
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - etl_network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U airflow"]
      interval: 10s
      timeout: 5s
      retries: 5

  # MongoDB Database
  mongodb:
    image: mongo:7.0
    container_name: mongodb
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_DATABASE: etl_db
    volumes:
      - mongodb_data:/data/db
    networks:
      - etl_network

  # Airflow Webserver
  airflow-webserver:
    build:
      context: ./airflow
      dockerfile: Dockerfile
    container_name: airflow
    environment:
      - AIRFLOW__CORE__EXECUTOR=LocalExecutor
      - AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@postgres:5432/airflow
      - AIRFLOW__CORE__FERNET_KEY=46BKJoQYlPPOexq0OhDZnIlNepKFf87WFwLbfzqDDho=
      - AIRFLOW__CORE__LOAD_EXAMPLES=False
      - AIRFLOW__WEBSERVER__SECRET_KEY=secret
    ports:
      - "8080:8080"
    volumes:
      - ./airflow/dags:/opt/airflow/dags
      - ./airflow/data:/opt/airflow/data
      - airflow_logs:/opt/airflow/logs
    networks:
      - etl_network
    depends_on:
      postgres:
        condition: service_healthy
    command: >
      bash -c "airflow db init &&
               airflow users create --username admin --password admin --firstname Admin --lastname User --role Admin --email admin@example.com || true &&
               airflow webserver"

  # Airflow Scheduler
  airflow-scheduler:
    build:
      context: ./airflow
      dockerfile: Dockerfile
    container_name: airflow-scheduler
    environment:
      - AIRFLOW__CORE__EXECUTOR=LocalExecutor
      - AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@postgres:5432/airflow
      - AIRFLOW__CORE__FERNET_KEY=46BKJoQYlPPOexq0OhDZnIlNepKFf87WFwLbfzqDDho=
    volumes:
      - ./airflow/dags:/opt/airflow/dags
      - ./airflow/data:/opt/airflow/data
      - airflow_logs:/opt/airflow/logs
    networks:
      - etl_network
    depends_on:
      postgres:
        condition: service_healthy
    command: airflow scheduler

  # FastAPI Service
  fastapi:
    build:
      context: ./fastapi
      dockerfile: Dockerfile
    container_name: fastapi_app
    ports:
      - "8000:8000"
    environment:
      - POSTGRES_HOST=postgres
      - POSTGRES_PORT=5432
      - POSTGRES_USER=airflow
      - POSTGRES_PASSWORD=airflow
      - POSTGRES_DB=airflow
      - MONGODB_HOST=mongodb
      - MONGODB_PORT=27017
    networks:
      - etl_network
    depends_on:
      - postgres
      - mongodb

  # Streamlit Service
  streamlit:
    build:
      context: ./streamlit
      dockerfile: Dockerfile
    container_name: streamlit_app
    ports:
      - "8501:8501"
    environment:
      - POSTGRES_HOST=postgres
      - POSTGRES_PORT=5432
      - POSTGRES_USER=airflow
      - POSTGRES_PASSWORD=airflow
      - POSTGRES_DB=airflow
      - MONGODB_HOST=mongodb
      - MONGODB_PORT=27017
    networks:
      - etl_network
    depends_on:
      - postgres
      - mongodb

volumes:
  postgres_data:
  mongodb_data:
  airflow_logs:

networks:
  etl_network:
    driver: bridge
```

### 📝 Points Clés à Expliquer

#### Services
- **postgres** : Base de données pour Airflow et les données ETL
- **mongodb** : Base de données NoSQL pour stockage alternatif
- **airflow-webserver** : Interface web d'Airflow
- **airflow-scheduler** : Planificateur des DAGs
- **fastapi** : API REST
- **streamlit** : Interface de visualisation

#### Configuration importante
- **depends_on** : Définit l'ordre de démarrage
- **healthcheck** : Vérifie que PostgreSQL est prêt
- **networks** : Permet la communication entre conteneurs
- **volumes** : Persiste les données et partage les fichiers
- **environment** : Variables d'environnement pour la configuration

#### Ports exposés
- `5432` : PostgreSQL
- `27017` : MongoDB
- `8080` : Airflow Web UI
- `8000` : FastAPI
- `8501` : Streamlit

---

## 🚀 Étape 5 : Préparer les données d'entrée

### Instructions

1. Créez le fichier `airflow/data/input.csv` avec des données de test :

```csv
id,name,value,category
1,Product A,100,Electronics
2,Product B,200,Clothing
3,Product C,150,Food
4,Product D,300,Electronics
5,Product E,50,Clothing
```

---

## 🚀 Étape 6 : Lancer l'application

### Instructions

1. **Construire et démarrer tous les services** :

```bash
docker-compose up -d --build
```

2. **Vérifier que tous les conteneurs sont démarrés** :

```bash
docker-compose ps
```

3. **Vérifier les logs en cas d'erreur** :

```bash
# Logs de tous les services
docker-compose logs

# Logs d'un service spécifique
docker-compose logs airflow
docker-compose logs fastapi
docker-compose logs streamlit
```

---

## 🚀 Étape 7 : Tester l'application

### 1. Airflow (http://localhost:8080)

- **Connexion** : `admin` / `admin`
- **Activer le DAG** : Recherchez `csv_to_postgres` et activez-le
- **Trigger manuel** : Cliquez sur le bouton "Play" pour exécuter le DAG
- **Vérifier les logs** : Cliquez sur les tâches pour voir leur exécution

### 2. FastAPI (http://localhost:8000)

- **Documentation Swagger** : http://localhost:8000/docs
- **Tester l'endpoint** : 
  - GET `/data` : Récupérer toutes les données
  - GET `/health` : Vérifier l'état de l'API

### 3. Streamlit (http://localhost:8501)

- **Interface de visualisation** : Affiche les graphiques et tableaux
- **Actualisation** : Recharge automatiquement les données

### 4. PostgreSQL

Connexion via CLI :

```bash
docker exec -it postgres_db psql -U airflow -d airflow
```

Vérifier les données :

```sql
\dt                          -- Lister les tables
SELECT * FROM etl_data;      -- Voir les données
```

### 5. MongoDB

Connexion via CLI :

```bash
docker exec -it mongodb mongosh
```

Commandes MongoDB :

```javascript
show dbs
use etl_db
show collections
db.etl_data.find()
```

---

## 🔧 Commandes Docker Utiles

### Gestion des conteneurs

```bash
# Démarrer les services
docker-compose up -d

# Arrêter les services
docker-compose down

# Arrêter et supprimer les volumes (⚠️ supprime les données)
docker-compose down -v

# Reconstruire les images
docker-compose build

# Reconstruire et redémarrer
docker-compose up -d --build

# Voir les logs en temps réel
docker-compose logs -f

# Redémarrer un service spécifique
docker-compose restart airflow
```

### Débogage

```bash
# Accéder au shell d'un conteneur
docker exec -it airflow bash
docker exec -it fastapi_app bash
docker exec -it streamlit_app bash

# Inspecter un conteneur
docker inspect airflow

# Voir l'utilisation des ressources
docker stats

# Nettoyer les ressources non utilisées
docker system prune -a
```

---

## 🐛 Résolution des Problèmes Courants

### Problème 1 : Airflow ne démarre pas

**Symptôme** : Le conteneur Airflow redémarre en boucle

**Solutions** :
1. Vérifier que PostgreSQL est bien démarré :
   ```bash
   docker-compose logs postgres
   ```

2. Vérifier les logs Airflow :
   ```bash
   docker-compose logs airflow
   ```

3. Réinitialiser la base de données :
   ```bash
   docker-compose down -v
   docker-compose up -d
   ```

### Problème 2 : FastAPI ne se connecte pas à PostgreSQL

**Solutions** :
1. Vérifier les variables d'environnement dans docker-compose.yml
2. S'assurer que le réseau est bien configuré
3. Tester la connexion :
   ```bash
   docker exec -it fastapi_app ping postgres
   ```

### Problème 3 : Le DAG ne trouve pas le fichier CSV

**Solutions** :
1. Vérifier que le volume est bien monté :
   ```bash
   docker exec -it airflow ls -la /opt/airflow/data
   ```

2. Vérifier les chemins dans le DAG

3. Vérifier les permissions du fichier :
   ```bash
   chmod 644 airflow/data/input.csv
   ```

### Problème 4 : Port déjà utilisé

**Symptôme** : `Bind for 0.0.0.0:8080 failed: port is already allocated`

**Solutions** :
1. Changer le port dans docker-compose.yml :
   ```yaml
   ports:
     - "8081:8080"  # Au lieu de 8080:8080
   ```

2. Ou arrêter le service qui utilise le port :
   ```bash
   # Windows
   netstat -ano | findstr :8080
   taskkill /PID <PID> /F
   ```

---

## 📊 Architecture et Flux de Données

```
┌─────────────┐
│  input.csv  │
└──────┬──────┘
       │
       ▼
┌─────────────────┐      ┌──────────────┐
│  Airflow DAG    │─────▶│ PostgreSQL   │
│  (ETL Process)  │      │   (Storage)  │
└─────────────────┘      └──────┬───────┘
                                │
                    ┌───────────┴───────────┐
                    ▼                       ▼
            ┌───────────────┐      ┌──────────────┐
            │   FastAPI     │      │  Streamlit   │
            │  (REST API)   │      │   (Visuali-  │
            │               │      │   zation)    │
            └───────────────┘      └──────────────┘
```

---

## ✅ Critères de Réussite du Workshop

À la fin du workshop, vous devez avoir :

1. ✅ Créé les 3 Dockerfiles (Airflow, FastAPI, Streamlit)
2. ✅ Créé le fichier docker-compose.yml avec tous les services
3. ✅ Lancé tous les conteneurs avec succès
4. ✅ Exécuté le DAG Airflow pour charger les données dans PostgreSQL
5. ✅ Testé l'API FastAPI via Swagger
6. ✅ Visualisé les données dans Streamlit
7. ✅ Compris les interactions entre les différents services

---

## 🎓 Concepts Docker Appris

- **Dockerfiles** : Création d'images personnalisées
- **Multi-stage builds** : (optionnel) Optimisation des images
- **Docker Compose** : Orchestration de services multiples
- **Réseaux Docker** : Communication inter-conteneurs
- **Volumes Docker** : Persistance et partage de données
- **Variables d'environnement** : Configuration des conteneurs
- **Health checks** : Gestion des dépendances entre services
- **Logs et débogage** : Diagnostiquer les problèmes

---

## 📚 Ressources Supplémentaires

- [Documentation Docker](https://docs.docker.com/)
- [Documentation Docker Compose](https://docs.docker.com/compose/)
- [Documentation Airflow](https://airflow.apache.org/docs/)
- [Documentation FastAPI](https://fastapi.tiangolo.com/)
- [Documentation Streamlit](https://docs.streamlit.io/)

---

## 🏆 Défis Bonus

Une fois le workshop terminé, essayez ces défis :

1. **Sécurité** : Ajouter une authentification JWT à FastAPI
2. **Optimisation** : Utiliser des images multi-stage pour réduire la taille
3. **Monitoring** : Ajouter un service de monitoring (Prometheus/Grafana)
4. **CI/CD** : Créer un pipeline GitHub Actions pour build et test
5. **Scaling** : Utiliser CeleryExecutor pour Airflow
6. **Redis** : Ajouter Redis comme cache pour FastAPI

---

Bon workshop ! 🚀🐳
