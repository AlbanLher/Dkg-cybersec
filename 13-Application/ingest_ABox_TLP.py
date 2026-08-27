#!/usr/bin/env python3
"""
Ingestion & Restitution de l'ABox Privée (Phase 3 - Governance TLP).
Lit : 12-Donnees/ABox_init/inventory.json (ou local)
Génère : 12-Donnees/TLP-RED_ABox_Cybersec/ABox_Cybersec.ttl & ABox_Cybersec.md
Classification : TLP:RED (Strictement Restreint)
"""

import json
from pathlib import Path
from rdflib import RDF, RDFS, OWL, XSD, Graph, Literal, Namespace

BASE_DIR = Path(__file__).resolve().parent.parent
ABOX_INIT_JSON = BASE_DIR / "12-Donnees" / "ABox_init" / "inventory.json"
ABOX_RED_DIR = BASE_DIR / "12-Donnees" / "TLP-RED_ABox_Cybersec"
ABOX_TTL = ABOX_RED_DIR / "ABox_Cybersec.ttl"
ABOX_MD = ABOX_RED_DIR / "ABox_Cybersec.md"


def ingest_abox_tlp():
    # Fallback si inventory.json n'existe pas dans ABox_init
    if ABOX_INIT_JSON.exists():
        with open(ABOX_INIT_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        # Mock d'inventaire par défaut
        data = {
            "assets": [
                {
                    "id": "srv-web-01",
                    "label": "Serveur Web Production",
                    "ip": "192.168.1.50",
                    "components": [
                        {
                            "id": "sw-nginx-1201",
                            "label": "NGINX Web Server v1.20.1",
                            "vulnerabilities": ["CVE-2021-23017"]
                        }
                    ]
                }
            ]
        }

    g = Graph()
    DKG = Namespace("http://dkg.cybersec.org/tbox#")
    ABOX = Namespace("http://dkg.cybersec.org/abox#")
    RBOX = Namespace("http://dkg.cybersec.org/rbox#")

    g.bind("dkg", DKG)
    g.bind("abox", ABOX)
    g.bind("rbox", RBOX)

    # Header Ontologie ABox
    abox_ont = ABOX[""]
    g.add((abox_ont, RDF.type, OWL.Ontology))
    g.add((abox_ont, OWL.imports, DKG[""]))

    mermaid_lines = ["```mermaid", "graph TD"]
    mermaid_lines.append("    classDef assetStyle fill:#1f77b4,color:#fff,stroke:#333,stroke-width:2px;")
    mermaid_lines.append("    classDef softStyle fill:#2ca02c,color:#fff,stroke:#333,stroke-width:1px;")
    mermaid_lines.append("    classDef vulnStyle fill:#d62728,color:#fff,stroke:#333,stroke-width:2px;")

    # Ingestion Assets
    for asset in data.get("assets", []):
        a_uri = ABOX[asset["id"]]
        g.add((a_uri, RDF.type, DKG.Asset))
        g.add((a_uri, RDFS.label, Literal(asset["label"], lang="fr")))
        if "ip" in asset:
            g.add((a_uri, DKG.ipAddress, Literal(asset["ip"], datatype=XSD.string)))

        mermaid_lines.append(f'    {asset["id"]}["🖥️ {asset["label"]}<br/>IP: {asset.get("ip","")}"]:::assetStyle')

        for sw in asset.get("components", []):
            sw_uri = ABOX[sw["id"]]
            g.add((sw_uri, RDF.type, DKG.SoftwareComponent))
            g.add((sw_uri, RDFS.label, Literal(sw["label"], lang="fr")))
            g.add((a_uri, DKG.hasInstalledComponent, sw_uri))

            mermaid_lines.append(f'    {sw["id"]}["📦 {sw["label"]}"]:::softStyle')
            mermaid_lines.append(f'    {asset["id"]} -->|hasInstalledComponent| {sw["id"]}')

            # Pointeur vers la RBox pour les CVE
            for cve_id in sw.get("vulnerabilities", []):
                cve_uri = RBOX[cve_id]
                g.add((sw_uri, DKG.hasVulnerability, cve_uri))
                mermaid_lines.append(f'    {cve_id}["⚠️ {cve_id}"]:::vulnStyle')
                mermaid_lines.append(f'    {sw["id"]} -->|hasVulnerability| {cve_id}')

    mermaid_lines.append("```")

    # Écriture TTL
    ABOX_RED_DIR.mkdir(parents=True, exist_ok=True)
    if ABOX_TTL.exists():
        ABOX_TTL.unlink()
    g.serialize(destination=ABOX_TTL, format="turtle")

    # Écriture MD
    md_content = f"""# Restitution Visuelle ABox Privée (TLP:RED)

**Classification :** `TLP:RED` (Strictement Restreint)  
**Source RDF :** `12-Donnees/TLP-RED_ABox_Cybersec/ABox_Cybersec.ttl`  

---

## 1. Topologie du SI Privé

{chr(10).join(mermaid_lines)}
"""
    ABOX_MD.write_text(md_content, encoding="utf-8")
    print(f"✓ ABox TLP:RED et doc visualisable générées dans : {ABOX_RED_DIR}")


if __name__ == "__main__":
    ingest_abox_tlp()
