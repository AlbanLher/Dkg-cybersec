#!/usr/bin/env python3
"""
Script d'Ingestion ABox (DKG Cybersec - Phase 2).
Lit : 12-Donnees/ABox_init/inventory.json
Génère : 12-Donnees/ABox_init/ABox_Cybersec.ttl
Conforme à : 11-Principes_Architecture/Specifications/SpecificationNormativeIngestionABox.md
"""

import json
import time
from pathlib import Path
from rdflib import RDF, RDFS, OWL, XSD, Graph, Literal, Namespace

# Dynamic base path resolution
BASE_DIR = Path(__file__).resolve().parent.parent
INVENTORY_JSON = BASE_DIR / "12-Donnees" / "ABox_init" / "inventory.json"
ABOX_OUT = BASE_DIR / "12-Donnees" / "ABox_init" / "ABox_Cybersec.ttl"


def ingest_inventory():
    if not INVENTORY_JSON.exists():
        raise FileNotFoundError(f"Fichier introuvable : {INVENTORY_JSON}")

    # Charge l'inventaire JSON
    with open(INVENTORY_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    g = Graph()

    # Namespaces
    DKG = Namespace("http://dkg.cybersec.org/tbox#")
    ABOX = Namespace("http://dkg.cybersec.org/abox#")

    g.bind("dkg", DKG)
    g.bind("abox", ABOX)
    g.bind("owl", OWL)
    g.bind("rdfs", RDFS)
    g.bind("xsd", XSD)

    # Entête Ontologie ABox & Import TBox
    abox_ont = ABOX[""]
    g.add((abox_ont, RDF.type, OWL.Ontology))
    g.add((abox_ont, OWL.imports, DKG[""]))
    g.add(
        (
            abox_ont,
            RDFS.label,
            Literal("ABox Instance Graph - DKG Cybersec", lang="fr"),
        )
    )
    g.add(
        (
            abox_ont,
            RDFS.comment,
            Literal(
                f"Généré automatiquement par ingest_inventory.py le {time.ctime()}",
                lang="fr",
            ),
        )
    )

    # Ingestion des Assets & Composants
    assets = data.get("assets", [])
    for asset in assets:
        asset_id = asset["id"]
        asset_uri = ABOX[asset_id]

        # Instanciation Asset (dkg:Asset)
        g.add((asset_uri, RDF.type, DKG.Asset))
        if "label" in asset:
            g.add((asset_uri, RDFS.label, Literal(asset["label"], lang="fr")))

        # Propriétés spécifiques Asset
        if "ip" in asset:
            g.add(
                (
                    asset_uri,
                    DKG.ipAddress,
                    Literal(asset["ip"], datatype=XSD.string),
                )
            )

        # Traitement des logiciels installés
        for sw in asset.get("installed_software", []):
            sw_id = sw["id"]
            sw_uri = ABOX[sw_id]

            # Instanciation SoftwareComponent
            g.add((sw_uri, RDF.type, DKG.SoftwareComponent))
            if "label" in sw:
                g.add((sw_uri, RDFS.label, Literal(sw["label"], lang="fr")))
            if "version" in sw:
                g.add(
                    (
                        sw_uri,
                        DKG.version,
                        Literal(sw["version"], datatype=XSD.string),
                    )
                )
            if "cpe" in sw:
                g.add(
                    (
                        sw_uri,
                        DKG.cpeIdentifier,
                        Literal(sw["cpe"], datatype=XSD.string),
                    )
                )

            # Liaison Asset -> SoftwareComponent (dkg:hasInstalledComponent)
            g.add((asset_uri, DKG.hasInstalledComponent, sw_uri))

            # Traitement des Vulnérabilités connues (déclarées locales)
            for cve_id in sw.get("known_vulnerabilities", []):
                vuln_uri = ABOX[cve_id]
                g.add((vuln_uri, RDF.type, DKG.Vulnerability))
                g.add(
                    (
                        vuln_uri,
                        RDFS.label,
                        Literal(f"Vulnérabilité {cve_id}", lang="fr"),
                    )
                )

                # Liaison SoftwareComponent -> Vulnerability (dkg:hasVulnerability)
                g.add((sw_uri, DKG.hasVulnerability, vuln_uri))

    # Écriture forcée sur disque
    ABOX_OUT.parent.mkdir(parents=True, exist_ok=True)
    if ABOX_OUT.exists():
        ABOX_OUT.unlink()

    g.serialize(destination=ABOX_OUT, format="turtle")

    mtime = time.ctime(ABOX_OUT.stat().st_mtime)
    print(f"✓ ABox maître générée avec succès : {ABOX_OUT}")
    print(f"  └─ Date de modification : {mtime}")
    print(f"  └─ Nombre total de triplets RDF : {len(g)}")


if __name__ == "__main__":
    ingest_inventory()
