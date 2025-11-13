# DataFlow Insight - Configuration Docker

Ce projet configure un environnement de data science avec Jupyter Notebook, PySpark et MongoDB.

---

## 📋 Architecture du Projet

Le projet est composé de deux services principaux :
1. **MongoDB** - Base de données NoSQL pour stocker les données
2. **Jupyter Notebook** - Environnement de développement avec PySpark pour l'analyse de données

---

## 📄 Dockerfile

Le Dockerfile crée une image personnalisée basée sur Jupyter avec PySpark.

```dockerfile
# Image de base : Jupyter avec PySpark 3.5.0 préinstallé
FROM jupyter/pyspark-notebook:spark-3.5.0

# Passage en mode root pour installer des paquets système
USER root

# Installation des outils MongoDB et dépendances système
RUN apt-get update && apt-get install -y \
    wget \              # Outil de téléchargement
    curl \              # Outil de transfert de données
    && rm -rf /var/lib/apt/lists/*  # Nettoyage du cache pour réduire la taille de l'image

# Retour à l'utilisateur jovyan (utilisateur par défaut de Jupyter)
USER $NB_UID

# Définition du répertoire de travail
WORKDIR /home/jovyan/work

# Copie du fichier des dépendances Python
COPY requirements.txt .

# Installation des dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie des fichiers du projet avec les bonnes permissions
COPY --chown=$NB_UID:$NB_GID . .

# Exposition du port Jupyter Notebook
EXPOSE 8888

# Exposition du port Spark UI (interface de monitoring Spark)
EXPOSE 4040

# Commande de démarrage : lance Jupyter sans authentification
CMD ["start-notebook.sh", "--NotebookApp.token=''", "--NotebookApp.password=''"]
```

### 🔍 Explication des instructions :

- **FROM** : Utilise l'image officielle Jupyter avec PySpark préinstallé
- **USER root** : Passe en mode administrateur pour installer des packages système
- **RUN apt-get** : Installe wget et curl pour télécharger des fichiers
- **USER $NB_UID** : Revient à l'utilisateur non-privilégié pour la sécurité
- **WORKDIR** : Définit `/home/jovyan/work` comme répertoire de travail
- **COPY requirements.txt** : Copie le fichier des dépendances Python
- **RUN pip install** : Installe les packages Python listés dans requirements.txt
- **COPY --chown** : Copie tous les fichiers du projet avec les bonnes permissions
- **EXPOSE** : Documente les ports utilisés (8888 pour Jupyter, 4040 pour Spark UI)
- **CMD** : Démarre Jupyter sans mot de passe (à modifier en production !)

---

## 🐳 Docker Compose

Le fichier `docker-compose.yml` orchestre les services et définit l'architecture multi-conteneurs.

```yaml
version: '3.8'

services:
  # Service MongoDB
  mongodb:
    image: mongo:7.0                          # Image MongoDB version 7.0
    container_name: dataflow-insight-mongo    # Nom du conteneur
    ports:
      - "27017:27017"                         # Port MongoDB (host:container)
    environment:
      MONGO_INITDB_DATABASE: dataflow_insight # Nom de la base de données initiale
    volumes:
      - mongodb_data:/data/db                 # Persistance des données MongoDB
    networks:
      - dataflow-insight-net                  # Réseau partagé

  # Service Jupyter avec PySpark
  jupyter:
    build: .                                  # Construction depuis le Dockerfile local
    container_name: dataflow-insight-jupyter  # Nom du conteneur
    ports:
      - "8888:8888"                           # Port Jupyter Notebook
      - "4041:4040"                           # Port Spark UI (redirigé vers 4041 sur l'hôte)
    environment:
      - JUPYTER_ENABLE_LAB=yes                # Active JupyterLab (interface moderne)
      - GRANT_SUDO=yes                        # Autorise les commandes sudo dans le conteneur
    volumes:
      - ./data:/home/jovyan/work/data                     # Dossier data partagé
      - ./load.ipynb:/home/jovyan/work/load.ipynb         # Notebook principal
      - ./notebooks:/home/jovyan/work/notebooks           # Dossier notebooks partagé
    depends_on:
      - mongodb                               # Démarre MongoDB avant Jupyter
    networks:
      - dataflow-insight-net                  # Réseau partagé avec MongoDB

# Déclaration des volumes persistants
volumes:
  mongodb_data:                               # Volume pour stocker les données MongoDB

# Déclaration des réseaux
networks:
  dataflow-insight-net:                       # Réseau bridge pour la communication inter-conteneurs
    driver: bridge
```

### 🔍 Explication de la configuration :

#### **Service MongoDB**
- **image: mongo:7.0** : Utilise l'image officielle MongoDB version 7.0
- **ports: "27017:27017"** : Expose MongoDB sur le port par défaut
- **environment** : Crée automatiquement une base de données nommée `dataflow_insight`
- **volumes** : Persiste les données dans un volume Docker nommé `mongodb_data`
- **networks** : Connecté au réseau `dataflow-insight-net` pour communiquer avec Jupyter

#### **Service Jupyter**
- **build: .** : Construit l'image à partir du Dockerfile dans le répertoire courant
- **ports** : 
  - `8888:8888` → Accès à Jupyter via http://localhost:8888
  - `4041:4040` → Accès à Spark UI via http://localhost:4041
- **environment** :
  - `JUPYTER_ENABLE_LAB=yes` : Active l'interface JupyterLab moderne
  - `GRANT_SUDO=yes` : Permet d'exécuter des commandes root si nécessaire
- **volumes** : Montage bidirectionnel pour :
  - Partager les données entre l'hôte et le conteneur
  - Éditer les notebooks directement depuis l'hôte
  - Persister le travail même si le conteneur est supprimé
- **depends_on** : Assure que MongoDB démarre avant Jupyter
- **networks** : Permet à Jupyter de se connecter à MongoDB via le nom `mongodb`

#### **Volumes**
- **mongodb_data** : Volume géré par Docker pour persister les données de MongoDB

#### **Networks**
- **dataflow-insight-net** : Réseau de type bridge permettant aux conteneurs de communiquer entre eux par leur nom

---

## 🚀 Utilisation

### Démarrer les services
```bash
docker-compose up -d
```

### Accéder aux services
- **Jupyter Notebook** : http://localhost:8888
- **Spark UI** : http://localhost:4041 (quand Spark est actif)
- **MongoDB** : localhost:27017

### Connexion à MongoDB depuis Jupyter
Dans vos notebooks, utilisez l'URL de connexion :
```python
mongo_url = "mongodb://mongodb:27017/dataflow_insight"
```

### Arrêter les services
```bash
docker-compose down
```

### Arrêter et supprimer les données
```bash
docker-compose down -v
```

---

## 📁 Structure du Projet

```
.
├── Dockerfile              # Configuration de l'image Jupyter personnalisée
├── docker-compose.yml      # Orchestration des services
├── requirements.txt        # Dépendances Python
├── load.ipynb              # Notebook principal
├── data/                   # Dossier des données (partagé)
└── notebooks/              # Dossier des notebooks (partagé)
```

---

## ⚠️ Notes de Sécurité

- **Authentification désactivée** : Le Jupyter démarre sans mot de passe (`--NotebookApp.token=''`)
  - ⚠️ **À ne pas utiliser en production !**
  - Pour activer l'authentification, supprimez cette option du CMD dans le Dockerfile
  
- **Sudo activé** : `GRANT_SUDO=yes` permet des commandes root dans le conteneur
  - Utile pour le développement, mais risqué en production

---

## 🔧 Personnalisation

### Ajouter des packages Python
Éditez le fichier `requirements.txt` et reconstruisez l'image :
```bash
docker-compose build
docker-compose up -d
```

### Modifier les ports
Changez les ports dans `docker-compose.yml`, par exemple :
```yaml
ports:
  - "9999:8888"  # Jupyter accessible sur le port 9999
```

### Ajouter des variables d'environnement
Ajoutez-les dans la section `environment` du service concerné :
```yaml
environment:
  - MA_VARIABLE=valeur
```