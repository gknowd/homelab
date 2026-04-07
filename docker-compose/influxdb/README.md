# InfluxDB

InfluxDB is an open-source time series database designed for high-performance storage and retrieval of time-stamped data.

## Deployment with Portainer

### Option 1: Using Portainer Stacks (Recommended)

1. Open Portainer and navigate to **Stacks** in the left sidebar
2. Click **+ Add stack**
3. Name your stack (e.g., `influxdb`)
4. Select **Upload** and upload the `docker-compose.yml` file, or paste the contents into the **Web editor**
5. (Optional) Configure environment variables in the **Environment variables** section
6. Click **Deploy the stack**

### Option 2: Using Portainer with Git Repository

1. Open Portainer and navigate to **Stacks**
2. Click **+ Add stack**
3. Select **Repository**
4. Enter your Git repository URL and specify the path to the compose file
5. Click **Deploy the stack**

### Option 3: Manual Docker Compose

```bash
docker compose up -d
```

## Configuration

### Automatic Setup (Environment Variables)

Uncomment and configure the environment variables in `docker-compose.yml` for automated initialization:

| Variable | Description |
|----------|-------------|
| `DOCKER_INFLUXDB_INIT_MODE` | Set to `setup` for automatic initialization |
| `DOCKER_INFLUXDB_INIT_USERNAME` | Initial admin username |
| `DOCKER_INFLUXDB_INIT_PASSWORD` | Initial admin password (use a strong password) |
| `DOCKER_INFLUXDB_INIT_ORG` | Initial organization name |
| `DOCKER_INFLUXDB_INIT_BUCKET` | Initial bucket name |
| `DOCKER_INFLUXDB_INIT_RETENTION` | Data retention period (e.g., `1w`, `30d`, `0` for infinite) |
| `DOCKER_INFLUXDB_INIT_ADMIN_TOKEN` | Admin API token (generate a secure token) |

### Manual Setup (UI)

1. Access the InfluxDB UI at `http://<your-host>:8086`
2. Complete the onboarding wizard to create your initial user, organization, and bucket

## Accessing InfluxDB

- **Web UI**: `http://<your-host>:8086`
- **API**: `http://<your-host>:8086/api/v2`

## Best Practices & Security

### Disable HTTP (Enable HTTPS)

It's not secure to expose InfluxDB via HTTP. Choose one of the following options:

#### Option 1: Use Custom TLS Certificates

1. Mount your certificate files in the `docker-compose.yml`:
   ```yaml
   volumes:
     - /path/to/cert.pem:/etc/ssl/cert.pem:ro
     - /path/to/cert-key.pem:/etc/ssl/cert-key.pem:ro
   ```

2. Uncomment the command line to enable TLS:
   ```yaml
   command: influxd --tls-cert=/etc/ssl/cert.pem --tls-key=/etc/ssl/cert-key.pem
   ```

#### Option 2: Use a Reverse Proxy (Recommended)

Use Traefik, Nginx, or another reverse proxy to terminate TLS and forward traffic to InfluxDB. See the [traefik](../traefik/) folder for an example configuration.

### Data Backup

Backup your InfluxDB data regularly:

```bash
# Using InfluxDB CLI inside the container
docker exec influxdb influx backup /tmp/backup --token <your-token>

# Copy backup to host
docker cp influxdb:/tmp/backup ./influxdb-backup
```

## Volumes

| Volume | Path | Description |
|--------|------|-------------|
| `influxdb-data` | `/var/lib/influxdb2` | Database data storage |
| `influxdb-config` | `/etc/influxdb2` | Configuration files |

## Additional References

- [Official InfluxDB Documentation](https://docs.influxdata.com/influxdb/latest/)
- [InfluxDB Docker Hub](https://hub.docker.com/_/influxdb)
- [InfluxDB API Reference](https://docs.influxdata.com/influxdb/latest/api/)