# Objective
I wanted to create a project that help with my Linux Admin/Devops skills, was viewable by employers, and interesting to me. At the same time I didn't want to do something that was already done and had a step-by-step guide with it, like having an HTTP server with a static web page. Hosting my own minecraft server seemed more interactive and also something that I could actually use for myself.

Although the [Setup Guide](docs/setup.md) focuses on a local approach, a VPS for this project to simulate working outside local networks. I chose to provide instructions for a local setup for simplicity.

# Setting Up
When thinking about how I was going to pull this off, I decided to list out all the skills I wanted to showcase and then find a way to incorporate into the project. Here's what I started with:

- Linux server administration with RHEL
- systemd service management
- Containerization
- Ansible automation and repeatable provisioning
- CI/CD
- Prometheus and Grafana for monitoring
- Troubleshooting real deployment issues

I'm happy to say that I learned a lot more with this project, but with this as the foundation it was time to think about the architecture. Wasn't sure how I was going to get it done, but I knew I wanted a simple webpage that allowed you to press a button to turn the server on/off. AI was able to help with coming with a plan that made sense.

The user will interact with the browser with will interact with Docker to start a Minecraft container. That's all the product is, but the real work comes after with setting up CI/CD, documenting, creating Ansible playbooks, and setting up Prometheus/Grafana.

# Installing Docker
This was straightforward. Download Docker on to the VPS I was using and then run the Minecraft container to confirm it works.

And already I ran into my first dilemma. The VPS has a public IP, and in order to test the container on my local machine I would need to expose the port on the VPS. Don't want just anyone connecting to it, so I had to find a way to only allow myself access.

Looking up how to do this pointed me towards local port forwarding, which I hadn't done before. I pointed the container to the loopback address so only the Docker host can access it. From there I used `ssh -L` so the host would connect to the VPS when it detected a connection to port 25565 (Minecraft's default port) on my host machine. Not sure if it's the best way to test, but it's secure and allowed me to confirm that the container on the VPS was working as it should.

I also started my first bit of automation here by creating a compose file.

# Documenting with MediaWiki
One of my goals was to also create a wiki on the VPS. For this I made a compose file that spun up a MediaWiki and MariaDB container. I was already notating the entire process with my own notes, but showing my ability to document only strengthens this project. The notes I took are in Markdown, and MediaWiki has its own markup language so transferring notes over took a LONG time.

Eventually I decided to pause this for now and revisit as an add-on. I still had my own personal documentation which was important and I was more excited to learn something new. Now that the project is finished I can go back and add the Wiki setup in the repo. Some of the documentation from the wiki will be included here, [Architecture](docs/architecture.md), and [Troubleshooting](docs/troubleshooting.md). 

# Python Web Interface
-

# CI/CD
-

# Ansible
-

# Monitoring
-

# Security and Monitoring
-

# Testing
- 
