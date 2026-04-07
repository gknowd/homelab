# Dockhand

Dockhand is a lightweight Docker container management UI that provides a simple interface for managing your Docker containers, images, networks, and volumes.

## Prerequisites

- Docker Engine installed
- Docker Compose v2+

## Installation

1. Clone or navigate to this directory:

   ```bash
   cd docker-compose/dockhand
   ```

2. Start the container:

   ```bash
   docker compose up -d
   ```

3. Access the web UI at: `http://localhost:3000`

## Configuration

### Environment Variables

| Variable | Default           | Description              |
| -------- | ----------------- | ------------------------ |
| `TZ`     | `America/New_York`| Container timezone       |

### Volumes

| Path              | Description                     |
| ----------------- | ------------------------------- |
| `/app/data`       | Persistent application data     |
| `/var/run/docker.sock` | Docker socket (read-only)  |

### Ports

| Port | Description |
| ---- | ----------- |
| 3000 | Web UI      |

## Usage

### Start

```bash
docker compose up -d
```

### Stop

```bash
docker compose down
```

### View Logs

```bash
docker compose logs -f dockhand
```

### Update

```bash
docker compose pull
docker compose up -d
```

## Security Considerations

- The Docker socket is mounted read-only to limit potential security risks
- Consider placing behind a reverse proxy (e.g., Traefik) with authentication for remote access
- Restrict access to trusted users only, as container management provides significant system access

## Troubleshooting

### Cannot connect to Docker

Ensure the Docker socket has proper permissions:

```bash
sudo chmod 666 /var/run/docker.sock
```

Or add your user to the docker group:

```bash
sudo usermod -aG docker $USER
```

### Port already in use

Modify the port mapping in `docker-compose.yaml`:

```yaml
ports:
  - "3001:3000"  # Change 3001 to your preferred port
```
