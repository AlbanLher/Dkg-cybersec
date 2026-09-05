#!/usr/bin/env python3
"""
export_phase3_cti_md.py
Génération de la documentation Markdown synthétique de l'ABox CTI Externe (TLP:CLEAR).
Aligné avec le schéma TBox centralisé (tbox#), incluant la table d'acronymes et les diagrammes Mermaid.
"""

import sys
import shutil
from pathlib import Path
from rdflib import Graph

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from config import (
    ABOX_CTI_PATH,
    DIR_CTI_CLEAR,
    DOC_CTI_MD_PATH,
    DIR_SNAPSHOT_P3,
    DKG_TBOX,
    DKG_CTI
)

def generate_cti_markdown():
    g = Graph()
    g.parse(str(ABOX_CTI_PATH), format="turtle")

    md_filename = DOC_CTI_MD_PATH
    snapshot_md_path = DIR_SNAPSHOT_P3 / md_filename
    master_md_path = DIR_CTI_CLEAR / md_filename

    lines = [
        "# 📑 Livrable Phase 3 - ABox CTI Externe & Référentiels Menaces",
        "",
        "**Classification :** `TLP:CLEAR` (Public / Partageable)  ",
        f"**Source Turtle :** `{ABOX_CTI_PATH.name}`  ",
        f"**Nombre total de triples RDF :** {len(g)}  ",
        "",
        "---",
        "",
        "## 📖 Glossaire & Acronymes",
        "",
        "| Acronyme | Définition Complète | Contextualisation DKG |",
        "| :--- | :--- | :--- |",
        "| **APT** | Advanced Persistent Threat | Groupe d'attaquants hautement qualifiés menant des attaques ciblées et prolongées. |",
        "| **CTI** | Cyber Threat Intelligence | Renseignements structurés sur les menaces informatiques. |",
        "| **CVE** | Common Vulnerabilities and Exposures | Dictionnaire public des vulnérabilités de sécurité connues. |",
        "| **CWE** | Common Weakness Enumeration | Système de classification des faiblesses logicielles et matérielles. |",
        "| **CAPEC** | Common Attack Pattern Enumeration and Classification | Référentiel des schémas et patterns d'attaque. |",
        "| **CVSS** | Common Vulnerability Scoring System | Système standardisé d'évaluation de la sévérité des vulnérabilités. |",
        "| **TLP** | Traffic Light Protocol | Norme de classification du niveau de partage de l'information. |",
        "| **RDF** | Resource Description Framework | Modèle de données en graphe sous forme de triplets (Sujet-Prédicat-Objet). |",
        "",
        "---",
        "",
        "## 🔄 Flux d'Ingestion Structuré (Pipeline Phase 3)",
        "",
        "```mermaid",
        "flowchart LR",
        "    A[Sources CTI Structurées: NVD / MITRE] -->|Parsing JSON / XML| B(Extracteur Phase 3)",
        "    B -->|Mappage Ontologique| C[Génération Triplets RDF]",
        "    C -->|Validation SHACL| D{Conforme?}",
        "    D -->|Non| E[Rejet / Error Log]",
        "    D -->|Oui| F[Snapshot Phase 3]",
        "    F -->|Synchronisation| G[Master CTI TLP:CLEAR]",
        "```",
        "",
        "---",
        "",
        "## 📊 Synthèse des Entités CTI Ingestées",
        "",
        "| Classe Schéma (`dkg:`) | Nombre d'Instances |",
        "| :--- | :--- |"
    ]
    
    # Requête de comptage des entités CTI
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
        "## 🔗 Cartographie du Référentiel CTI Externe",
        "",
        "```mermaid",
        "graph TD",
        "    subgraph TLP:CLEAR [Chainage CTI Structuré]",
        "        CVE[dkg:Vulnerability / CVE] -->|dkg:cvssScore| SCORE[Score CVSS]",
        "        CVE -->|dkg:hasWeakness| CWE[dkg:Weakness / CWE]",
        "        CWE -->|dkg:hasThreatPattern| CAPEC[dkg:ThreatPattern / CAPEC]",
        "    end",
        "```",
        "",
        "---",
        "",
        "## 🔗 Détail des Dépendances Multi-Hop (CVE -> CWE -> CAPEC)",
        "",
        "| Vulnérabilité (CVE) | Score CVSS | Faiblesse (CWE) | Pattern d'Attaque (CAPEC) |",
        "| :--- | :--- | :--- | :--- |"
    ])
    
    # Requête de parcours CTI
    query_chain = """
    PREFIX dkg: <http://dkg.cybersec.org/tbox#>
    PREFIX cti: <http://dkg.cybersec.org/cti#>
    
    SELECT ?cve ?score ?cwe ?capec WHERE {
        ?cve a dkg:Vulnerability .
        OPTIONAL { ?cve dkg:cvssScore ?score . }
        OPTIONAL { ?cve dkg:hasWeakness ?cwe . }
        OPTIONAL { ?cwe dkg:hasThreatPattern ?capec . }
    }
    """
    
    for row in g.query(query_chain):
        cve = str(row.cve).split("#")[-1] if "#" in str(row.cve) else str(row.cve).split("/")[-1]
        score = str(row.score) if row.score else "N/A"
        cwe = str(row.cwe).split("#")[-1] if row.cwe and "#" in str(row.cwe) else (str(row.cwe).split("/")[-1] if row.cwe else "N/A")
        capec = str(row.capec).split("#")[-1] if row.capec and "#" in str(row.capec) else (str(row.capec).split("/")[-1] if row.capec else "N/A")
        lines.append(f"| `{cve}` | `{score}` | `{cwe}` | `{capec}` |")

    lines.extend(["", "---", "*Document généré automatiquement conformément aux exigences de livrables TLP:CLEAR.*"])

    # 1. Écriture Snapshot P3
    DIR_SNAPSHOT_P3.mkdir(parents=True, exist_ok=True)
    with open(snapshot_md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"📦 Documentation Snapshot générée : {snapshot_md_path}")

    # 2. Synchronisation Master TLP:CLEAR (sécurité anti-SameFileError)
    DIR_CTI_CLEAR.mkdir(parents=True, exist_ok=True)
    if snapshot_md_path.resolve() != master_md_path.resolve():
        shutil.copy(snapshot_md_path, master_md_path)
        print(f"✅ Documentation Master synchronisée : {master_md_path}")

if __name__ == "__main__":
    generate_cti_markdown()
