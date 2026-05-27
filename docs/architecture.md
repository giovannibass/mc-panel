# Architecture

## Overview

## Request Flow
What happens when someone clicks a button in the dashboard?

The user clicks a button on the web dashboard. This interacts with the Nginx proxy, which will forward the request to Django. The action of the container starting is triggered when a certain URL is entered (whih is triggered by the button). [mc-panel/dashboard/urls.py](mc-panel/dashboard/urls.py) controls what Python function runs after requesting at URL. For the container starting, it's going to request that the `server_start` function is ran which starts the container. A similar process is followed when stopping the container.

## Component Responsibilities

What each component does

Browser | Serves as web control panel that so the user can turn the Minecraft container on/off.
Nginx | Proxy that sits in front of the webapp. Any interaction the user makes goes here first.
Ansible | Tool for provisioning the server with the necessary packages/configurations for this project.
GitHub Actions | Automation tool that can run checks on code before it gets merged.
Docker Engine | Runs the containers and interacts with other tools like Pyhton that can manage them.
Minecraft Server container | The Minecraft server
Prometheus | Queries data
Grafana | Displays queried data from Prometheus on convenient dashboards
Django | Framework used for the control panel webapp.
Gunicorn | Complements Django by running Python code for the webapp
systemd | 

## Container Management Flow

How does Django control Minecraft container?

Docker runs the game, Django runs the web control panel. How do we get the two to work together?

Gunicorn is what sits inbetween the http server and Docker.

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

## CI/CD Flow

GitHub Actions verifies and helps manage changes before they are deployed.

## Monitoring Architecture

The Prometheus/Grafana stack work together to monitor the status of the Linux environment as well as the container environment.

Prometheus
Grafana
nodeExporter
cAdvisor

## Network and Service Exposure

Nginx acts as the public facing web service.

Should list here all the publicly exposed ports.

## Security Boundaries

Think about how the components you chose led to a more secure environment.

## Architecture Decisions
