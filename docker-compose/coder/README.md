# Coder Docker Compose Setup

[Coder](https://coder.com/) is a self-hosted cloud development environment (CDE) platform. It provisions remote workspaces — running in Docker, Kubernetes, or cloud VMs — that developers connect to via browser, SSH, or their local IDE. Coder centralizes dev environments so every engineer starts from the same reproducible template, eliminating "works on my machine" problems.

This stack runs the Coder server backed by the shared PostgreSQL instance at `postgres.cloudtorq.io` and exposes the UI through Traefik at `https://coder.cloudtorq.io`. Workspace apps (e.g. code-server, Jupyter) are routed through the wildcard domain `*.coder.cloudtorq.io`.

---

## Prerequisites

- Docker and Docker Compose installed on your host
- The external `traefik` Docker network already exists
- DNS for `coder.cloudtorq.io` and `*.coder.cloudtorq.io` pointing to your host
- A database and user created on `postgres.cloudtorq.io` (see below)
- (Optional) Portainer for web-based stack management

---

## Database Setup

Before starting the stack, create the Coder database and user on your PostgreSQL server:

```sql
CREATE USER coder WITH PASSWORD 'your_strong_password';
CREATE DATABASE coder OWNER coder;
```

---

## Quick Start (Command Line)

1. **Set up environment variables:**

   Copy `.env.example` to `.env` and fill in your values:
   ```bash
   cp .env.example .env
   ```

   Edit `.env`:
   ```env
   CODER_DB_USER=coder
   CODER_DB_PASSWORD=your_strong_password
   CODER_DB_NAME=coder
   ```

2. **Ensure the Traefik network exists:**
   ```bash
   docker network create traefik
   ```
   Skip this step if the network already exists.

3. **Start the stack:**
   ```bash
   docker compose up -d
   ```

4. **Complete first-run setup:**

   On first start, Coder will print a one-time setup URL in its logs. Open it to create the admin user:
   ```bash
   docker compose logs coder
   ```
   Look for a line like:
   ```
   View the Web UI: https://coder.cloudtorq.io
   ```
   Or follow the setup URL printed to the console if the admin account hasn't been created yet.

5. **Access Coder:**
   - Web UI: https://coder.cloudtorq.io

6. **Stop the stack:**
   ```bash
   docker compose down
   ```

---

## Using with Portainer

1. **Add a new stack:**
   - In Portainer, go to **Stacks** > **Add stack**.
   - Paste the contents of `docker-compose.yaml` into the editor.
   - In the **Environment variables** section, add the following:
     - `CODER_DB_USER`
     - `CODER_DB_PASSWORD`
     - `CODER_DB_NAME`
   - Deploy the stack.

2. **Networks:**
   - The stack joins the external `traefik` network. Ensure it exists before deploying:
     ```bash
     docker network create traefik
     ```

3. **Traefik integration:**
   - The stack is pre-configured for HTTPS with automatic Let's Encrypt certificates.
   - Both the main domain (`coder.cloudtorq.io`) and workspace subdomains (`*.coder.cloudtorq.io`) are routed through a single Traefik router rule.

---

## Workspace Templates

After logging in, you'll need to create at least one **template** before developers can launch workspaces. Coder provides starter templates for Docker, Kubernetes, AWS EC2, and more.

To get started quickly with Docker-based workspaces (uses the Docker socket mounted in this compose file):

```bash
docker exec -it coder coder templates init
```

Follow the prompts to select a starter template, then push it:

```bash
cd your-template-dir
coder templates push
```

Alternatively, use the **Templates** section in the Web UI to import community templates.

---

## Customization

- **Domain:** Update `CODER_ACCESS_URL`, `CODER_WILDCARD_ACCESS_URL`, and Traefik labels if using a different domain.
- **TLS resolver:** The Traefik label `certresolver=letsencrypt` assumes a Let's Encrypt resolver named `letsencrypt` is configured in your Traefik instance. Update this to match your resolver name.
- **Database:** The connection string is built from the three `CODER_DB_*` env vars. If you need additional Postgres options (e.g. `sslmode=require`), edit the `CODER_PG_CONNECTION_URL` in the compose file directly.
- **Docker socket:** The `/var/run/docker.sock` mount allows Coder to provision Docker-based workspaces on the host. Remove this volume if you are only using external provisioners (Kubernetes, cloud VMs).

---

## Troubleshooting

- **View logs:**
  ```bash
  docker compose logs -f coder
  ```

- **Cannot connect to database:** Verify the user and database exist on `postgres.cloudtorq.io` and that the host allows connections from your Docker host's IP.

- **Wildcard subdomains not resolving:** Ensure your DNS provider has a wildcard `A` record (`*.coder.cloudtorq.io → <host IP>`) in addition to the apex record.

- **Traefik network missing:**
  ```bash
  docker network create traefik
  ```

- **Permission denied on Docker socket:** The Coder container needs read/write access to `/var/run/docker.sock`. On some hosts you may need to add the container to the `docker` group:
  ```yaml
  group_add:
    - "999"  # docker group GID — verify with: stat -c '%g' /var/run/docker.sock
  ```

---

## References

- [Coder Documentation](https://coder.com/docs)
- [Coder Docker Compose Guide](https://coder.com/docs/install/docker)
- [Coder Template Starters](https://registry.coder.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Traefik Documentation](https://doc.traefik.io/traefik/)
- [Portainer Documentation](https://docs.portainer.io/)
