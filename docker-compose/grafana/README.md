**Grafana (Docker Compose)**

- **Location:** [docker-compose/grafana/docker-compose.yml](docker-compose/grafana/docker-compose.yml)

Overview
- This folder provides a Docker Compose setup to run a single Grafana instance for development, home lab, or small deployments. The compose file mounts persistent storage for dashboards, plugins and configuration.

Prerequisites
- Docker and Docker Compose installed on the host.
- Optional: a reverse proxy (Traefik, Nginx) and TLS for secure public access.

Ports
- `3000` — Grafana web UI (changeable in the compose file or reverse proxy)

Persistent storage
- The compose mounts a host path or named volume for Grafana data (`/var/lib/grafana` inside the container). Ensure the host path exists and is writable by Docker, or switch to a named Docker volume.

Quick start
```bash
cd docker-compose/grafana
docker compose up -d
```

Stop and remove
```bash
docker compose down
```

Default credentials
- On first start Grafana uses `admin` / `admin` (you will be prompted to change the password). If you override initial admin credentials via environment variables (`GF_SECURITY_ADMIN_USER`, `GF_SECURITY_ADMIN_PASSWORD`) those will apply.

Common environment variables
- `GF_SECURITY_ADMIN_USER` — admin username
- `GF_SECURITY_ADMIN_PASSWORD` — admin password
- `GF_SERVER_ROOT_URL` — root URL when behind a proxy
- `GF_USERS_ALLOW_SIGN_UP` — disable self sign-up in production

Configuring provisioning and dashboards
- Use the `provisioning/` directory (if present) to add datasources or dashboard provisioning files. When using `provisioning`, Grafana will load datasources and dashboards on startup.

Reverse proxy & TLS
- For internet-facing deployments, run Grafana behind a reverse proxy (Traefik, Nginx) and terminate TLS there. Set `GF_SERVER_ROOT_URL` to the publicly reachable URL.

Backups and upgrades
- Back up the data volume or host path (dashboards, plugins, sqlite DB). When upgrading Grafana, stop the container, pull the new image, and start the container again.

Troubleshooting
- No UI on port 3000: verify `docker compose ps` and `docker compose logs grafana`.
- Permission errors writing to storage: confirm ownership and permissions on the host path:

```bash
ls -ld /path/to/grafana/data
sudo chown $(id -u):$(id -g) /path/to/grafana/data
```

- Reset admin password (example using container):

```bash
docker compose exec grafana grafana-cli admin reset-admin-password NewPassword
```

Security notes
- This compose is intended for local/home lab use. For production enable authentication, RBAC, HTTPS, and restrict access with a reverse proxy or network rules.

References
- Grafana docs: https://grafana.com/docs/grafana/latest/

If you want, I can also:
- Add a `provisioning/` example for a Prometheus datasource and a sample dashboard.
- Switch the compose to use a named Docker volume and update the README with exact paths.
# Installation

## Deployment

Copy the `docker-compose.yml` template into your project folder and start the container.

## Configuration

Visit the Grafana Web Interface `http://localhost:3000`, and login with Grafana's default username and password: `admin`.

*For more info visit:* [Official Grafana Getting started Documentation](https://grafana.com/docs/grafana/latest/getting-started/getting-started/)

# Best-Practices & Post-Installation

## Disable HTTP

It's not secure to expose Grafana via the HTTP protocol. 

### Use a Reverse Proxy

- [ ] Use a Reverse Proxy to securely expose administrative services.

# Additional Referfences

[Official Grafana Documentation](https://grafana.com/docs/grafana/latest/)