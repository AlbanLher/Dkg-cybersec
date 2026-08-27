#!/usr/bin/env python3
"""
Script Constructeur de la TBox Maître (DKG Cybersec).
Génère programmatiquement : 12-Donnees/TBox_init/TBox_Cybersec.ttl
Conforme à : 11-Principes_Architecture/Specifications/SpecificationNormativeSortiesFormatsTBox.md
"""

import time
from pathlib import Path
from rdflib import RDF, RDFS, OWL, SKOS, Graph, Literal, Namespace

# Dynamic base path resolution (Remonte à la racine du dépôt)
BASE_DIR = Path(__file__).resolve().parent.parent # .parent
TBOX_DIR = BASE_DIR / "12-Donnees" / "TBox_init"
TTL_OUT = TBOX_DIR / "TBox_Cybersec.ttl"


def build_tbox():
    g = Graph()

    # Namespaces
    DKG = Namespace("http://dkg.cybersec.org/tbox#")
    g.bind("dkg", DKG)
    g.bind("owl", OWL)
    g.bind("rdfs", RDFS)
    g.bind("skos", SKOS)

    # Ontologie header
    ontology_uri = DKG[""]
    g.add((ontology_uri, RDF.type, OWL.Ontology))
    g.add(
        (
            ontology_uri,
            RDFS.label,
            Literal("Ontologie DKG Cybersec", lang="fr"),
        )
    )
    g.add(
        (
            ontology_uri,
            RDFS.comment,
            Literal(
                "TBox minimale pour le DKG Cybersec - Phase 1 Initialisation",
                lang="fr",
            ),
        )
    )

    # 1. Définition des Classes avec SKOS (Synonymes & Acronymes)
    classes = [
        (
            "Asset",
            "Actif Privé",
            "Équipement informatique physique ou virtuel du SI.",
            ["Serveur", "Host", "Machine", "Équipement"],
        ),
        (
            "SoftwareComponent",
            "Composant Logiciel",
            "Brique logicielle ou système d'exploitation installé.",
            ["CPE", "Package", "Application", "OS"],
        ),
        (
            "Vulnerability",
            "Vulnérabilité",
            "Faille de sécurité répertoriée publiquement.",
            ["CVE", "Breche", "Faille"],
        ),
        (
            "Weakness",
            "Faiblesse Logicielle",
            "Catégorisation des erreurs de conception/code.",
            ["CWE", "Faiblesse"],
        ),
    ]

    for class_id, label, comment, alt_labels in classes:
        cls_uri = DKG[class_id]
        g.add((cls_uri, RDF.type, OWL.Class))
        g.add((cls_uri, RDFS.label, Literal(label, lang="fr")))
        g.add((cls_uri, RDFS.comment, Literal(comment, lang="fr")))
        for alt in alt_labels:
            g.add((cls_uri, SKOS.altLabel, Literal(alt, lang="fr")))

    # 2. Définition des Propriétés
    properties = [
        (
            "hasInstalledComponent",
            "a composant installé",
            DKG.Asset,
            DKG.SoftwareComponent,
        ),
        (
            "hasVulnerability",
            "présente vulnérabilité",
            DKG.SoftwareComponent,
            DKG.Vulnerability,
        ),
        (
            "classifiedUnder",
            "classé sous faiblesse",
            DKG.Vulnerability,
            DKG.Weakness,
        ),
    ]

    for prop_id, label, domain, rng in properties:
        prop_uri = DKG[prop_id]
        g.add((prop_uri, RDF.type, OWL.ObjectProperty))
        g.add((prop_uri, RDFS.label, Literal(label, lang="fr")))
        g.add((prop_uri, RDFS.domain, domain))
        g.add((prop_uri, RDFS.range, rng))

    # Assure l'existence du dossier de destination
    TBOX_DIR.mkdir(parents=True, exist_ok=True)

    # CORRECTION : Force la suppression préalable si le fichier existe pour réinitialiser les droits / verrous
    if TTL_OUT.exists():
        TTL_OUT.unlink()

    # Écriture brute sur le disque
    ttl_data = g.serialize(format="turtle")
    TTL_OUT.write_text(ttl_data, encoding="utf-8")

    # Vérification de l'horodatage
    mtime = time.ctime(TTL_OUT.stat().st_mtime)
    print(f"✓ TBox maître réécrite avec succès : {TTL_OUT}")
    print(f"  └─ Emplacement réel : {TTL_OUT.resolve()}")
    print(f"  └─ Date de modification : {mtime}")


if __name__ == "__main__":
    build_tbox()
