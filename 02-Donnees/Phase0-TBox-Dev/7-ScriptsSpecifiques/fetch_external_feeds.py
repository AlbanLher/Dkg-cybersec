import urllib.request
from pathlib import Path

# URL de la taxonomie ou du feed
MITRE_MOBILE_URL = "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/mobile-attack/mobile-attack.json"

def fetch_feed():
    dest_dir = Path(__file__).resolve().parents[1] / "1-Lexique" / "External_Input" / "Public"
    dest_file = dest_dir / "mitre_mobile_attack_stix.json"
    
    print(f"📥 Téléchargement de MITRE ATT&CK Mobile...")
    urllib.request.urlretrieve(MITRE_MOBILE_URL, dest_file)
    print(f"✅ Fichier enregistré dans : {dest_file.name}")

if __name__ == "__main__":
    fetch_feed()
