#!/usr/bin/env python3
"""
generate_phase3_cti_abox.py
Ingestion des flux externes NVD/CAPEC (TLP:CLEAR).
Génère l'ABox CTI Externe en ECRITURE DIRECTE dans le Master Transversal
(GOU_2 v2.3 — plus de relais snapshot, figeage par tag git).
Rév. 2026-11-25 (étape 3, vague 3) : ancrage core.config (l ancien acces
top-level visait un module disparu lors du découpage v2) + suppression
du relais Snapshot P3 / copie miroir — écriture directe du TTL
Master, démarrage depuis n importe où.
"""

import json
import sys
from pathlib import Path

# Ancrage SSOT vers 03-Application/ pour importer core.config
APP_DIR = Path(__file__).resolve().parent.parent.parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from rdflib import Graph, Literal, RDF, RDFS, OWL, XSD
from core.config import (
    DKG_TBOX,
    DKG_CTI,
    DIR_ABOX_EXTERNE,
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
    g.bind("dkg-cti", DKG_CTI)
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
        
        if "description" in info:
            g.add((cve_uri, RDFS.comment, Literal(info["description"], lang="en")))
            
        if "cvss_score" in info:
            g.add((cve_uri, DKG_TBOX.cvssScore, Literal(float(info["cvss_score"]), datatype=XSD.float)))

        # Drapeau CISA KEV (xsd:boolean)
        is_kev = info.get("is_cisa_kev", info.get("isCisaKev", False))
        g.add((cve_uri, DKG_TBOX.isCisaKev, Literal(bool(is_kev), datatype=XSD.boolean)))

        # Liaison CWE via le prédicat de la zone CTI Externe (dkg:exploitsWeakness,
        # signature du CTI coché attendue par le greffon audit — pas de réconciliation
        # hasWeakness ici : celle-ci ne norme que l'ABox RED interne, TBox §25)
        if "cwe_id" in info and info["cwe_id"]:
            cwe_uri = DKG_CTI[info["cwe_id"]]
            g.add((cwe_uri, RDF.type, DKG_TBOX.Weakness))
            g.add((cve_uri, DKG_TBOX.exploitsWeakness, cwe_uri))

            # Liaison CAPEC
            if "capec_id" in info and info["capec_id"]:
                capec_uri = DKG_CTI[info["capec_id"]]
                g.add((capec_uri, RDF.type, DKG_TBOX.ThreatPattern))
                if "capec_title" in info:
                    g.add((capec_uri, RDFS.label, Literal(info["capec_title"], lang="en")))
                if "capec_description" in info:
                    g.add((capec_uri, RDFS.comment, Literal(info["capec_description"], lang="en")))
                g.add((cwe_uri, DKG_TBOX.hasThreatPattern, capec_uri))

    return g


def generate_phase3():
    print(f"Chargement des données CTI depuis : {INPUT_CTI_JSON_PATH}")
    cti_data = load_external_feed(INPUT_CTI_JSON_PATH)

    print("Génération du graphe RDF CTI Externe...")
    g = build_cti_graph(cti_data)

    # Écriture DIRECTE dans le Master Transversal TLP:CLEAR (GOU_2 v2.3)
    DIR_ABOX_EXTERNE.mkdir(parents=True, exist_ok=True)
    g.serialize(destination=str(ABOX_CTI_PATH), format="turtle")
    print(f"✅ ABox CTI Externe générée en direct (Master TLP:CLEAR) : {ABOX_CTI_PATH} ({len(g)} triplets)")


if __name__ == "__main__":
    generate_phase3()
