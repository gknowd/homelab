
# n8n Docker Compose & Portainer Setup

This guide explains how to deploy n8n with PostgreSQL using Docker Compose, with persistent storage and Traefik reverse proxy, and how to deploy/manage it using Portainer.

---

## Prerequisites

- Docker and Docker Compose installed on your host
- (Optional) Portainer installed for web-based management
- (Optional) Traefik configured as a reverse proxy (see Traefik docs)
- DNS for your domain (e.g., `n8n.cloudtorq.io`) pointing to your host

---

## Quick Start (Command Line)

1. **Set up environment variables:**

   Create a `.env` file in this directory with:
   ```env
   POSTGRES_PASSWORD=your_strong_password
   ```

2. **Ensure persistent storage directories exist:**
   ```bash
   sudo mkdir -p /mnt/storage/postgresql-n8n
   sudo mkdir -p /mnt/storage/n8n
   sudo chown -R 999:999 /mnt/storage/postgresql-n8n
   sudo chown -R 1000:1000 /mnt/storage/n8n
   ```

3. **Start the stack:**
   ```bash
   docker compose up -d
   ```

4. **Access n8n:**
   - Via Traefik: https://n8n.cloudtorq.io (or your configured domain)
   - Default port: 5678 (if not using Traefik)

5. **Stop the stack:**
   ```bash
   docker compose down
   ```

---

## Using with Portainer

1. **Add a new stack:**
   - In Portainer, go to **Stacks** > **Add stack**.
   - Paste the contents of `docker-compose.yaml` into the editor.
   - In the **Environment variables** section, add `POSTGRES_PASSWORD` and set your password.
   - Deploy the stack.

2. **Persistent storage:**
   - Make sure `/mnt/storage/postgresql-n8n` and `/mnt/storage/n8n` exist and are writable as above.

3. **Networks:**
   - The stack uses two networks: `n8n-network` (created by Compose) and `traefik` (must exist and be external).
   - If the `traefik` network does not exist, create it:
     ```bash
     docker network create traefik
     ```

4. **Traefik integration:**
   - The stack is pre-configured for Traefik with HTTPS, automatic certificate, and HTTP-to-HTTPS redirect.
   - Update labels and domain as needed for your environment.

---

## Customization

- Change environment variables in the compose file or `.env` as needed.
- Adjust volumes for different storage locations.
- Update Traefik labels for your domain and certificate resolver.

---

## Troubleshooting

- View logs:
  ```bash
  docker compose logs n8n
  docker compose logs postgres
  ```
- Ensure no other service is using port 5678 if not using Traefik.
- Check Portainer's stack logs for deployment errors.

---

## References

- [n8n Documentation](https://docs.n8n.io/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Portainer Documentation](https://docs.portainer.io/)
- [Traefik Documentation](https://doc.traefik.io/traefik/)
