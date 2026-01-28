# Homelab

This repository contains the configuration, orchestration, and documentation for a personal homelab environment. It collects Docker Compose stacks, Kubernetes manifests, Terraform definitions, and other operational artifacts used to run and maintain services for development, automation, monitoring, and experimentation.

This README is intended for operators who will deploy or maintain the environment, contributors who want to add integrations or services, and reviewers who want an overview of architecture and operational patterns.

Table of Contents
- Overview
- Goals
- Repo layout
- Services (what's included)
- Deployment & quick start
- Networking, TLS, and domains
- Storage & backups
- Secrets & credentials
- Development & contributing
- Operational notes
- License & contact

## Goals

- Provide reproducible, documented infrastructure for a small home/cloud hybrid environment.
- Keep everything auditable and code-first where practical (Terraform, Docker Compose, Kubernetes manifests).
- Make on-premise and cloud services easy to bootstrap for testing and demos.

## Repository layout

Top-level directories of interest:

- `docker-compose/` — Docker Compose stacks for many services. Each service has its own subdirectory with a `docker-compose.yml` and README.
	- `traefik/`, `portainer/`, `grafana/`, `influxdb/`, `mongodb/`, `postgresql/`, `redis/`, `loki/`, `promtail/`, `n8n/`, `mosquitto/`, `rabbitmq/`, `uptimekuma/`, etc.
- `kubernetes/` — Kubernetes manifests and configuration used for cluster deployments.
- `terraform/` — Terraform modules and environment definitions for provisioning cloud or VM infrastructure.
- `proxmox/` — Proxmox configuration and network layout files for the virtualization host(s).
- `infrastructure/` — Misc infra scripts and helper configuration.
- `azure-devops/` — CI/CD and agent configuration for on-prem build agents.
- `phi2-container/` — Local packaging for the Phi-2 model container and model runner scripts.
- `diagrams/` — Architecture diagrams (PNG/SVG/Diagrams source).

Refer to each folder's README for service-specific configuration and run instructions.

## What’s included (high level)

- Ingress & routing: Traefik as the primary edge reverse proxy with ACME support and Cloudflare DNS challenge.
- Container management: Portainer and Portainer Agent for GUI-driven container and stack management.
- Datastores: PostgreSQL, MongoDB, Redis, InfluxDB.
- Observability: Grafana, Loki, Promtail, Prometheus integrations via Docker Compose stacks.
- Logs & tracing: Loki+Promtail for centralised logs; Seq available for structured logs.
- Message brokers: RabbitMQ and Mosquitto (MQTT) for IoT and internal message workflows.
- Automation: n8n for workflows and JetBrains Space on-premises stack (space-on-premises).
- AI/ML: Packaging for Phi-2 model container and helper scripts to run locally.

## Deployment & Quick start

These instructions assume a Linux host or VM with Docker and Docker Compose available. Many services expect a machine with a stable public IP and a DNS provider (Cloudflare) configured for ACME DNS.

1) Clone the repo:

```bash
git clone https://github.com/<your-org>/homelab.git
cd homelab
```

2) Review environment variables for the stacks you intend to run. Most Compose stacks include a `.env` or README pointing to required values.

3) Bring up Traefik first (edge routing + TLS):

```bash
cd docker-compose/traefik
docker compose up -d
```

4) Start other stacks behind Traefik (examples):

```bash
cd ../../docker-compose/grafana
docker compose up -d

cd ../postgresql
docker compose up -d
```

5) Use Portainer for visual management:

```bash
cd ../portainer
docker compose up -d
```

Notes:
- Many stacks assume an external Docker network named `traefik` — the Traefik stack README shows how to create it if needed.
- Service-specific README files detail database initialization, volumes, and sample credentials.

## Networking, TLS, and domains

- Traefik handles TLS and routing. ACME configuration uses Cloudflare DNS challenge in production.
- Domain conventions used here are `*.cloudtorq.io` and similar; update the traefik and service hostnames to match your domain.
- If running behind a firewall/NAT, forward 80/443 and any required service ports.

## Storage & backups

- Persistent storage for services is mounted under `/mnt/storage/<service-name>` by convention in many stacks. Check each `docker-compose.yml` for volumes.
- Backup strategy suggestions:
	- Database dumps (Postgres `pg_dump`, MongoDB `mongodump`) to a different host or object storage.
	- Grafana and Prometheus config snapshots.
	- Periodic snapshot of `/mnt/storage` or relevant Docker volumes.

Example: backup a Postgres container

```bash
docker exec -t my_postgres_container pg_dumpall -c -U postgres_user > pg_dump_$(date +%F).sql
```

## Secrets & credentials

- Do NOT commit secrets to this repository. Use a secrets manager (Vault, SOPS, or the Docker secrets mechanism) or environment files excluded via `.gitignore`.
- Some stacks include an `.env.example` — copy to `.env` and fill in secrets locally.

## Development & contributing

- Contributions are welcome. When adding a service:
	1. Add a subdirectory under `docker-compose/` or appropriate top-level folder.
	2. Include a `docker-compose.yml`, `README.md`, and `.env.example` explaining required variables.
	3. Ensure new services follow network and labels conventions (Traefik labels for routing).

- Branching & PRs:
	- Fork or branch the repo and open a Pull Request with a clear description of the change and testing steps.

- Coding & formatting:
	- Keep compose files readable and avoid embedding secrets.

## Operational notes

- Portainer is used for day-to-day container operations and stack management — use it for quick restarts and inspecting logs.
- For reproducible infra, prefer `terraform/` to spin up VMs or cloud resources.
- For Kubernetes deployments, manifests live in `kubernetes/` and expect a cluster with appropriate storage classes.

## Useful commands

Start all Compose stacks in a directory tree (example):

```bash
find docker-compose -maxdepth 2 -type f -name 'docker-compose.yml' -execdir docker compose up -d \;
```

Run Terraform (example):

```bash
cd terraform
terraform init
terraform plan
terraform apply
```

Inspect logs for a service:

```bash
docker compose -f docker-compose/grafana/docker-compose.yml logs -f
```

## Security considerations

- Rotate any credentials and API tokens regularly.
- Limit public exposure: only expose services that need external access and use Traefik routing with auth where appropriate.
- Use firewall rules and port whitelisting for management interfaces (Portainer, Proxmox UI).

## License

This repository is licensed under the MIT License — see `LICENSE` at the repository root.

## Contact & acknowledgements

- Maintainer: Greg Knowd — gknowd@shocklink.com
- Thanks to the many homelab authors and community guides used as references.

---

For any changes you'd like to see in this README (examples, diagrams, or runbooks), tell me which area to expand next.