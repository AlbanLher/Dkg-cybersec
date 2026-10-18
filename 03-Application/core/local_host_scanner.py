# 03-Application/agents/local_host_scanner.py
# =============================================================================
# LocalHostScanner v2 — scan RÉEL non intrusif du poste (TLP:RED, .private/)
# Terrain « scan » du démonstrateur P8, à côté des seeds foyer/hote simulés.
# Non intrusif : lecture locale uniquement (hostname, IP, OS, runtime,
# ports locaux en écoute sondés sur 127.0.0.1 — jamais de paquet vers
# l'extérieur, jamais d'écriture hors .private/).
# HITL : ce module ne s'exécute QUE sur clic explicite (routes_phase8
# POST /scan) — jamais au chargement. Le consentement est journalisé.
# =============================================================================
import sys
from pathlib import Path
import platform
import socket
import shutil
import sysconfig
import json
import logging

sys.path.append(str(Path(__file__).resolve().parent.parent))
from core.config import SECURE_INPUT_HOST_SCAN_PATH

logger = logging.getLogger("LocalHostScanner")

# Ports locaux sondés (connect_ex 127.0.0.1, timeout 0.1 s — non intrusif)
PROBE_PORTS = [21, 22, 23, 80, 443, 445, 554, 1900, 3000, 3306,
               5432, 5900, 6379, 8080, 8443, 9090, 11434]
PORT_NAMES = {21: "FTP", 22: "SSH", 23: "Telnet", 80: "HTTP", 443: "HTTPS",
              445: "SMB", 554: "RTSP", 1900: "UPnP", 3000: "HTTP-Dev",
              3306: "MySQL", 5432: "PostgreSQL", 5900: "VNC", 6379: "Redis",
              8080: "HTTP-Alt", 8443: "HTTPS-Alt", 9090: "Prometheus",
              11434: "Ollama"}


def _listening_local_ports() -> list:
    """Sonde non intrusive : ports en écoute sur 127.0.0.1 uniquement."""
    opened = []
    for port in PROBE_PORTS:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.1)
            if s.connect_ex(("127.0.0.1", port)) == 0:
                name = PORT_NAMES.get(port, "unknown")
                opened.append(f"{name} (Port {port})")
    return opened


def _detect_components() -> list:
    """Détection locale de composants logiciels (lecture, jamais d'exécution
    de binaire tiers : shutil.which + versions de l'interpréteur courant).
    componentId au format du fonds CTI (comp-*) — la confrontation P9
    s'appliquera telle quelle si le fonds référence le produit."""
    comps = [{
        "component_id": "comp-cpython",
        "name": "CPython (interpréteur courant)",
        "version": platform.python_version(),
        "support_status": "supported",
    }]
    # Binaires courants présents dans le PATH (présence only — discret)
    for cmd, cid, name in [
        ("node", "comp-nodejs", "Node.js"),
        ("docker", "comp-docker-engine", "Docker Engine"),
        ("git", "comp-git", "Git"),
        ("nginx", "comp-nginx", "Nginx"),
        ("apache2", "comp-apache-http-server", "Apache HTTP Server"),
        ("java", "comp-openjdk", "OpenJDK"),
    ]:
        if shutil.which(cmd):
            comps.append({"component_id": cid, "name": name,
                          "version": "unknown", "support_status": "unknown"})
    return comps


class LocalHostScanner:
    """Collecte TLP:RED du poste réel → JSON .private/ (SSOT config.py)."""

    def __init__(self):
        self.output_path = SECURE_INPUT_HOST_SCAN_PATH

    def scan_current_host(self) -> dict:
        logger.info("Scan du poste local (TLP:RED, non intrusif)...")
        hostname = socket.gethostname()
        try:
            local_ip = socket.gethostbyname(hostname)
        except Exception:
            local_ip = "127.0.0.1"

        host_env = {
            "scan_source": "real-local-host",
            "household_assets": [{
                "asset_id": "asset_user_host_machine",
                "name": f"Poste de Travail Hôte ({hostname})",
                "ip_address": local_ip,
                "os": f"{platform.system()} {platform.release()}",
                "exposed_services": _listening_local_ports(),
                "zone": "LAN-SECURE",
            }],
            "software_components": _detect_components(),
        }

        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.output_path, "w", encoding="utf-8") as f:
            json.dump(host_env, f, indent=4, ensure_ascii=False)
        logger.info(f"[SUCCESS] Scan TLP:RED enregistré : {self.output_path}")
        return host_env


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    print("=== Scan local (TLP:RED) — exécution MANUELLE/HITL uniquement ===")
    data = LocalHostScanner().scan_current_host()
    print(json.dumps(data, indent=2, ensure_ascii=False))
