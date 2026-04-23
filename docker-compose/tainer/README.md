# Tainer Docker Compose Setup

This guide explains how to deploy Tainer using Docker Compose with Traefik reverse proxy, HTTPS certificates from Let's Encrypt, and persistent host storage.

## Prerequisites

- Docker and Docker Compose installed on your host
- Traefik deployed and attached to an external Docker network named `traefik`
- DNS record for `tainer.cloudtorq.io` pointing to your host public IP
- Host directory `/mnt/storage/tainer-data` created and writable by Docker
- (Optional) Portainer installed for stack-based management

## Directory Structure

```text
/home/gknowd/Projects/homelab/docker-compose/tainer/
  docker-compose.yml
  README.md

/mnt/storage/tainer-data   # persistent Tainer application data
```

## Current Compose Configuration

The stack in `docker-compose.yml` is configured to:

- Run image `tainersh/tainer:latest`
- Persist data with bind mount `/mnt/storage/tainer-data:/app/data`
- Publish via Traefik at `https://tainer.cloudtorq.io`
- Redirect HTTP to HTTPS
- Request certificates using Traefik resolver `letsencrypt`

## Quick Start (CLI)

1. Create persistent storage path:

```bash
sudo mkdir -p /mnt/storage/tainer-data
sudo chown -R 1001:1001 /mnt/storage/tainer
```

2. Ensure the external Traefik network exists:

```bash
docker network ls | grep traefik || docker network create traefik
```

3. Change into the stack directory:

```bash
cd /Users/gknowd/Projects/homelab/docker-compose/tainer
```

4. Validate the compose file:

```bash
docker compose config
```

5. Start Tainer:

```bash
docker compose up -d
```

6. Check service health:

```bash
docker compose ps
docker compose logs -f tainer
```

7. Open in browser:

- `https://tainer.cloudtorq.io`

## Deployment with Portainer

1. Open Portainer UI.
2. Go to **Stacks** -> **Add stack**.
3. Name the stack (example: `tainer`).
4. Paste the contents of `docker-compose.yml` from this directory.
5. Deploy the stack.
6. Confirm the container is running and attached to the `traefik` network.

## Traefik Labels Used

The compose file includes these routing labels:

- `traefik.enable=true`
- `traefik.docker.network=traefik`
- `traefik.http.routers.tainer.rule=Host(`tainer.cloudtorq.io`)`
- `traefik.http.routers.tainer.entrypoints=websecure`
- `traefik.http.routers.tainer.tls=true`
- `traefik.http.routers.tainer.tls.certresolver=letsencrypt`
- `traefik.http.services.tainer.loadbalancer.server.port=3000`
- HTTP redirect router and middleware for HTTPS enforcement

## Operations

Start:

```bash
docker compose up -d
```

Stop:

```bash
docker compose down
```

Restart:

```bash
docker compose restart
```

Update image:

```bash
docker compose pull
docker compose up -d
```

## Backup and Restore

Backup data directory:

```bash
sudo tar -czf /tmp/tainer-data-backup-$(date +%F).tar.gz /mnt/storage/tainer-data
```

Restore data directory:

```bash
sudo tar -xzf /tmp/tainer-data-backup-YYYY-MM-DD.tar.gz -C /
```

After restore, restart stack:

```bash
docker compose restart tainer
```

## Troubleshooting

- Container not starting:
  - Run `docker compose logs tainer`
  - Verify `/mnt/storage/tainer-data` exists and is writable

- 404 or bad gateway from Traefik:
  - Confirm Tainer is on `traefik` network
  - Confirm service label port is `3000`
  - Verify Traefik container is healthy

- TLS certificate not issued:
  - Confirm DNS for `tainer.cloudtorq.io` points to your host
  - Verify Traefik `letsencrypt` resolver is configured and working
  - Check Traefik logs for ACME errors

- Data not persisting:
  - Verify bind mount path is exactly `/mnt/storage/tainer-data:/app/data`
  - Check host filesystem permissions

## Security Notes

- Keep Traefik dashboard protected and not publicly exposed without auth.
- Restrict who can access the Tainer URL.
- Keep Docker and images updated regularly.
- Back up `/mnt/storage/tainer-data` on a schedule.

## References

- [Traefik Documentation](https://doc.traefik.io/traefik/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Portainer Documentation](https://docs.portainer.io/)
- [Docker Hub: tainersh/tainer](https://hub.docker.com/r/tainersh/tainer)
