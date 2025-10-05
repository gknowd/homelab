# n8n Docker Compose Setup

This guide explains how to use the provided `docker-compose.yaml` file to run n8n on your Docker host.

## Prerequisites
- Docker installed on your host
- Docker Compose installed (v2 recommended)

## Quick Start

1. **Clone or copy the `docker-compose.yaml` file to your host:**
   ```bash
   cd /path/to/your/docker-compose/n8n
   ```

2. **(Optional) Configure Environment Variables:**
   - If your setup requires custom environment variables, create a `.env` file in this directory or edit the variables directly in `docker-compose.yaml`.

3. **Start n8n using Docker Compose:**
   ```bash
   docker compose up -d
   ```
   This command will pull the required images (if not already present) and start the n8n service in detached mode.

4. **Access n8n:**
   - Open your browser and go to: `http://localhost:5678` (or the port you configured)

5. **Stop n8n:**
   ```bash
   docker compose down
   ```
   This will stop and remove the containers, but your data will persist if you have configured volumes.

## Customization
- Edit the `docker-compose.yaml` file to change ports, volumes, or environment variables as needed.
- For production deployments, consider securing your instance and using external databases or storage.

## Troubleshooting
- Check logs with:
  ```bash
  docker compose logs n8n
  ```
- Ensure no other service is using the configured port (default: 5678).

## References
- [n8n Documentation](https://docs.n8n.io/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
