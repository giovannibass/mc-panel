# Setup Guide

This guide explains how to set up `mc-panel` on a fresh Rocky Linux 9 VM. This setup also assumes you are running Ansible **inside the same VM** that you want to configure, but changes can be made to provision this to a remote server.

After setup, the dashboard should be available at:

```text
http://127.0.0.1:8000
```

---

## 1. Install required packages

Log into the Rocky 9 VM and install the required system packages:

```bash
sudo dnf install -y git epel-release python3-pip python3.12 python3.12-pip
sudo dnf install -y pipx
```

---

## 2. Install Ansible Core

Install Ansible Core using Python 3.12:

```bash
pipx install --python python3.12 ansible-core==2.20.3
```

Verify the Ansible version:

```bash
ansible --version
```

You should see:

```text
ansible [core 2.20.3]
```

---

## 3. Clone the repository

```bash
mkdir -p ~/project
cd ~/project
git clone https://github.com/giovannibass/mc-panel.git
cd mc-panel/ansible
```

---

## 4. Install required Ansible collections

Run this command from inside the `mc-panel/ansible` directory:

```bash
ansible-galaxy collection install -r collections/requirements.yml -p ./collections --force
```

This installs the required Ansible collections that are going to be used by the playbook.

---

## 5. Inventory file

Copy the local inventory example:

```bash
cp inventory.local.ini.example inventory.ini
```

Open the file:

```bash
vim inventory.ini
```

For a local Rocky 9 VM test, the file should look similar to this:

```ini
[mcservers]
mc1 ansible_connection=local ansible_python_interpreter=/usr/bin/python3

[mcservers:vars]
django_allowed_hosts=127.0.0.1,localhost
django_debug=false
```

Everything can be left as is. For those you want to provision this to a remote server there is a `inventory.remote.ini.example` template available as well. Save and exit the file.

---

## 6. Test Ansible connectivity

```bash
ansible -i inventory.ini mcservers -m ping
```
Should return a success.

---

## 7. Run the Ansible playbook

Run the live playbook:

```bash
ansible-playbook -i inventory.ini site.yml -K
```

Enter your sudo password when prompted. It will ask for a BECOME password, but you will still use your sudo password. It's at this point that everything will install.

---

## Important note about `--check`

Please don't use `--check` to do a dry run for the playbook. The dry run will likely fail because because there's a task that tries to install Docker packages and it can't do that because a Docker repository can't be created in check mode. Will adjust the playbooks so `--check` can be ran in the future.

---

## 8. Add your user to the Docker group

After the playbook installs Docker, add your current user to the Docker group. This will let the user run Docker commands without being prompted for the sudo password.

```bash
sudo usermod -aG docker "$(whoami)"
newgrp docker
```

Confirm that your user can access Docker without using sudo.

```bash
docker ps
```

---

## 9. Fix the systemd service user and group

The `mc-panel` systemd service needs run as a valid user and group.

Edit the service file:

```bash
sudo vim /etc/systemd/system/mc-panel.service
```

Find the lines that look like this:

```ini
User=plato
Group=plato
```

Change `plato` so it matches the user and group you want to run the web app as.

For this local VM setup, you can use your current user.

For example, if your user is `gio` and your group is `gio`, use:

```ini
User=gio
Group=gio
```

---

## 10. Reload systemd and restart mc-panel

After changing the service file, reload systemd:

```bash
sudo systemctl daemon-reload
```

Restart the service:

```bash
sudo systemctl restart mc-panel
```

Check the service status:

```bash
sudo systemctl status mc-panel
```

The service should show:

```text
active (running)
```

---

## 11. Open the dashboard

The Django web app runs on port `8000`.

Open this in your browser:

```text
http://127.0.0.1:8000
