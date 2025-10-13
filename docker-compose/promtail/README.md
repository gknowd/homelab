# Promtail Docker Compose Setup

This guide explains how to deploy Grafana Promtail using Docker Compose and Portainer, with persistent storage, syslog ingestion, and best practices for configuration and security.

## Prerequisites
- Docker and Docker Compose installed on your host
- Portainer installed and running (see https://www.portainer.io/installation/)
- Directory `/mnt/storage/promtail` exists and is writable by Docker
- Promtail config file at `/mnt/storage/promtail/promtail-config.yaml`

## Directory Structure
```
/home/gknowd/homelab/docker-compose/promtail/docker-compose.yaml
/mnt/storage/promtail/promtail-config.yaml   # Promtail config file
/mnt/storage/promtail/                      # Promtail state and data
```

## docker-compose.yaml Example
```
version: '3.8'
services:
  promtail:
    image: grafana/promtail:latest
    container_name: promtail
    restart: unless-stopped
    volumes:
      - /mnt/storage/promtail/promtail-config.yaml:/etc/promtail/promtail.yaml:ro
      - /var/log:/var/log:ro
      - /mnt/storage/promtail:/promtail
    command: -config.file=/etc/promtail/promtail.yaml
    ports:
      - "514:514/udp"
      - "1514:1514/tcp"
```

## Steps to Deploy with Portainer

### 1. Prepare the Data Directory and Config File
Ensure the data directory and config file exist and are owned by the user running Docker:
```bash
sudo mkdir -p /mnt/storage/promtail
sudo touch /mnt/storage/promtail/promtail-config.yaml
sudo chown 1000:1000 /mnt/storage/promtail/promtail-config.yaml
sudo chown -R 1000:1000 /mnt/storage/promtail
```

### 2. Create Your Promtail Config
Edit `/mnt/storage/promtail/promtail-config.yaml` with your desired configuration. For syslog ingestion, include a `syslog` receiver block, e.g.:
```yaml
server:
  http_listen_port: 9080
  grpc_listen_port: 0

positions:
  filename: /promtail/positions.yaml

clients:
  - url: http://loki:3100/loki/api/v1/push

receivers:
  syslog:
    listen_address: 0.0.0.0:514
    labels:
      job: syslog
```

### 3. Open Portainer
- Go to your Portainer web UI (e.g., http://your-server:9000)
- Log in with your credentials

### 4. Deploy the Stack
1. In Portainer, go to **Stacks** > **Add stack**
2. Name your stack (e.g., `promtail`)
3. Copy and paste the contents of `docker-compose.yaml` into the web editor
4. Deploy the stack

### 5. Send Syslog Data to Promtail
- Configure other servers to send syslog data to your host's IP on UDP port 514 or TCP port 1514.
- Promtail will ingest and forward logs to Loki as configured.

## Security Notes
- Only expose syslog ports if you intend to receive logs from other servers. Use firewalls to restrict access if needed.
- Data and state are persisted in `/mnt/storage/promtail`.
- Always use a secure Promtail config and restrict access to sensitive log data.

## Troubleshooting
- Check Portainer and container logs for errors if Promtail does not start.
- Ensure `/mnt/storage/promtail` and the config file are readable by the container (UID 1000 by default).
- For syslog issues, verify your config and network/firewall settings.

## References
- [Promtail Documentation](https://grafana.com/docs/loki/latest/clients/promtail/)
- [Promtail Docker Hub](https://hub.docker.com/r/grafana/promtail)
- [Portainer Documentation](https://docs.portainer.io/)

---

For further customization or questions, feel free to ask!
