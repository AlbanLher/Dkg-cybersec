#!/usr/bin/env python3
"""
export_phase4_ner_md.py
Génération de la documentation Markdown synthétique miroir (TLP:CLEAR)
pour l'ABox CTI Unstructured post-extraction.
"""

import sys
import shutil
from pathlib import Path
from rdflib import Graph

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from config import (
    ABOX_CTI_U_PATH,
    ABOX_CTI_U_MD_PATH,
    DIR_CTI_CLEAR,
    DIR_SNAPSHOT_P4
)


def generate_ner_markdown() -> None:
    g = Graph()
    if ABOX_CTI_U_PATH.exists():
        g.parse(str(ABOX_CTI_U_PATH), format="turtle")

    snapshot_md_path = DIR_SNAPSHOT_P4 / ABOX_CTI_U_MD_PATH.name
    master_md_path = ABOX_CTI_U_MD_PATH

    lines = [
        "# 📑 Livrable Phase 4 - Ingestion CTI Non Structurée (ABox-U)",
        "",
        "**Classification :** `TLP:CLEAR` (Public / Partageable)  ",
        f"**Source Turtle :** `{ABOX_CTI_U_PATH.name}`  ",
        f"**Nombre total de triples RDF :** {len(g)}  ",
        "",
        "---",
        "",
        "## 📖 Glossaire & Acronymes",
        "",
        "| Acronyme | Définition Complète | Contextualisation DKG |",
        "| :--- | :--- | :--- |",
        "| **APT** | Advanced Persistent Threat | Groupe d'attaquants qualifiés menant des opérations ciblées. |",
        "| **CTI** | Cyber Threat Intelligence | Renseignements structurés sur les menaces informatiques. |",
        "| **CVE** | Common Vulnerabilities and Exposures | Référentiel des vulnérabilités publiques connues. |",
        "| **TLP** | Traffic Light Protocol | Norme de restriction du partage de l'information. |",
        "| **RDF** | Resource Description Framework | Modèle de représentation sous forme de graphes de triplets. |",
        "",
        "---",
        "",
        "## 🔄 Flux d'Ingestion & Validation Qualité",
        "",
        "```mermaid",
        "flowchart LR",
        "    A[Avis Textuel Brut] -->|Parsing / Regex| B(Extractor CTI)",
        "    B -->|Calcul Score| C{Confidence >= 0.85?}",
        "    C -->|Non| D[Rejet / Journal d'Audit]",
        "    C -->|Oui| E[Instanciation Triplets RDF]",
        "    E --> F[Snapshot Phase 4]",
        "    F -->|Synchro SSOT| G[Master CTI TLP:CLEAR]",
        "```",
        "",
        "---",
        "",
        "## 📊 Entités Extraites & Niveaux de Confiance",
        "",
        "| URI Entité (`cti:`) | Classe (`dkg:`) | Libellé / Concept | Score Confiance |",
        "| :--- | :--- | :--- | :--- |"
    ]

    query_ner = """
    PREFIX dkg:  <http://dkg.cybersec.org/tbox#>
    PREFIX cti:  <http://dkg.cybersec.org/cti#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

    SELECT ?s ?type ?label ?acronym ?score WHERE {
        ?s a ?type .
        OPTIONAL { ?s rdfs:label ?label . }
        OPTIONAL { ?s skos:altLabel ?acronym . }
        OPTIONAL { ?s dkg:nerConfidenceScore ?score . }
        FILTER(STRSTARTS(STR(?type), "http://dkg.cybersec.org/tbox#"))
    }
    ORDER BY DESC(?score)
    """

    for row in g.query(query_ner):
        uri_name = str(row.s).split("#")[-1] if "#" in str(row.s) else str(row.s).split("/")[-1]
        type_name = str(row.type).split("#")[-1]
        label = str(row.label) if row.label else "N/A"
        acronym_str = f" (`{row.acronym}`)" if row.acronym else ""
        score = f"**{float(row.score):.2f}**" if row.score else "N/A"
        lines.append(f"| `{uri_name}` | `dkg:{type_name}` | {label}{acronym_str} | {score} |")

    lines.extend([
        "",
        "---",
        "",
        "## 🔗 Topology Network Graph (Extraite)",
        "",
        "```mermaid",
        "graph TD",
        "    subgraph TLP:CLEAR [Périmètre CTI External Unstructured]",
        "        TA[cti:ThreatActor-APT29] -->|dkg:exploitsVulnerability| VULN[cti:CVE-2024-21887]",
        "        TA -->|dkg:hasThreatPattern| PAT[cti:Pattern-SpearphishingLink-T1566_002]",
        "    end",
        "```",
        "",
        "---",
        "",
        "## 🔗 Détail des Relations Extraites",
        "",
        "| Menace (Threat Actor) | Vulnérabilité (CVE) | Pattern (ATT&CK) |",
        "| :--- | :--- | :--- |"
    ])

    query_relations = """
    PREFIX dkg: <http://dkg.cybersec.org/tbox#>

    SELECT ?actor ?cve ?pattern WHERE {
        ?actor a dkg:ThreatActor .
        OPTIONAL { ?actor dkg:exploitsVulnerability ?cve . }
        OPTIONAL { ?actor dkg:hasThreatPattern ?pattern . }
    }
    """

    for row in g.query(query_relations):
        actor = str(row.actor).split("#")[-1] if "#" in str(row.actor) else str(row.actor).split("/")[-1]
        cve = str(row.cve).split("#")[-1] if row.cve and "#" in str(row.cve) else "N/A"
        pattern = str(row.pattern).split("#")[-1] if row.pattern and "#" in str(row.pattern) else "N/A"
        lines.append(f"| `{actor}` | `{cve}` | `{pattern}` |")

    lines.extend(["", "---", "*Document miroir généré automatiquement.*"])

    # 1. Écriture Snapshot
    DIR_SNAPSHOT_P4.mkdir(parents=True, exist_ok=True)
    with open(snapshot_md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"📦 Documentation Snapshot créée : {snapshot_md_path}")

    # 2. Copie Master
    DIR_CTI_CLEAR.mkdir(parents=True, exist_ok=True)
    if snapshot_md_path.resolve() != master_md_path.resolve():
        shutil.copy(snapshot_md_path, master_md_path)
        print(f"✅ Documentation Master synchronisée : {master_md_path}")


if __name__ == "__main__":
    generate_ner_markdown()
