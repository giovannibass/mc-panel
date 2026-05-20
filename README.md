# mc-panel

`mc-panel` is a Linux-hosted Minecraft control panel that can be deployed with Ansible and managed through Django, Docker, Ansible, Nginx, Gunicorn, and systemd.

Once the setup is complete, you can use the web dashboard to view and manage your own Minecraft server container.

---

# Quick Start

For full setup instructions, see [Setup Guide](docs/setup.md).

1. Clone the repository.
2. Configure the Ansible inventory file.
3. Run the Ansible playbook.
4. Open the dashboard in a browser.

# Architecture

Basic overview of how each layer interacts with the next. Turning on/off the Minecraft server in the web browser will go through each of these steps before reaching the container itself.

**User Browser -> Nginx Reverse Proxy -> Gunicorn / Django App -> Docker Engine -> Minecraft Container**

Ansible provisions the server.
Prometheus/Grafana monitor the system.
GitHub Actions handles CI/deploy checks.

# Documentation

- [Setup Guide](docs/setup.md)
- [Case Study](docs/case-study.md)
- [Architecture](docs/architecture.md)
- [Troubleshooting](docs/troubleshooting.md)

# Skills Demonstrated

- Linux server administration on Rocky Linux
- systemd service management
- Nginx reverse proxy configuration
- Gunicorn deployment for a Django application
- Docker container management
- Ansible automation and repeatable provisioning
- GitHub Actions CI/deployment workflow
- Prometheus and Grafana monitoring
- Firewall and service exposure awareness
- Troubleshooting real deployment issues

# Known Limitations

- Only tested with Rocky 9
- Only allows control of one server
- Setup instructions do not explain remote setup, although that is possible

# Future Improvements
- Completed documentation including detailed overview of the architecture involved, troubleshooting guide, and improving the monitoring dashboards.
- Support multiple Minecraft servers.
- Better error handling for dashboard.
- Include HTTPS by default.
