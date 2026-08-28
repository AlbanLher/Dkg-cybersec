#!/usr/bin/env python3
"""
Moteur de Requête Global SPARQL Transverse DKG (Phase 3).
Unifie les graphes ABox, TBox et RBox en établissant le lien 
Asset -> Composant Logiciel -> Vulnérabilité (CVE) -> Faiblesse (CWE).
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
    for label, file_path in [("TBox TLP:AMBER", TBOX_TTL), ("ABox TLP:RED", ABOX_TTL), ("RBox TLP:CLEAR", RBOX_TTL)]:
        if file_path.exists():
            kg.parse(file_path, format="turtle")
            print(f"  ├─ {label} chargée.")
        else:
            print(f"  ⚠️  Fichier introuvable : {file_path}")

    print(f"\n📊 Total des triplets unifiés en mémoire : {len(kg)}")

    # Requête SPARQL explicite reliant la chaîne complète Asset -> SW -> CVE -> CWE
    sparql_query = """
    PREFIX dkg: <http://dkg.cybersec.org/tbox#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?assetName ?ip ?swName ?cveUri ?cvss ?cweLabel WHERE {
        # 1. Traversée stricte Asset -> Composant Logiciel dans l'ABox
        ?asset a dkg:Asset ;
               rdfs:label ?assetName ;
               ?pComp ?sw .
        FILTER(REGEX(STR(?pComp), "hasInstalledComponent|hasComponent|installed"))

        # 2. Informations du composant et lien vers la CVE
        ?sw rdfs:label ?swName ;
            ?pVuln ?cveUri .
        FILTER(REGEX(STR(?pVuln), "hasVulnerability|vulnerability"))

        # 3. Métadonnées optionnelles (IP, CVSS, CWE)
        OPTIONAL { 
            ?asset ?pIp ?ip . 
            FILTER(REGEX(STR(?pIp), "ipAddress|ip"))
        }
        OPTIONAL { 
            ?cveUri ?pCvss ?cvss . 
            FILTER(REGEX(STR(?pCvss), "cvssScore|score"))
        }
        OPTIONAL {
            ?cveUri ?pClass ?cwe .
            FILTER(REGEX(STR(?pClass), "classifiedUnder"))
            ?cwe rdfs:label ?cweLabel .
        }
    }
    """

    results = kg.query(sparql_query)

    print("\n🚨 [RAPPORT DE SÉCURITÉ UNIFIÉ DKG] 🚨")
    print("=" * 80)

    count = 0
    for row in results:
        count += 1
        cve_name = str(row.cveUri).split("#")[-1] if row.cveUri else "Aucune CVE"
        cvss = str(row.cvss) if row.cvss else "N/A"
        cwe = str(row.cweLabel) if row.cweLabel else "Non classifié"
        ip = str(row.ip) if row.ip else "N/A"
        sw = str(row.swName) if row.swName else "N/A"

        print(f"• ÉQUIPEMENT : {row.assetName} (IP: {ip})")
        print(f"  └─ Composant  : {sw}")
        print(f"  └─ Faille CVE : {cve_name} (Score CVSS: {cvss})")
        print(f"  └─ Faiblesse  : {cwe}")
        print("-" * 80)

    if count == 0:
        print("⚠️ Aucun lien complet (Asset -> Composant -> CVE) n'a été trouvé.")


if __name__ == "__main__":
    execute_global_query()
