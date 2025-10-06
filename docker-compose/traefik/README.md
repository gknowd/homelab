# Traefik Docker Compose Deployment Guide

This guide provides comprehensive instructions for deploying Traefik using the provided `docker-compose.yml` file, including best practices and steps for deploying with Portainer.

## Prerequisites
- Docker and Docker Compose installed on your host
- Portainer installed and running (see https://www.portainer.io/installation/)
- A Docker network named `traefik` created and set as external
- DNS records for your domain (e.g., `traefik.cloudtorq.io`) pointing to your host's public IP
- Cloudflare API token with DNS edit permissions for your domain
- Directory `/home/gknowd/letsencrypt` exists and is writable by Docker

## Directory Structure
```
/home/gknowd/homelab/docker-compose/traefik/docker-compose.yml
/home/gknowd/letsencrypt                # Let's Encrypt data will be stored here
```

## docker-compose.yml Example
```
services:
  traefik:
    image: traefik:v3.5
    container_name: traefik
    restart: unless-stopped
    networks:
      - traefik
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - /home/gknowd/letsencrypt:/letsencrypt
    environment:
      CLOUDFLARE_API_TOKEN: "${CLOUDFLARE_API_TOKEN}"
      CF_API_TOKEN: "${CLOUDFLARE_API_TOKEN}"
      CF_DNS_API_TOKEN: "${CLOUDFLARE_API_TOKEN}"
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.traefik-dashboard.rule=Host(`traefik.cloudtorq.io`)"
      - "traefik.http.routers.traefik-dashboard.entrypoints=websecure"
      - "traefik.http.routers.traefik-dashboard.tls.certresolver=letsencrypt"
      - "traefik.http.routers.traefik-dashboard.service=api@internal"
    command:
      - "--providers.docker=true"
      - "--providers.docker.exposedByDefault=false"
      - "--api.dashboard=true"
      - "--certificatesresolvers.letsencrypt.acme.dnschallenge=true"
      - "--certificatesresolvers.letsencrypt.acme.dnschallenge.provider=cloudflare"
      - "--certificatesresolvers.letsencrypt.acme.email=greg@cloudtorq.com"
      - "--certificatesresolvers.letsencrypt.acme.storage=/letsencrypt/acme.json"
      - "--entrypoints.web.address=:80"
      - "--entrypoints.web.http.redirections.entrypoint.to=websecure"
      - "--entrypoints.web.http.redirections.entrypoint.scheme=https"
      - "--entrypoints.websecure.address=:443"
      - "--entrypoints.websecure.http.tls=true"
      - "--entrypoints.websecure.http.tls.certResolver=letsencrypt"
      - "--entrypoints.websecure.http.tls.domains[0].main=cloudtorq.io"
      - "--entrypoints.websecure.http.tls.domains[0].sans=*.cloudtorq.io"

networks:
  traefik:
    external: true
```

## Steps to Deploy with Portainer

### 1. Prepare the Let's Encrypt Directory
Ensure the directory exists and is owned by the user running Docker:
```bash
sudo mkdir -p /home/gknowd/letsencrypt
sudo chown 1000:1000 /home/gknowd/letsencrypt
```

### 2. Create the External Docker Network (if not already created)
```bash
docker network create traefik
```

### 3. Set Up Cloudflare API Token
- Create a Cloudflare API token with `Zone:DNS:Edit` permissions for your domain.
- In Portainer, you will set the environment variable `CLOUDFLARE_API_TOKEN` when deploying the stack.

### 4. Open Portainer
- Go to your Portainer web UI (e.g., http://your-server:9000)
- Log in with your credentials

### 5. Deploy the Stack
1. In Portainer, go to **Stacks** > **Add stack**
2. Name your stack (e.g., `traefik`)
3. Copy and paste the contents of `docker-compose.yml` into the web editor
4. Under **Environment variables**, add:
    - `CLOUDFLARE_API_TOKEN` (your Cloudflare API token)
5. Deploy the stack

### 6. Configure DNS
- Ensure your DNS provider (Cloudflare) has an A or CNAME record for `traefik.cloudtorq.io` pointing to your host's public IP.

### 7. Access the Traefik Dashboard
- Once deployed and DNS has propagated, access the dashboard at:  
  `https://traefik.cloudtorq.io`

## Security Notes
- The dashboard is exposed without authentication. For production, consider adding authentication middleware.
- The Let's Encrypt data is stored on the host for certificate persistence.
- Only containers with explicit Traefik labels will be routed.

## Troubleshooting
- Check Portainer and container logs for errors if Traefik does not start.
- Ensure the external Docker network `traefik` exists and is attached to other services you want Traefik to route.
- Make sure `/home/gknowd/letsencrypt` is writable by the container (UID 1000 by default).
- For DNS/SSL issues, verify your Cloudflare API token and DNS records.

## References
- [Traefik Documentation](https://doc.traefik.io/traefik/)
- [Traefik Docker Image](https://hub.docker.com/_/traefik)
- [Portainer Documentation](https://docs.portainer.io/)
- [Let's Encrypt](https://letsencrypt.org/)

---

For further customization or questions, feel free to ask!
