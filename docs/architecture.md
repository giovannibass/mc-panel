# Architecture
Everything starts with the user interacting with the Django web app through a browser. Django is able to communicate with Docker which is how the Minecaft container is able to start/stop. Below is a simple arrow chart that demonstrates how each layer interacts with the next to get the desired result.

User Browser -> Gunicorn / Django App -> Docker Engine -> Minecraft Container

Outside the processes involved for maintaining the app, they are other pieces that help with making administration of the map much easier. All of these are broken down in the next section.

## Ansible

## Django Webapp

## Prometheus/Grafana

## CI/CD

## MediaWiki
