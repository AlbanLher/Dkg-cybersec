#!/usr/bin/env python3
"""
Script de Diagnostic & Génération SPARQL Automatique.
Inspecte les 56 triplets en mémoire et reconstruit la requête exacte.
"""

from pathlib import Path
from rdflib import Graph

BASE_DIR = Path(__file__).resolve().parent.parent
TBOX_TTL = BASE_DIR / "12-Donnees" / "TLP-AMBER_TBox_Cybersec" / "TBox_Cybersec.ttl"
ABOX_TTL = BASE_DIR / "12-Donnees" / "TLP-RED_ABox_Cybersec" / "ABox_Cybersec.ttl"
RBOX_TTL = BASE_DIR / "12-Donnees" / "TLP-CLEAR_RBox_NVD-CWE" / "RBox_Cybersec.ttl"


def debug_and_query():
    kg = Graph()
    for file_path in [TBOX_TTL, ABOX_TTL, RBOX_TTL]:
        if file_path.exists():
            kg.parse(file_path, format="turtle")

    print(f"📊 Nombre total de triplets : {len(kg)}\n")
    print("🔍 INSPECTION DE LA STRUCTURE DU GRAPHE :")
    print("=" * 80)

    # 1. Lister tous les Predicates (Propriétés) utilisés
    predicates = set(kg.predicates())
    print("\n[1] Prédicats / Propriétés détectés dans le graphe :")
    for p in sorted(predicates):
        print(f"  • {p}")

    # 2. Lister les types de sujets
    print("\n[2] Échantillon de triplets de l'ABox & RBox :")
    for s, p, o in list(kg)[:15]:
        print(f"  S: {s}\n  P: {p}\n  O: {o}\n  " + "-" * 40)

    # 3. Requête SPARQL ultra-agnostique (découverte automatique des chemins)
    discovery_query = """
    SELECT DISTINCT ?asset ?p1 ?component ?p2 ?cve WHERE {
        ?asset ?p1 ?component .
        ?component ?p2 ?cve .
        FILTER(CONTAINS(STR(?cve), "CVE") || CONTAINS(STR(?component), "sw-") || CONTAINS(STR(?component), "nginx"))
    }
    """
    
    results = kg.query(discovery_query)
    print("\n[3] Découverte automatique des relations Asset -> Component -> CVE :")
    found = False
    for row in results:
        found = True
        print(f"  Asset : {row.asset}")
        print(f"   ├─ P1 (Asset -> Comp) : {row.p1}")
        print(f"   ├─ Component          : {row.component}")
        print(f"   ├─ P2 (Comp -> CVE)   : {row.p2}")
        print(f"   └─ CVE                : {row.cve}")
        print("  " + "=" * 60)

    if not found:
        print("  ⚠️ Aucune chaîne à 2 sauts (Asset -> Comp -> CVE) trouvée.")
        print("  Analyse des liens directs depuis l'Asset :")
        for s, p, o in kg.triples((None, None, None)):
            if "srv-" in str(s) or "Asset" in str(o):
                print(f"    {s}  ==[{p}]==>  {o}")


if __name__ == "__main__":
    debug_and_query()
