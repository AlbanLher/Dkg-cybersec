#!/usr/bin/env python3
"""
Script de génération des sorties dérivées de la TBox (JSON et Markdown).
Conforme à la spécification : 11-Principes_Architecture/SpecificationNormativeSortiesFormatsTBox.md
"""

import json
from pathlib import Path
from rdflib import RDF, RDFS, Graph, Namespace

# Résolution dynamique du dossier racine
BASE_DIR = Path(__file__).resolve().parent.parent
TBOX_DIR = BASE_DIR / "12-Donnees" / "TBox_init"

TTL_FILE = TBOX_DIR / "TBox_Cybersec.ttl"
JSON_FILE = TBOX_DIR / "TBox_Cybersec.json"
MD_FILE = TBOX_DIR / "TBox_Cybersec.md"

SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")


def generate_outputs():
    if not TTL_FILE.exists():
        print(f"❌ Erreur : Fichier maître introuvable : {TTL_FILE}")
        return

    g = Graph()
    g.parse(TTL_FILE, format="turtle")

    classes = []
    properties = []

    # Extraction des classes et annotations SKOS
    for s, p, o in g.triples((None, RDF.type, None)):
        if "Class" in str(o):
            label = g.value(s, RDFS.label)
            comment = g.value(s, RDFS.comment)
            alt_labels = [str(al) for al in g.objects(s, SKOS.altLabel)]
            classes.append(
                {
                    "uri": str(s),
                    "name": str(s).split("#")[-1],
                    "label": str(label) if label else "",
                    "synonyms": alt_labels,
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

    # -------------------------------------------------------------------------
    # 1. Export JSON (EXG-JSON)
    # -------------------------------------------------------------------------
    tbox_json = {
        "ontology": "DKG Cybersec TBox",
        "version": "1.0",
        "classes": classes,
        "properties": properties,
    }

    TBOX_DIR.mkdir(parents=True, exist_ok=True)
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(tbox_json, f, indent=2, ensure_ascii=False)
    print(f"✓ Format Machine (JSON) généré : {JSON_FILE}")

    # -------------------------------------------------------------------------
    # 2. Export Markdown & Lexique (EXG-MD)
    # -------------------------------------------------------------------------
    md_content = [
        "# Documentation Normative et Lexique de la TBox Cyberdéfense\n",
        "Ce document est généré automatiquement depuis `TBox_Cybersec.ttl` conformément à la spécification `SpecificationNormativeSortiesFormatsTBox.md`.\n",
        "## 1. Référentiel des Acronymes et Standards W3C / Cyber\n",
        "| Acronyme | Nom Complet | Description / Rôle |",
        "|---|---|---|",
        "| **RDF** | Resource Description Framework | Modèle de données universel sous forme de triplets. |",
        "| **RDFS** | RDF Schema | Extension de vocabulaire pour structurer classes et propriétés. |",
        "| **OWL** | Web Ontology Language | Langage d'ontologie riche pour exprimer la sémantique. |",
        "| **SKOS** | Simple Knowledge Organization System | Vocabulaire W3C pour thésaurus et lexiques (`skos:altLabel`). |",
        "| **TTL** | Turtle | Formats de sérialisation texte lisible (Source de vérité). |",
        "| **SPARQL** | SPARQL Query Language | Langage de requête pour graphes de connaissances. |",
        "| **TBox** | Terminological Box | Schéma abstrait définissant concepts et relations. |",
        "| **ABox** | Assertional Box | Ensemble des données réelles instanciées dans le SI. |",
        "| **CPE** | Common Platform Enumeration | Dénomination unifiée des produits informatiques. |",
        "| **CVE** | Common Vulnerabilities and Exposures | Dictionnaire public des vulnérabilités de sécurité. |",
        "| **CWE** | Common Weakness Enumeration | Catégorisation des faiblesses d'architecture logicielle. |\n",
        "## 2. Vues Graphiques de l'Ontologie (Mermaid.js)\n",
        "### 2.1 Vue Synthétique Globale (Niveau 0)\n",
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
        "### 2.2 Zoom Métier : Inventaire SI & Actifs (Niveau 1)\n",
        "```mermaid",
        "graph LR",
        "    Asset[Actif Privé] -->|hasInstalledComponent| SoftwareComponent[Composant Logiciel]",
        "```\n",
        "### 2.3 Zoom Métier : Threat Intelligence & CVE (Niveau 1)\n",
        "```mermaid",
        "graph LR",
        "    SoftwareComponent[Composant Logiciel] -->|hasVulnerability| Vulnerability[CVE Public]",
        "    Vulnerability -->|classifiedUnder| Weakness[CWE]",
        "```\n",
        "## 3. Dictionnaire des Classes & Lexique Métier\n",
        "| Concept | Libellé FR | Synonymes / Acronymes (SKOS) | Description |",
        "|---|---|---|---|",
    ]

    for c in classes:
        synonyms_str = (
            ", ".join([f"`{s}`" for s in c["synonyms"]])
            if c["synonyms"]
            else "-"
        )
        md_content.append(
            f"| **{c['name']}** | {c['label']} | {synonyms_str} | {c['description']} |"
        )

    md_content.extend(
        [
            "\n## 4. Dictionnaire des Relations et Attributs\n",
            "| Propriété | Domaine (Origine) | Range (Cible) | Libellé FR |",
            "|---|---|---|---|",
        ]
    )
    for p in properties:
        md_content.append(
            f"| `{p['name']}` | {p['domain']} | {p['range']} | {p['label']} |"
        )

    with open(MD_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(md_content))
    print(f"✓ Format Humain & Lexique (Markdown) généré : {MD_FILE}")


if __name__ == "__main__":
    generate_outputs()
