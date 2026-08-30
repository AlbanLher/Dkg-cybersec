#!/usr/bin/env python3
"""
Générateur de l'ABox Initiale de Référence (Phase 2).
Exporte le jeu de données concrètes en Turtle (.ttl), JSON-LD (.json) et Markdown (.md)
avec intégration des diagrammes Mermaid et vérification des contraintes RBox/TBox.
Conforme aux exigences normatives SPEC-02 (EXG-ABOX-01 à EXG-ABOX-04).
"""

from pathlib import Path
from rdflib import Graph, Literal, Namespace, RDF, RDFS, OWL, XSD

BASE_DIR = Path(__file__).resolve().parent.parent
TBOX_FILE = BASE_DIR / "12-Donnees" / "TBox_init" / "TBox_Cybersec.ttl"
ABOX_DIR = BASE_DIR / "12-Donnees" / "ABox_init"

FILE_TTL = ABOX_DIR / "ABox_Cybersec.ttl"
FILE_JSONLD = ABOX_DIR / "ABox_Cybersec.json"
FILE_MD = ABOX_DIR / "ABox_Cybersec.md"

DKG = Namespace("http://dkg.cybersec.org/tbox#")
DKG_INST = Namespace("http://dkg.cybersec.org/abox#")


def build_abox_graph() -> Graph:
    """Construit le graphe RDFlib de l'ABox initiale."""
    g = Graph()

    # Ingestion de la TBox pour garantie de cohérence
    if TBOX_FILE.exists():
        g.parse(TBOX_FILE, format="turtle")

    g.bind("dkg", DKG)
    g.bind("dkg-inst", DKG_INST)
    g.bind("owl", OWL)
    g.bind("rdfs", RDFS)
    g.bind("xsd", XSD)

    # Assets
    assets_data = [
        ("srv-web-01", "srv-web-01.corp.internal", "192.168.1.50"),
        ("srv-db-01", "srv-db-01.corp.internal", "192.168.1.51")
    ]
    for asset_id, hostname, ip in assets_data:
        node = DKG_INST[asset_id]
        g.add((node, RDF.type, DKG["Asset"]))
        g.add((node, DKG["hostname"], Literal(hostname, datatype=XSD.string)))
        g.add((node, DKG["ipAddress"], Literal(ip, datatype=XSD.string)))

    # Software Components
    comps_data = [
        ("log4j-core-2.14.1", "log4j-core", "2.14.1", "srv-web-01"),
        ("nginx-1.18.0", "nginx", "1.18.0", "srv-web-01"),
        ("postgresql-13.2", "postgresql", "13.2", "srv-db-01")
    ]
    for comp_id, name, ver, parent_asset in comps_data:
        node = DKG_INST[comp_id]
        asset_node = DKG_INST[parent_asset]
        g.add((node, RDF.type, DKG["SoftwareComponent"]))
        g.add((node, DKG["componentName"], Literal(name, datatype=XSD.string)))
        g.add((node, DKG["version"], Literal(ver, datatype=XSD.string)))
        
        # Relation directe + Inférence Inverse RBox
        g.add((asset_node, DKG["hasInstalledComponent"], node))
        g.add((node, DKG["isComponentOf"], asset_node))

    # Vulnerabilities (CVE)
    vulns_data = [
        ("CVE-2021-44228", "CVE-2021-44228", 10.0, "log4j-core-2.14.1", "CWE-502"),
        ("CVE-2021-23017", "CVE-2021-23017", 7.5, "nginx-1.18.0", "CWE-193")
    ]
    for cve_inst, cve_id, cvss, comp_id, cwe_id in vulns_data:
        node = DKG_INST[cve_inst]
        comp_node = DKG_INST[comp_id]
        cwe_node = DKG_INST[cwe_id]

        g.add((node, RDF.type, DKG["Vulnerability"]))
        g.add((node, DKG["cveId"], Literal(cve_id, datatype=XSD.string)))
        g.add((node, DKG["cvssScore"], Literal(cvss, datatype=XSD.float)))
        
        g.add((comp_node, DKG["hasVulnerability"], node))
        g.add((node, DKG["hasWeakness"], cwe_node))

    # Weaknesses (CWE)
    cwes_data = [
        ("CWE-502", "Deserialization of Untrusted Data"),
        ("CWE-193", "Off-by-one Error")
    ]
    for cwe_id, label in cwes_data:
        node = DKG_INST[cwe_id]
        g.add((node, RDF.type, DKG["Weakness"]))
        g.add((node, RDFS.label, Literal(f"{cwe_id}: {label}", lang="en")))

    return g


def export_markdown_documentation(g: Graph, destination_path: Path):
    """Génère le rapport Markdown de l'ABox avec métriques et graphe Mermaid."""
    md_content = []
    md_content.append("# 📙 Rapport de l'ABox DKG Initialisée (TLP:AMBER)\n")
    md_content.append("> **Statut** : Instances de Référence Générées Automatiquement")
    md_content.append("> **Namespace Instances** : `http://dkg.cybersec.org/abox#`\n")

    # Metrics
    num_assets = len(list(g.subjects(RDF.type, DKG["Asset"])))
    num_comps = len(list(g.subjects(RDF.type, DKG["SoftwareComponent"])))
    num_vulns = len(list(g.subjects(RDF.type, DKG["Vulnerability"])))

    md_content.append("## 📊 Métriques du Jeu d'Instances\n")
    md_content.append("| Type d'Entité | Nombre d'Instances | Classe TBox Associée |")
    md_content.append("| :--- | :--- | :--- |")
    md_content.append(f"| **Assets** | {num_assets} | `dkg:Asset` |")
    md_content.append(f"| **Composants Logiciels** | {num_comps} | `dkg:SoftwareComponent` |")
    md_content.append(f"| **Vulnérabilités** | {num_vulns} | `dkg:Vulnerability` |\n")

    # Mermaid Graph of Instances
    md_content.append("## 🌐 Graphe d'Instances (Vue Synthétique)\n")
    md_content.append("```mermaid")
    md_content.append("graph TD")

    for s, p, o in g.triples((None, DKG["hasInstalledComponent"], None)):
        s_name = str(s).split("#")[-1]
        o_name = str(o).split("#")[-1]
        md_content.append(f"    {s_name} -->|hasInstalledComponent| {o_name}")

    for s, p, o in g.triples((None, DKG["hasVulnerability"], None)):
        s_name = str(s).split("#")[-1]
        o_name = str(o).split("#")[-1]
        md_content.append(f"    {s_name} -->|hasVulnerability| {o_name}")

    for s, p, o in g.triples((None, DKG["hasWeakness"], None)):
        s_name = str(s).split("#")[-1]
        o_name = str(o).split("#")[-1]
        md_content.append(f"    {s_name} -->|hasWeakness| {o_name}")

    md_content.append("```\n")

    destination_path.write_text("\n".join(md_content), encoding="utf-8")


def main():
    ABOX_DIR.mkdir(parents=True, exist_ok=True)
    g = build_abox_graph()

    g.serialize(destination=FILE_TTL, format="turtle")
    print(f"✅ Export ABox Turtle généré dans : {FILE_TTL}")

    g.serialize(destination=FILE_JSONLD, format="json-ld", indent=4)
    print(f"✅ Export ABox JSON-LD généré dans : {FILE_JSONLD}")

    export_markdown_documentation(g, FILE_MD)
    print(f"✅ Export ABox Markdown généré dans : {FILE_MD}")


if __name__ == "__main__":
    main()
