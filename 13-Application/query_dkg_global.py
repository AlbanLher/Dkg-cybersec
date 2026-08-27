#!/usr/bin/env python3
"""
Moteur de Requête Global SPARQL Transverse DKG (Phase 3).
Charge en mémoire :
  - TBox (12-Donnees/TLP-AMBER_TBox_Cybersec/TBox_Cybersec.ttl)
  - ABox (12-Donnees/TLP-RED_ABox_Cybersec/ABox_Cybersec.ttl)
  - RBox (12-Donnees/TLP-CLEAR_RBox_NVD-CWE/RBox_Cybersec.ttl)
Exécute une requête croisée unifiant les 3 piliers.
"""

from pathlib import Path
from rdflib import Graph

BASE_DIR = Path(__file__).resolve().parent.parent
TBOX_TTL = BASE_DIR / "12-Donnees" / "TLP-AMBER_TBox_Cybersec" / "TBox_Cybersec.ttl"
ABOX_TTL = BASE_DIR / "12-Donnees" / "TLP-RED_ABox_Cybersec" / "ABox_Cybersec.ttl"
RBOX_TTL = BASE_DIR / "12-Donnees" / "TLP-CLEAR_RBox_NVD-CWE" / "RBox_Cybersec.ttl"


def execute_global_query():
    kg = Graph()

    print("🔍 Chargement des graphes DKG...")
    if TBOX_TTL.exists():
        kg.parse(TBOX_TTL, format="turtle")
        print("  ├─ TBox TLP:AMBER chargée.")
    if ABOX_TTL.exists():
        kg.parse(ABOX_TTL, format="turtle")
        print("  ├─ ABox TLP:RED chargée.")
    if RBOX_TTL.exists():
        kg.parse(RBOX_TTL, format="turtle")
        print("  └─ RBox TLP:CLEAR chargée.")

    print(f"\n📊 Total des triplets unifiés en mémoire : {len(kg)}")

    # Requête SPARQL Traversant ABox -> RBox -> TBox
    sparql_query = """
    PREFIX dkg: <http://dkg.cybersec.org/tbox#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?assetName ?ip ?swName ?cveId ?cvss ?cweLabel WHERE {
        # 1. Requête dans l'ABox Privée (TLP:RED)
        ?asset a dkg:Asset ;
               rdfs:label ?assetName ;
               dkg:ipAddress ?ip ;
               dkg:hasInstalledComponent ?sw .
        
        ?sw rdfs:label ?swName ;
            dkg:hasVulnerability ?cve .

        # 2. Rejointoiement dans la RBox Publique (TLP:CLEAR) via l'URI de la CVE
        ?cve dkg:cvssScore ?cvss ;
             dkg:classifiedUnder ?cwe .
        
        ?cwe rdfs:label ?cweLabel .
    }
    """

    results = kg.query(sparql_query)

    print("\n🚨 [RAPPORT DE SÉCURITÉ UNIFIÉ DKG] 🚨")
    print("=" * 80)
    for row in results:
        cve_name = str(row.cveId).split("#")[-1] if row.cveId else "Inconnue"
        print(f"• ÉQUIPEMENT : {row.assetName} (IP: {row.ip})")
        print(f"  └─ Composant  : {row.swName}")
        print(f"  └─ Faille CVE : {cve_name} (Score CVSS: {row.cvss})")
        print(f"  └─ Faiblesse  : {row.cweLabel}")
        print("-" * 80)


if __name__ == "__main__":
    execute_global_query()
