# MongoDB Docker Compose Setup

This guide explains how to deploy MongoDB using Docker Compose and manage it with Portainer, using best practices for security and data persistence.

## Prerequisites
- Docker and Docker Compose installed on your host
- Portainer installed and running (see https://www.portainer.io/installation/)
- Directory `/mnt/storage/mongodb` exists on your host and is writable by Docker

## Directory Structure
```
/mnt/storage/mongodb           # MongoDB data will be stored here
/home/gknowd/homelab/docker-compose/mongodb/docker-compose.yml
```

## docker-compose.yml Example
```
version: '3.8'
services:
  mongodb:
    image: mongo:7.0
    container_name: mongodb
    restart: unless-stopped
    ports:
      - 127.0.0.1:27017:27017
    volumes:
      - /mnt/storage/mongodb:/data/db
    healthcheck:
      test: ["CMD", "mongosh", "--eval", "db.adminCommand('ping')"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 30s
```

## Steps to Deploy with Portainer

### 1. Prepare the Data Directory
Ensure the data directory exists and is owned by the user running Docker:
```bash
sudo mkdir -p /mnt/storage/mongodb
sudo chown 999:999 /mnt/storage/mongodb
```

### 2. Open Portainer
- Go to your Portainer web UI (e.g., http://your-server:9000)
- Log in with your credentials

### 3. Deploy the Stack
1. In Portainer, go to **Stacks** > **Add stack**
2. Name your stack (e.g., `mongodb`)
3. Copy and paste the contents of `docker-compose.yml` into the web editor
4. Under **Environment variables**, add:
    - `MONGO_INITDB_ROOT_USERNAME` (choose a strong username)
    - `MONGO_INITDB_ROOT_PASSWORD` (choose a strong password)
5. Deploy the stack

### 4. Verify MongoDB is Running
- Go to **Containers** in Portainer and check that the `mongodb` container is healthy
- You can connect to MongoDB locally on the host with:
  ```bash
  mongosh -u <username> -p <password> --host 127.0.0.1
  ```

## Security Notes
- The MongoDB port is only accessible from localhost for security. If you need remote access, adjust the `ports` section accordingly, but be sure to secure your instance.
- Always use strong credentials for the root user.
- Back up your data directory regularly.

## Troubleshooting
- If the container fails to start, check Portainer logs and ensure `/mnt/storage/mongodb` is writable by UID 999 (the default MongoDB user).
- For permission issues, you may need to adjust ownership or permissions on the data directory.

## References
- [MongoDB Docker Hub](https://hub.docker.com/_/mongo)
- [Portainer Documentation](https://docs.portainer.io/)
- [MongoDB Documentation](https://www.mongodb.com/docs/)

---

For further customization or questions, feel free to ask!
