#!/usr/bin/env python3
"""
Générateur de la TBox & RBox Stricte (Socle Structurel Sémantique - Phase 1)
Conforme aux exigences normatives SPEC-01 (EXG-TBOX-01 à EXG-TBOX-04).
"""

from pathlib import Path
from rdflib import Graph, Literal, Namespace, RDF, RDFS, OWL, XSD

# Correction du chemin de sortie vers le répertoire canonique TBox_init
BASE_DIR = Path(__file__).resolve().parent.parent
TBOX_OUT = BASE_DIR / "12-Donnees" / "TBox_init" / "TBox_Cybersec.ttl"

def build_tbox():
    g = Graph()

    # Déclaration du Namespace unique (EXG-TBOX-01)
    DKG = Namespace("http://dkg.cybersec.org/tbox#")
    
    g.bind("dkg", DKG)
    g.bind("owl", OWL)
    g.bind("rdfs", RDFS)
    g.bind("xsd", XSD)

    # ---------------------------------------------------------
    # 1. ONTOLOGY METADATA
    # ---------------------------------------------------------
    onto_uri = DKG[""]
    g.add((onto_uri, RDF.type, OWL.Ontology))
    g.add((onto_uri, RDFS.label, Literal("Ontologie DKG Cybersec - TBox & RBox Stricte", lang="fr")))
    g.add((onto_uri, RDFS.comment, Literal("Socle structurel définissant le vocabulaire, les classes et les propriétés de sécurité.", lang="fr")))

    # ---------------------------------------------------------
    # 2. CLASSES DECLARATION (EXG-TBOX-02)
    # ---------------------------------------------------------
    classes = [
        ("Asset", "Équipement ou ressource de l'infrastructure informatique."),
        ("SoftwareComponent", "Composant logiciel, service ou brique applicative installé sur un Asset."),
        ("Vulnerability", "Faiblesse ou vulnérabilité de sécurité identifiée (ex: CVE)."),
        ("Weakness", "Type de faiblesse logicielle sous-jacente (ex: CWE)."),
        ("ThreatPattern", "Modèle d'attaque ou pattern d'exploitation (ex: CAPEC).")
    ]

    for class_name, comment in classes:
        cls_uri = DKG[class_name]
        g.add((cls_uri, RDF.type, OWL.Class))
        g.add((cls_uri, RDFS.label, Literal(class_name, lang="en")))
        g.add((cls_uri, RDFS.comment, Literal(comment, lang="fr")))

    # ---------------------------------------------------------
    # 3. OBJECT PROPERTIES DECLARATION (EXG-TBOX-03 & EXG-TBOX-04)
    # ---------------------------------------------------------
    
    # Asset -> SoftwareComponent
    has_comp = DKG["hasInstalledComponent"]
    g.add((has_comp, RDF.type, OWL.ObjectProperty))
    g.add((has_comp, RDFS.label, Literal("hasInstalledComponent", lang="en")))
    g.add((has_comp, RDFS.domain, DKG["Asset"]))
    g.add((has_comp, RDFS.range, DKG["SoftwareComponent"]))

    # Axiome RBox Stricte : Relation Inverse (EXG-TBOX-04)
    is_comp_of = DKG["isComponentOf"]
    g.add((is_comp_of, RDF.type, OWL.ObjectProperty))
    g.add((is_comp_of, RDFS.label, Literal("isComponentOf", lang="en")))
    g.add((is_comp_of, RDFS.domain, DKG["SoftwareComponent"]))
    g.add((is_comp_of, RDFS.range, DKG["Asset"]))
    g.add((is_comp_of, OWL.inverseOf, has_comp))

    # SoftwareComponent -> Vulnerability
    has_vuln = DKG["hasVulnerability"]
    g.add((has_vuln, RDF.type, OWL.ObjectProperty))
    g.add((has_vuln, RDFS.label, Literal("hasVulnerability", lang="en")))
    g.add((has_vuln, RDFS.domain, DKG["SoftwareComponent"]))
    g.add((has_vuln, RDFS.range, DKG["Vulnerability"]))

    # Vulnerability -> Weakness (CWE)
    has_cwe = DKG["hasWeakness"]
    g.add((has_cwe, RDF.type, OWL.ObjectProperty))
    g.add((has_cwe, RDFS.label, Literal("hasWeakness", lang="en")))
    g.add((has_cwe, RDFS.domain, DKG["Vulnerability"]))
    g.add((has_cwe, RDFS.range, DKG["Weakness"]))

    # ---------------------------------------------------------
    # 4. DATATYPE PROPERTIES DECLARATION
    # ---------------------------------------------------------
    datatype_props = [
        ("hostname", DKG["Asset"], XSD.string, "Nom d'hôte ou FQDN de l'équipement."),
        ("ipAddress", DKG["Asset"], XSD.string, "Adresse IP de l'équipement."),
        ("componentName", DKG["SoftwareComponent"], XSD.string, "Nom du composant logiciel."),
        ("version", DKG["SoftwareComponent"], XSD.string, "Version installée du composant."),
        ("cvssScore", DKG["Vulnerability"], XSD.float, "Score de gravité CVSS v3/v4."),
        ("cveId", DKG["Vulnerability"], XSD.string, "Identifiant canonique CVE.")
    ]

    for prop_name, domain_cls, range_type, comment in datatype_props:
        prop_uri = DKG[prop_name]
        g.add((prop_uri, RDF.type, OWL.DatatypeProperty))
        g.add((prop_uri, RDFS.label, Literal(prop_name, lang="en")))
        g.add((prop_uri, RDFS.domain, domain_cls))
        g.add((prop_uri, RDFS.range, range_type))
        g.add((prop_uri, RDFS.comment, Literal(comment, lang="fr")))

    # ---------------------------------------------------------
    # 5. SÉRIALISATION TURTLE (.ttl)
    # ---------------------------------------------------------
    TBOX_OUT.parent.mkdir(parents=True, exist_ok=True)
    g.serialize(destination=TBOX_OUT, format="turtle")
    print(f"✅ TBox & RBox Stricte générées avec succès dans : {TBOX_OUT}")
    print(f"ℹ️  Nombre total de triplets générés : {len(g)}")

if __name__ == "__main__":
    build_tbox()
