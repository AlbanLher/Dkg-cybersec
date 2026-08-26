#!/usr/bin/env python3
"""Script de génération multiformat (.json et .md) avec diagrammes visuels Mermaid.js et acronymes"""

import json
from pathlib import Path
from rdflib import RDF, RDFS, Graph, Namespace

BASE_DIR = Path(__file__).resolve().parent.parent
TBOX_DIR = BASE_DIR / "12-Donnees" / "TBox_init"

TTL_FILE = TBOX_DIR / "TBox_Cybersec.ttl"
JSON_FILE = TBOX_DIR / "TBox_Cybersec.json"
MD_FILE = TBOX_DIR / "TBox_Cybersec.md"


def export_tbox():
    if not TTL_FILE.exists():
        print(f"❌ Fichier introuvable : {TTL_FILE}")
        return

    g = Graph()
    g.parse(TTL_FILE, format="turtle")

    SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")

    classes = []
    properties = []

    for s, p, o in g.triples((None, RDF.type, None)):
        if "Class" in str(o):
            label = g.value(s, RDFS.label)
            comment = g.value(s, RDFS.comment)
            alt_labels = [str(al) for al in g.objects(s, SKOS.altLabel)]
            classes.append(
                {
                    "name": str(s).split("#")[-1],
                    "label": str(label) if label else "",
                    "synonyms": ", ".join(alt_labels) if alt_labels else "-",
                    "description": str(comment) if comment else "",
                }
            )

    for s, p, o in g.triples((None, RDF.type, None)):
        if "Property" in str(o):
            label = g.value(s, RDFS.label)
            domain = g.value(s, RDFS.domain)
            rng = g.value(s, RDFS.range)
            properties.append(
                {
                    "name": str(s).split("#")[-1],
                    "label": str(label) if label else "",
                    "domain": str(domain).split("#")[-1] if domain else "Any",
                    "range": str(rng).split("#")[-1] if rng else "Any",
                }
            )

    # Export Markdown Enrichi avec Graphiques Mermaid.js
    md_content = [
        "# Documentation et Modélisation Visuelle de la TBox\n",
        "## 1. Schéma Visuel Synthétique (Niveau Global)\n",
        "```mermaid",
        "classDiagram",
        "    class Asset {",
        "        +hostname : string",
        "        +ipAddress : string",
        "    }",
        "    class SoftwareComponent {",
        "        +cpeIdentifier : string",
        "    }",
        "    class Vulnerability {",
        "        +cvssScore : float",
        "    }",
        "    class Weakness",
        "    Asset \"1\" --> \"*\" SoftwareComponent : hasInstalledComponent",
        "    SoftwareComponent \"*\" --> \"*\" Vulnerability : hasVulnerability",
        "    Vulnerability \"*\" --> \"1\" Weakness : classifiedUnder",
        "```\n",
        "## 2. Zoom Métier : Domaine Système & Inventaire SI (Niveau 1)\n",
        "```mermaid",
        "graph LR",
        "    Asset[Actif Privé] -->|hasInstalledComponent| SoftwareComponent[Composant Logiciel]",
        "```\n",
        "## 3. Zoom Métier : Domaine Cyber & Threat Intelligence (Niveau 1)\n",
        "```mermaid",
        "graph LR",
        "    SoftwareComponent[Composant Logiciel] -->|hasVulnerability| Vulnerability[CVE Public]",
        "    Vulnerability -->|classifiedUnder| Weakness[CWE]",
        "```\n",
        "## 4. Dictionnaire des Classes & Synonymes Métier\n",
        "| Concept | Libellé | Synonymes / Acronymes | Description |",
        "|---|---|---|---|",
    ]

    for c in classes:
        md_content.append(
            f"| **{c['name']}** | {c['label']} | {c['synonyms']} | {c['description']} |"
        )

    md_content.extend(
        [
            "\n## 5. Relations et Attributs\n",
            "| Propriété | Origine | Cible | Libellé |",
            "|---|---|---|---|",
        ]
    )
    for p in properties:
        md_content.append(
            f"| `{p['name']}` | {p['domain']} | {p['range']} | {p['label']} |"
        )

    TBOX_DIR.mkdir(parents=True, exist_ok=True)
    with open(MD_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(md_content))
    print(f"✓ Markdown mis à jour avec vue visuelle : {MD_FILE}")


if __name__ == "__main__":
    export_tbox()
