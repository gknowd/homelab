# Gitea Docker Compose Setup

This guide explains how to deploy Gitea using Docker Compose, Portainer, and Traefik, with PostgreSQL as the database and persistent storage for Git repositories.

## Prerequisites
- Docker and Docker Compose installed on your host
- Portainer installed and running (see https://www.portainer.io/installation/)
- Traefik reverse proxy deployed and running on the `traefik` Docker network
- DNS record for `gitea.cloudtorq.io` pointing to your host's public IP
- Directories `/mnt/storage/gitea/data` and `/mnt/storage/gitea/postgres` exist and are writable by Docker

## Directory Structure
```
/home/gknowd/homelab/docker-compose/gitea/docker-compose.yml
/mnt/storage/gitea/data          # Gitea data (repos, config, etc.)
/mnt/storage/gitea/postgres      # PostgreSQL database
```

## docker-compose.yml Overview
The compose file includes:
- **Gitea:** Git hosting service with web UI
- **PostgreSQL:** Database for Gitea
- **Traefik integration:** HTTPS access via gitea.cloudtorq.io
- **SSH access:** Port 2222 for Git SSH operations

## Steps to Deploy with Portainer

### 1. Prepare the Data Directories
Ensure the data directories exist and have correct ownership:
```bash
sudo mkdir -p /mnt/storage/gitea/data
sudo mkdir -p /mnt/storage/gitea/postgres
sudo chown -R 1000:1000 /mnt/storage/gitea/data
sudo chown -R 999:999 /mnt/storage/gitea/postgres
```

### 2. Open Portainer
- Go to your Portainer web UI (e.g., http://your-server:9000)
- Log in with your credentials

### 3. Deploy the Stack
1. In Portainer, go to **Stacks** > **Add stack**
2. Name your stack (e.g., `gitea`)
3. Copy and paste the contents of `docker-compose.yml` into the web editor
4. (Optional) Under **Environment variables**, you can override database credentials:
   - `GITEA__database__PASSWD` - Database password
   - `POSTGRES_PASSWORD` - Must match the above
5. Deploy the stack

### 4. Configure DNS
- Ensure your DNS provider has an A or CNAME record for `gitea.cloudtorq.io` pointing to your host's public IP.

### 5. Initial Gitea Setup
1. Access Gitea at: `https://gitea.cloudtorq.io`
2. Complete the initial setup wizard:
   - Database settings are pre-configured
   - Set your admin username and password
   - Configure SSH settings (SSH port: 2222)
   - Review and adjust other settings as needed
3. Click "Install Gitea"

### 6. SSH Access for Git
To clone/push repositories via SSH:
```bash
git clone ssh://git@gitea.cloudtorq.io:2222/username/repo.git
```
Make sure port 2222 is accessible from your network.

## Security Notes
- The Gitea web interface is exposed via HTTPS using Traefik and Let's Encrypt.
- SSH access is on port 2222 (not the default 22) to avoid conflicts.
- Database credentials are set in environment variables. For production, use strong passwords and consider using Docker secrets.
- Data is persisted in `/mnt/storage/gitea/` for durability.
- Regularly back up your data directories.

## Troubleshooting
- Check Portainer and container logs for errors if Gitea does not start.
- Ensure the external Docker network `traefik` exists and is attached to Traefik and Gitea.
- Make sure `/mnt/storage/gitea/data` is writable by UID 1000 and `/mnt/storage/gitea/postgres` by UID 999.
- For DNS/SSL issues, verify your DNS records and Traefik configuration.
- If SSH doesn't work, ensure port 2222 is open in your firewall.

## References
- [Gitea Documentation](https://docs.gitea.io/)
- [Gitea Docker Hub](https://hub.docker.com/r/gitea/gitea)
- [Traefik Documentation](https://doc.traefik.io/traefik/)
- [Portainer Documentation](https://docs.portainer.io/)

---

For further customization or questions, feel free to ask!
