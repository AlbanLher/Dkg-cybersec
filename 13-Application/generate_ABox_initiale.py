#!/usr/bin/env python3
"""
Générateur de Vue Humaine ABox (Markdown + Diagramme Mermaid.js).
Lit : 12-Donnees/ABox_init/ABox_Cybersec.ttl
Génère : 12-Donnees/ABox_init/ABox_Cybersec.md
Conforme à : EXG-ABOX-VIS-01
"""

from pathlib import Path
from rdflib import RDF, RDFS, Graph, Namespace

BASE_DIR = Path(__file__).resolve().parent.parent
ABOX_TTL = BASE_DIR / "12-Donnees" / "ABox_init" / "ABox_Cybersec.ttl"
ABOX_MD = BASE_DIR / "12-Donnees" / "ABox_init" / "ABox_Cybersec.md"


def generate_abox_markdown():
    g = Graph()
    g.parse(ABOX_TTL, format="turtle")

    DKG = Namespace("http://dkg.cybersec.org/tbox#")

    # Extraction des nœuds et relations pour Mermaid
    mermaid_lines = ["```mermaid", "graph TD"]

    # Style Mermaid pour différencier les types d'instances
    mermaid_lines.append("    classDef assetStyle fill:#1f77b4,color:#fff,stroke:#333,stroke-width:2px;")
    mermaid_lines.append("    classDef softStyle fill:#2ca02c,color:#fff,stroke:#333,stroke-width:1px;")
    mermaid_lines.append("    classDef vulnStyle fill:#d62728,color:#fff,stroke:#333,stroke-width:2px;")

    # Process Assets
    assets = list(g.subjects(RDF.type, DKG.Asset))
    for asset in assets:
        asset_id = str(asset).split("#")[-1]
        label = g.value(asset, RDFS.label) or asset_id
        mermaid_lines.append(f'    {asset_id}["🖥️ {label}"]:::assetStyle')

        # Software Components rattachés
        for sw in g.objects(asset, DKG.hasInstalledComponent):
            sw_id = str(sw).split("#")[-1]
            sw_label = g.value(sw, RDFS.label) or sw_id
            mermaid_lines.append(f'    {sw_id}["📦 {sw_label}"]:::softStyle')
            mermaid_lines.append(f"    {asset_id} -->|hasInstalledComponent| {sw_id}")

            # Vulnerabilities rattachées
            for vuln in g.objects(sw, DKG.hasVulnerability):
                vuln_id = str(vuln).split("#")[-1]
                mermaid_lines.append(f'    {vuln_id}["⚠️ {vuln_id}"]:::vulnStyle')
                mermaid_lines.append(f"    {sw_id} -->|hasVulnerability| {vuln_id}")

    mermaid_lines.append("```")

    # Rédaction du Markdown
    md_content = f"""# Restitution Visuelle ABox - Cartographie des Instances SI

**Source :** `12-Donnees/ABox_init/ABox_Cybersec.ttl`  
**Nombre de Triplets RDF :** {len(g)}

---

## 1. Topologie du SI Privé (Diagramme Mermaid.js)

{chr(10).join(mermaid_lines)}

---

## 2. Inventaire Synthétique des Instances

| Type DKG | Identifiant Instance (URI) | Libellé / Label |
|---|---|---|
"""
    for s, p, o in g.triples((None, RDF.type, None)):
        if "abox#" in str(s):
            inst_id = str(s).split("#")[-1]
            type_id = str(o).split("#")[-1]
            lbl = g.value(s, RDFS.label) or "-"
            md_content += f"| `{type_id}` | `abox:{inst_id}` | {lbl} |\n"

    # Écriture du fichier Markdown
    if ABOX_MD.exists():
        ABOX_MD.unlink()
    ABOX_MD.write_text(md_content, encoding="utf-8")
    print(f"✓ Documentation visuelle ABox générée : {ABOX_MD}")


if __name__ == "__main__":
    generate_abox_markdown()
