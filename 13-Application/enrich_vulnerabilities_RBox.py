#!/usr/bin/env python3
"""
Script d'Enrichissement RBox Externe (DKG Cybersec - Phase 3).
Lit : 12-Donnees/TLP-CLEAR_RBox_NVD-CWE/nvd_cwe_mock.json
Génère : 12-Donnees/TLP-CLEAR_RBox_NVD-CWE/RBox_Cybersec.ttl
Conforme à : 11-Principes_Architecture/Specifications/SpecificationNormativeEnrichissementRBox.md
Classification : TLP:CLEAR (Open Data Public)
"""

import json
import time
from pathlib import Path
from rdflib import RDF, RDFS, OWL, XSD, Graph, Literal, Namespace

# Dynamic base path resolution
BASE_DIR = Path(__file__).resolve().parent.parent
RBOX_DIR = BASE_DIR / "12-Donnees" / "TLP-CLEAR_RBox_NVD-CWE"
MOCK_JSON = RBOX_DIR / "nvd_cwe_mock.json"
RBOX_TTL = RBOX_DIR / "RBox_Cybersec.ttl"


def enrich_rbox():
    if not MOCK_JSON.exists():
        raise FileNotFoundError(f"Fichier de feed mock introuvable : {MOCK_JSON}")

    with open(MOCK_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    g = Graph()

    # Namespaces
    DKG = Namespace("http://dkg.cybersec.org/tbox#")
    RBOX = Namespace("http://dkg.cybersec.org/rbox#")

    g.bind("dkg", DKG)
    g.bind("rbox", RBOX)
    g.bind("owl", OWL)
    g.bind("rdfs", RDFS)
    g.bind("xsd", XSD)

    # Entête Ontologie RBox
    rbox_ont = RBOX[""]
    g.add((rbox_ont, RDF.type, OWL.Ontology))
    g.add((rbox_ont, OWL.imports, DKG[""]))
    g.add(
        (
            rbox_ont,
            RDFS.label,
            Literal("RBox Public Reference Graph - DKG Cybersec", lang="en"),
        )
    )
    g.add(
        (
            rbox_ont,
            RDFS.comment,
            Literal(
                f"Généré automatiquement le {time.ctime()} à partir du feed {data.get('metadata', {}).get('source', 'NVD/CWE')}",
                lang="fr",
            ),
        )
    )

    # 1. Ingestion des Weaknesses (MITRE CWE)
    for cwe in data.get("weaknesses", []):
        cwe_id = cwe["cwe_id"]
        cwe_uri = RBOX[cwe_id]

        g.add((cwe_uri, RDF.type, DKG.Weakness))
        if "label" in cwe:
            g.add((cwe_uri, RDFS.label, Literal(cwe["label"], lang="en")))
        if "description" in cwe:
            g.add((cwe_uri, RDFS.comment, Literal(cwe["description"], lang="fr")))

    # 2. Ingestion des Vulnerabilities (NVD CVE) & Liaisons vers CWE
    for cve in data.get("vulnerabilities", []):
        cve_id = cve["cve_id"]
        cve_uri = RBOX[cve_id]

        g.add((cve_uri, RDF.type, DKG.Vulnerability))
        if "label" in cve:
            g.add((cve_uri, RDFS.label, Literal(cve["label"], lang="en")))
        if "cvss_score" in cve:
            g.add(
                (
                    cve_uri,
                    DKG.cvssScore,
                    Literal(cve["cvss_score"], datatype=XSD.float),
                )
            )
        if "cvss_vector" in cve:
            g.add(
                (
                    cve_uri,
                    DKG.cvssVector,
                    Literal(cve["cvss_vector"], datatype=XSD.string),
                )
            )

        # Liaison avec la catégorie CWE (dkg:classifiedUnder)
        if "cwe_id" in cve:
            cwe_uri = RBOX[cve["cwe_id"]]
            g.add((cve_uri, DKG.classifiedUnder, cwe_uri))

    # Écriture forcée sur disque
    RBOX_DIR.mkdir(parents=True, exist_ok=True)
    if RBOX_TTL.exists():
        RBOX_TTL.unlink()

    g.serialize(destination=RBOX_TTL, format="turtle")

    mtime = time.ctime(RBOX_TTL.stat().st_mtime)
    print(f"✓ RBox maître générée avec succès : {RBOX_TTL}")
    print(f"  └─ Date de modification : {mtime}")
    print(f"  └─ Nombre total de triplets RDF : {len(g)}")


if __name__ == "__main__":
    enrich_rbox()
