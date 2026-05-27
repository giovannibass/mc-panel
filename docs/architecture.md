# Architecture

## Overview

## Request Flow
What happens when someone clicks a button in the dashboard?

## Component Responsibilities

What each component does

Browser
Nginx
Ansible
GitHub Actions
Docker Engine
Minecraft Server container
Prometheus
Grafana
Django
Gunicorn
systemd

## Container Management Flow

How does Django control Minecraft container?

Docker runs the game, Django runs the web control panel. How do we get the two to work together?

## Ansible Provisioning Flow

How is the playbook organized? The purpose of Ansible in the project is to make server setup easy and repeatable.

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
