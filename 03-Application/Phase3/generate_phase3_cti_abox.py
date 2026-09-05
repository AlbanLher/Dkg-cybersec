#!/usr/bin/env python3
"""
generate_phase3_cti.py
Ingestion des flux externes NVD/CAPEC (TLP:CLEAR).
Génère l'ABox CTI Externe et synchronise Snapshot Phase 3 / Master CTI.
"""

import json
import shutil
import sys
from pathlib import Path

# Ancrage SSOT
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from rdflib import Graph, Literal, RDF, RDFS, OWL, XSD
from config import (
    DKG_TBOX,
    DKG_CTI,
    DIR_SNAPSHOT_P3,
    DIR_CTI_CLEAR,
    ABOX_CTI_PATH,
    INPUT_CTI_JSON_PATH
)

def load_external_feed(feed_path: Path) -> dict:
    if not feed_path.exists():
        raise FileNotFoundError(f"Fichier d'entrée CTI introuvable : {feed_path}")
    with open(feed_path, "r", encoding="utf-8") as f:
        return json.load(f)

def build_cti_graph(cti_data: dict) -> Graph:
    g = Graph()
    g.bind("dkg", DKG_TBOX)
    g.bind("cti", DKG_CTI)
    g.bind("owl", OWL)
    g.bind("rdf", RDF)
    g.bind("rdfs", RDFS)
    g.bind("xsd", XSD)

    # En-tête Ontologie CTI
    cti_ont = DKG_CTI["ABox_CTI_External"]
    g.add((cti_ont, RDF.type, OWL.Ontology))
    g.add((cti_ont, RDFS.label, Literal("DKG External CTI Feed - TLP:CLEAR", lang="en")))

    for cve_id, info in cti_data.items():
        cve_uri = DKG_CTI[cve_id]
        g.add((cve_uri, RDF.type, DKG_TBOX.Vulnerability))
        g.add((cve_uri, RDFS.comment, Literal(info["description"], lang="en")))
        g.add((cve_uri, DKG_TBOX.cvssScore, Literal(float(info["cvss_score"]), datatype=XSD.float)))

        # Liaison CWE
        if "cwe_id" in info:
            cwe_uri = DKG_CTI[info["cwe_id"]]
            g.add((cwe_uri, RDF.type, DKG_TBOX.Weakness))
            g.add((cve_uri, DKG_TBOX.hasWeakness, cwe_uri))

            # Liaison CAPEC
            if "capec_id" in info:
                capec_uri = DKG_CTI[info["capec_id"]]
                g.add((capec_uri, RDF.type, DKG_TBOX.ThreatPattern))
                g.add((capec_uri, RDFS.label, Literal(info["capec_title"], lang="en")))
                g.add((capec_uri, RDFS.comment, Literal(info["capec_description"], lang="en")))
                g.add((cwe_uri, DKG_TBOX.hasThreatPattern, capec_uri))

    return g

def generate_phase3():
    print(f"Chargement des données CTI depuis : {INPUT_CTI_JSON_PATH}")
    cti_data = load_external_feed(INPUT_CTI_JSON_PATH)

    print("Génération du graphe RDF CTI Externe...")
    g = build_cti_graph(cti_data)

    # Création des répertoires
    DIR_SNAPSHOT_P3.mkdir(parents=True, exist_ok=True)
    DIR_CTI_CLEAR.mkdir(parents=True, exist_ok=True)

    # 1. Écriture dans Snapshot P3
    snapshot_ttl = DIR_SNAPSHOT_P3 / ABOX_CTI_PATH.name
    g.serialize(destination=str(snapshot_ttl), format="turtle")
    print(f"📦 Snapshot CTI généré : {snapshot_ttl} ({len(g)} triplets)")

    # 2. Copie miroir vers Master CTI (TLP:CLEAR)
    shutil.copy(snapshot_ttl, ABOX_CTI_PATH)
    print(f"✅ Master CTI synchronisé : {ABOX_CTI_PATH}")

if __name__ == "__main__":
    generate_phase3()
