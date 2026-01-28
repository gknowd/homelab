# Homelab

My #homelab is an ever evolving set of hardware, tools and software which makes up the environment in which I work and play.

## Thank You!
**I want to give a big shoutout to all  homelabbers on the internet who provide so much great content and time saving instruction to the rest of us! You have saved my countless hours of time and pulling my hair out**

## Application Index

This repository contains configurations and documentation for the following homelab services and infrastructure:

### Infrastructure & Orchestration

- **[Traefik](./docker-compose/traefik/)** - Modern reverse proxy with automatic HTTPS via Let's Encrypt, supports Cloudflare DNS challenge
- **[Portainer](./docker-compose/portainer/)** - Web-based Docker container management UI
- **[Portainer Agent](./docker-compose/portainer-agent/)** - Agent for managing remote Docker hosts from Portainer
- **[Terraform](./terraform/)** - Infrastructure as Code configurations
- **[Kubernetes](./kubernetes/)** - Kubernetes cluster configurations
- **[Proxmox](./proxmox/)** - Proxmox virtualization environment configurations
- **[Infrastructure](./infrastructure/)** - General infrastructure configurations

### Databases

- **[PostgreSQL](./docker-compose/postgresql/)** - Relational database server with persistent storage at `/mnt/storage/postgresql-server`
- **[MongoDB](./docker-compose/mongodb/)** - NoSQL document database accessible on localhost:27017
- **[Redis](./docker-compose/redis/)** - In-memory data store for caching and session management
- **[InfluxDB](./docker-compose/influxdb/)** - Time-series database for metrics and monitoring data

### Monitoring & Logging

- **[Loki](./docker-compose/loki/)** - Grafana Loki log aggregation system accessible at `https://loki.cloudtorq.io`
- **[Promtail](./docker-compose/promtail/)** - Log collection agent for Loki with syslog ingestion (UDP:514, TCP:1514)
- **[Grafana](./docker-compose/grafana/)** - Visualization and analytics platform for metrics and logs
- **[Seq](./docker-compose/seq/)** - Structured logging platform accessible at `https://seq.cloudtorq.io`
- **[Uptime Kuma](./docker-compose/uptimekuma/)** - Self-hosted uptime monitoring tool at `https://uptime.cloudtorq.io`

### Message Brokers

- **[Mosquitto](./docker-compose/mosquitto/)** - Eclipse Mosquitto MQTT message broker (ports 1883, 9001)
- **[RabbitMQ](./docker-compose/rabbitmq/)** - Message queue broker with management interface (ports 5672, 15672)

### Automation & Development

- **[n8n](./docker-compose/n8n/)** - Workflow automation platform with PostgreSQL backend, accessible at `https://n8n.cloudtorq.io`
- **[JetBrains Space](./docker-compose/space-on-premises/)** - Complete software development platform (on-premises) with integrated VCS, packages, and collaboration tools
- **[Azure DevOps](./azure-devops/)** - Azure DevOps configurations and Docker agent setup
- **[.NET Projects](./dotnet/)** - .NET application configurations

### AI & Machine Learning

- **[Phi2 Container](./phi2-container/)** - Phi-2 AI model container setup

### Documentation

- **[Diagrams](./diagrams/)** - Architecture and infrastructure diagrams

## Deployment

Most services are deployed using Docker Compose and managed through Portainer. Services that require external access are routed through Traefik with automatic HTTPS certificates from Let's Encrypt.

### Common Patterns

- **Persistent Storage**: Most services store data in `/mnt/storage/[service-name]`
- **Networking**: Services requiring public access use the `traefik` external Docker network
- **SSL/TLS**: Automated certificate management via Traefik with Cloudflare DNS challenge
- **Domains**: Services are typically accessible at `[service].cloudtorq.io`

## Recipies and configurations

[[Azure DevOps is Awesome!]]