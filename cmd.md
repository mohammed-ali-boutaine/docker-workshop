## basics commandes

**Images**

```bash
# download image from docker hub
docker pull <image>

# list all images
docker images

# remove an image 
docker rmi <image>

# build image from dockerfile
docker build -t <name> .
```

**Containers**

```bash
# show running containers
docker run <image>

# show running containers
docker ps 
# show all containers (running or sptoped)
docker ps -a

# Stop a running container
docker stop <container>

# Start a stopped container
ocker start <container>

# restart container
docker restart <container>

# Remove container
docker rm <container>

# Enter inside container

docker exec -it <container> bash
```