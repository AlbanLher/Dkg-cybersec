#!/usr/bin/env python3
"""
Générateur de Vue Humaine RBox (Markdown + Diagramme Mermaid.js).
Lit : 12-Donnees/TLP-CLEAR_RBox_NVD-CWE/RBox_Cybersec.ttl
Génère : 12-Donnees/TLP-CLEAR_RBox_NVD-CWE/RBox_Cybersec.md
Conforme à : EXG-RBOX-03 (TLP:CLEAR)
"""

from pathlib import Path
from rdflib import RDF, RDFS, Graph, Namespace

BASE_DIR = Path(__file__).resolve().parent.parent
RBOX_DIR = BASE_DIR / "12-Donnees" / "TLP-CLEAR_RBox_NVD-CWE"
RBOX_TTL = RBOX_DIR / "RBox_Cybersec.ttl"
RBOX_MD = RBOX_DIR / "RBox_Cybersec.md"


def generate_rbox_markdown():
    g = Graph()
    g.parse(RBOX_TTL, format="turtle")

    DKG = Namespace("http://dkg.cybersec.org/tbox#")

    mermaid_lines = [
        "```mermaid",
        "graph TD",
        "    classDef cveStyle fill:#d62728,color:#fff,stroke:#333,stroke-width:2px;",
        "    classDef cweStyle fill:#ff7f0e,color:#fff,stroke:#333,stroke-width:2px;",
        '    subgraph Vulnerabilities ["Vulnerabilities - NVD (TLP:CLEAR)"]',
    ]

    # CVEs
    cves = list(g.subjects(RDF.type, DKG.Vulnerability))
    for cve in cves:
        cve_id = str(cve).split("#")[-1]
        score = g.value(cve, DKG.cvssScore) or "N/A"
        label = g.value(cve, RDFS.label) or cve_id
        mermaid_lines.append(
            f'        {cve_id}["⚠️ <b>{cve_id}</b><br/><i>{label}</i><br/>Score CVSS: {score}"]'
        )

    mermaid_lines.append("    end")
    mermaid_lines.append(
        '    subgraph Weaknesses ["Weaknesses - MITRE CWE (TLP:CLEAR)"]'
    )

    # CWEs
    cwes = list(g.subjects(RDF.type, DKG.Weakness))
    for cwe in cwes:
        cwe_id = str(cwe).split("#")[-1]
        label = g.value(cwe, RDFS.label) or cwe_id
        mermaid_lines.append(f'        {cwe_id}["🛡️ <b>{cwe_id}</b><br/><i>{label}</i>"]')

    mermaid_lines.append("    end")

    # Appliquer les styles via 'class' pour éviter les erreurs de syntaxe
    for cve in cves:
        cve_id = str(cve).split("#")[-1]
        mermaid_lines.append(f"    class {cve_id} cveStyle;")
    for cwe in cwes:
        cwe_id = str(cwe).split("#")[-1]
        mermaid_lines.append(f"    class {cwe_id} cweStyle;")

    # Liaisons (classifiedUnder)
    for cve in cves:
        cve_id = str(cve).split("#")[-1]
        for cwe in g.objects(cve, DKG.classifiedUnder):
            cwe_id = str(cwe).split("#")[-1]
            mermaid_lines.append(f"    {cve_id} -->|classifiedUnder| {cwe_id}")

    mermaid_lines.append("```")

    md_content = f"""# Restitution Visuelle RBox - Référentiel Externe (Open Data)

**Classification :** `TLP:CLEAR`  
**Source :** `12-Donnees/TLP-CLEAR_RBox_NVD-CWE/RBox_Cybersec.ttl`  
**Nombre de Triplets RDF :** {len(g)}

---

## 1. Graphe d'Enrichissement RBox (Mermaid.js)

{chr(10).join(mermaid_lines)}

---

## 2. Dictionnaire des Vulnérabilités & Faiblesses

| Type DKG | Identifiant | Libellé / Score |
|---|---|---|
"""
    for s, p, o in g.triples((None, RDF.type, None)):
        if "rbox#" in str(s):
            inst_id = str(s).split("#")[-1]
            type_id = str(o).split("#")[-1]
            lbl = g.value(s, RDFS.label) or "-"
            md_content += f"| `{type_id}` | `rbox:{inst_id}` | {lbl} |\n"

    if RBOX_MD.exists():
        RBOX_MD.unlink()
    RBOX_MD.write_text(md_content, encoding="utf-8")
    print(f"✓ Documentation visuelle RBox générée : {RBOX_MD}")


if __name__ == "__main__":
    generate_rbox_markdown()
