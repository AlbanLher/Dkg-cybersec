#!/usr/bin/env python3
"""
Générateur ABox Enrichie & Master Consolidé TLP:RED (Phase 3).
Alimente 12-Donnees/ABox_enriched/ et 12-Donnees/TLP_RED_Consolidation_ABox/.
"""

from pathlib import Path
from datetime import datetime, timezone
from rdflib import Graph, Literal, Namespace, RDF, RDFS, OWL, XSD

from ingest_external_nvd_capec import ingest_external_data, fetch_enrichment_data
from consolidate_master_TLP_AMBER_TBox  import main as consolidate_tbox_master

BASE_DIR = Path(__file__).resolve().parent.parent

ENRICHED_DIR = BASE_DIR / "12-Donnees" / "ABox_enriched"
CONSOLIDATION_ABOX_DIR = BASE_DIR / "12-Donnees" / "TLP_RED_Consolidation_ABox"

FILE_SNAPSHOT_TTL = ENRICHED_DIR / "ABox_Cybersec_enriched.ttl"
FILE_MASTER_TTL = CONSOLIDATION_ABOX_DIR / "DKG_ABox_Master.ttl"
FILE_MASTER_JSON = CONSOLIDATION_ABOX_DIR / "DKG_ABox_Master.json"
FILE_MASTER_MD = CONSOLIDATION_ABOX_DIR / "DKG_ABox_Master.md"

DKG = Namespace("http://dkg.cybersec.org/tbox#")
DKG_INST = Namespace("http://dkg.cybersec.org/abox#")


def build_enriched_abox_graph() -> Graph:
    g = ingest_external_data()
    external_data = fetch_enrichment_data()
    now_iso = datetime.now(timezone.utc).isoformat()

    tlp_clear = DKG_INST["TLP-CLEAR"]
    tlp_red = DKG_INST["TLP-RED"]

    g.add((tlp_clear, RDF.type, DKG["TLPMarking"]))
    g.add((tlp_clear, DKG["tlpColor"], Literal("CLEAR", datatype=XSD.string)))

    g.add((tlp_red, RDF.type, DKG["TLPMarking"]))
    g.add((tlp_red, DKG["tlpColor"], Literal("RED", datatype=XSD.string)))

    # Marquage TLP:RED sur entités du SI (Assets et Composants)
    for asset in g.subjects(RDF.type, DKG["Asset"]):
        g.add((asset, DKG["hasTLPMarking"], tlp_red))

    for comp in g.subjects(RDF.type, DKG["SoftwareComponent"]):
        g.add((comp, DKG["hasTLPMarking"], tlp_red))

    # Marquage TLP:CLEAR sur référentiels publics (CVE, CWE, CAPEC)
    for cve_node in list(g.subjects(RDF.type, DKG["Vulnerability"])):
        g.add((cve_node, DKG["hasTLPMarking"], tlp_clear))
        cve_id = str(list(g.objects(cve_node, DKG["cveId"]))[0]) if list(g.objects(cve_node, DKG["cveId"])) else str(cve_node).split("#")[-1]

        if cve_id in external_data:
            meta = external_data[cve_id]
            g.add((cve_node, DKG["cveDescription"], Literal(meta["description"], datatype=XSD.string)))
            g.add((cve_node, DKG["cvssV3Vector"], Literal(meta["cvss_vector"], datatype=XSD.string)))
            g.add((cve_node, DKG["severityLabel"], Literal(meta["severity"], datatype=XSD.string)))
            g.add((cve_node, DKG["lastEnrichedAt"], Literal(now_iso, datatype=XSD.dateTime)))

    for cwe_node in list(g.subjects(RDF.type, DKG["Weakness"])):
        g.add((cwe_node, DKG["hasTLPMarking"], tlp_clear))
        cwe_id = str(cwe_node).split("#")[-1]

        if cwe_id in external_data:
            capec_info = external_data[cwe_id]
            capec_node = DKG_INST[capec_info["capec_id"]]

            g.add((capec_node, RDF.type, DKG["ThreatPattern"]))
            g.add((capec_node, RDFS.label, Literal(f"{capec_info['capec_id']}: {capec_info['capec_title']}", lang="en")))
            g.add((capec_node, DKG["patternDescription"], Literal(capec_info["capec_description"], datatype=XSD.string)))
            g.add((capec_node, DKG["hasTLPMarking"], tlp_clear))
            g.add((capec_node, DKG["lastEnrichedAt"], Literal(now_iso, datatype=XSD.dateTime)))

            g.add((cwe_node, DKG["hasThreatPattern"], capec_node))

    return g


def export_abox_master_markdown(g: Graph, destination_path: Path):
    md = []
    md.append("# 🔴 DKG Master ABox Consolidée - Graphe d'Attaque (TLP:RED)\n")
    md.append("> **Classification Globale** : `TLP:RED` (Strictement confidentiel - Usage interne restreint)  ")
    md.append("> **Répertoire** : `12-Donnees/TLP_RED_Consolidation_ABox/`\n")

    md.append("## 📊 Synthèse des Instances Consolidées\n")
    md.append("| Entité / Concept | Nb Instances | Niveau TLP |")
    md.append("| :--- | :--- | :--- |")
    md.append(f"| **Équipements (Assets)** | {len(list(g.subjects(RDF.type, DKG['Asset'])))} | `TLP:RED` |")
    md.append(f"| **Composants Logiques** | {len(list(g.subjects(RDF.type, DKG['SoftwareComponent'])))} | `TLP:RED` |")
    md.append(f"| **Vulnérabilités (CVE)** | {len(list(g.subjects(RDF.type, DKG['Vulnerability'])))} | `TLP:CLEAR` |")
    md.append(f"| **Faiblesses (CWE)** | {len(list(g.subjects(RDF.type, DKG['Weakness'])))} | `TLP:CLEAR` |")
    md.append(f"| **Patterns d'Attaque (CAPEC)** | {len(list(g.subjects(RDF.type, DKG['ThreatPattern'])))} | `TLP:CLEAR` |\n")

    md.append("## 🌐 Visualisation du Graphe d'Attaque Consolidé\n")
    md.append("```mermaid")
    md.append("graph TD")

    for s, p, o in g.triples((None, DKG["hasInstalledComponent"], None)):
        md.append(f"    {str(s).split('#')[-1]}[{str(s).split('#')[-1]} - TLP:RED] -->|hasInstalledComponent| {str(o).split('#')[-1]}")

    for s, p, o in g.triples((None, DKG["hasVulnerability"], None)):
        md.append(f"    {str(s).split('#')[-1]} -->|hasVulnerability| {str(o).split('#')[-1]}[{str(o).split('#')[-1]} - TLP:CLEAR]")

    for s, p, o in g.triples((None, DKG["hasWeakness"], None)):
        md.append(f"    {str(s).split('#')[-1]} -->|hasWeakness| {str(o).split('#')[-1]}")

    for s, p, o in g.triples((None, DKG["hasThreatPattern"], None)):
        md.append(f"    {str(s).split('#')[-1]} -->|hasThreatPattern| {str(o).split('#')[-1]}")

    md.append("```\n")

    destination_path.write_text("\n".join(md), encoding="utf-8")


def main():
    ENRICHED_DIR.mkdir(parents=True, exist_ok=True)
    CONSOLIDATION_ABOX_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Consolidation TBox Master
    consolidate_tbox_master()

    # 2. Consolidation ABox Master TLP:RED
    g = build_enriched_abox_graph()

    g.serialize(destination=FILE_SNAPSHOT_TTL, format="turtle")
    g.serialize(destination=FILE_MASTER_TTL, format="turtle")
    g.serialize(destination=FILE_MASTER_JSON, format="json-ld", indent=4)
    export_abox_master_markdown(g, FILE_MASTER_MD)

    print(f"✅ Master ABox TLP:RED (TTL, JSON-LD, MD) généré dans : {CONSOLIDATION_ABOX_DIR}")


if __name__ == "__main__":
    main()
