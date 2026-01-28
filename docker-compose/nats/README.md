**NATS (Docker Compose)**

- **Location:** [docker-compose/nats/docker-compose.yml](docker-compose/nats/docker-compose.yml)
- **Config:** [docker-compose/nats/nats.conf](docker-compose/nats/nats.conf)

Overview
 - This folder runs a single-node NATS server (with JetStream enabled) via Docker Compose.
 - The compose file exposes the client port, cluster routes port, and the HTTP monitoring port.

Included files
 - `docker-compose.yml` — Docker Compose service definition for NATS.
 - `nats.conf` — NATS server configuration (JetStream store directory, HTTP monitoring).
 - `data/` (or configured host path) — persistent storage for JetStream data.

Prerequisites
 - Docker and Docker Compose installed on the host.

Ports
 - `4222` (client connections)
 - `6222` (cluster routes)
 - `8222` (HTTP monitoring)

Volumes / Persistence
 - By default the compose mounts a host path into the container as the JetStream store.
 - The compose file currently maps `./mnt/storage/nats` on the compose folder to `/data` inside the container. Change this host path if you want a different persistence location.

Storage configuration
- Do I need to configure `/mnt/storage/nats`?
  - Yes — the host path used by the `volumes:` mapping must exist and be writable by Docker, or you can switch to a Docker named volume instead.
  - The compose file currently uses a host path. There are three common options:

  1) Use an absolute host path (recommended when you want control over where data lands):

     - Update `docker-compose.yml` to use an absolute path (example):

       ```yaml
       services:
         nats:
           volumes:
             - /mnt/storage/nats:/data
       ```

     - Create the directory and give Docker ownership (run on the host):

       ```bash
       sudo mkdir -p /mnt/storage/nats
       sudo chown $(id -u):$(id -g) /mnt/storage/nats
       ```

  2) Use a relative path inside the compose folder:

     - The compose currently references `./mnt/storage/nats` relative to this folder. If you prefer that, create it:

       ```bash
       mkdir -p docker-compose/nats/mnt/storage/nats
       ```

     - Make sure the path is writable by the Docker daemon user.

  3) Use a Docker named volume (no host path required):

     - Change the `volumes:` section in `docker-compose.yml` to:

       ```yaml
       services:
         nats:
           volumes:
             - nats_data:/data

       volumes:
         nats_data:
       ```

     - Docker will manage storage under `/var/lib/docker/volumes` (or your configured Docker data root).

Which to choose?
- For development: a named volume (`nats_data`) is simplest and avoids host-permission issues.
- For backups, monitoring, or specific disk placement: use an absolute host path like `/mnt/storage/nats` so you can control mountpoints and backup routines.

Quick checks and troubleshooting
- If NATS cannot write JetStream files, check container logs and verify the host path is writable:

  ```bash
  docker compose logs -f nats
  ls -ld /mnt/storage/nats
  ```

- If you change the compose file to use an absolute path, recreate the container:

  ```bash
  docker compose down
  docker compose up -d
  ```

Start
```bash
cd docker-compose/nats
docker compose up -d
```

Stop
```bash
docker compose down
```

Logs
```bash
docker compose logs -f nats
```

Quick checks
 - Monitoring UI / server metrics: http://localhost:8222/
 - Check server status via HTTP API: `curl http://localhost:8222/headers` or `curl http://localhost:8222/`.
 - If you have the `nats` CLI installed locally, connect like:
   `nats --server 127.0.0.1:4222 stream ls`

Using the `nats-box` container (example)
 - To use the `nats` CLI without installing it locally, run:
```bash
docker run --rm -it --network host natsio/nats-box nats --server 127.0.0.1:4222 stream ls
```
Note: the `--network host` approach works on Linux hosts; adapt networking if you run Docker Desktop or a different network setup.

Configuration notes
 - The compose passes `-c /etc/nats/nats.conf` to the server; modify `nats.conf` to change JetStream or monitoring settings.
 - To pin the image to a specific version change `image: nats:latest` to e.g. `nats:2.10.5` in `docker-compose.yml`.

Troubleshooting
 - Container fails to start: check `docker compose logs nats` for errors.
 - Port conflicts: ensure `4222`, `6222`, `8222` are free on the host or change the host-side port mapping in the compose file.
 - Data not persisted: verify the host path used in the `volumes:` section exists and is writable by Docker.

Security & production notes
 - This compose is intended for local development and testing. For production, enable authentication, TLS, and cluster configuration in `nats.conf`.
 - Consider running multiple NATS nodes and configuring proper routing and persistent storage for JetStream HA.

What changed in this folder
 - A simple Docker Compose setup and `nats.conf` to run a JetStream-enabled server locally.

If you want, I can also:
 - Add authentication/TLS examples in `nats.conf`.
 - Adjust the compose to use a named Docker volume instead of a host path.
