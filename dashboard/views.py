# dashboard/views.py
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .docker_service import list_mc_servers, start_container, stop_container


def home(request):
    servers = list_mc_servers()
    return render(request, "dashboard/home.html", {"servers": servers})


@require_POST
def server_start(request, container_id: str):
    try:
        start_container(container_id)
        messages.success(request, "Server starting...")
    except Exception as e:
        messages.error(request, f"Failed to start: {e}")
    return redirect("home")


@require_POST
def server_stop(request, container_id: str):
    try:
        stop_container(container_id)
        messages.success(request, "Server stopping...")
    except Exception as e:
        messages.error(request, f"Failed to stop: {e}")
    return redirect("home")

