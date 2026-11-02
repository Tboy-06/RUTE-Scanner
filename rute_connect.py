"""
RuteConnect Engine - Proprietary Remote Tunnel & Mobile Pairing Bridge
Rebranded and adapted from the FreeDomain / secure namespace architecture.
Provides zero-configuration local-to-phone pairing and remote tunnel generation.
"""

import socket
import secrets
from typing import Dict, Any

_PAIRING_TOKEN = secrets.token_hex(4).upper()


class RuteConnect:
    """Manages pairing and remote accessibility for mobile trading."""

    @staticmethod
    def get_connection_manifest(port: int = 8080) -> Dict[str, Any]:
        """Returns direct pairing info, local LAN URLs, and remote tunnel guides."""
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
        except Exception:
            local_ip = "127.0.0.1"
        finally:
            s.close()

        return {
            "pairing_code": _PAIRING_TOKEN,
            "local_network": {
                "url": f"http://{local_ip}:{port}",
                "status": "ACTIVE_ON_LOCAL_WIFI",
                "ip": local_ip,
                "port": port
            },
            "remote_cellular_bridge": {
                "status": "READY_TO_LAUNCH",
                "recommended_tunnel": "Cloudflare Quick Tunnel (Free, zero port-forwarding, HTTPS encrypted)",
                "one_line_command": f"winget install Cloudflare.cloudflared; cloudflared tunnel --url http://localhost:{port}"
            }
        }
