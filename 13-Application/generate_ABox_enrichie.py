#!/usr/bin/env python3
"""
Générateur de l'ABox Enrichie & Consolidation Master (Phase 3).
Produit le snapshot 12-Donnees/ABox_enriched/ et synchronise les dossiers canoniques:
- 12-Donnees/Socle_TBox/ (DKG_TBox_Master.ttl)
- 12-Donnees/Consolidation_ABox/ (DKG_ABox_Master.ttl)
Conforme aux exigences SPEC-03 et marquage TLP.
"""

from pathlib import Path
from datetime import datetime, timezone
from rdflib import Graph, Literal, Namespace, RDF, RDFS, OWL, XSD

from ingest_external_nvd_capec import ingest_external_data, fetch_enrichment_data
from generate_TBox_initiale import build_tbox_graph

BASE_DIR = Path(__file__).resolve().parent.parent

# Dossiers d'exportation
ENRICHED_DIR = BASE_DIR / "12-Donnees" / "ABox_enriched"
SOCLE_TBOX_DIR = BASE_DIR / "12-Donnees" / "Socle_TBox"
CONSOLIDATION_ABOX_DIR = BASE_DIR / "12-Donnees" / "Consolidation_ABox"

FILE_SNAPSHOT_TTL = ENRICHED_DIR / "ABox_Cybersec_enriched.ttl"
FILE_SNAPSHOT_MD = ENRICHED_DIR / "ABox_Cybersec_enriched.md"

FILE_MASTER_TBOX = SOCLE_TBOX_DIR / "DKG_TBox_Master.ttl"
FILE_MASTER_ABOX = CONSOLIDATION_ABOX_DIR / "DKG_ABox_Master.ttl"

DKG = Namespace("http://dkg.cybersec.org/tbox#")
DKG_INST = Namespace("http://dkg.cybersec.org/abox#")


def build_enriched_abox_graph() -> Graph:
    g = ingest_external_data()
    external_data = fetch_enrichment_data()
    now_iso = datetime.now(timezone.utc).isoformat()

    # Déclaration des instances TLP
    tlp_clear = DKG_INST["TLP-CLEAR"]
    tlp_amber = DKG_INST["TLP-AMBER"]

    g.add((tlp_clear, RDF.type, DKG["TLPMarking"]))
    g.add((tlp_clear, DKG["tlpColor"], Literal("CLEAR", datatype=XSD.string)))

    g.add((tlp_amber, RDF.type, DKG["TLPMarking"]))
    g.add((tlp_amber, DKG["tlpColor"], Literal("AMBER", datatype=XSD.string)))

    # 1. Marquage TLP:AMBER sur entités SI internes (Assets & Components)
    for asset in g.subjects(RDF.type, DKG["Asset"]):
        g.add((asset, DKG["hasTLPMarking"], tlp_amber))

    for comp in g.subjects(RDF.type, DKG["SoftwareComponent"]):
        g.add((comp, DKG["hasTLPMarking"], tlp_amber))

    # 2. Enrichissement NVD & TLP:CLEAR sur Vulnérabilités
    for cve_node in list(g.subjects(RDF.type, DKG["Vulnerability"])):
        g.add((cve_node, DKG["hasTLPMarking"], tlp_clear))
        cve_id = str(list(g.objects(cve_node, DKG["cveId"]))[0]) if list(g.objects(cve_node, DKG["cveId"])) else str(cve_node).split("#")[-1]

        if cve_id in external_data:
            meta = external_data[cve_id]
            g.add((cve_node, DKG["cveDescription"], Literal(meta["description"], datatype=XSD.string)))
            g.add((cve_node, DKG["cvssV3Vector"], Literal(meta["cvss_vector"], datatype=XSD.string)))
            g.add((cve_node, DKG["severityLabel"], Literal(meta["severity"], datatype=XSD.string)))
            g.add((cve_node, DKG["lastEnrichedAt"], Literal(now_iso, datatype=XSD.dateTime)))

    # 3. Enrichissement CAPEC & TLP:CLEAR sur Faiblesses
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


def main():
    # Création des répertoires cible
    ENRICHED_DIR.mkdir(parents=True, exist_ok=True)
    SOCLE_TBOX_DIR.mkdir(parents=True, exist_ok=True)
    CONSOLIDATION_ABOX_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Génération & Synchronisation Master TBox
    master_tbox_graph = build_tbox_graph()
    master_tbox_graph.serialize(destination=FILE_MASTER_TBOX, format="turtle")
    print(f"✅ Master TBox mise à jour : {FILE_MASTER_TBOX}")

    # 2. Génération Snapshot & Master ABox
    enriched_abox_graph = build_enriched_abox_graph()
    
    # Export Snapshot Phase 3
    enriched_abox_graph.serialize(destination=FILE_SNAPSHOT_TTL, format="turtle")
    print(f"✅ Snapshot Phase 3 généré : {FILE_SNAPSHOT_TTL}")

    # Export Master ABox Consolidé (Cible SPARQL/Phase 4)
    enriched_abox_graph.serialize(destination=FILE_MASTER_ABOX, format="turtle")
    print(f"✅ Master ABox Consolidé mis à jour : {FILE_MASTER_ABOX}")


if __name__ == "__main__":
    main()
