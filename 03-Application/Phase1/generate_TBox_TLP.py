#!/usr/bin/env python3
"""
Générateur de la TBox Maître Enrichie (Phase 3 - Governance TLP).
Lit : Spécification TBox + Concepts RBox (Weakness, cvssScore, classifiedUnder)
Génère : 12-Donnees/TLP-AMBER_TBox_Cybersec/TBox_Cybersec.ttl
Classification : TLP:AMBER (Confidentiel Interne)
"""

from pathlib import Path
from rdflib import RDF, RDFS, OWL, XSD, Graph, Literal, Namespace

BASE_DIR = Path(__file__).resolve().parent.parent
TBOX_DIR = BASE_DIR / "12-Donnees" / "TLP-AMBER_TBox_Cybersec"
TBOX_TTL = TBOX_DIR / "TBox_Cybersec.ttl"


def generate_tbox_tlp():
    g = Graph()
    DKG = Namespace("http://dkg.cybersec.org/tbox#")

    g.bind("dkg", DKG)
    g.bind("owl", OWL)
    g.bind("rdfs", RDFS)
    g.bind("xsd", XSD)

    # Entête Ontologie TBox
    tbox_ont = DKG[""]
    g.add((tbox_ont, RDF.type, OWL.Ontology))
    g.add(
        (
            tbox_ont,
            RDFS.label,
            Literal("DKG Cybersecurity Master TBox (TLP:AMBER)", lang="en"),
        )
    )
    g.add(
        (
            tbox_ont,
            RDFS.comment,
            Literal(
                "Ontologie maître et dictionnaire sémantique du DKG.", lang="fr"
            ),
        )
    )

    # --- Classes Principales ---
    classes = [
        ("Asset", "Équipement informatique / Asset SI", "Toute ressource matérielle ou virtuelle du SI."),
        ("SoftwareComponent", "Composant Logiciel", "Brique logicielle, service ou application installée."),
        ("Vulnerability", "Vulnérabilité / Faille", "Faille de sécurité référencée (ex: CVE)."),
        ("Weakness", "Faiblesse Logicielle / CWE", "Catégorie de défaut de conception ou d'implémentation (ex: CWE-193)."),
    ]

    for class_name, label_fr, comment_fr in classes:
        cls_uri = DKG[class_name]
        g.add((cls_uri, RDF.type, OWL.Class))
        g.add((cls_uri, RDFS.label, Literal(label_fr, lang="fr")))
        g.add((cls_uri, RDFS.comment, Literal(comment_fr, lang="fr")))

    # --- Propriétés d'Objets (ObjectProperties) ---
    obj_props = [
        ("hasInstalledComponent", "Asset", "SoftwareComponent", "a installé le composant"),
        ("hasVulnerability", "SoftwareComponent", "Vulnerability", "présente la vulnérabilité"),
        ("classifiedUnder", "Vulnerability", "Weakness", "est classé sous la faiblesse"),
    ]

    for prop_name, domain_name, range_name, label_fr in obj_props:
        p_uri = DKG[prop_name]
        g.add((p_uri, RDF.type, OWL.ObjectProperty))
        g.add((p_uri, RDFS.domain, DKG[domain_name]))
        g.add((p_uri, RDFS.range, DKG[range_name]))
        g.add((p_uri, RDFS.label, Literal(label_fr, lang="fr")))

    # --- Propriétés de Données (DatatypeProperties) ---
    data_props = [
        ("ipAddress", "Asset", XSD.string, "Adresse IP"),
        ("cvssScore", "Vulnerability", XSD.float, "Score CVSS (0.0 - 10.0)"),
        ("cvssVector", "Vulnerability", XSD.string, "Vecteur CVSS v3.1"),
    ]

    for prop_name, domain_name, range_type, label_fr in data_props:
        p_uri = DKG[prop_name]
        g.add((p_uri, RDF.type, OWL.DatatypeProperty))
        g.add((p_uri, RDFS.domain, DKG[domain_name]))
        g.add((p_uri, RDFS.range, range_type))
        g.add((p_uri, RDFS.label, Literal(label_fr, lang="fr")))

    # Sauvegarde
    TBOX_DIR.mkdir(parents=True, exist_ok=True)
    if TBOX_TTL.exists():
        TBOX_TTL.unlink()
    g.serialize(destination=TBOX_TTL, format="turtle")
    print(f"✓ TBox TLP:AMBER régénérée avec succès : {TBOX_TTL} ({len(g)} triplets)")


if __name__ == "__main__":
    generate_tbox_tlp()
