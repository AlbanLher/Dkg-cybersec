import sys
from pathlib import Path
import platform
import socket
import json
import logging

# Ajout du chemin parent pour importer config.py
sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import SECURE_INPUT_RESIDENTIAL_PATH

logger = logging.getLogger("LocalHostScanner")

class LocalHostScanner:
    def __init__(self):
        self.output_path = SECURE_INPUT_RESIDENTIAL_PATH

    def scan_current_host(self) -> dict:
        """Exécute un scan local non intrusif du poste (contexte TLP:RED sécurisé)."""
        logger.info("Scan du poste local en cours (contexte TLP:RED)...")
        
        hostname = socket.gethostname()
        try:
            local_ip = socket.gethostbyname(hostname)
        except Exception:
            local_ip = "127.0.0.1"

        os_name = f"{platform.system()} {platform.release()}"
        
        # Structure de l'inventaire enrichie du poste local de l'utilisateur
        host_env = {
            "household_assets": [
                {
                    "asset_id": "asset_user_host_machine",
                    "name": f"Poste de Travail Hôte ({hostname})",
                    "ip_address": local_ip,
                    "os": os_name,
                    "exposed_services": ["SSH", "HTTP-Proxy", "Docker-Daemon"],
                    "zone": "LAN-SECURE"
                },
                {
                    "asset_id": "asset_residential_cam",
                    "name": "Caméra IP Salon",
                    "ip_address": "192.168.1.50",
                    "os": "Embedded Linux",
                    "exposed_services": ["RTSP", "HTTP"],
                    "zone": "LAN"
                }
            ]
        }
        
        # Sauvegarde stricte dans le dossier .private (ignoré par Git)
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.output_path, "w", encoding="utf-8") as f:
            json.dump(host_env, f, indent=4, ensure_ascii=False)
            
        logger.info(f"[SUCCESS] Données TLP:RED locales enregistrées dans : {self.output_path}")
        return host_env

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    scanner = LocalHostScanner()
    scanner.scan_current_host()
