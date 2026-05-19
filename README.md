# mc-panel

`mc-panel` is a Linux-hosted Minecraft control panel that can be deployed with Ansible and managed through systemd, Docker, Nginx.

Once the setup is complete, you can use the web dashboard to view and manage the Minecraft server container.

---

# Architecture

Basic overview of how each layer interacts with the next. Turning on/off the Minecraft server in the web browser will go through each of these steps before reaching the container itself.

**User Browser -> Nginx Reverse Proxy -> Gunicorn / Django App -> Docker Engine -> Minecraft Container**

Ansible provisions the server.
Prometheus/Grafana monitor the system.
GitHub Actions handles CI/deploy checks.
