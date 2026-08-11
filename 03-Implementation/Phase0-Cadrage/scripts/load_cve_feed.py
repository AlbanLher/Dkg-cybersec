#!/usr/bin/env python3
"""
Charge les dernières CVE depuis l'API CVE CIRCL et les convertit en RDF/TTL.
Usage: python load_cve_feed.py > cve_data.ttl
"""
import requests
from datetime import datetime, timedelta

# API CVE CIRCL (gratuit, pas besoin de clé)
CVE_API_URL = "https://cve.circl.lu/api/last"

def fetch_recent_cves(days=7):
    """Récupère les CVE des derniers `days` jours."""
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    url = f"{CVE_API_URL}/{start_date}/{end_date}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def cve_to_ttl(cve):
    """Convertit une CVE en format TTL."""
    cve_id = cve["id"]
    cvss = cve.get("cvss", 0)
    description = cve.get("summary", "").replace('"', '\\"').replace("\n", " ")
    return f"""
@prefix cve: <https://cve.mitre.org/> .
@prefix : <http://example.org/cyber-ontology#> .

cve:{cve_id} a :Vulnerability ;
    foaf:name "{cve_id}" ;
    :cvssScore {cvss} ;
    :description "{description}" .
"""

def main():
    cves = fetch_recent_cves(days=30)  # Dernières CVE des 30 jours
    print("@prefix : <http://example.org/cyber-ontology#> .")
    print("@prefix cve: <https://cve.mitre.org/> .")
    print("@prefix foaf: <http://xmlns.com/foaf/0.1/> .")
    print("\n# Généré le " + datetime.now().isoformat() + "\n")
    for cve in cves:
        print(cve_to_ttl(cve))

if __name__ == "__main__":
    main()
