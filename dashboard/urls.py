# dashboard/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("servers/<str:container_id>/start/", views.server_start, name="server_start"),
    path("servers/<str:container_id>/stop/", views.server_stop, name="server_stop"),
]

