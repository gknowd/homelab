# Loki Docker Compose Setup

This guide explains how to deploy Grafana Loki using Docker Compose, Portainer, and Traefik, with persistent storage and secure HTTPS routing.

## Prerequisites
- Docker and Docker Compose installed on your host
- Portainer installed and running (see https://www.portainer.io/installation/)
- Traefik reverse proxy deployed and running on the `traefik` Docker network
- DNS record for `loki.cloudtorq.io` pointing to your host's public IP
- Directory `/mnt/storage/loki` exists and is writable by Docker

## Directory Structure
```
/home/gknowd/homelab/docker-compose/loki/docker-componse.yaml
/mnt/storage/loki                # Loki data will be stored here
```

## docker-componse.yaml Example
```
version: '3.8'
services:
  loki:
    image: grafana/loki:latest
    container_name: loki
    restart: unless-stopped
    volumes:
      - /mnt/storage/loki:/loki
    command: -config.file=/etc/loki/local-config.yaml
    networks:
      - traefik
    labels:
      - "traefik.enable=true"
      - "traefik.docker.network=traefik"
      - "traefik.http.routers.loki.rule=Host(`loki.cloudtorq.io`)"
      - "traefik.http.routers.loki.entrypoints=websecure"
      - "traefik.http.routers.loki.tls=true"
      - "traefik.http.routers.loki.tls.certresolver=letsencrypt"
      - "traefik.http.services.loki.loadbalancer.server.port=3100"
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://localhost:3100/ready"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 30s
networks:
  traefik:
    external: true
```

## Steps to Deploy with Portainer

### 1. Prepare the Data Directory
Ensure the data directory exists and is owned by the user running Docker:
```bash
sudo mkdir -p /mnt/storage/loki
# Loki runs as UID 10001. Set correct ownership and permissions:
sudo chown -R 10001:10001 /mnt/storage/loki
sudo chmod -R 755 /mnt/storage/loki
```
If you see a permission error like `mkdir /loki/rules: permission denied`, make sure the directory and all subdirectories are owned by UID 10001 and have write permissions.

### 2. Open Portainer
- Go to your Portainer web UI (e.g., http://your-server:9000)
- Log in with your credentials

### 3. Deploy the Stack
1. In Portainer, go to **Stacks** > **Add stack**
2. Name your stack (e.g., `loki`)
3. Copy and paste the contents of `docker-componse.yaml` into the web editor
4. Deploy the stack

### 4. Configure DNS
- Ensure your DNS provider has an A or CNAME record for `loki.cloudtorq.io` pointing to your host's public IP.

### 5. Access Loki
- Once deployed and DNS has propagated, access Loki at:  
  `https://loki.cloudtorq.io`
- You can integrate Loki with Grafana for log visualization and querying.

## Security Notes
- Loki is exposed via HTTPS using Traefik and Let's Encrypt.
- Data is persisted in `/mnt/storage/loki` for durability.
- For production, consider restricting access to Loki and securing Traefik dashboard.

## Troubleshooting
- Check Portainer and container logs for errors if Loki does not start.
- Ensure the external Docker network `traefik` exists and is attached to Traefik and Loki.
- Make sure `/mnt/storage/loki` is writable by the container (UID 1000 by default).
- For DNS/SSL issues, verify your DNS records and Traefik configuration.

## References
- [Loki Documentation](https://grafana.com/docs/loki/latest/)
- [Loki Docker Hub](https://hub.docker.com/r/grafana/loki)
- [Traefik Documentation](https://doc.traefik.io/traefik/)
- [Portainer Documentation](https://docs.portainer.io/)

---

For further customization or questions, feel free to ask!
