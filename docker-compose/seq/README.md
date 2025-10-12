# Seq Docker Compose Setup

This guide explains how to deploy Seq (datalust/seq) using Docker Compose and Traefik, including steps for Portainer deployment and best practices for data persistence and security.

## Prerequisites
- Docker and Docker Compose installed on your host
- Portainer installed and running (see https://www.portainer.io/installation/)
- Traefik reverse proxy deployed and running on the `traefik` Docker network
- DNS record for `seq.cloudtorq.io` pointing to your host's public IP
- Directory `/mnt/storage/seq-data` exists and is writable by Docker

## Directory Structure
```
/home/gknowd/homelab/docker-compose/seq/docker-compose.yml
/mnt/storage/seq-data                # Seq data will be stored here
```

## docker-compose.yml Example
```
version: '3.8'
services:
  seq:
    image: datalust/seq:latest
    container_name: seq
    restart: unless-stopped
    volumes:
  - /mnt/storage/seq-data:/data
    environment:
      - ACCEPT_EULA=Y
      - SEQ_BASEURI=https://seq.cloudtorq.io
    networks:
      - traefik
    labels:
      - "traefik.enable=true"
      - "traefik.docker.network=traefik"
      - "traefik.http.routers.seq.rule=Host(`seq.cloudtorq.io`)"
      - "traefik.http.routers.seq.entrypoints=websecure"
      - "traefik.http.routers.seq.tls=true"
      - "traefik.http.routers.seq.tls.certresolver=letsencrypt"
      - "traefik.http.services.seq.loadbalancer.server.port=80"
      - "traefik.http.routers.seq-redirect.rule=Host(`seq.cloudtorq.io`)"
      - "traefik.http.routers.seq-redirect.entrypoints=web"
      - "traefik.http.routers.seq-redirect.middlewares=redirect-to-https"
      - "traefik.http.middlewares.redirect-to-https.redirectscheme.scheme=https"
networks:
  traefik:
    external: true
```

## Steps to Deploy with Portainer

### 1. Prepare the Data Directory
Ensure the data directory exists and is owned by the user running Docker:
```bash
sudo mkdir -p /mnt/storage/seq-data
sudo chown 1000:1000 /mnt/storage/seq-data
```

### 2. Open Portainer
- Go to your Portainer web UI (e.g., http://your-server:9000)
- Log in with your credentials

### 3. Deploy the Stack
1. In Portainer, go to **Stacks** > **Add stack**
2. Name your stack (e.g., `seq`)
3. Copy and paste the contents of `docker-compose.yml` into the web editor
4. Deploy the stack

### 4. Configure DNS
- Ensure your DNS provider has an A or CNAME record for `seq.cloudtorq.io` pointing to your host's public IP.

### 5. Access Seq
- Once deployed and DNS has propagated, access Seq at:  
  `https://seq.cloudtorq.io`

## Security Notes
- The Seq service is exposed via HTTPS using Traefik and Let's Encrypt.
- Data is persisted in `/home/gknowd/seq-data` for durability.
- For production, consider restricting access to Seq and securing Traefik dashboard.

## Troubleshooting
- Check Portainer and container logs for errors if Seq does not start.
- Ensure the external Docker network `traefik` exists and is attached to Traefik and Seq.
- Make sure `/home/gknowd/seq-data` is writable by the container (UID 1000 by default).
- For DNS/SSL issues, verify your DNS records and Traefik configuration.

## References
- [Seq Documentation](https://docs.datalust.co/docs)
- [Seq Docker Hub](https://hub.docker.com/r/datalust/seq)
- [Traefik Documentation](https://doc.traefik.io/traefik/)
- [Portainer Documentation](https://docs.portainer.io/)

---

For further customization or questions, feel free to ask!
