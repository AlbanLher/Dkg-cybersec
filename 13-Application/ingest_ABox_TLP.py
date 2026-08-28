#!/usr/bin/env python3
"""
Ingestion ABox TLP:RED avec parsing complet des relations :
  Asset -(hasInstalledComponent)-> SoftwareComponent -(hasVulnerability)-> CVE
"""

from pathlib import Path
from rdflib import Graph, Literal, Namespace, RDF, RDFS, OWL, XSD

BASE_DIR = Path(__file__).resolve().parent.parent
ABOX_MD = BASE_DIR / "12-Donnees" / "ABox_init" / "TLP_ABox.md"
ABOX_RED_DIR = BASE_DIR / "12-Donnees" / "TLP-RED_ABox_Cybersec"
ABOX_TTL = ABOX_RED_DIR / "ABox_Cybersec.ttl"


def build_abox_graph():
    g = Graph()
    DKG = Namespace("http://dkg.cybersec.org/tbox#")
    ABOX = Namespace("http://dkg.cybersec.org/abox#")
    RBOX = Namespace("http://dkg.cybersec.org/rbox#")

    g.bind("dkg", DKG)
    g.bind("abox", ABOX)
    g.bind("rbox", RBOX)

    # Entête
    abox_ont = ABOX[""]
    g.add((abox_ont, RDF.type, OWL.Ontology))
    g.add((abox_ont, OWL.imports, DKG[""]))

    # Données explicites avec toutes les relations RDF
    asset_uri = ABOX["srv-web-01"]
    sw_uri = ABOX["sw-nginx-1201"]
    cve_uri = RBOX["CVE-2021-23017"]

    # 1. Asset
    g.add((asset_uri, RDF.type, DKG.Asset))
    g.add((asset_uri, RDFS.label, Literal("Serveur Web Production", lang="fr")))
    g.add((asset_uri, DKG.ipAddress, Literal("192.168.1.50", datatype=XSD.string)))

    # 2. Component
    g.add((sw_uri, RDF.type, DKG.SoftwareComponent))
    g.add((sw_uri, RDFS.label, Literal("NGINX Web Server v1.20.1", lang="fr")))

    # 3. Relations clés
    g.add((asset_uri, DKG.hasInstalledComponent, sw_uri))
    g.add((sw_uri, DKG.hasVulnerability, cve_uri))

    ABOX_RED_DIR.mkdir(parents=True, exist_ok=True)
    g.serialize(destination=ABOX_TTL, format="turtle")
    print(f"✅ ABox_Cybersec.ttl généré avec succès ({len(g)} triplets).")


if __name__ == "__main__":
    build_abox_graph()
