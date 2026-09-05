#!/usr/bin/env python3
"""
export_phase2_abox_md.py
Génération de la documentation Markdown synthétique de l'ABox Master (TLP:RED).
Aligné avec le schéma TBox centralisé (tbox#).
"""

import sys
import shutil
from pathlib import Path
from rdflib import Graph


# 1. Ancrage sys.path vers 03-Application/ pour importer config.py
APP_DIR = Path(__file__).resolve().parent.parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from rdflib import Graph, Literal, RDF, RDFS, OWL, XSD
from config import (
    DKG_TBOX,
    DKG_DATA,
    DIR_INPUT_P2,
    DIR_SNAPSHOT_P2,
    DIR_MASTER_ABOX,
    ABOX_MASTER_PATH,
)


def generate_abox_markdown():
    g = Graph()
    g.parse(str(ABOX_MASTER_PATH), format="turtle")
    
    # Chemins de destination pour la parité Master / Snapshot
    md_filename = "DOC_MASTER_ABOX.md"
    snapshot_md_path = DIR_SNAPSHOT_P2 / md_filename
    master_md_path = DIR_MASTER_ABOX / md_filename

    lines = [
        "# 📑 Livrable ABox Master - DKG CyberSec",
        "",
        "**Classification :** `TLP:RED` (Confidentiel)  ",
        f"**Source Turtle :** `{ABOX_MASTER_PATH.name}`  ",
        f"**Nombre total de triples RDF :** {len(g)}  ",
        "",
        "---",
        "",
        "## 📚 Glossaire des Acronymes",
        "",
        "| Acronyme | Définition Complète | Description / Rôle dans le DKG |",
        "| :--- | :--- | :--- |",
        "| **ABox** | Assertion Box | Composant du Knowledge Graph contenant les faits et instances d'objets. |",
        "| **TBox** | Terminology Box | Composant contenant les règles, ontologies, classes et propriétés du schéma. |",
        "| **CTI** | Cyber Threat Intelligence | Renseignement sur les menaces informatiques pour anticiper les attaques. |",
        "| **CVE** | Common Vulnerabilities and Exposures | Dictionnaire des failles de sécurité connues publiquement. |",
        "| **CWE** | Common Weakness Enumeration | Système de classification des faiblesses logicielles et matérielles. |",
        "| **CAPEC** | Common Attack Pattern Enumeration and Classification | Catalogue des schémas et tactiques d'attaque. |",
        "| **SHACL** | Shapes Constraint Language | Langage de validation des structures de graphes RDF sous CWA. |",
        "| **CWA** | Closed World Assumption | Hypothèse du monde clos. |",
        "",
        "---",
        "",
        "## 📊 Synthèse des Instances par Classe TBox",
        "",
        "| Classe Schéma (`dkg:`) | Nombre d'Instances |",
        "| :--- | :--- |"
    ]
    
    # Requête comptage alignée sur tbox#
    query_count = """
    PREFIX dkg: <http://dkg.cybersec.org/tbox#>
    SELECT ?type (COUNT(?s) AS ?count) WHERE {
        ?s a ?type .
        FILTER(STRSTARTS(STR(?type), "http://dkg.cybersec.org/tbox#"))
    }
    GROUP BY ?type
    ORDER BY DESC(?count)
    """
    for row in g.query(query_count):
        type_name = str(row[0]).split("#")[-1]
        lines.append(f"| `dkg:{type_name}` | **{row[1]}** |")
        
    lines.extend([
        "",
        "---",
        "",
        "## 🧬 Représentation Visuelle de la Chaîne CTI (Diagramme Mermaid)",
        "",
        "```mermaid",
        "graph TD",
        "    subgraph Infrastructure [Socle Système - TLP:RED]",
        "        Asset[dkg:Asset<br/><i>ex: Asset-Srv-Prod-01</i>] -->|hasInstalledComponent| Comp[dkg:SoftwareComponent<br/><i>ex: Comp-Apache-2-4-49</i>]",
        "    end",
        "    subgraph Threat_Chain [Chaîne de Menace CTI]",
        "        Comp -->|hasVulnerability| CVE[dkg:Vulnerability<br/><i>ex: CVE-2021-41773</i>]",
        "        CVE -->|hasWeakness| CWE[dkg:Weakness<br/><i>ex: CWE-22 Path Traversal</i>]",
        "        CWE -->|hasThreatPattern| CAPEC[dkg:ThreatPattern<br/><i>ex: CAPEC-126 Path Traversal</i>]",
        "    end",
        "    style Asset fill:#bbf,stroke:#333,stroke-width:2px",
        "    style Comp fill:#ddf,stroke:#333,stroke-width:1px",
        "    style CVE fill:#f9f,stroke:#333,stroke-width:2px",
        "    style CWE fill:#ffe,stroke:#333,stroke-width:1px",
        "    style CAPEC fill:#fbf,stroke:#333,stroke-width:2px",
        "```",
        "",
        "---",
        "",
        "## 🔗 Cartographie Détaillée de l'ABox Master",
        "",
        "| Asset | Composant | Vulnérabilité (CVE) | Faiblesse (CWE) | Threat Pattern (CAPEC) |",
        "| :--- | :--- | :--- | :--- | :--- |"
    ])
    
    # Requête cartographie alignée sur tbox# et hasWeakness
    query_chain = """
    PREFIX dkg: <http://dkg.cybersec.org/tbox#>
    SELECT ?asset ?comp ?cve ?cwe ?capec WHERE {
        ?asset a dkg:Asset ;
               dkg:hasInstalledComponent ?comp .
        ?comp dkg:hasVulnerability ?cve .
        OPTIONAL { ?cve dkg:hasWeakness ?cwe . }
        OPTIONAL { ?cwe dkg:hasThreatPattern ?capec . }
    }
    """
    
    for row in g.query(query_chain):
        asset = str(row.asset).split("#")[-1]
        comp = str(row.comp).split("#")[-1]
        cve = str(row.cve).split("#")[-1]
        cwe = str(row.cwe).split("#")[-1] if row.cwe else "N/A"
        capec = str(row.capec).split("#")[-1] if row.capec else "N/A"
        lines.append(f"| `{asset}` | `{comp}` | `{cve}` | `{cwe}` | `{capec}` |")

    lines.extend(["", "---", "*Document généré automatiquement conformément aux exigences de livrables TLP:RED.*"])

    # 1. Écriture prioritaire dans Snapshot
    DIR_SNAPSHOT_P2.mkdir(parents=True, exist_ok=True)
    with open(snapshot_md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"📦 Documentation Snapshot générée : {snapshot_md_path}")

    # 2. Copie vers Master (Garantie de parité)
    DIR_MASTER_ABOX.mkdir(parents=True, exist_ok=True)
    shutil.copy(snapshot_md_path, master_md_path)
    print(f"✅ Documentation Master synchronisée : {master_md_path}")

if __name__ == "__main__":
    generate_abox_markdown()
