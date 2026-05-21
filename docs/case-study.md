# Objective
I wanted to create a project that help with my Linux Admin/Devops skills, was viewable by employers, and interesting to me. At the same time I didn't want to do something that was already done and had a step-by-step guide with it, like having an HTTP server with a static web page. Hosting my own minecraft server seemed more interactive and also something that I could actually use for myself.

Although the [Setup Guide](setup.md) focuses on a local approach, a VPS for this project to simulate working outside local networks. I chose to provide instructions for a local setup for simplicity.

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
The general flow is someone pushes code, CI checks it, and then once it passes it would be ready for manual deployment. I had worked with git and GitHub in the past when cloning other repositories, but not to this extent.

The CI part is done with GitHub Actions. The workflow has been setup to install the needed dependencies to verify the Django webapp is able to boot up. Since I was testing on my VPS I couldn't easily confirm that all of this worked outside my environment. The workflow wouldn't be able to confirm that for sure, but it did catch a lot of obvious errors I missed.

Along with that I had to get used to branch workflow. Since I'm the only person on this project I could have cmopleted skipped this and avoided the need to add any branch protection, but I wanted to keep an admin mindset while doing this. In a real production environment people aren't just merging every commit through main, they have to make a pull request. To limit myself to using the correct process I disabled the admin bypass in the branch rules. Got used to it pretty quickly.

A Continuous Deployment pipeline isn't something that I wanted. I still wanted to manually deploy changes that were made. I opted for a Continuous Delivery pipeline with the goal of pressing a button in GitHub Actions that will SSH in the VPS, pull down the latest code, and then restart the mc-panel service.

# Ansible
Started out as a steep learning curve, but quickly turned into my favorite part. Before this project had some experience with Ansible, but it was limited and I was used to putting everything into one playbook. I didn't understand the purpose of roles or creating multiple playbooks for one task. Still, I knew that this was something that Linux admins did so I went forward with making roles.

When I started out and there were only a few tasks, I still couldn't see the value with roles. But has those few turned into over 100 I became grateful that I was using them. Roles let me split up server configuration into chunks. Whenever there was an error (and there were a lot) I was able to quickly narrow down where it was contained since it would be tied to a certain role. Using roles also encouraged me not to hard-code everything and make use of variables. This was helpful since if I had to change a template or a file path, I would only need to change the variables instead of updating every instance where I would call upon something.

I had used documentation for the previous steps, like for Docker and Django, but I got the most value out of the Ansible doucmentation. I used a lot of modules I wasn't familiar with, was able to get comfortable with the syntax, and adding options I didn't even know existed. By the end of this section I was added roles for docker, minecraft, the webapp, and a common role to get some basic packages installed.

It took a long time to get through this section, but it was easy to add on new roles since I had a good foundation set up.

# Monitoring
My least favorite part. There really wasn't that much to monitor except the one minecraft container I had so it and seeing one line move up and down on a graph wasn't interesting, but I'm still glad I learned this. It is much easier to look a dashboard rather than run command to determine if something is up and running. Used a combination of Prometheus, Grafana, cAdvisor, and Node Exporter.

Pulling a community made dashboard was an easy way to monitor the system, but I still needed a custom dashboard for monitoring the containers (and for learning how to make a dashboard). Learning PromQL queries took some time, but after a while I was able to find queries that were able to show memory/CPU usage of the minecraft container. I also found a separate query that was able to show me how many containers are active. It was pretty bare bones, but still lets me assess the state of the server at a glance.

I made compose files that were used for setting up Prometheus/Grafana, but the custom dashboard were left on the server and I didn't include a way of transferring them over. That does mean not every aspect of this project has been reproducbile, but I do want to explore options for automating the monitoring setup in the future.

# Security
So far I've had everything listening to the local host to keep any ports form being exposed. That's not very practical though since the whole point of a VPS is to remotely access a server. Thought about what the public surface should look like and here's what I came up with:

| Service       | Public Surface     | Port  |
| ------------- | ------------------ | ----- |
| SSH           | Public, but secure | 22    |
| Minecraft     | Public             | 25565 |
| Grafana       | Private            | 3000  |
| Django        | Private            | 8000  |
| MediaWiki     | Private            | 8080  |
| Prometheus    | Private            | 9090  |
| MariaDB       | Private            | 3306  |
| Node-Exporter | Private            | 9100  |

Exposing the minecraft port was simple. I adjusted some compose files so it stops pointing towards the local host. Inthe VPS I set up a proxy using Nginx, made sense to give our web services some kind of protection. I also wants to enable https. I didn't have a domain and was going to skip over this, but Let's Encrypt just released Certbot support for IP address certifications as I was working on this project.The certificate only lasts for about a week so I set up a renewal hook to automatically renew the certificate.

fail2ban was added to prevent people attempting to login through SSH. Logging in with a password was already disabled as well as root login, but fail2ban still helps with tracking failed authentication attempts and banning bots.

Lastly I configured the firewall so it match the public surface table above. Only port 22 and 25565 were open.

# Testing
This was the most exciting part. A lot of work was done setting everything up, but so far I've only tested on the VPS. Clearly the VPS is going to have all the required dependencies so I need to ensure that someone looking at this can reproduce this without issue. Found some problems almost immediately. There was some information hard coded in system service files that referenced a specific user which caused the web app to fail. Also I had additional added an Ansible vault to secure the Django secret key, but I didn't consider that other people wouldn't be able to access that vault.

Had to make some significant changes, the biggest being that I added the process for creating the Django secret key within Ansible so that would be kept secret. With the kinks worked out, I loaded up a fresh Rocky Linux 9 VM and was able to confirm that nothing breaks which feels great.

There's still some room to improve though. As of right you would still need to set up the monitoring dashboard even though the containers are present in the repo. With the webapp working, I figured it was time to get to some documentation (like this case study) and revisit once the project looks more presentable.

# Conclusion
Lots of challenges, but I loved this project. Going in I wasn't confident in my Linux skills. I had my RHCSA, but didn't have a good grasp of what a production environment may look like. Not only did I learn these processes, but I applied them in a practical way. Not only do I know what architecture, or know what the playbook says, but it's something I now understand in a clear in distinct way.
