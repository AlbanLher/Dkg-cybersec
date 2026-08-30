#!/usr/bin/env python3
"""
Ingesteur d'inventaires applicatifs et système vers l'ABox RDF (Phase 2).
Lit des structures d'inventaires brutes et génère le graphe RDF mis à jour dans 12-Donnees/ABox_init/.
"""

import json
from pathlib import Path
from rdflib import Graph, Literal, Namespace, RDF, RDFS, OWL, XSD

BASE_DIR = Path(__file__).resolve().parent.parent
TBOX_FILE = BASE_DIR / "12-Donnees" / "TBox_init" / "TBox_Cybersec.ttl"
ABOX_DIR = BASE_DIR / "12-Donnees" / "ABox_init"
OUTPUT_TTL = ABOX_DIR / "ABox_Cybersec.ttl"

DKG = Namespace("http://dkg.cybersec.org/tbox#")
DKG_INST = Namespace("http://dkg.cybersec.org/abox#")


def ingest_inventory_data(inventory_json: str) -> Graph:
    """Ingère un JSON d'inventaire et construit l'ABox correspondante."""
    g = Graph()
    if TBOX_FILE.exists():
        g.parse(TBOX_FILE, format="turtle")

    g.bind("dkg", DKG)
    g.bind("dkg-inst", DKG_INST)

    data = json.loads(inventory_json)

    for host in data.get("hosts", []):
        asset_uri = DKG_INST[host["id"]]
        g.add((asset_uri, RDF.type, DKG["Asset"]))
        g.add((asset_uri, DKG["hostname"], Literal(host["hostname"], datatype=XSD.string)))
        g.add((asset_uri, DKG["ipAddress"], Literal(host["ip"], datatype=XSD.string)))

        for comp in host.get("components", []):
            comp_uri = DKG_INST[comp["id"]]
            g.add((comp_uri, RDF.type, DKG["SoftwareComponent"]))
            g.add((comp_uri, DKG["componentName"], Literal(comp["name"], datatype=XSD.string)))
            g.add((comp_uri, DKG["version"], Literal(comp["version"], datatype=XSD.string)))

            # Relations bidirectionnelles (TBox/RBox)
            g.add((asset_uri, DKG["hasInstalledComponent"], comp_uri))
            g.add((comp_uri, DKG["isComponentOf"], asset_uri))

            for cve in comp.get("vulnerabilities", []):
                cve_uri = DKG_INST[cve["id"]]
                g.add((cve_uri, RDF.type, DKG["Vulnerability"]))
                g.add((cve_uri, DKG["cveId"], Literal(cve["id"], datatype=XSD.string)))
                g.add((cve_uri, DKG["cvssScore"], Literal(float(cve["cvss"]), datatype=XSD.float)))

                g.add((comp_uri, DKG["hasVulnerability"], cve_uri))

                if "cwe" in cve:
                    cwe_uri = DKG_INST[cve["cwe"]]
                    g.add((cwe_uri, RDF.type, DKG["Weakness"]))
                    g.add((cve_uri, DKG["hasWeakness"], cwe_uri))

    return g


if __name__ == "__main__":
    sample_inventory = """
    {
        "hosts": [
            {
                "id": "srv-proxy-01",
                "hostname": "proxy01.corp.internal",
                "ip": "10.0.0.1",
                "components": [
                    {
                        "id": "haproxy-2.2.0",
                        "name": "haproxy",
                        "version": "2.2.0",
                        "vulnerabilities": [
                            {
                                "id": "CVE-2021-40346",
                                "cvss": 8.5,
                                "cwe": "CWE-400"
                            }
                        ]
                    }
                ]
            }
        ]
    }
    """
    ABOX_DIR.mkdir(parents=True, exist_ok=True)
    graph = ingest_inventory_data(sample_inventory)
    graph.serialize(destination=OUTPUT_TTL, format="turtle")
    print(f"✅ Ingestion effectuée et ABox enregistrée dans : {OUTPUT_TTL}")
