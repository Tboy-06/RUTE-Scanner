"""
Cloudflare Mobile Tunnel Bridge for RUTE Scanner
Allows opening the local scanner on any phone over 4G/5G mobile cellular networks
without port-forwarding or router configuration.
"""

import os
import re
import sys
import time
import subprocess
import threading
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger("tunnel_manager")

_TUNNEL_PROC: Optional[subprocess.Popen] = None
_PUBLIC_URL: Optional[str] = None
_TUNNEL_STATUS: str = "stopped"
_STOP_REQUESTED = False


def _find_cloudflared_bin() -> Optional[str]:
    """Finds cloudflared executable in local project bin or system PATH."""
    local_bin = os.path.join(os.path.dirname(__file__), "bin", "cloudflared.exe")
    if os.path.isfile(local_bin):
        return local_bin

    # Search PATH
    for path_dir in os.environ.get("PATH", "").split(os.pathsep):
        candidate = os.path.join(path_dir, "cloudflared.exe")
        if os.path.isfile(candidate):
            return candidate

    return None


def start_tunnel(port: int = 8080) -> Dict[str, Any]:
    """Starts cloudflared quick tunnel and extracts the public trycloudflare.com URL."""
    global _TUNNEL_PROC, _PUBLIC_URL, _TUNNEL_STATUS, _STOP_REQUESTED

    if _TUNNEL_PROC and _TUNNEL_PROC.poll() is None and _PUBLIC_URL:
        return {"status": "running", "url": _PUBLIC_URL, "port": port}

    cloudflared = _find_cloudflared_bin()
    if not cloudflared:
        return {
            "status": "error",
            "message": "cloudflared.exe not found in bin/ or system PATH.",
            "url": None
        }

    _STOP_REQUESTED = False
    _PUBLIC_URL = None
    _TUNNEL_STATUS = "starting"

    cmd = [cloudflared, "tunnel", "--url", f"http://127.0.0.1:{port}"]

    try:
        # On Windows, hide command window
        startupinfo = None
        if os.name == "nt":
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = 0

        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            startupinfo=startupinfo
        )
        _TUNNEL_PROC = proc

        # Read output in background thread to find URL
        def _monitor_output():
            global _PUBLIC_URL, _TUNNEL_STATUS
            url_pattern = re.compile(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com")
            while proc.poll() is None and not _STOP_REQUESTED:
                line = proc.stdout.readline()
                if not line:
                    break
                match = url_pattern.search(line)
                if match:
                    _PUBLIC_URL = match.group(0)
                    _TUNNEL_STATUS = "running"
                    logger.info(f"Cloudflare Tunnel active at: {_PUBLIC_URL}")
            if not _STOP_REQUESTED:
                _TUNNEL_STATUS = "stopped"

        thread = threading.Thread(target=_monitor_output, daemon=True)
        thread.start()

        # Quick check for URL to appear (up to 2.5s)
        start_wait = time.time()
        while time.time() - start_wait < 2.5:
            if _PUBLIC_URL:
                return {"status": "running", "url": _PUBLIC_URL, "port": port}
            time.sleep(0.2)

        return {"status": "starting", "message": "Tunnel is initializing in background.", "url": _PUBLIC_URL, "port": port}

    except Exception as e:
        _TUNNEL_STATUS = "error"
        return {"status": "error", "message": str(e), "url": None}


def stop_tunnel() -> Dict[str, Any]:
    """Stops the active cloudflared tunnel."""
    global _TUNNEL_PROC, _PUBLIC_URL, _TUNNEL_STATUS, _STOP_REQUESTED
    _STOP_REQUESTED = True
    if _TUNNEL_PROC:
        try:
            _TUNNEL_PROC.terminate()
            _TUNNEL_PROC.wait(timeout=2)
        except Exception:
            try:
                _TUNNEL_PROC.kill()
            except Exception:
                pass
        _TUNNEL_PROC = None

    _PUBLIC_URL = None
    _TUNNEL_STATUS = "stopped"
    return {"status": "stopped"}


def get_tunnel_status() -> Dict[str, Any]:
    """Returns the current status of the Cloudflare tunnel."""
    global _TUNNEL_PROC, _PUBLIC_URL, _TUNNEL_STATUS
    is_alive = _TUNNEL_PROC is not None and _TUNNEL_PROC.poll() is None
    if not is_alive and _TUNNEL_STATUS == "running":
        _TUNNEL_STATUS = "stopped"
        _PUBLIC_URL = None

    return {
        "status": _TUNNEL_STATUS if is_alive else "stopped",
        "url": _PUBLIC_URL if is_alive else None,
        "is_available": _find_cloudflared_bin() is not None
    }
