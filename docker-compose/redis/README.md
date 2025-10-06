# Redis Docker Compose Setup

This guide provides step-by-step instructions for deploying Redis using Docker Compose and managing it with Portainer, following best practices for security and data persistence.

## Prerequisites
- Docker and Docker Compose installed on your host
- Portainer installed and running (see https://www.portainer.io/installation/)
- Directory `/mnt/storage/redis` exists on your host and is writable by Docker

## Directory Structure
```
/mnt/storage/redis                # Redis data will be stored here
/home/gknowd/homelab/docker-compose/redis/docker-compose.yml
```

## docker-compose.yml Example
```
version: '3.8'
services:
  redis:
    image: redis:7.2
    container_name: redis
    command: redis-server --loglevel warning
    restart: unless-stopped
    ports:
      - 127.0.0.1:6379:6379
    volumes:
      - /mnt/storage/redis:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 30s
```

## Steps to Deploy with Portainer

### 1. Prepare the Data Directory
Ensure the data directory exists and is owned by the user running Docker:
```bash
sudo mkdir -p /mnt/storage/redis
sudo chown 999:999 /mnt/storage/redis
```

### 2. Open Portainer
- Go to your Portainer web UI (e.g., http://your-server:9000)
- Log in with your credentials

### 3. Deploy the Stack
1. In Portainer, go to **Stacks** > **Add stack**
2. Name your stack (e.g., `redis`)
3. Copy and paste the contents of `docker-compose.yml` into the web editor
4. Deploy the stack

### 4. Verify Redis is Running
- Go to **Containers** in Portainer and check that the `redis` container is healthy
- You can connect to Redis locally on the host with:
  ```bash
  redis-cli -h 127.0.0.1
  ```

## Security Notes
- The Redis port is only accessible from localhost for security. If you need remote access, adjust the `ports` section accordingly, but be sure to secure your instance (e.g., with a password and/or firewall).
- Back up your data directory regularly.

## Custom Configuration
If you want to use a custom `redis.conf` file:
1. Create your config file at `/mnt/storage/redis/redis.conf`
2. Update the `command` and `volumes` sections in `docker-compose.yml`:
   ```yaml
   command: redis-server /usr/local/etc/redis/redis.conf --loglevel warning
   volumes:
     - /mnt/storage/redis:/data
     - /mnt/storage/redis/redis.conf:/usr/local/etc/redis/redis.conf:ro
   ```

## Troubleshooting
- If the container fails to start, check Portainer logs and ensure `/mnt/storage/redis` is writable by UID 999 (the default Redis user).
- For permission issues, you may need to adjust ownership or permissions on the data directory.

## References
- [Redis Docker Hub](https://hub.docker.com/_/redis)
- [Portainer Documentation](https://docs.portainer.io/)
- [Redis Documentation](https://redis.io/docs/)

---

For further customization or questions, feel free to ask!
