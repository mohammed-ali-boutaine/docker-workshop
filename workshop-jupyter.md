# Workshop : Dockerisation d'une Application Jupyter + PySpark + MongoDB

## 🎯 Objectif du Workshop

Apprendre à dockeriser une application de data science avec :
- **Jupyter Notebook** avec **PySpark** pour l'analyse de données
- **MongoDB** pour le stockage des données
- **Docker Compose** pour orchestrer les services

---

## 📋 Prérequis

- Docker et Docker Compose installés
- Connaissances de base en Python et Jupyter
- Éditeur de code (VS Code recommandé)

---

## 📁 Structure du Projet à Créer

```
jupyter-project/
│
├── docker-compose.yml          # À créer : orchestration des services
├── Dockerfile                  # À créer : image Jupyter personnalisée
├── requirements.txt            # À créer : dépendances Python
├── data/                       # Dossier pour les données
│   └── input.csv               # Fichier de données
├── notebooks/                  # Dossier pour les notebooks
│   └── analysis.ipynb
└── load.ipynb                  # Notebook principal
```

---

## 🚀 Étape 1 : Créer le fichier requirements.txt

### Objectif
Définir toutes les dépendances Python nécessaires pour le projet.

### Instructions

1. Créez le fichier `requirements.txt` à la racine du projet

2. Contenu du fichier :

```txt
# Data Processing
pandas>=2.0.0
numpy>=1.24.0

# Database Connectors
pymongo>=4.0.0
psycopg2-binary>=2.9.0

# Data Visualization
matplotlib>=3.7.0
seaborn>=0.12.0
plotly>=5.17.0

# Spark Extensions
pyspark>=3.5.0

# Utilities
python-dotenv>=1.0.0
```

### 📝 Points Clés à Expliquer

- **pandas** : Manipulation et analyse de données
- **pymongo** : Connexion à MongoDB
- **matplotlib/seaborn/plotly** : Visualisation de données
- **pyspark** : Analyse distribuée avec Spark
- **python-dotenv** : Gestion des variables d'environnement

---

## 🚀 Étape 2 : Créer le Dockerfile

### Objectif
Créer une image Docker personnalisée basée sur Jupyter avec PySpark intégré.

### Instructions

1. Créez le fichier `Dockerfile` à la racine du projet

2. Contenu du Dockerfile :

```dockerfile
# Image de base : Jupyter avec PySpark 3.5.0 préinstallé
FROM jupyter/pyspark-notebook:spark-3.5.0

# Passer en mode root pour installer des paquets système
USER root

# Installer les outils MongoDB et autres dépendances système
RUN apt-get update && apt-get install -y \
    wget \              # Outil de téléchargement de fichiers
    curl \              # Outil de transfert de données
    && rm -rf /var/lib/apt/lists/*  # Nettoyer le cache pour réduire la taille

# Revenir à l'utilisateur jovyan (utilisateur par défaut de Jupyter)
USER $NB_UID

# Définir le répertoire de travail
WORKDIR /home/jovyan/work

# Copier le fichier des dépendances Python
COPY requirements.txt .

# Installer les dépendances Python sans cache
RUN pip install --no-cache-dir -r requirements.txt

# Copier tous les fichiers du projet avec les bonnes permissions
COPY --chown=$NB_UID:$NB_GID . .

# Exposer le port Jupyter Notebook (8888)
EXPOSE 8888

# Exposer le port Spark UI (4040)
EXPOSE 4040

# Commande de démarrage : lancer Jupyter sans authentification
CMD ["start-notebook.sh", "--NotebookApp.token=''", "--NotebookApp.password=''"]
```

### 📝 Explication Ligne par Ligne

#### Section 1 : Image de Base
```dockerfile
FROM jupyter/pyspark-notebook:spark-3.5.0
```
- Utilise l'image officielle Jupyter qui inclut :
  - Python 3.x
  - Jupyter Notebook/Lab
  - PySpark 3.5.0 préconfiguré
  - Toutes les dépendances Spark

#### Section 2 : Installation des Outils Système
```dockerfile
USER root
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*
```
- **USER root** : Passe en mode administrateur (nécessaire pour apt-get)
- **apt-get update** : Met à jour la liste des paquets
- **apt-get install** : Installe wget et curl
- **rm -rf /var/lib/apt/lists/** : Nettoie le cache pour réduire la taille de l'image

#### Section 3 : Configuration Utilisateur
```dockerfile
USER $NB_UID
WORKDIR /home/jovyan/work
```
- **USER $NB_UID** : Revient à l'utilisateur non-privilégié (jovyan) pour la sécurité
- **WORKDIR** : Définit le répertoire de travail (où s'ouvriront les notebooks)

#### Section 4 : Installation des Dépendances Python
```dockerfile
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
```
- **COPY requirements.txt** : Copie uniquement requirements.txt en premier (optimisation du cache Docker)
- **pip install --no-cache-dir** : Installe les packages sans garder le cache (réduit la taille)

#### Section 5 : Copie des Fichiers du Projet
```dockerfile
COPY --chown=$NB_UID:$NB_GID . .
```
- **COPY --chown** : Copie tous les fichiers avec les bonnes permissions
- **$NB_UID:$NB_GID** : Assigne les fichiers à l'utilisateur jovyan

#### Section 6 : Exposition des Ports
```dockerfile
EXPOSE 8888
EXPOSE 4040
```
- **8888** : Port pour accéder à Jupyter Notebook
- **4040** : Port pour l'interface de monitoring Spark

#### Section 7 : Commande de Démarrage
```dockerfile
CMD ["start-notebook.sh", "--NotebookApp.token=''", "--NotebookApp.password=''"]
```
- **start-notebook.sh** : Script fourni par l'image Jupyter
- **--NotebookApp.token=''** : Désactive le token d'authentification
- **--NotebookApp.password=''** : Désactive le mot de passe
- ⚠️ **ATTENTION** : Ne jamais utiliser en production ! (pour le développement uniquement)

---

## 🚀 Étape 3 : Créer le fichier docker-compose.yml

### Objectif
Orchestrer les services Jupyter et MongoDB et définir leur communication.

### Instructions

1. Créez le fichier `docker-compose.yml` à la racine du projet

2. Contenu du docker-compose.yml :

```yaml
version: '3.8'

services:
  # Service MongoDB
  mongodb:
    image: mongo:7.0                          # Image MongoDB version 7.0
    container_name: dataflow-insight-mongo    # Nom personnalisé du conteneur
    ports:
      - "27017:27017"                         # Port MongoDB (host:container)
    environment:
      MONGO_INITDB_DATABASE: dataflow_insight # Nom de la base de données initiale
    volumes:
      - mongodb_data:/data/db                 # Volume pour persister les données
    networks:
      - dataflow-insight-net                  # Réseau partagé avec Jupyter

  # Service Jupyter avec PySpark
  jupyter:
    build: .                                  # Construire depuis le Dockerfile local
    container_name: dataflow-insight-jupyter  # Nom personnalisé du conteneur
    ports:
      - "8888:8888"                           # Port Jupyter Notebook
      - "4041:4040"                           # Port Spark UI (redirigé vers 4041)
    environment:
      - JUPYTER_ENABLE_LAB=yes                # Active JupyterLab (interface moderne)
      - GRANT_SUDO=yes                        # Permet les commandes sudo
    volumes:
      - ./data:/home/jovyan/work/data                     # Partage le dossier data
      - ./load.ipynb:/home/jovyan/work/load.ipynb         # Monte le notebook principal
      - ./notebooks:/home/jovyan/work/notebooks           # Partage le dossier notebooks
    depends_on:
      - mongodb                               # Démarre MongoDB avant Jupyter
    networks:
      - dataflow-insight-net                  # Réseau partagé avec MongoDB

# Déclaration des volumes persistants
volumes:
  mongodb_data:                               # Volume pour les données MongoDB

# Déclaration des réseaux
networks:
  dataflow-insight-net:                       # Réseau bridge pour communication
    driver: bridge
```

### 📝 Explication Détaillée du Docker Compose

#### Service MongoDB

##### Configuration de Base
```yaml
mongodb:
  image: mongo:7.0
  container_name: dataflow-insight-mongo
```
- **image: mongo:7.0** : Utilise l'image officielle MongoDB version 7.0
- **container_name** : Nom fixe pour faciliter les références

##### Ports
```yaml
ports:
  - "27017:27017"
```
- **Format** : `host:container`
- **27017** : Port par défaut de MongoDB
- Permet d'accéder à MongoDB depuis l'hôte (localhost:27017)

##### Variables d'Environnement
```yaml
environment:
  MONGO_INITDB_DATABASE: dataflow_insight
```
- Crée automatiquement une base de données nommée `dataflow_insight` au premier démarrage

##### Volumes
```yaml
volumes:
  - mongodb_data:/data/db
```
- **mongodb_data** : Volume Docker nommé (défini en bas du fichier)
- **/data/db** : Chemin interne où MongoDB stocke ses données
- **Persistance** : Les données survivent à l'arrêt/suppression du conteneur

##### Réseaux
```yaml
networks:
  - dataflow-insight-net
```
- Connecte MongoDB au réseau personnalisé
- Permet à Jupyter de communiquer avec MongoDB via le nom `mongodb`

---

#### Service Jupyter

##### Configuration de Base
```yaml
jupyter:
  build: .
  container_name: dataflow-insight-jupyter
```
- **build: .** : Construit l'image depuis le Dockerfile dans le répertoire courant
- Préféré à `image:` car on utilise une image personnalisée

##### Ports
```yaml
ports:
  - "8888:8888"  # Jupyter
  - "4041:4040"  # Spark UI
```
- **8888:8888** : Accès à Jupyter via http://localhost:8888
- **4041:4040** : Spark UI accessible via http://localhost:4041
  - Port hôte différent (4041) pour éviter les conflits

##### Variables d'Environnement
```yaml
environment:
  - JUPYTER_ENABLE_LAB=yes
  - GRANT_SUDO=yes
```
- **JUPYTER_ENABLE_LAB=yes** : Active JupyterLab (interface moderne et puissante)
- **GRANT_SUDO=yes** : Permet d'exécuter des commandes root si nécessaire

##### Volumes (Montage Bidirectionnel)
```yaml
volumes:
  - ./data:/home/jovyan/work/data
  - ./load.ipynb:/home/jovyan/work/load.ipynb
  - ./notebooks:/home/jovyan/work/notebooks
```

**Format** : `chemin_hôte:chemin_conteneur`

1. **./data:/home/jovyan/work/data**
   - Partage le dossier `data` de l'hôte avec le conteneur
   - Les modifications sont synchronisées dans les deux sens
   - Permet de lire/écrire des fichiers CSV, JSON, etc.

2. **./load.ipynb:/home/jovyan/work/load.ipynb**
   - Monte un notebook spécifique
   - Permet d'éditer le notebook depuis l'hôte ou le conteneur

3. **./notebooks:/home/jovyan/work/notebooks**
   - Partage un dossier entier de notebooks
   - Facilite l'organisation de plusieurs notebooks

**Avantages des volumes** :
- ✅ Modifications persistantes
- ✅ Édition depuis VS Code ou Jupyter
- ✅ Backup facile (les fichiers sont sur l'hôte)
- ✅ Travail collaboratif (partage de fichiers)

##### Dépendances
```yaml
depends_on:
  - mongodb
```
- Démarre MongoDB avant Jupyter
- Assure que MongoDB est disponible quand Jupyter démarre
- ⚠️ Ne garantit pas que MongoDB soit prêt (juste démarré)

##### Réseaux
```yaml
networks:
  - dataflow-insight-net
```
- Même réseau que MongoDB
- Permet la communication : Jupyter peut accéder à MongoDB via `mongodb:27017`

---

#### Volumes Nommés

```yaml
volumes:
  mongodb_data:
```
- **mongodb_data** : Volume géré par Docker
- Stocké dans `/var/lib/docker/volumes/` (Linux/Mac) ou dans WSL (Windows)
- Persiste même après `docker-compose down`
- Supprimé seulement avec `docker-compose down -v`

---

#### Réseaux

```yaml
networks:
  dataflow-insight-net:
    driver: bridge
```
- **driver: bridge** : Réseau de type pont (par défaut)
- Crée un réseau privé virtuel pour les conteneurs
- Les conteneurs peuvent communiquer par leur nom :
  - Depuis Jupyter : `mongodb://mongodb:27017/dataflow_insight`
  - Le nom `mongodb` est résolu automatiquement

**Avantages du réseau personnalisé** :
- ✅ Isolation : seuls les conteneurs du réseau peuvent communiquer
- ✅ Résolution DNS automatique par nom de conteneur
- ✅ Sécurité accrue

---

## 🚀 Étape 4 : Préparer les Données

### Instructions

1. Créez le dossier `data/` :
```bash
mkdir data
```

2. Créez le fichier `data/input.csv` avec des données de test :

```csv
id,name,category,value,date
1,Product A,Electronics,299.99,2024-01-15
2,Product B,Clothing,49.99,2024-01-16
3,Product C,Food,12.50,2024-01-17
4,Product D,Electronics,599.99,2024-01-18
5,Product E,Clothing,79.99,2024-01-19
6,Product F,Food,8.99,2024-01-20
7,Product G,Electronics,199.99,2024-01-21
8,Product H,Clothing,39.99,2024-01-22
9,Product I,Food,15.00,2024-01-23
10,Product J,Electronics,399.99,2024-01-24
```

---

## 🚀 Étape 5 : Créer un Notebook de Démonstration

### Instructions

1. Créez le fichier `load.ipynb` à la racine du projet

2. Contenu du notebook (exemple de code) :

```python
# Cell 1: Import des bibliothèques
import pandas as pd
import pymongo
from pyspark.sql import SparkSession

# Cell 2: Initialiser Spark
spark = SparkSession.builder \
    .appName("DataFlow Insight") \
    .getOrCreate()

print("Spark Version:", spark.version)

# Cell 3: Charger les données CSV
df = pd.read_csv('/home/jovyan/work/data/input.csv')
print("Données chargées:")
print(df.head())

# Cell 4: Connexion à MongoDB
client = pymongo.MongoClient("mongodb://mongodb:27017/")
db = client["dataflow_insight"]
collection = db["products"]

print("Connecté à MongoDB")

# Cell 5: Insérer les données dans MongoDB
data_dict = df.to_dict("records")
collection.insert_many(data_dict)
print(f"{len(data_dict)} documents insérés dans MongoDB")

# Cell 6: Vérifier l'insertion
count = collection.count_documents({})
print(f"Nombre total de documents: {count}")

# Cell 7: Analyse avec PySpark
spark_df = spark.createDataFrame(df)
spark_df.show()

# Cell 8: Statistiques de base
print("\nStatistiques par catégorie:")
spark_df.groupBy("category").count().show()
```

---

## 🚀 Étape 6 : Lancer l'Application

### Instructions

1. **Construire et démarrer les services** :

```bash
docker-compose up -d --build
```

2. **Vérifier l'état des conteneurs** :

```bash
docker-compose ps
```

Résultat attendu :
```
NAME                         STATUS    PORTS
dataflow-insight-jupyter     Up        0.0.0.0:8888->8888/tcp, 0.0.0.0:4041->4040/tcp
dataflow-insight-mongo       Up        0.0.0.0:27017->27017/tcp
```

3. **Vérifier les logs** :

```bash
# Logs de tous les services
docker-compose logs

# Logs d'un service spécifique
docker-compose logs jupyter
docker-compose logs mongodb

# Suivre les logs en temps réel
docker-compose logs -f jupyter
```

---

## 🚀 Étape 7 : Utiliser l'Application

### 1. Accéder à Jupyter

**URL** : http://localhost:8888

- Pas de mot de passe requis (configuré dans le Dockerfile)
- Vous verrez l'interface JupyterLab
- Les dossiers `data/`, `notebooks/` et le fichier `load.ipynb` sont visibles

### 2. Ouvrir et Exécuter le Notebook

1. Cliquez sur `load.ipynb`
2. Exécutez les cellules une par une (Shift + Enter)
3. Vérifiez les sorties de chaque cellule

### 3. Vérifier Spark UI

**URL** : http://localhost:4041 (quand Spark est actif)

- Monitoring des jobs Spark
- Statistiques de performance
- Détails des tâches exécutées

### 4. Vérifier MongoDB

**Via CLI Docker** :
```bash
docker exec -it dataflow-insight-mongo mongosh
```

**Commandes MongoDB** :
```javascript
// Afficher les bases de données
show dbs

// Utiliser la base dataflow_insight
use dataflow_insight

// Afficher les collections
show collections

// Afficher tous les documents
db.products.find().pretty()

// Compter les documents
db.products.countDocuments()

// Recherche par catégorie
db.products.find({category: "Electronics"}).pretty()

// Statistiques
db.products.aggregate([
  {$group: {_id: "$category", count: {$sum: 1}}}
])
```

### 5. Connexion MongoDB depuis Python

Dans vos notebooks, utilisez cette URL de connexion :

```python
# Format : mongodb://nom_conteneur:port/nom_database
mongo_url = "mongodb://mongodb:27017/dataflow_insight"

# Avec pymongo
import pymongo
client = pymongo.MongoClient(mongo_url)
db = client["dataflow_insight"]
```

**Pourquoi `mongodb` et pas `localhost` ?**
- `mongodb` : Nom du conteneur dans le réseau Docker
- Docker résout automatiquement ce nom vers l'IP du conteneur
- `localhost` ne fonctionnerait pas (référencerait le conteneur Jupyter lui-même)

---

## 🔧 Commandes Docker Utiles

### Gestion des Services

```bash
# Démarrer les services
docker-compose up -d

# Arrêter les services
docker-compose down

# Arrêter et supprimer les volumes (⚠️ supprime les données MongoDB)
docker-compose down -v

# Reconstruire les images
docker-compose build

# Reconstruire et redémarrer
docker-compose up -d --build

# Redémarrer un service spécifique
docker-compose restart jupyter
docker-compose restart mongodb
```

### Logs et Debugging

```bash
# Voir tous les logs
docker-compose logs

# Logs d'un service
docker-compose logs jupyter
docker-compose logs mongodb

# Suivre les logs en temps réel
docker-compose logs -f

# Logs des 50 dernières lignes
docker-compose logs --tail=50
```

### Accès aux Conteneurs

```bash
# Shell dans le conteneur Jupyter
docker exec -it dataflow-insight-jupyter bash

# Shell dans MongoDB
docker exec -it dataflow-insight-mongo mongosh

# Shell en tant que root
docker exec -it -u root dataflow-insight-jupyter bash
```

### Inspection et Monitoring

```bash
# Informations détaillées sur un conteneur
docker inspect dataflow-insight-jupyter

# Statistiques en temps réel
docker stats

# Voir les volumes
docker volume ls

# Voir les réseaux
docker network ls

# Inspecter un réseau
docker network inspect docker-workshop_dataflow-insight-net
```

---

## 🐛 Résolution des Problèmes Courants

### Problème 1 : Port 8888 déjà utilisé

**Symptôme** :
```
Bind for 0.0.0.0:8888 failed: port is already allocated
```

**Solutions** :

1. **Changer le port dans docker-compose.yml** :
```yaml
ports:
  - "8889:8888"  # Utiliser le port 8889 sur l'hôte
```

2. **Trouver et arrêter le processus** :
```bash
# Windows
netstat -ano | findstr :8888
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :8888
kill -9 <PID>
```

---

### Problème 2 : Jupyter ne trouve pas le fichier CSV

**Symptôme** :
```
FileNotFoundError: [Errno 2] No such file or directory: '/home/jovyan/work/data/input.csv'
```

**Solutions** :

1. **Vérifier le volume dans docker-compose.yml** :
```yaml
volumes:
  - ./data:/home/jovyan/work/data
```

2. **Vérifier que le fichier existe sur l'hôte** :
```bash
ls -la data/input.csv
```

3. **Vérifier dans le conteneur** :
```bash
docker exec -it dataflow-insight-jupyter ls -la /home/jovyan/work/data
```

4. **Vérifier les permissions** :
```bash
chmod 644 data/input.csv
```

---

### Problème 3 : Impossible de se connecter à MongoDB

**Symptôme** :
```
pymongo.errors.ServerSelectionTimeoutError: mongodb:27017: [Errno -2] Name or service not known
```

**Solutions** :

1. **Vérifier que MongoDB est démarré** :
```bash
docker-compose ps mongodb
```

2. **Vérifier les logs MongoDB** :
```bash
docker-compose logs mongodb
```

3. **Tester la connexion réseau** :
```bash
docker exec -it dataflow-insight-jupyter ping mongodb
```

4. **Vérifier le réseau** :
```bash
docker network ls
docker network inspect docker-workshop_dataflow-insight-net
```

5. **Utiliser la bonne URL de connexion** :
```python
# ✅ Correct (dans Docker)
client = pymongo.MongoClient("mongodb://mongodb:27017/")

# ❌ Incorrect
client = pymongo.MongoClient("mongodb://localhost:27017/")
```

---

### Problème 4 : Erreur "Permission Denied"

**Symptôme** :
```
PermissionError: [Errno 13] Permission denied: '/home/jovyan/work/data/output.csv'
```

**Solutions** :

1. **Changer les permissions du dossier** :
```bash
chmod -R 777 data/
```

2. **Vérifier l'utilisateur dans le conteneur** :
```bash
docker exec -it dataflow-insight-jupyter whoami
# Devrait afficher : jovyan
```

3. **Relancer avec les bonnes permissions** :
```bash
docker-compose down
chmod -R 777 data/
docker-compose up -d
```

---

### Problème 5 : Spark UI n'est pas accessible

**Symptôme** : http://localhost:4041 ne répond pas

**Solutions** :

1. **Vérifier que Spark est actif** :
   - Spark UI n'est disponible que quand un job Spark est en cours
   - Exécutez une cellule avec du code PySpark

2. **Vérifier le port dans docker-compose.yml** :
```yaml
ports:
  - "4041:4040"  # Port hôte : Port conteneur
```

3. **Voir les logs** :
```bash
docker-compose logs jupyter | grep spark
```

---

### Problème 6 : Le conteneur redémarre en boucle

**Symptôme** :
```bash
docker-compose ps
# STATUS: Restarting
```

**Solutions** :

1. **Voir les logs d'erreur** :
```bash
docker-compose logs jupyter
```

2. **Vérifier la syntaxe du Dockerfile** :
```bash
docker-compose build jupyter
```

3. **Tester l'image manuellement** :
```bash
docker run -it --rm jupyter/pyspark-notebook:spark-3.5.0 bash
```

4. **Reconstruire from scratch** :
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

---

## 📊 Architecture du Projet

```
┌─────────────────────────────────────────────────────────┐
│                     Docker Host                          │
│                                                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │          Network: dataflow-insight-net           │  │
│  │                                                   │  │
│  │  ┌──────────────────┐    ┌──────────────────┐  │  │
│  │  │                  │    │                  │  │  │
│  │  │  Jupyter + Spark │◄───┤    MongoDB      │  │  │
│  │  │                  │    │                  │  │  │
│  │  │  Port: 8888      │    │  Port: 27017    │  │  │
│  │  │  Spark UI: 4040  │    │                  │  │  │
│  │  └────────┬─────────┘    └────────┬─────────┘  │  │
│  │           │                       │            │  │
│  └───────────┼───────────────────────┼────────────┘  │
│              │                       │                │
│              ▼                       ▼                │
│      ┌──────────────┐        ┌─────────────┐        │
│      │   Volumes    │        │   Volumes   │        │
│      │  ./data      │        │ mongodb_data│        │
│      │  ./notebooks │        └─────────────┘        │
│      │  ./load.ipynb│                                │
│      └──────────────┘                                │
│                                                        │
└────────────────────────────────────────────────────────┘
        ▲              ▲               ▲
        │              │               │
    Port 8888      Port 4041      Port 27017
        │              │               │
        └──────────────┴───────────────┘
                Browser Access
```

---

## ✅ Critères de Réussite du Workshop

À la fin du workshop, vous devez avoir :

1. ✅ Créé le `Dockerfile` pour Jupyter avec PySpark
2. ✅ Créé le fichier `requirements.txt` avec toutes les dépendances
3. ✅ Créé le `docker-compose.yml` orchestrant Jupyter et MongoDB
4. ✅ Lancé les deux conteneurs avec succès
5. ✅ Accédé à JupyterLab via http://localhost:8888
6. ✅ Chargé des données CSV dans un DataFrame pandas
7. ✅ Inséré des données dans MongoDB
8. ✅ Vérifié les données dans MongoDB via mongosh
9. ✅ Utilisé PySpark pour analyser les données
10. ✅ Compris la communication entre conteneurs via le réseau Docker

---

## 🎓 Concepts Docker Appris

### Dockerfile
- ✅ Utilisation d'images de base spécialisées
- ✅ Gestion des utilisateurs (root vs user)
- ✅ Installation de dépendances système et Python
- ✅ Copie de fichiers avec permissions appropriées
- ✅ Exposition de ports multiples
- ✅ Configuration de la commande de démarrage

### Docker Compose
- ✅ Définition de services multiples
- ✅ Build vs image (quand construire vs utiliser une image)
- ✅ Montage de volumes (bind mounts)
- ✅ Volumes nommés pour la persistance
- ✅ Configuration des réseaux personnalisés
- ✅ Gestion des dépendances entre services
- ✅ Variables d'environnement

### Réseaux Docker
- ✅ Communication inter-conteneurs par nom
- ✅ Résolution DNS automatique
- ✅ Isolation réseau

### Volumes
- ✅ Partage bidirectionnel hôte-conteneur
- ✅ Persistance des données
- ✅ Volumes nommés vs bind mounts

---

## 🏆 Défis Bonus

Une fois le workshop terminé, essayez ces défis :

### Défi 1 : Ajouter l'Authentification à Jupyter
Modifiez le Dockerfile pour activer l'authentification :

```dockerfile
# Remplacer la dernière ligne par :
CMD ["start-notebook.sh", "--NotebookApp.token='votre-token'"]
```

### Défi 2 : Ajouter PostgreSQL
Ajoutez un service PostgreSQL au docker-compose.yml :

```yaml
postgres:
  image: postgres:15-alpine
  environment:
    POSTGRES_PASSWORD: password
    POSTGRES_DB: analytics
  ports:
    - "5432:5432"
  networks:
    - dataflow-insight-net
```

### Défi 3 : Optimiser l'Image Docker
Utilisez une image multi-stage pour réduire la taille :

```dockerfile
# Build stage
FROM jupyter/pyspark-notebook:spark-3.5.0 as builder
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Runtime stage
FROM jupyter/pyspark-notebook:spark-3.5.0
COPY --from=builder /opt/conda /opt/conda
```

### Défi 4 : Ajouter un Dashboard
Ajoutez un service Streamlit pour visualiser les données MongoDB

### Défi 5 : Automatiser le Chargement
Créez un script Python qui charge automatiquement les données au démarrage

### Défi 6 : Monitoring
Ajoutez MongoDB Express pour une interface web de MongoDB :

```yaml
mongo-express:
  image: mongo-express
  ports:
    - "8081:8081"
  environment:
    ME_CONFIG_MONGODB_SERVER: mongodb
  networks:
    - dataflow-insight-net
```

---

## 📚 Ressources Supplémentaires

- [Documentation Docker](https://docs.docker.com/)
- [Documentation Docker Compose](https://docs.docker.com/compose/)
- [Documentation Jupyter](https://jupyter-docker-stacks.readthedocs.io/)
- [Documentation PySpark](https://spark.apache.org/docs/latest/api/python/)
- [Documentation MongoDB](https://www.mongodb.com/docs/)
- [Documentation PyMongo](https://pymongo.readthedocs.io/)

---

## 💡 Conseils et Bonnes Pratiques

### Développement
- 🔄 Utilisez `--build` pour reconstruire après modification du Dockerfile
- 📝 Gardez `requirements.txt` à jour
- 💾 Sauvegardez régulièrement vos notebooks
- 🧹 Nettoyez les volumes et images inutilisés régulièrement

### Sécurité
- 🔒 Ne désactivez jamais l'authentification en production
- 🔑 Utilisez des variables d'environnement pour les secrets
- 👤 Exécutez toujours en tant qu'utilisateur non-root quand possible
- 🌐 Ne exposez pas les ports sensibles publiquement

### Performance
- ⚡ Utilisez `--no-cache-dir` avec pip pour réduire la taille des images
- 📦 Ordonnez les instructions Dockerfile du moins au plus changeant
- 💿 Utilisez des volumes nommés pour les données importantes
- 🎯 Limitez les ressources si nécessaire (CPU, RAM)

---

Bon workshop ! 🚀🐳📊
