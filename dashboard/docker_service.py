# dashboard/docker_service.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import docker
from docker.errors import NotFound, APIError


@dataclass
class ServerInfo:
    id: str
    name: str
    status: str           # e.g. "running", "exited"
    is_running: bool
    mc_type: str          # e.g. "java", "bedrock", or "unknown"
    ports: List[str]      # e.g. ["25565/tcp -> 0.0.0.0:25565"]


def _client() -> docker.DockerClient:
    # Uses the default local socket: unix:///var/run/docker.sock
    return docker.from_env()


def list_mc_servers() -> List[ServerInfo]:
    """
    List containers that look like Minecraft servers (filtered by label).
    """
    client = _client()

    containers = client.containers.list(
        all=True,
        filters={"label": "mc.platform=true"},
    )

    servers: List[ServerInfo] = []
    for c in containers:
        attrs: Dict[str, Any] = c.attrs  # raw Docker API data (big dict)
        labels = attrs.get("Config", {}).get("Labels", {}) or {}
        mc_type = labels.get("mc.type", "unknown")

        port_lines: List[str] = []
        ports = attrs.get("NetworkSettings", {}).get("Ports", {}) or {}
        # ports example: {"25565/tcp": [{"HostIp":"0.0.0.0","HostPort":"25565"}], ...}
        for container_port, mappings in ports.items():
            if not mappings:
                port_lines.append(f"{container_port} -> (not published)")
                continue
            for m in mappings:
                host_ip = m.get("HostIp", "")
                host_port = m.get("HostPort", "")
                port_lines.append(f"{container_port} -> {host_ip}:{host_port}")

        servers.append(
            ServerInfo(
                id=c.id,
                name=c.name,
                status=c.status,
                is_running=(c.status == "running"),
                mc_type=mc_type,
                ports=sorted(port_lines),
            )
        )

    # nice stable order in the UI
    return sorted(servers, key=lambda s: s.name.lower())


def start_container(container_id: str) -> None:
    client = _client()
    try:
        c = client.containers.get(container_id)
        c.start()
    except NotFound as e:
        raise ValueError("Container not found") from e
    except APIError as e:
        raise RuntimeError(f"Docker API error: {e.explanation}") from e


def stop_container(container_id: str, timeout: int = 10) -> None:
    client = _client()
    try:
        c = client.containers.get(container_id)
        c.stop(timeout=timeout)
    except NotFound as e:
        raise ValueError("Container not found") from e
    except APIError as e:
        raise RuntimeError(f"Docker API error: {e.explanation}") from e

