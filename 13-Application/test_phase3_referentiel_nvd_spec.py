#!/usr/bin/env python3
"""
Test de Conformité Phase 3 : Alignement Référentiel NVD & Pre-flight Checks
Contrôle les exigences EXG-REF-01 à EXG-REF-03 et EXG-GOV-04.
"""

import sys
from pathlib import Path
from rdflib import Graph

BASE_DIR = Path(__file__).resolve().parent.parent
ABOX_TTL = BASE_DIR / "12-Donnees" / "TLP-RED_ABox_Cybersec" / "ABox_Cybersec.ttl"
REFERENTIEL_NVD_TTL = BASE_DIR / "12-Donnees" / "TLP-CLEAR_RBox_NVD-CWE" / "RBox_Cybersec.ttl"


def test_referentiel_nvd_alignment():
    print("==================================================")
    print("🔍 [PHASE 3] Vérification Alignement Référentiel NVD/CWE")
    print("==================================================")

    assert ABOX_TTL.exists(), f"❌ Fichier ABox introuvable : {ABOX_TTL}"
    assert REFERENTIEL_NVD_TTL.exists(), f"❌ [EXG-REF-01] Fichier Référentiel NVD introuvable : {REFERENTIEL_NVD_TTL}"

    # Chargement Unifié des Graphes (ABox Infrastructure + Referentiel NVD)
    g = Graph()
    g.parse(ABOX_TTL, format="turtle")
    g.parse(REFERENTIEL_NVD_TTL, format="turtle")
    print(f"ℹ️  Nombre total de triplets dans le graphe unifié : {len(g)}")

    # EXG-REF-01 : Validation de la Match Key d'Alignement CVE
    query_cve_match = """
    PREFIX dkg: <http://dkg.cybersec.org/tbox#>
    PREFIX rbox: <http://dkg.cybersec.org/rbox#>

    ASK {
        ?comp dkg:hasVulnerability ?cve .
        FILTER(STRSTARTS(STR(?cve), "http://dkg.cybersec.org/rbox#CVE-"))
    }
    """
    assert bool(g.query(query_cve_match)), "❌ [EXG-REF-01] Les URIs de vulnérabilités dans l'ABox ne correspondent pas au format rbox#CVE-..."
    print("✅ [EXG-REF-01] Format des Match Keys CVE validé.")

    # EXG-REF-02 & 03 : Résilience SPARQL et Enrichissement CVSS
    query_optional_enrichment = """
    PREFIX dkg: <http://dkg.cybersec.org/tbox#>

    ASK {
        ?cve a dkg:Vulnerability .
        OPTIONAL { ?cve dkg:cvssScore ?score . }
    }
    """
    assert bool(g.query(query_optional_enrichment)), "❌ [EXG-REF-03] Structure d'enrichissement NVD non reconnue."
    print("✅ [EXG-REF-02/03] Enrichissement NVD/CVSS opérationnel avec requêtage résilient.")

    # EXG-GOV-04 : Pre-flight Check Global (Chaîne Complète)
    preflight_check = """
    PREFIX dkg: <http://dkg.cybersec.org/tbox#>

    ASK {
        ?asset dkg:hasInstalledComponent ?comp .
        ?comp dkg:hasVulnerability ?cve .
        ?cve dkg:cvssScore ?score .
    }
    """
    assert bool(g.query(preflight_check)), "❌ [EXG-GOV-04] PRE-FLIGHT CHECK ÉCHOUÉ : Impossible de joindre Asset -> Composant -> CVE -> CVSS."
    print("✅ [EXG-GOV-04] Pre-flight Check réussi : La chaîne d'information transversale est complète.")

    print("\n🎉 PHASE 3 VALIDE : L'alignement avec le dictionnaire NVD/CWE est opérationnel.\n")


if __name__ == "__main__":
    try:
        test_referentiel_nvd_alignment()
    except AssertionError as e:
        print(e)
        sys.exit(1)
