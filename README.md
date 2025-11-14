# Docker Workshop

## Table des matières
1. [Introduction à Docker](#introduction-à-docker)
2. [Concepts fondamentaux](#concepts-fondamentaux)
3. [Avantages de Docker](#avantages-de-docker)
4. [Cas d'usage](#cas-dusage)
5. [Composants Docker](#composants-docker)

---

## Introduction à Docker

Docker est une plateforme open-source qui permet de créer, déployer et exécuter des applications dans des **conteneurs**. Un conteneur est une unité standardisée de logiciel qui empaquette le code et toutes ses dépendances, permettant à l'application de s'exécuter rapidement et de manière fiable d'un environnement informatique à un autre.

---

## Concepts fondamentaux

### Qu'est-ce que la conteneurisation ?

La conteneurisation est une méthode de virtualisation légère qui permet d'exécuter plusieurs applications isolées sur un même système d'exploitation hôte. Contrairement aux machines virtuelles, les conteneurs partagent le noyau du système d'exploitation, ce qui les rend plus légers et plus rapides.

### Machine Virtuelle (VM)

Une **Machine Virtuelle (VM)** est une émulation complète d'un système informatique qui fournit les fonctionnalités d'un ordinateur physique. Chaque VM inclut :
- Un système d'exploitation complet (OS invité)
- Des applications et leurs dépendances
- Des ressources virtuelles (CPU, RAM, disque, réseau)
- Un hyperviseur pour gérer la virtualisation

**Caractéristiques :**
- Isolation complète au niveau système
- Chaque VM nécessite son propre OS
- Démarrage lent (plusieurs minutes)
- Consommation importante de ressources
- Utilisées pour isoler des environnements complets

### Namespaces (Espaces de noms)

Les **namespaces** sont une fonctionnalité du noyau Linux qui fournit l'isolation nécessaire pour créer des conteneurs. Chaque namespace isole un aspect spécifique du système, permettant à un processus d'avoir sa propre vue des ressources système.

#### Types de namespaces et leurs rôles :

1. **PID (Process ID)** : Isole les identifiants de processus
   - Chaque conteneur a sa propre numérotation de processus
   - Le processus principal du conteneur voit son PID comme 1

2. **NET (Network)** : Isole les interfaces réseau
   - Chaque conteneur possède sa propre interface réseau, adresse IP et ports
   - Permet à plusieurs conteneurs d'utiliser le même port

3. **MNT (Mount)** : Isole les points de montage du système de fichiers
   - Chaque conteneur a sa propre arborescence de fichiers
   - Modifications isolées sans affecter l'hôte

4. **UTS (Unix Timesharing System)** : Isole le hostname et le nom de domaine
   - Chaque conteneur peut avoir son propre nom d'hôte
   - Utile pour identifier les conteneurs

5. **IPC (Inter-Process Communication)** : Isole la communication inter-processus
   - Sépare les files de messages, sémaphores et mémoire partagée
   - Les processus d'un conteneur ne peuvent pas communiquer avec ceux d'un autre

6. **USER** : Isole les identifiants utilisateurs et groupes
   - Permet de mapper les utilisateurs du conteneur aux utilisateurs de l'hôte
   - Renforce la sécurité en limitant les privilèges

### Docker vs Machines Virtuelles

![Architecture VM vs Docker](./public/demo.png)

| Caractéristique | Docker (Conteneurs) | Machines Virtuelles |
|----------------|---------------------|---------------------|
| **Taille** | Léger (Mo) | Lourd (Go) |
| **Démarrage** | Secondes | Minutes |
| **Isolation** | Niveau processus | Niveau système |
| **Performance** | Native | Overhead de virtualisation |
| **Portabilité** | Très élevée | Moyenne |

---

## Avantages de Docker

### 1. **Portabilité**
- Les conteneurs fonctionnent de manière identique sur n'importe quelle infrastructure (local, cloud, hybride)
- "Build once, run anywhere" - Construisez une fois, exécutez partout

### 2. **Isolation**
- Chaque conteneur s'exécute de manière isolée
- Évite les conflits entre dépendances et versions

### 3. **Légèreté**
- Les conteneurs partagent le noyau du système d'exploitation
- Démarrage rapide et utilisation optimale des ressources

### 4. **Scalabilité**
- Facile à dupliquer et à distribuer
- Idéal pour les architectures microservices

### 5. **Versioning et réutilisabilité**
- Les images Docker peuvent être versionnées
- Partage facile via Docker Hub ou registres privés

### 6. **Environnements cohérents**
- Élimine le problème "ça marche sur ma machine"
- Même environnement du développement à la production

### 7. **CI/CD simplifié**
- Intégration facile dans les pipelines DevOps
- Tests automatisés dans des environnements reproductibles

---

## Cas d'usage

### 1. **Développement local**
- Créer des environnements de développement reproductibles
- Tester avec différentes versions de langages/frameworks

### 2. **Microservices**
- Déployer et gérer des architectures distribuées
- Chaque service dans son propre conteneur

### 3. **Intégration et déploiement continus (CI/CD)**
- Tests automatisés dans des environnements isolés
- Déploiements rapides et fiables

### 4. **Migration vers le cloud**
- Faciliter la migration d'applications existantes
- Portabilité entre différents fournisseurs cloud

### 5. **Isolation d'applications**
- Exécuter plusieurs versions d'une même application
- Tester sans impacter l'environnement système

---

## Composants Docker

### 1. Docker Daemon

Le **Docker daemon** (ou **dockerd**) est le processus d'arrière-plan persistant qui gère toutes les opérations Docker sur une machine hôte. Il s'agit du composant serveur de l'architecture Docker, responsable de l'écoute des commandes du client Docker (ligne de commande), de la construction, de l'exécution et de la gestion des objets Docker tels que les conteneurs, les images, les réseaux et les volumes. En bref, lorsque vous tapez une commande Docker, le client l'envoie au Docker daemon, qui exécute ensuite la requête.

---

### 2. Images Docker

Une **image Docker** est un modèle en lecture seule qui contient tout le nécessaire pour exécuter une application :
- Code source
- Bibliothèques
- Dépendances
- Variables d'environnement
- Fichiers de configuration

#### Caractéristiques des images :
- **Immuables** : une fois créées, elles ne changent pas
- **Composées de couches** : chaque modification crée une nouvelle couche
- **Partageables** : disponibles sur Docker Hub ou registres privés
- **Versionnées** : utilisation de tags (ex: `nginx:latest`, `node:18-alpine`)

---

### 2. Conteneurs Docker

Un **conteneur** est une instance exécutable d'une image Docker. C'est l'environnement isolé dans lequel votre application s'exécute.

#### Caractéristiques des conteneurs :
- **Éphémères** : peuvent être créés, démarrés, arrêtés et supprimés facilement
- **Isolés** : processus séparés avec leur propre système de fichiers
- **Légers** : partagent le noyau de l'OS hôte
- **Multiples** : plusieurs conteneurs peuvent être créés à partir d'une même image

---

### 3. Dockerfile

Un **Dockerfile** est un fichier texte contenant une série d'instructions pour créer automatiquement une image Docker.

#### Instructions principales :
- **FROM** : définit l'image de base
- **WORKDIR** : définit le répertoire de travail
- **COPY** / **ADD** : copie des fichiers dans l'image
- **RUN** : exécute des commandes lors de la construction
- **ENV** : définit des variables d'environnement
- **EXPOSE** : documente les ports exposés
- **CMD** / **ENTRYPOINT** : commande à exécuter au démarrage du conteneur

---

### 4. Volumes Docker

Les **volumes** sont le mécanisme préféré pour persister les données générées et utilisées par les conteneurs Docker. Contrairement aux conteneurs qui sont éphémères, les volumes permettent de conserver les données même après la suppression d'un conteneur. Il existe trois types de stockage : les volumes (gérés par Docker, recommandés), les bind mounts (montage d'un répertoire de l'hôte), et les tmpfs mounts (stockage en mémoire sur Linux). Les volumes offrent une performance optimale et facilitent le partage de données entre conteneurs.

---

### 5. Réseaux Docker

Les **réseaux Docker** permettent aux conteneurs de communiquer entre eux et avec le monde extérieur. Docker propose plusieurs types de réseaux : bridge (par défaut, réseau privé interne), host (utilise directement le réseau de l'hôte), none (aucun réseau), overlay (pour la communication multi-hôtes avec Swarm), et macvlan (attribue une adresse MAC au conteneur). Les conteneurs connectés au même réseau peuvent communiquer entre eux en utilisant simplement leurs noms de conteneur.

---

### 6. Docker Compose

**Docker Compose** est un outil qui permet de définir et d'exécuter des applications multi-conteneurs avec un fichier YAML.

#### Pourquoi Docker Compose ?
- Simplification de la gestion d'applications complexes
- Configuration déclarative (Infrastructure as Code)
- Environnements reproductibles
- Orchestration locale

---

### 7. Docker CLI (Command Line Interface)

Le **Docker CLI** est l'interface en ligne de commande qui permet d'interagir avec Docker Engine pour gérer les conteneurs, images, volumes et réseaux. Il offre une interface unifiée pour toutes les opérations Docker, communique avec Docker Engine via une API REST, et est disponible sur Windows, macOS et Linux. Le CLI est extensible avec des plugins et suit une structure de commandes simple : `docker [OPTIONS] COMMAND [ARG...]`.

---

### 8. Docker Hub

**Docker Hub** est le registre public officiel de Docker où vous pouvez trouver et partager des millions d'images de conteneurs. Il héberge des images officielles vérifiées (nginx, postgres, redis, etc.) et permet aux développeurs de publier leurs propres images publiques ou privées. Docker Hub facilite le partage et la distribution d'applications conteneurisées à travers des fonctionnalités comme les builds automatiques depuis GitHub/Bitbucket et les intégrations CI/CD.

---

## Ressources supplémentaires

- [Documentation officielle Docker](https://docs.docker.com/)
- [Docker Hub](https://hub.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Best Practices Dockerfile](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)

---

## Conclusion

Docker est un outil puissant qui simplifie le développement, le déploiement et la gestion d'applications. En maîtrisant les concepts d'**images**, de **conteneurs**, de **Dockerfile**, de **volumes**, de **réseaux** et de **Docker Compose**, vous serez en mesure de créer des environnements reproductibles et scalables pour vos projets.

Bonne pratique avec Docker !
