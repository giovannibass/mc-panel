# Troubleshooting
List of the issues I ran into while working on the project. These are copied straight from the notes that I took which helps see how I went about solving some issues. There were a lot of instances where I didn't get it right on the first try, but as the project moved forward I became more confident in my abilities to spot and fix issues.

# Docker

## Docker Engine not connecting to Docker API

After installing I enable the service and confirmed the status. Also used the `hello-world` image. This downloads a test image and runs it as a container with a confirmation message.

```bash
[plato@mcserver ~]$ sudo systemctl enable docker
Created symlink /etc/systemd/system/multi-user.target.wants/docker.service → /usr/lib/systemd/system/docker.service.
[plato@mcserver ~]$ sudo systemctl status docker
○ docker.service - Docker Application Container Engine
     Loaded: loaded (/usr/lib/systemd/system/docker.service; enabled; preset: disabled)
     Active: inactive (dead)
TriggeredBy: ○ docker.socket
       Docs: https://docs.docker.com
[plato@mcserver ~]$ sudo docker run hello-world
failed to connect to the docker API at unix:///var/run/docker.sock; check if the path is correct and if the daemon is running: dial unix /var/run/docker.sock: connect: no such file or directory
```

Good thing I checked with the test image because it looks like we have an error where the service can't connect to the docker API. The reason it wasn't working didn't take long to find... the service wasn't on.

# Python Web Interface

## Testing Django App

*This was right after I put all the python files into their appropriate folders. The next step was to run the Django app and make sure there weren't any issues.*

Now I'm supposed to run the app and test.

```bash
(.venv) gio@pop-os:~/projects/mc-panel$ python manage.py runserver
Watching for file changes with StatReloader
Performing system checks...

Exception in thread django-main-thread:
Traceback (most recent call last):
  File "/usr/lib/python3.12/threading.py", line 1073, in _bootstrap_inner
    self.run()
  File "/usr/lib/python3.12/threading.py", line 1010, in run
    self._target(*self._args, **self._kwargs)
  File "/home/gio/projects/mc-panel/.venv/lib/python3.12/site-packages/django/utils/autoreload.py", line 64, in wrapper
    fn(*args, **kwargs)
  File "/home/gio/projects/mc-panel/.venv/lib/python3.12/site-packages/django/core/management/commands/runserver.py", line 134, in inner_run
    self.check(**check_kwargs)
  File "/home/gio/projects/mc-panel/.venv/lib/python3.12/site-packages/django/core/management/base.py", line 496, in check
    all_issues = checks.run_checks(
                 ^^^^^^^^^^^^^^^^^^
```

I get a whole bunch of errors when running this. From a quick glance it looks like most of them aren't from any of the scripts I made. 2 of them are from `urls.py`, but their file path is different then the one I put in there. Was able to troubleshoot on my own and realized I forgot to import the `include` module. Here is the error I saw that led me to checking out the file.

```
 File "/home/gio/projects/mc-panel/mcpanel/urls.py", line 22, in <module>
    path("", include("dashboard.urls")),
             ^^^^^^^
NameError: name 'include' is not defined
```

After attempting to run again I didn't get any immediate errors!

```bash
(.venv) gio@pop-os:~/projects/mc-panel$ python manage.py runserver
```

When visiting the url `127.0.0.1:8000` I was welcomed with a **DockerException 'Permission Denied'** error through. I'll go through it and see what's happening. Looks like it was able to connect to Docker, but Django doesn't have permission to access it.

Looking at Docker documentation stated that this normally won't work out of the gate because the user running the Django app needs to be in the *docker* group. I didn't even know that Docker made a group when installing but I checked and it's there.

```bash
(.venv) gio@pop-os:~/projects/mc-panel$ cat /etc/group | grep dock
docker:x:986:
```

Adding myself to the docker group:

```bash
(.venv) gio@pop-os:~/projects/mc-panel$ sudo usermod -aG docker gio
[sudo] password for gio:
(.venv) gio@pop-os:~/projects/mc-panel$ id gio
uid=1000(gio) gid=1000(gio) groups=1000(gio),4(adm),27(sudo),108(lpadmin),986(docker)
```

Now I'll try running the Django app again:

```bash
(.venv) gio@pop-os:~/projects/mc-panel$ python manage.py runserver
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
```

Once again no immediate issues. Now I'll go back to `127.0.0.1:8000` and see what I have. Opened it and I'll still getting the same permission denied error. Not sure why this is happening. My guess right now is that since as a user I need to run `sudo` with docker, permission is denied since `sudo` is not being ran in the code itself.

That thinking was kind of on the right path. When looking back at the documentation, it let me know that users in the *docker* group shouldn't have to use `sudo` when using docker commands. Even though I'm in the group now, I may need to try this in a new terminal with a new login session.

Something interesting is happening here:

```bash
gio@pop-os:~$ id gio
uid=1000(gio) gid=1000(gio) groups=1000(gio),4(adm),27(sudo),108(lpadmin),986(docker)
gio@pop-os:~$ docker ps
permission denied while trying to connect to the docker API at unix:///var/run/docker.sock
gio@pop-os:~$ id
uid=1000(gio) gid=1000(gio) groups=1000(gio),4(adm),27(sudo),108(lpadmin)
```

When I first run `id gio`, I'm in the *docker* group. After running `docker ps` and then `id`  it shows I'm not in the `docker` group? After looking this up `id` on it's own will show what groups the current shell process are using. Hopped into a new login session and it's showing that the shell process is now using the *docker* group. Was able to use a docker command without sudo to confirm.

```bash
gio@pop-os:~$ id gio
uid=1000(gio) gid=1000(gio) groups=1000(gio),4(adm),27(sudo),108(lpadmin),986(docker)
gio@pop-os:~$ id
uid=1000(gio) gid=1000(gio) groups=1000(gio),4(adm),27(sudo),108(lpadmin),986(docker)
gio@pop-os:~$ docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

Running the Django app again to see if this will finally work...

And we have a dashboard!

# CI/CD

## GitHub ACtions Setup

_After adding a CI workflow with GitHub Actions I tested it out and immediately got a failure. The value of the workflow was clear, since it showed me that I forgot to add Docker as a module._

After pushing I checked the **Actions** tab on GitHub and I can see that the workflow has been added, but there's a large 'X' so I'm going to assume something went wrong. Can see that it failed under the sanity checks section, specifically when running `docker_service.py`. From looking at the errors themselves we can narrow down what failed:

```
File "/home/runner/work/mc-panel/mc-panel/dashboard/docker_service.py", line 7, in <module>

	import docker

ModuleNotFoundError: No module named 'docker'
Error: Process completed with exit code 1.
```

Wasn't able to find the module `docker`. The Python `docker` module is something that needs to be installed. It's likely that we don't have this included in `requirements.txt`. The fix is simple, we just need to add docker to `requirements.txt`.

```
asgiref==3.11.0
Django==6.0.1
sqlparse==0.5.5
docker
```

Before we commit and push we'll want to commit docker to a specific version for consistency. The easiest way is to check and see what version of the Docker module is in use. We'll need to recreate our python virtual environment first.

```bash
gio@pop-os:~/projects/mc-panel$ python3 -m venv .venv

gio@pop-os:~/projects/mc-panel$ source .venv/bin/activate

(.venv) gio@pop-os:~/projects/mc-panel$ python -m pip install --upgrade pip
Requirement already satisfied: pip in ./.venv/lib/python3.12/site-packages (26.0)
Collecting pip
  Downloading pip-26.0.1-py3-none-any.whl.metadata (4.7 kB)
Downloading pip-26.0.1-py3-none-any.whl (1.8 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.8/1.8 MB 11.5 MB/s  0:00:00
Installing collected packages: pip
  Attempting uninstall: pip
    Found existing installation: pip 26.0
    Uninstalling pip-26.0:
      Successfully uninstalled pip-26.0
Successfully installed pip-26.0.1

(.venv) gio@pop-os:~/projects/mc-panel$ pip install -r requirements.txt
Requirement already satisfied: asgiref==3.11.0 in ./.venv/lib/python3.12/site-packages (from -r requirements.txt (line 1)) (3.11.0)
Requirement already satisfied: Django==6.0.1 in ./.venv/lib/python3.12/site-packages (from -r requirements.txt (line 2)) (6.0.1)
Requirement already satisfied: sqlparse==0.5.5 in ./.venv/lib/python3.12/site-packages (from -r requirements.txt (line 3)) (0.5.5)
Requirement already satisfied: docker==7.1.0 in ./.venv/lib/python3.12/site-packages (from -r requirements.txt (line 4)) (7.1.0)
...
```

Made a virtual environment and installed everything from `requirements.txt` so it has the same dependency CI installs. The output shows we are using `7.1.0` for the docker module. We could have also ran `python -m pip show docker` to check now. With these changes made we'll commit, push, and the CI workflow should automatically run again.

```bash
gio@pop-os:~/mc-panel$ git status
On branch main
Your branch is up to date with 'origin/main'.

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   requirements.txt

no changes added to commit (use "git add" and/or "git commit -a")

gio@pop-os:~/mc-panel$ cat requirements.txt
asgiref==3.11.0
Django==6.0.1
sqlparse==0.5.5
docker==7.1.0

gio@pop-os:~/mc-panel$ git add requirements.txt

gio@pop-os:~/mc-panel$ git commit -m "Added Docker SDK dependency to requirements.txt"
[main 9e90711] Added Docker SDK dependency to requirements.txt
 ...
 
gio@pop-os:~/mc-panel$ git push
Enumerating objects: 5, done.
...
```

Everything passed now! Looks like not being able to import the docker module was the only hold up.

## Making the Django app a service

_When setting up CD, I wanted to make the Django app a service since systemd services are easier to control. The idea was to install gunicorn to start the Django app, make a systemd unit file, and then test the service. Installed unicron instead of gunicorn which messed everything up._

After adding executable permissions to the script, we'll go ahead and test it to see what happens.

```bash
(.venv) gio@pop-os:~/mc-panel$ sudo vim /usr/local/bin/deploy-mc-panel.sh
```

Installing it in `/usr/local/bin` because we want to separate the application code from the operation tools we're using.

Config files go in `/etc`, binaries/scripts go in `/usr/loca/bin`, data in `/var`, etc. Keeping that separation is a good practice.

```bash
gio@pop-os:~$ sudo systemctl status mc-panel --no-pager
× mc-panel.service - mc-panel Django app (gunicorn)
     Loaded: loaded (/etc/systemd/system/mc-panel.service; enabled; preset: enabled)
     Active: failed (Result: exit-code) since Thu 2026-02-26 17:18:47 EST; 1h 32min ago
   Duration: 1ms
    Process: 1797 ExecStart=/home/gio/mc-panel/.venv/bin/gunicorn mcpanel.wsgi:application --bind 127.0.0.1:8000 (code=exited, status=203/EXEC)
   Main PID: 1797 (code=exited, status=203/EXEC)
        CPU: 548us

Feb 26 17:18:47 pop-os systemd[1]: mc-panel.service: Scheduled restart job, restart counter is at 5.
Feb 26 17:18:47 pop-os systemd[1]: mc-panel.service: Start request repeated too quickly.
Feb 26 17:18:47 pop-os systemd[1]: mc-panel.service: Failed with result 'exit-code'.
Feb 26 17:18:47 pop-os systemd[1]: Failed to start mc-panel.service - mc-panel Django app (gunicorn).
```

Immediately got an error when running the script. The message shows that gunicorn wasn't able to start. I went to the file path shown in the process, but found that `~/mc-panel/.venv/bin/gunicorn` didn't exist. Retracted my steps and saw that I installed `unicorn` instead of `gunicorn`. Using `pip install gunicorn` and trying again should fix this.

```bash
(.venv) gio@pop-os:~/mc-panel$ sudo systemctl status mc-panel.service
● mc-panel.service - mc-panel Django app (gunicorn)
     Loaded: loaded (/etc/systemd/system/mc-panel.service; enabled; preset: enabled)
     Active: active (running) since Thu 2026-02-26 19:01:14 EST; 1s ago
   Main PID: 13140 (gunicorn)
      Tasks: 3 (limit: 18935)
     Memory: 18.8M (peak: 18.8M)
        CPU: 71ms
     CGroup: /system.slice/mc-panel.service
             ├─13140 /home/gio/mc-panel/.venv/bin/python /home/gio/mc-panel/.venv/bin/gunicorn mcpanel.wsgi:>
             └─13142 /home/gio/mc-panel/.venv/bin/python /home/gio/mc-panel/.venv/bin/gunicorn mcpanel.wsgi:
```

After actually installing `gunicorn` the service is up and running.

# Ansbile

## Installing Python Packages

_Was working on the webapp role which required that I install packages. Ran into an error stating that a task for installing Python dependencies had failed._

Documentation for the `ansible.builtin.pip` module shows that we can point this to a `requirements.txt` file with the `requiremetns:` parameter.

```yml
- name: Ensure webapp Python dependencies are installed
  ansible.builtin.pip:
    requirements: "{{ webapp_dir }}/requirements.txt"
    virtualenv: "{{ webapp_venv_dir }}"
```

`virtualenv` tells Ansible to install packages with the virtual environment instead of the system Python.

Running the check...and we got an error stating that the task has failed. Won't copy the whole thing, but here's a snippet:

```
TASK [webapp : Ensure webapp Python dependencies are installed] ********************************************
[ERROR]: Task failed: Module failed: Failed to import the required Python library (packaging) on mcserver's Python /usr/bin/python3.12. Please read the module documentation and install it in the appropriate location. If the required library is installed, but Ansible is using the wrong Python interpreter, please consult the documentation on ansible_python_interpreter: No module named 'packaging'
```

The VPS doesn't have the Python 3.12 support packages it needs. We'll add a task before the venv/pip tasks run to make sure this is corrected.

```yml
- name: Ensure webapp code is deployed
  ansible.builtin.git:
    repo: "{{ webapp_repo_url }}"
    dest: "{{ webapp_dir }}"
    version: "{{ webapp_version }}"

- name: Ensure Python 3.12 packaging tools are installed
  ansible.builtin.package:
    name:
      - python3.12-pip
      - python3.12-setuptools
    state: present
```

Running the check... we see a change in this task, but still get the same error. Did the live run this time and we got an error saying that Django 6.0.1 doesn't exists, when it does exists:

```bash
ERROR: No matching distribution found for Django==6.0.1
WARNING: You are using pip version 21.3.1; however, version 26.0.1 is available.
You should consider upgrading via the '/srv/webapp/.venv/bin/python3 -m pip install --upgrade pip' command.
```

I believe we can figure out the problem from here though.

- Django 6.0.1 only supports Python 3.12+
- RHEL/Rocky points to Python 3.9 by default. [https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/installing_and_using_dynamic_programming_languages/assembly_installing-and-using-python_installing-and-using-dynamic-programming-languages]
- We can look at the virtual environment python version to see if 3.9 is being used.

```bash
[plato@mcserver ~]$ /srv/webapp/.venv/bin/python --version
Python 3.9.25
```

If we can get our virtual environment to use 3.12, then the problem should be solved. We'll go to our `Ensure webapp virtual envrionmetn exists task` and change

```
cmd: python3 -m venv {{ webapp_venv_dir }}
```

to 

```
cmd: python3.12 -m venv {{ webapp_venv_dir }}
```

Running the check... and we get no errors! Took a while to troubleshoot, but this was a good learning experience. When checking the virtual environment python version again we can see I have 3.12 now.

```
[plato@mcserver ~]$ /srv/webapp/.venv/bin/python --version
Python 3.12.12

