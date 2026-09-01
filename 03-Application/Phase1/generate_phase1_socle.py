import os
import shutil
from pathlib import Path
from rdflib import Graph, Namespace, Literal, URIRef, BNode
from rdflib.namespace import RDF, RDFS, OWL, XSD, SH, SKOS

BASE_DIR = Path(__file__).resolve().parent.parent.parent
MASTER_DIR = BASE_DIR / "02-Donnees" / "Master_Transversal" / "TLP_AMBER_Socle_TBox"
SNAPSHOT_DIR = BASE_DIR / "02-Donnees" / "Snapshots_Phases" / "Phase_1_Socle"

DKG_TBOX = Namespace("http://dkg.cybersec.org/tbox#")
DKG_DATA = Namespace("http://dkg.cybersec.org/data#")

def build_tbox_graph() -> Graph:
    g = Graph()
    g.bind("dkg", DKG_TBOX)
    g.bind("owl", OWL)
    g.bind("rdfs", RDFS)
    g.bind("skos", SKOS)

    # 1. Classes TBox + Couche Lexicale SKOS
    classes_data = [
        ("Asset", "Actif", "Asset", "Ressource SI", "Ressource informatique du SI (serveur, poste, équipement réseau)."),
        ("SoftwareComponent", "Composant Logiciel", "Software Component", "Paquet applicatif", "Composant logiciel, bibliothèque ou dépendance système."),
        ("Vulnerability", "Vulnérabilité", "Vulnerability", "Faille de sécurité", "Faiblesse logicielle exploitable répertoriée (CVE)."),
        ("Weakness", "Faiblesse", "Weakness", "Type d'erreur logicielle", "Famille d'erreur logicielle sous-jacente (CWE)."),
        ("ThreatPattern", "Schéma de Menace", "Threat Pattern", "Mode opératoire d'attaque", "Motif ou schéma d'attaque documenté (CAPEC)."),
        ("TLPMarking", "Marquage TLP", "TLP Marking", "Niveau de confidentialité", "Niveau de classification et de partage de l'information.")
    ]

    for cls_name, pref_fr, pref_en, alt_fr, def_fr in classes_data:
        cls_uri = DKG_TBOX[cls_name]
        g.add((cls_uri, RDF.type, OWL.Class))
        g.add((cls_uri, RDFS.label, Literal(cls_name, lang="fr")))
        # Annotations SKOS
        g.add((cls_uri, SKOS.prefLabel, Literal(pref_fr, lang="fr")))
        g.add((cls_uri, SKOS.prefLabel, Literal(pref_en, lang="en")))
        g.add((cls_uri, SKOS.altLabel, Literal(alt_fr, lang="fr")))
        g.add((cls_uri, SKOS.definition, Literal(def_fr, lang="fr")))

    # 2. Propriétés Objet (ObjectProperties) & SKOS
    object_properties = [
        ("hasInstalledComponent", "Asset", "SoftwareComponent", "isComponentOf", "a pour composant", "has installed component", "Associe un composant logiciel à un actif SI"),
        ("isComponentOf", "SoftwareComponent", "Asset", "hasInstalledComponent", "est composant de", "is component of", "Associe un actif SI au composant installé"),
        ("hasVulnerability", "SoftwareComponent", "Vulnerability", "isVulnerabilityOf", "a pour vulnérabilité", "has vulnerability", "Lie un composant à une vulnérabilité connue"),
        ("isVulnerabilityOf", "Vulnerability", "SoftwareComponent", "hasVulnerability", "impacte le composant", "is vulnerability of", "Lie une vulnérabilité au composant impacté"),
        ("hasWeakness", "Vulnerability", "Weakness", None, "est de type faiblesse", "has weakness", "Associe une vulnérabilité à un type d'erreur CWE"),
        ("hasTLPMarking", "Thing", "TLPMarking", None, "a pour marquage TLP", "has TLP marking", "Applique une classification TLP sur l'entité")
    ]

    for prop_name, domain, range_cls, inverse_name, pref_fr, pref_en, comment in object_properties:
        prop_uri = DKG_TBOX[prop_name]
        g.add((prop_uri, RDF.type, OWL.ObjectProperty))
        dom_uri = OWL.Thing if domain == "Thing" else DKG_TBOX[domain]
        rng_uri = DKG_TBOX[range_cls]
        g.add((prop_uri, RDFS.domain, dom_uri))
        g.add((prop_uri, RDFS.range, rng_uri))
        g.add((prop_uri, RDFS.comment, Literal(comment, lang="fr")))
        # Annotations SKOS
        g.add((prop_uri, SKOS.prefLabel, Literal(pref_fr, lang="fr")))
        g.add((prop_uri, SKOS.prefLabel, Literal(pref_en, lang="en")))
        if inverse_name:
            g.add((prop_uri, OWL.inverseOf, DKG_TBOX[inverse_name]))

    # 3. Propriétés de Données (DatatypeProperties)
    datatype_properties = [
        ("assetId", "Asset", XSD.string, "identifiant d'actif", "asset identifier"),
        ("hostname", "Asset", XSD.string, "nom d'hôte", "hostname"),
        ("componentId", "SoftwareComponent", XSD.string, "identifiant de composant", "component identifier"),
        ("cveId", "Vulnerability", XSD.string, "identifiant CVE", "CVE identifier"),
        ("cvssScore", "Vulnerability", XSD.float, "score CVSS", "CVSS score"),
        ("cweId", "Weakness", XSD.string, "identifiant CWE", "CWE identifier")
    ]

    for prop_name, domain, range_dt, pref_fr, pref_en in datatype_properties:
        prop_uri = DKG_TBOX[prop_name]
        g.add((prop_uri, RDF.type, OWL.DatatypeProperty))
        g.add((prop_uri, RDFS.domain, DKG_TBOX[domain]))
        g.add((prop_uri, RDFS.range, range_dt))
        g.add((prop_uri, SKOS.prefLabel, Literal(pref_fr, lang="fr")))
        g.add((prop_uri, SKOS.prefLabel, Literal(pref_en, lang="en")))

    return g

def build_shacl_graph() -> Graph:
    g = Graph()
    g.bind("dkg", DKG_TBOX)
    g.bind("sh", SH)

    asset_shape = DKG_TBOX["AssetShape"]
    g.add((asset_shape, RDF.type, SH.NodeShape))
    g.add((asset_shape, SH.targetClass, DKG_TBOX["Asset"]))
    
    vuln_shape = DKG_TBOX["VulnerabilityShape"]
    g.add((vuln_shape, RDF.type, SH.NodeShape))
    g.add((vuln_shape, SH.targetClass, DKG_TBOX["Vulnerability"]))
    
    prop_cvss = BNode()
    g.add((vuln_shape, SH.property, prop_cvss))
    g.add((prop_cvss, SH.path, DKG_TBOX["cvssScore"]))
    g.add((prop_cvss, SH.datatype, XSD.float))
    g.add((prop_cvss, SH.maxInclusive, Literal(10.0, datatype=XSD.float)))

    return g

def generate_markdown_doc(target_path: Path):
    lines = [
        "# 📚 Documentation du Socle Ontologique TBox / RBox / SKOS",
        "",
        "> **Spécification** : Conforme SPEC-01  ",
        "> **Classification** : `TLP:AMBER`  ",
        "> **Domaine** : CyberSécurité & DKG",
        "",
        "---",
        "",
        "## 📖 1. Glossaire des Acronymes",
        "* **TBox** : Terminological Box (Structure logique, classes et hiérarchies)",
        "* **RBox** : Role Box (Propriétés, relations et leurs axiomes)",
        "* **ABox** : Assertional Box (Données factuelles et instances)",
        "* **OWL** : Web Ontology Language (Modélisation sémantique et logique)",
        "* **SKOS** : Simple Knowledge Organization System (Gestion lexicale et multilingue)",
        "* **SHACL** : Shapes Constraint Language (Validation de données ABox)",
        "* **TLP** : Traffic Light Protocol",
        "",
        "---",
        "",
        "## 📊 2. Représentation Graphique du Schéma (Mermaid.js)",
        "```mermaid",
        "classDiagram",
        "    class Asset {",
        "        +string assetId",
        "        +string hostname",
        "    }",
        "    class SoftwareComponent {",
        "        +string componentId",
        "        +string name",
        "    }",
        "    class Vulnerability {",
        "        +string cveId",
        "        +float cvssScore",
        "    }",
        "    class Weakness {",
        "        +string cweId",
        "    }",
        "    class ThreatPattern {",
        "        +string capecId",
        "    }",
        "    class TLPMarking {",
        "        +string color",
        "    }",
        "",
        "    Asset \"1\" --> \"*\" SoftwareComponent : hasInstalledComponent",
        "    SoftwareComponent \"1\" --> \"*\" Vulnerability : hasVulnerability",
        "    Vulnerability \"*\" --> \"*\" Weakness : hasWeakness",
        "    Asset \"*\" --> \"1\" TLPMarking : hasTLPMarking",
        "```",
        "",
        "---",
        "",
        "## 🏷️ 3. Dictionnaire des Classes (OWL & SKOS)",
        "",
        "| Classe | Label FR (`skos:prefLabel`) | Label EN | Synonyme (`skos:altLabel`) | Définition (`skos:definition`) |",
        "| :--- | :--- | :--- | :--- | :--- |",
        "| `Asset` | Actif | Asset | Ressource SI | Ressource informatique du SI (serveur, poste, réseau). |",
        "| `SoftwareComponent` | Composant Logiciel | Software Component | Paquet applicatif | Composant logiciel, bibliothèque ou dépendance système. |",
        "| `Vulnerability` | Vulnérabilité | Vulnerability | Faille de sécurité | Faiblesse logicielle exploitable répertoriée (CVE). |",
        "| `Weakness` | Faiblesse | Weakness | Type d'erreur logicielle | Famille d'erreur logicielle sous-jacente (CWE). |",
        "| `ThreatPattern` | Schéma de Menace | Threat Pattern | Mode opératoire d'attaque | Motif ou schéma d'attaque documenté (CAPEC). |",
        "| `TLPMarking` | Marquage TLP | TLP Marking | Niveau de confidentialité | Niveau de classification et de partage de l'information. |",
        "",
        "---",
        "",
        "## 🔗 4. Propriétés d'Objets (Object Properties & RBox)",
        "",
        "| Propriété | Domaine | Portée (Range) | Inverse | Label FR | Description |",
        "| :--- | :--- | :--- | :--- | :--- | :--- |",
        "| `hasInstalledComponent` | `Asset` | `SoftwareComponent` | `isComponentOf` | a pour composant | Lie un actif aux logiciels installés |",
        "| `isComponentOf` | `SoftwareComponent` | `Asset` | `hasInstalledComponent` | est composant de | Lie un composant à l'actif hôte |",
        "| `hasVulnerability` | `SoftwareComponent` | `Vulnerability` | `isVulnerabilityOf` | a pour vulnérabilité | Associe un composant à ses vulnérabilités |",
        "| `isVulnerabilityOf` | `Vulnerability` | `SoftwareComponent` | `hasVulnerability` | impacte le composant | Associe une CVE au composant impacté |",
        "| `hasWeakness` | `Vulnerability` | `Weakness` | N/A | est de type faiblesse | Cartographie une CVE vers sa catégorie CWE |",
        "| `hasTLPMarking` | `owl:Thing` | `TLPMarking` | N/A | a pour marquage TLP | Restreint la visibilité TLP d'un élément |",
        "",
        "---",
        "",
        "## 🔢 5. Propriétés de Données (Datatype Properties)",
        "",
        "| Propriété | Domaine | Type (Datatype) | Label FR | Label EN |",
        "| :--- | :--- | :--- | :--- | :--- |",
        "| `assetId` | `Asset` | `xsd:string` | identifiant d'actif | asset identifier |",
        "| `hostname` | `Asset` | `xsd:string` | nom d'hôte | hostname |",
        "| `componentId` | `SoftwareComponent` | `xsd:string` | identifiant de composant | component identifier |",
        "| `cveId` | `Vulnerability` | `xsd:string` | identifiant CVE | CVE identifier |",
        "| `cvssScore` | `Vulnerability` | `xsd:float` | score CVSS | CVSS score |",
        "| `cweId` | `Weakness` | `xsd:string` | identifiant CWE | CWE identifier |",
        ""
    ]
    with open(target_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

def main():
    print("Initialisation de la génération Phase 1 (avec SKOS)...")
    
    MASTER_DIR.mkdir(parents=True, exist_ok=True)
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)

    tbox_g = build_tbox_graph()
    tbox_ttl = MASTER_DIR / "DKG_TBox_Master.ttl"
    tbox_json = MASTER_DIR / "DKG_TBox_Master.json"
    tbox_g.serialize(destination=str(tbox_ttl), format="turtle")
    tbox_g.serialize(destination=str(tbox_json), format="json-ld")

    shacl_g = build_shacl_graph()
    shacl_ttl = MASTER_DIR / "shapes_abox.ttl"
    shacl_g.serialize(destination=str(shacl_ttl), format="turtle")

    md_file = MASTER_DIR / "DKG_TBox_Master.md"
    generate_markdown_doc(md_file)

    syn_g = Graph()
    syn_g.bind("dkg", DKG_TBOX)
    syn_g.bind("data", DKG_DATA)
    syn_g.add((DKG_DATA["asset-01"], RDF.type, DKG_TBOX["Asset"]))
    syn_g.serialize(destination=str(MASTER_DIR / "synthetic_qualification.ttl"), format="turtle")

    for file in MASTER_DIR.glob("*.*"):
        shutil.copy(file, SNAPSHOT_DIR / file.name)
        
    print(f"Génération réussie dans : {MASTER_DIR}")
    print(f"Snapshot synchronisé dans : {SNAPSHOT_DIR}")

if __name__ == "__main__":
    main()
