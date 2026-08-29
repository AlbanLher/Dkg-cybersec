#!/usr/bin/env python3
"""
Consolideur du Socle TBox Master (TLP:AMBER).
Met à jour l'ontologie canonique complète dans 12-Donnees/TLP_AMBER_Socle_TBox/
sans altérer le script initial de la Phase 1.
"""

from pathlib import Path
from rdflib import Graph, Literal, Namespace, RDF, RDFS, OWL, XSD

BASE_DIR = Path(__file__).resolve().parent.parent
SOCLE_TBOX_DIR = BASE_DIR / "12-Donnees" / "TLP_AMBER_Socle_TBox"

FILE_MASTER_TTL = SOCLE_TBOX_DIR / "DKG_TBox_Master.ttl"
FILE_MASTER_JSONLD = SOCLE_TBOX_DIR / "DKG_TBox_Master.json"
FILE_MASTER_MD = SOCLE_TBOX_DIR / "DKG_TBox_Master.md"

DKG = Namespace("http://dkg.cybersec.org/tbox#")


def build_master_tbox_graph() -> Graph:
    g = Graph()
    g.bind("dkg", DKG)
    g.bind("owl", OWL)
    g.bind("rdfs", RDFS)
    g.bind("xsd", XSD)

    classes = ["Asset", "SoftwareComponent", "Vulnerability", "Weakness", "ThreatPattern", "TLPMarking"]
    for c in classes:
        g.add((DKG[c], RDF.type, OWL.Class))

    obj_props = [
        ("hasInstalledComponent", DKG["Asset"], DKG["SoftwareComponent"]),
        ("isComponentOf", DKG["SoftwareComponent"], DKG["Asset"]),
        ("hasVulnerability", DKG["SoftwareComponent"], DKG["Vulnerability"]),
        ("hasWeakness", DKG["Vulnerability"], DKG["Weakness"]),
        ("hasThreatPattern", DKG["Weakness"], DKG["ThreatPattern"]),
        ("hasTLPMarking", OWL.Thing, DKG["TLPMarking"])
    ]
    for prop, dom, ran in obj_props:
        g.add((DKG[prop], RDF.type, OWL.ObjectProperty))
        g.add((DKG[prop], RDFS.domain, dom))
        g.add((DKG[prop], RDFS.range, ran))

    g.add((DKG["isComponentOf"], OWL.inverseOf, DKG["hasInstalledComponent"]))

    data_props = [
        ("hostname", DKG["Asset"], XSD.string),
        ("ipAddress", DKG["Asset"], XSD.string),
        ("componentName", DKG["SoftwareComponent"], XSD.string),
        ("version", DKG["SoftwareComponent"], XSD.string),
        ("cveId", DKG["Vulnerability"], XSD.string),
        ("cvssScore", DKG["Vulnerability"], XSD.float),
        ("cvssV3Vector", DKG["Vulnerability"], XSD.string),
        ("severityLabel", DKG["Vulnerability"], XSD.string),
        ("cveDescription", DKG["Vulnerability"], XSD.string),
        ("patternDescription", DKG["ThreatPattern"], XSD.string),
        ("lastEnrichedAt", OWL.Thing, XSD.dateTime),
        ("tlpColor", DKG["TLPMarking"], XSD.string)
    ]
    for prop, dom, ran in data_props:
        g.add((DKG[prop], RDF.type, OWL.DatatypeProperty))
        g.add((DKG[prop], RDFS.domain, dom))
        g.add((DKG[prop], RDFS.range, ran))

    return g


def export_tbox_markdown(g: Graph, destination_path: Path):
    md = []
    md.append("# 📖 DKG TBox Master - Ontologie Canonique\n")
    md.append("> **Classification** : `TLP:AMBER`  ")
    md.append("> **Répertoire** : `12-Donnees/TLP_AMBER_Socle_TBox/`\n")

    md.append("## 📌 Classes\n")
    md.append("| Classe | URI | Description |")
    md.append("| :--- | :--- | :--- |")
    for c in sorted(g.subjects(RDF.type, OWL.Class)):
        name = str(c).split("#")[-1]
        md.append(f"| **`dkg:{name}`** | `{c}` | Concept du modèle DKG |")

    md.append("\n## 🔗 Propriétés d'Objets\n")
    md.append("| Propriété | Domaine | Range |")
    md.append("| :--- | :--- | :--- |")
    for p in sorted(g.subjects(RDF.type, OWL.ObjectProperty)):
        name = str(p).split("#")[-1]
        dom = list(g.objects(p, RDFS.domain))
        ran = list(g.objects(p, RDFS.range))
        dom_name = str(dom[0]).split("#")[-1] if dom else "owl:Thing"
        ran_name = str(ran[0]).split("#")[-1] if ran else "owl:Thing"
        md.append(f"| **`dkg:{name}`** | `dkg:{dom_name}` | `dkg:{ran_name}` |")

    md.append("\n## 🏷️ Propriétés de Données (Attributs)\n")
    md.append("| Attribut | Domaine | Datatype |")
    md.append("| :--- | :--- | :--- |")
    for p in sorted(g.subjects(RDF.type, OWL.DatatypeProperty)):
        name = str(p).split("#")[-1]
        dom = list(g.objects(p, RDFS.domain))
        ran = list(g.objects(p, RDFS.range))
        dom_name = str(dom[0]).split("#")[-1] if dom else "owl:Thing"
        ran_name = str(ran[0]).split("#")[-1] if ran else "xsd:string"
        md.append(f"| **`dkg:{name}`** | `dkg:{dom_name}` | `xsd:{ran_name}` |")

    destination_path.write_text("\n".join(md), encoding="utf-8")


def main():
    SOCLE_TBOX_DIR.mkdir(parents=True, exist_ok=True)
    g = build_master_tbox_graph()
    g.serialize(destination=FILE_MASTER_TTL, format="turtle")
    g.serialize(destination=FILE_MASTER_JSONLD, format="json-ld", indent=4)
    export_tbox_markdown(g, FILE_MASTER_MD)
    print(f"✅ TBox Master TLP:AMBER consolidée dans : {SOCLE_TBOX_DIR}")


if __name__ == "__main__":
    main()
