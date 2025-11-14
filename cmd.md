### Docker Commandes

```bash
# --- IMAGE MANAGEMENT ---

# Creates an Image using the Dockerfile in the current directory
docker build -t <name> .

# Lists all local Images
docker images

# Downloads an Image from a registry
docker pull <image>

# Removes a local Image
docker rmi <image>

# --- CONTAINER CONTROL ---

# Creates and starts a Container in the foreground (default)
docker run <image>

# Creates and starts a Container in the Background (-d), mapping ports (-p)
docker run -d -p 8080:80 <image>

# Shows only Running Containers (use often after -d)
docker ps

# Shows All Containers (running or stopped)
docker ps -a

# Gracefully stops a running Container
docker stop <name>

# Starts a previously stopped Container
docker start <name>

# Removes a stopped Container permanently
docker rm <name>
# --- DOCKER COMPOSE WORKFLOW ---

# Standard start/restart for configuration changes (YAML only)
# Automatically recreates containers if ports, envs, or volumes changed.
docker compose up -d

# Forces a rebuild of images and restarts services (MANDATORY after Dockerfile changes)
docker compose up --build -d

# Stops and removes all containers, networks, and resources (Cleanup)
docker compose down

# --- DEBUGGING & INSPECTION ---

# Opens an interactive shell inside a running Container
docker exec -it <name> bash

# Views the Container's output in real-time (for monitoring background processes)
docker logs -f <name>

# Finds the physical location (Mountpoint) of stored Volume data on the host disk
docker volume inspect <volume_name>

# Cleans up all unused resources (stopped containers, unused images, networks)
docker system prune