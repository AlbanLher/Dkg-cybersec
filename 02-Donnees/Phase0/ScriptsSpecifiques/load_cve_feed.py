#!/usr/bin/env python3
"""
Charge les dernières CVE depuis l'API CIRCL v2 (sans clé API).
Usage: python load_cve_feed.py > cve_data.ttl
"""
import requests
from datetime import datetime

# API CIRCL v2 (limite : 100 requêtes/jour sans clé)
CIRCL_API_URL = "https://cve.circl.lu/api/last/120"  # Dernières 120 CVE

def fetch_recent_cves():
    """Récupère les dernières CVE (120 max)."""
    try:
        response = requests.get(CIRCL_API_URL)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"Erreur HTTP : {e}")
        return []

def cve_to_ttl(cve):
    """Convertit une CVE en format TTL."""
    cve_id = cve.get("id", "unknown")
    cvss = cve.get("cvss", 0)
    summary = cve.get("summary", "").replace('"', '\\"').replace("\n", " ")
    return f"""
@prefix cve: <https://cve.mitre.org/> .
@prefix : <http://example.org/cyber-ontology#> .

cve:{cve_id} a :Vulnerability ;
    foaf:name "{cve_id}" ;
    :cvssScore {cvss} ;
    :description "{summary}" .
"""

def main():
    cves = fetch_recent_cves()
    if not cves:
        print("Aucune CVE récupérée.")
        return

    print("@prefix : <http://example.org/cyber-ontology#> .")
    print("@prefix cve: <https://cve.mitre.org/> .")
    print("@prefix foaf: <http://xmlns.com/foaf/0.1/> .")
    print(f"\n# Généré le {datetime.now().isoformat()}\n")
    for cve in cves:
        print(cve_to_ttl(cve))

if __name__ == "__main__":
    main()
