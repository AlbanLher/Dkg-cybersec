#!/usr/bin/env python3
"""
generate_phase2_abox.py
Génération automatisée de l'ABox Master (DKG Phase 2 - UseCase Cyber).
Lit un fichier JSON d'inventaire, génère le graphe RDF, puis l'enregistre
prioritairement dans le Snapshot avant de le synchroniser vers le Master.
"""
import json
import shutil
import sys
from pathlib import Path

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
    DIR_DATA
)

INVENTORY_JSON_PATH = DIR_INPUT_P2 / "inventory.json"

def load_inventory(json_path: Path) -> dict:
    if not json_path.exists():
        raise FileNotFoundError(f"Fichier d'inventaire introuvable : {json_path}")
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

def build_abox_graph(data: dict) -> Graph:
    g = Graph()
    g.bind("dkg", DKG_TBOX)
    g.bind("data", DKG_DATA)
    g.bind("owl", OWL)
    g.bind("rdf", RDF)
    g.bind("rdfs", RDFS)
    g.bind("xsd", XSD)

    # En-tête Ontologie ABox
    abox_ont = DKG_DATA["ABox_Master"]
    g.add((abox_ont, RDF.type, OWL.Ontology))
    g.add((abox_ont, RDFS.label, Literal("DKG ABox Master - Operational Cyber Security Graph", lang="fr")))

    # 1. TLP Markings
    for tlp_name in data.get("tlp_markings", []):
        tlp_uri = DKG_DATA[tlp_name]
        g.add((tlp_uri, RDF.type, DKG_TBOX.TLPMarking))
        g.add((tlp_uri, RDFS.label, Literal(tlp_name.replace("-", ":"), lang="en")))

    # 2. Threat Patterns
    for tp in data.get("threat_patterns", []):
        tp_uri = DKG_DATA[tp["id"]]
        g.add((tp_uri, RDF.type, DKG_TBOX.ThreatPattern))
        g.add((tp_uri, RDFS.label, Literal(tp["label"], lang="en")))
        g.add((tp_uri, RDFS.comment, Literal(tp["description"], lang="en")))

    # 3. Weaknesses
    for cwe in data.get("weaknesses", []):
        cwe_uri = DKG_DATA[cwe["id"]]
        g.add((cwe_uri, RDF.type, DKG_TBOX.Weakness))
        g.add((cwe_uri, RDFS.label, Literal(cwe["label"], lang="en")))
        if "threat_pattern_id" in cwe:
            tp_uri = DKG_DATA[cwe["threat_pattern_id"]]
            g.add((cwe_uri, DKG_TBOX.hasThreatPattern, tp_uri))

    # 4. Vulnerabilities
    for cve in data.get("vulnerabilities", []):
        cve_uri = DKG_DATA[cve["id"]]
        g.add((cve_uri, RDF.type, DKG_TBOX.Vulnerability))
        g.add((cve_uri, RDFS.label, Literal(cve["label"], lang="en")))
        g.add((cve_uri, DKG_TBOX.cvssScore, Literal(float(cve["cvss_score"]), datatype=XSD.float)))
        if "weakness_id" in cve:
            cwe_uri = DKG_DATA[cve["weakness_id"]]
            g.add((cve_uri, DKG_TBOX.hasWeakness, cwe_uri))

    # 5. Software Components
    for comp in data.get("software_components", []):
        comp_uri = DKG_DATA[comp["id"]]
        g.add((comp_uri, RDF.type, DKG_TBOX.SoftwareComponent))
        g.add((comp_uri, RDFS.label, Literal(comp["label"], lang="fr")))
        if "vulnerability_id" in comp:
            cve_uri = DKG_DATA[comp["vulnerability_id"]]
            g.add((comp_uri, DKG_TBOX.hasVulnerability, cve_uri))
            g.add((cve_uri, DKG_TBOX.isVulnerabilityOf, comp_uri))

    # 6. Assets
    for asset in data.get("assets", []):
        asset_uri = DKG_DATA[asset["id"]]
        g.add((asset_uri, RDF.type, DKG_TBOX.Asset))
        g.add((asset_uri, RDFS.label, Literal(asset["label"], lang="fr")))
        if "tlp_marking" in asset:
            tlp_uri = DKG_DATA[asset["tlp_marking"]]
            g.add((asset_uri, DKG_TBOX.hasTLPMarking, tlp_uri))
        if "installed_component_id" in asset:
            comp_uri = DKG_DATA[asset["installed_component_id"]]
            g.add((asset_uri, DKG_TBOX.hasInstalledComponent, comp_uri))
            g.add((comp_uri, DKG_TBOX.isComponentOf, asset_uri))

    return g

def generate_abox():
    print("Chargement des données d'inventaire...")
    inventory_data = load_inventory(INVENTORY_JSON_PATH)

    print("Construction du graphe RDF ABox...")
    g = build_abox_graph(inventory_data)

    # Création des répertoires cible
    DIR_SNAPSHOT_P2.mkdir(parents=True, exist_ok=True)
    DIR_MASTER_ABOX.mkdir(parents=True, exist_ok=True)

    # 1. ÉCRITURE PRIORITAIRE DANS LE SNAPSHOT
    snapshot_ttl_path = DIR_SNAPSHOT_P2 / ABOX_MASTER_PATH.name
    g.serialize(destination=str(snapshot_ttl_path), format="turtle")
    print(f"📦 Snapshot ABox généré : {snapshot_ttl_path} ({len(g)} triplets)")

    # 2. COPIE DU SNAPSHOT VERS LE MASTER (Parité garantie)
    shutil.copy(snapshot_ttl_path, ABOX_MASTER_PATH)
    print(f"✅ Master ABox synchronisé depuis Snapshot : {ABOX_MASTER_PATH}")

if __name__ == "__main__":
    generate_abox()
