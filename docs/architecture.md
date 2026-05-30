# Architecture

## Request Flow
What happens when someone clicks a button in the dashboard?

The user clicks a button on the web dashboard. This interacts with the Nginx proxy, which will forward the request to Gunicorn. Gunicorn will start work processes that load the Django app. The action of the container starting is triggered when a certain URL is entered (whih is triggered by the button). [mc-panel/dashboard/urls.py](mc-panel/dashboard/urls.py) controls what Python function runs after requesting at URL. For the container starting, it's going to request the `server_start` function. Docker SDK is used to manager the Docker Engine through Python. Django uses Docker SDK to ask Docker Engine to start the minecraft container.

## Component Responsibilities

What each component does

| Component | Responsibility |
|---|---|
| Browser | Provides the user interface for the control panel so the user can view and manage the Minecraft server container. |
| Nginx | Acts as the reverse proxy in front of the web application. User requests reach Nginx first before being forwarded to the app. |
| Gunicorn | Runs the Django application as a production-style Python application server. |
| Django | Provides the web framework, dashboard views, and application logic for the control panel. |
| Docker Engine | Runs and manages the containers. The Django app can communicate with Docker to inspect or manage the Minecraft server container. |
| Minecraft Server Container | Runs the actual Minecraft server process. |
| systemd | Manages the Django/Gunicorn web application as a Linux service. |
| Ansible | Provisions the server with the required packages, configuration files, services, and application setup. |
| GitHub Actions | Runs automated checks on code before changes are merged or deployed. |
| Prometheus | Collects and queries metrics from the host and container environment. |
| Grafana | Displays Prometheus metrics in dashboards for easier monitoring and troubleshooting. |

## Ansible Provisioning Flow

How is the playbook organized? The purpose of Ansible in the project is to make server setup easy and repeatable.

This Ansible setup is split into 6 different roles in this order: common, docker, minecraft, webapp, monitoring, and security. The top-level playbook is simple and runs through each of the roles. Each role has its own `tasks/main.yml` playbook that runs through each task that needs to be ran.

### common

Verifies that common packages like git, curl, vim, and firewalld are installed needed before moving forward to making any significant changes. Future roles will depend on these packages being installed and ready to use.

### docker

The Minecraft server runs off a container, so it's important that we set up Docker early in the provisioning process.  THis tasks install all the packages needed for future roles to use.

### minecraft

Makes use of the Docker packages that were installed in the previous role to deploy a compose file and get the Minecraft container up and runnning.

### webapp

Pulls down the code for the webapp repo, making use of `git` which was installed in the common role. Here we also have the Django secret key created which is needed for authenticated. This role also deploys the systemd unit file used to start/manage the webapp.

### monitoring

Deploys the Prometheus/Grafana monitoring stack. Prometheus, Grafana, node-exporter, and cAdvisor are ran through containers and as of now you would need to setup the dashboard manually. I will need to include a guide for setting up a dashboard, but in the future I want to see if this process can also be automated through Ansible.

### security

Installs security packages, fail2ban being one of them.
