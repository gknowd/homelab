# PostgreSQL Docker Compose Setup

This directory contains a `docker-compose.yaml` file to run a PostgreSQL server in Docker. It also supports usage with Portainer.

## Prerequisites
- Docker and Docker Compose installed on your host
- (Optional) Portainer installed if you want to manage containers via a web UI

## Quick Start (Command Line)

1. **Set the PostgreSQL password:**
   - Create a `.env` file in this directory with the following content:
     ```env
     POSTGRES_PASSWORD=your_strong_password
     ```
   - You can change the `POSTGRES_USER` and `POSTGRES_DB` in the compose file if needed.

2. **Start the PostgreSQL container:**
   ```bash
   docker compose up -d
   ```

3. **Access PostgreSQL:**
   - The server will be available on port `5432` of your Docker host.
   - Data is stored persistently in `/mnt/storage/postgresql-server` on your host.

4. **Stop the container:**
   ```bash
   docker compose down
   ```

## Using with Portainer

1. **Add a new stack in Portainer:**
   - Go to your Portainer instance in your browser.
   - Navigate to **Stacks** > **Add stack**.
   - Copy and paste the contents of `docker-compose.yaml` into the editor.
   - In the **Environment variables** section, add `POSTGRES_PASSWORD` and set your desired password.
   - Deploy the stack.

2. **Persistent Storage:**
   - Ensure `/mnt/storage/postgresql` exists and is writable by Docker. You may need to create this directory on your host:
     ```bash
     sudo mkdir -p /mnt/storage/postgresql-server
     sudo chown 999:999 /mnt/storage/postgresql-server
     ```
     (PostgreSQL runs as UID 999 by default.)

3. **Managing the Stack:**
   - Use Portainer's UI to start, stop, or redeploy the stack as needed.

## Notes
- The default database, user, and password are set via environment variables. Change them as needed for your use case.
- The data directory is mapped to `/mnt/storage/postgresql-server` for persistence.
- If you change the mapped port, update the `ports` section in the compose file.

## References
- [PostgreSQL Docker Image](https://hub.docker.com/_/postgres)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Portainer Documentation](https://docs.portainer.io/)
