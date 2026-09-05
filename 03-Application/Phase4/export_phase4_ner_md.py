#!/usr/bin/env python3
"""
export_phase4_ner_md.py
Génération de la documentation Markdown synthétique post-NER (TLP:CLEAR)
avec intégration de la table des acronymes et des diagrammes Mermaid.
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
    DIR_SNAPSHOT_P4,
    DKG_TBOX,
    DKG_CTI
)

def generate_ner_markdown():
    g = Graph()
    g.parse(str(ABOX_CTI_PATH), format="turtle")
    
    md_filename = "DOC_CTI-U_ABOX.md"
    snapshot_md_path = DIR_SNAPSHOT_P4 / md_filename
    master_md_path = DIR_CTI_CLEAR / md_filename

    lines = [
        "# 📑 Livrable Phase 4 - Extraction NER & CTI Non Structurée",
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
        "| **NER** | Named Entity Recognition | Extraction automatique d'entités nommées depuis des bulletins CTI textuels. |",
        "| **CTI** | Cyber Threat Intelligence | Renseignements structurés sur les menaces informatiques. |",
        "| **CVE** | Common Vulnerabilities and Exposures | Dictionnaire public des vulnérabilités de sécurité connues. |",
        "| **CAPEC** | Common Attack Pattern Enumeration and Classification | Référentiel des schémas et patterns d'attaque. |",
        "| **TLP** | Traffic Light Protocol | Norme de classification du niveau de partage de l'information. |",
        "| **RDF** | Resource Description Framework | Modèle de données en graphe sous forme de triplets (Sujet-Prédicat-Objet). |",
        "",
        "---",
        "",
        "## 🔄 Flux d'Ingestion MLOps (Pipeline NER)",
        "",
        "```mermaid",
        "flowchart LR",
        "    A[Fichier Texte Brut] -->|Parsing NLP / Regex| B(Module NER)",
        "    B -->|Calcul de Score| C{Confidence Score >= 0.85?}",
        "    C -->|Non| D[Rejet / Dropped]",
        "    C -->|Oui| E[Génération Triplets RDF]",
        "    E --> F[Snapshot Phase 4]",
        "    F -->|Synchronisation| G[Master CTI TLP:CLEAR]",
        "```",
        "",
        "---",
        "",
        "## 📊 Entités Extraites par NER & Scores de Confiance",
        "",
        "| URI Entité (`cti:`) | Classe (`dkg:`) | Libellé / Acronyme | Score Confiance NER |",
        "| :--- | :--- | :--- | :--- |"
    ]
    
    # Requête SPARQL enrichie capturant l'acronyme SKOS (Socle) et le score NER (ABox)
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
        score = f"**{float(row.score):.2f}**" if row.score else "N/A (Socle)"
        lines.append(f"| `{uri_name}` | `dkg:{type_name}` | {label}{acronym_str} | {score} |")

    lines.extend([
        "",
        "---",
        "",
        "## 🔗 Network Graph Extraite du Texte",
        "",
        "```mermaid",
        "graph TD",
        "    subgraph TLP:CLEAR [Périmètre CTI Externe]",
        "        TA[cti:ThreatActor-APT29] -->|dkg:exploitsVulnerability| VULN[cti:CVE-2024-21887]",
        "        TA -->|dkg:hasThreatPattern| PAT[cti:Pattern-SpearphishingLink-T1566_002]",
        "    end",
        "```",
        "",
        "---",
        "",
        "## 🔗 Détail des Relations Multi-Hop",
        "",
        "| Attaquant (Threat Actor) | Vulnérabilité Exploitée (CVE) | Motif d'Attaque (CAPEC/ATT&CK) |",
        "| :--- | :--- | :--- |"
    ])

    # Requête pour relier ThreatActor -> CVE -> ThreatPattern
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
        cve = str(row.cve).split("#")[-1] if row.cve and "#" in str(row.cve) else (str(row.cve).split("/")[-1] if row.cve else "N/A")
        pattern = str(row.pattern).split("#")[-1] if row.pattern and "#" in str(row.pattern) else (str(row.pattern).split("/")[-1] if row.pattern else "N/A")
        lines.append(f"| `{actor}` | `{cve}` | `{pattern}` |")

    lines.extend(["", "---", "*Document généré automatiquement post-pipeline NER (Score Seuil >= 0.85).*"])

    # 1. Écriture Snapshot P4
    DIR_SNAPSHOT_P4.mkdir(parents=True, exist_ok=True)
    with open(snapshot_md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"📦 Documentation Snapshot générée : {snapshot_md_path}")

    # 2. Synchronisation Master TLP:CLEAR
    DIR_CTI_CLEAR.mkdir(parents=True, exist_ok=True)
    if snapshot_md_path.resolve() != master_md_path.resolve():
        shutil.copy(snapshot_md_path, master_md_path)
        print(f"✅ Documentation Master synchronisée : {master_md_path}")

if __name__ == "__main__":
    generate_ner_markdown()
