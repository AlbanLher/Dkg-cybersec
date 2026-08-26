#!/usr/bin/env python3
"""Script de génération multiformat (.json et .md) à partir de la TBox maître (.ttl)"""

import json
from pathlib import Path
from rdflib import RDF, RDFS, Graph, Namespace

# Définition des chemins
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "12-Données/TBox_init"

TTL_FILE = DATA_DIR / "TBox_Cybersec.ttl"
JSON_FILE = DATA_DIR / "TBox_Cybersec.json"
MD_FILE = DATA_DIR / "TBox_Cybersec.md"


def export_tbox():
    g = Graph()
    g.parse(TTL_FILE, format="turtle")

    DKG = Namespace("http://dkg.cybersec.org/tbox#")

    classes = []
    properties = []

    # Extraction des classes
    for s, p, o in g.triples((None, RDF.type, None)):
        if "Class" in str(o):
            label = g.value(s, RDFS.label)
            comment = g.value(s, RDFS.comment)
            classes.append(
                {
                    "uri": str(s),
                    "name": str(s).split("#")[-1],
                    "label": str(label) if label else "",
                    "description": str(comment) if comment else "",
                }
            )

    # Extraction des propriétés
    for s, p, o in g.triples((None, RDF.type, None)):
        if "Property" in str(o):
            label = g.value(s, RDFS.label)
            domain = g.value(s, RDFS.domain)
            rng = g.value(s, RDFS.range)
            properties.append(
                {
                    "uri": str(s),
                    "name": str(s).split("#")[-1],
                    "label": str(label) if label else "",
                    "domain": str(domain).split("#")[-1] if domain else "Any",
                    "range": str(rng).split("#")[-1] if rng else "Any",
                }
            )

    # 1. Export JSON
    tbox_json = {
        "ontology": "DKG Cybersec TBox",
        "classes": classes,
        "properties": properties,
    }
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(tbox_json, f, indent=2, ensure_ascii=False)
    print(f"✓ JSON généré : {JSON_FILE}")

    # 2. Export Markdown Métier (LIV-04)
    md_content = [
        "# Documentation Métier de la TBox Cybersec\n",
        "Ce document est généré automatiquement. Il présente les concepts métier du modèle de données.\n",
        "## 1. Entities / Classes Métier\n",
        "| Concept | Nom FR | Description |",
        "|---|---|---|",
    ]
    for c in classes:
        md_content.append(
            f"| **{c['name']}** | {c['label']} | {c['description']} |"
        )

    md_content.extend(
        [
            "\n## 2. Relations et Attributs\n",
            "| Propriété | Origine (Domaine) | Cible (Range) | Libellé |",
            "|---|---|---|---|",
        ]
    )
    for p in properties:
        md_content.append(
            f"| `{p['name']}` | {p['domain']} | {p['range']} | {p['label']} |"
        )

    with open(MD_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(md_content))
    print(f"✓ Documentation Markdown générée : {MD_FILE}")


if __name__ == "__main__":
    export_tbox()
