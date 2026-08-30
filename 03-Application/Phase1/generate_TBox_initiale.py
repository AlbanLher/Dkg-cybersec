#!/usr/bin/env python3
"""
Générateur Multi-formats de la TBox / RBox Stricte (Phase 1).
Exporte le socle structurel en Turtle (.ttl), JSON-LD (.json) et Markdown (.md)
avec intégration des diagrammes Mermaid et de la table des acronymes.
Conforme aux exigences normatives SPEC-01 (EXG-TBOX-01 à EXG-TBOX-04).
"""

from pathlib import Path
from rdflib import Graph, Literal, Namespace, RDF, RDFS, OWL, XSD

# 1. Correction du dossier de sortie : TBox_init
BASE_DIR = Path(__file__).resolve().parent.parent
TBOX_DIR = BASE_DIR / "12-Donnees" / "TBox_init"

FILE_TTL = TBOX_DIR / "TBox_Cybersec.ttl"
FILE_JSONLD = TBOX_DIR / "TBox_Cybersec.json"
FILE_MD = TBOX_DIR / "TBox_Cybersec.md"


def build_tbox_graph() -> Graph:
    """Construit le graphe RDFlib principal de la TBox/RBox."""
    g = Graph()

    DKG = Namespace("http://dkg.cybersec.org/tbox#")

    g.bind("dkg", DKG)
    g.bind("owl", OWL)
    g.bind("rdfs", RDFS)
    g.bind("xsd", XSD)

    # Métadonnées
    onto_uri = DKG[""]
    g.add((onto_uri, RDF.type, OWL.Ontology))
    g.add((onto_uri, RDFS.label, Literal("Ontologie DKG Cybersec - Socle Structurel", lang="fr")))
    g.add((onto_uri, RDFS.comment, Literal("TBox & RBox Stricte : définitions des classes, propriétés et relations.", lang="fr")))

    # Classes (EXG-TBOX-02)
    classes = [
        ("Asset", "Équipement ou ressource de l'infrastructure informatique (ex: serveur, VM)."),
        ("SoftwareComponent", "Composant logiciel ou brique applicative installée sur un Asset (ex: NGINX, OpenSSL)."),
        ("Vulnerability", "Vulnérabilité ou faille de sécurité identifiée (ex: CVE)."),
        ("Weakness", "Type de faiblesse logicielle sous-jacente (ex: CWE)."),
        ("ThreatPattern", "Modèle d'attaque ou pattern d'exploitation (ex: CAPEC).")
    ]

    for class_name, comment in classes:
        cls_uri = DKG[class_name]
        g.add((cls_uri, RDF.type, OWL.Class))
        g.add((cls_uri, RDFS.label, Literal(class_name, lang="en")))
        g.add((cls_uri, RDFS.comment, Literal(comment, lang="fr")))

    # Object Properties & Axiomes RBox (EXG-TBOX-03 & EXG-TBOX-04)
    has_comp = DKG["hasInstalledComponent"]
    g.add((has_comp, RDF.type, OWL.ObjectProperty))
    g.add((has_comp, RDFS.label, Literal("hasInstalledComponent", lang="en")))
    g.add((has_comp, RDFS.domain, DKG["Asset"]))
    g.add((has_comp, RDFS.range, DKG["SoftwareComponent"]))
    g.add((has_comp, RDFS.comment, Literal("Rattache un composant logiciel à un équipement.", lang="fr")))

    is_comp = DKG["isComponentOf"]
    g.add((is_comp, RDF.type, OWL.ObjectProperty))
    g.add((is_comp, RDFS.label, Literal("isComponentOf", lang="en")))
    g.add((is_comp, RDFS.domain, DKG["SoftwareComponent"]))
    g.add((is_comp, RDFS.range, DKG["Asset"]))
    g.add((is_comp, OWL.inverseOf, has_comp))

    has_vuln = DKG["hasVulnerability"]
    g.add((has_vuln, RDF.type, OWL.ObjectProperty))
    g.add((has_vuln, RDFS.label, Literal("hasVulnerability", lang="en")))
    g.add((has_vuln, RDFS.domain, DKG["SoftwareComponent"]))
    g.add((has_vuln, RDFS.range, DKG["Vulnerability"]))

    has_cwe = DKG["hasWeakness"]
    g.add((has_cwe, RDF.type, OWL.ObjectProperty))
    g.add((has_cwe, RDFS.label, Literal("hasWeakness", lang="en")))
    g.add((has_cwe, RDFS.domain, DKG["Vulnerability"]))
    g.add((has_cwe, RDFS.range, DKG["Weakness"]))

    # Datatype Properties
    datatype_props = [
        ("hostname", DKG["Asset"], XSD.string, "Nom d'hôte de l'équipement."),
        ("ipAddress", DKG["Asset"], XSD.string, "Adresse IP principale."),
        ("componentName", DKG["SoftwareComponent"], XSD.string, "Nom du produit logiciel."),
        ("version", DKG["SoftwareComponent"], XSD.string, "Version spécifique du composant."),
        ("cvssScore", DKG["Vulnerability"], XSD.float, "Score CVSS v3/v4 de gravité."),
        ("cveId", DKG["Vulnerability"], XSD.string, "Identifiant canonique CVE.")
    ]

    for prop_name, domain_cls, range_type, comment in datatype_props:
        prop_uri = DKG[prop_name]
        g.add((prop_uri, RDF.type, OWL.DatatypeProperty))
        g.add((prop_uri, RDFS.label, Literal(prop_name, lang="en")))
        g.add((prop_uri, RDFS.domain, domain_cls))
        g.add((prop_uri, RDFS.range, range_type))
        g.add((prop_uri, RDFS.comment, Literal(comment, lang="fr")))

    return g


def export_markdown_documentation(g: Graph, destination_path: Path):
    """Génère la documentation Markdown complète incluant le diagramme Mermaid et les acronymes."""
    md_content = []
    md_content.append("# 📗 Spécification de la TBox & RBox DKG (TLP:AMBER)\n")
    md_content.append("> **Statut** : Document d'Ontologie Généré Automatiquement")
    md_content.append("> **Namespace canonique** : `http://dkg.cybersec.org/tbox#`\n")

    # RESTITUTION EXIGENCES : Table des Acronymes
    md_content.append("## 📜 Glossaire & Acronymes Normatifs\n")
    md_content.append("| Acronyme | Nom Complet | Description |")
    md_content.append("| :--- | :--- | :--- |")
    md_content.append("| **TBox** | Terminology Box | Déclaration des classes, types et concepts de l'ontologie. |")
    md_content.append("| **RBox** | Relational Box | Déclaration des règles et propriétés d'objets (domaine, portée, inverses). |")
    md_content.append("| **ABox** | Assertion Box | Ensemble des instances et données concrètes (ex: serveurs réels, CVEs). |")
    md_content.append("| **CVE** | Common Vulnerabilities and Exposures | Dictionnaire des vulnérabilités de sécurité connues. |")
    md_content.append("| **CWE** | Common Weakness Enumeration | Système de classification des faiblesses software/hardware. |")
    md_content.append("| **CAPEC** | Common Attack Pattern Enumeration and Classification | Catalogues des schémas d'attaques employés par les adversaires. |\n")

    # RESTITUTION EXIGENCES : Diagramme Mermaid
    md_content.append("## 📊 Modèle Conceptuel (Diagramme Mermaid)\n")
    md_content.append("```mermaid")
    md_content.append("classDiagram")
    md_content.append("    direction LR")
    
    for s in g.subjects(RDF.type, OWL.ObjectProperty):
        name = str(s).split("#")[-1]
        domain = str(g.value(s, RDFS.domain) or "").split("#")[-1]
        range_ = str(g.value(s, RDFS.range) or "").split("#")[-1]
        md_content.append(f"    {domain} --> {range_} : {name}")

    md_content.append("```\n")

    # Tables des Classes et Propriétés
    md_content.append("## 1. Classes Ontologiques (`owl:Class`)\n")
    md_content.append("| Classe | Libellé | Description |")
    md_content.append("| :--- | :--- | :--- |")
    for s in g.subjects(RDF.type, OWL.Class):
        name = str(s).split("#")[-1]
        comment = str(g.value(s, RDFS.comment) or "N/A")
        md_content.append(f"| `dkg:{name}` | **{name}** | {comment} |")

    md_content.append("\n## 2. Propriétés d'Objets / Relations (`owl:ObjectProperty`)\n")
    md_content.append("| Relation | Domaine (`domain`) | Portée (`range`) | Axiome / Inverse |")
    md_content.append("| :--- | :--- | :--- | :--- |")
    for s in g.subjects(RDF.type, OWL.ObjectProperty):
        name = str(s).split("#")[-1]
        domain = str(g.value(s, RDFS.domain) or "").split("#")[-1]
        range_ = str(g.value(s, RDFS.range) or "").split("#")[-1]
        inverse = g.value(s, OWL.inverseOf)
        inverse_str = f"`owl:inverseOf dkg:{str(inverse).split('#')[-1]}`" if inverse else "-"
        md_content.append(f"| `dkg:{name}` | `dkg:{domain}` | `dkg:{range_}` | {inverse_str} |")

    md_content.append("\n## 3. Propriétés de Données (`owl:DatatypeProperty`)\n")
    md_content.append("| Propriété | Domaine (`domain`) | Type de Donnée (`range`) | Description |")
    md_content.append("| :--- | :--- | :--- | :--- |")
    for s in g.subjects(RDF.type, OWL.DatatypeProperty):
        name = str(s).split("#")[-1]
        domain = str(g.value(s, RDFS.domain) or "").split("#")[-1]
        range_ = str(g.value(s, RDFS.range) or "").split("#")[-1]
        comment = str(g.value(s, RDFS.comment) or "N/A")
        md_content.append(f"| `dkg:{name}` | `dkg:{domain}` | `xsd:{range_}` | {comment} |")

    destination_path.write_text("\n".join(md_content), encoding="utf-8")


def main():
    TBOX_DIR.mkdir(parents=True, exist_ok=True)
    g = build_tbox_graph()

    g.serialize(destination=FILE_TTL, format="turtle")
    print(f"✅ Export Turtle généré dans : {FILE_TTL}")

    g.serialize(destination=FILE_JSONLD, format="json-ld", indent=4)
    print(f"✅ Export JSON-LD généré dans : {FILE_JSONLD}")

    export_markdown_documentation(g, FILE_MD)
    print(f"✅ Export Markdown (avec Mermaid & Acronymes) généré dans : {FILE_MD}")


if __name__ == "__main__":
    main()
