import os
import sys
import shutil
from pathlib import Path
from rdflib import Graph, Literal

# 1. Résolution de la racine applicative et import SSOT (EXG-OR-05)
DIR_APP = Path(__file__).resolve().parent.parent
if str(DIR_APP) not in sys.path:
    sys.path.insert(0, str(DIR_APP))

# Import exclusif des constantes validées à l'étape A
from config import (
    DIR_SNAPSHOT_P1,
    DIR_MASTER_TBOX,
    TBOX_MASTER_PATH,
    SHACL_MASTER_PATH,
    DKG_TBOX,
    DKG_DATA,
    RDF,
    RDFS,
    OWL,
    SKOS,
    SH,
    XSD
)

# 2. Import des modèles Pydantic V2 (EXG-OR-07)
from Phase1.schemas import (
    OWLClassSchema,
    OWLObjectPropertySchema,
    OWLDatatypePropertySchema,
    SHACLCvssConstraintSchema
)


def get_validated_classes() -> list[OWLClassSchema]:
    raw_classes = [
        {"name": "Asset", "pref_label_fr": "Actif", "pref_label_en": "Asset", "alt_label_fr": "Ressource SI", "definition_fr": "Ressource informatique du SI (serveur, poste, équipement réseau)."},
        {"name": "SoftwareComponent", "pref_label_fr": "Composant Logiciel", "pref_label_en": "Software Component", "alt_label_fr": "Paquet applicatif", "definition_fr": "Composant logiciel, bibliothèque ou dépendance système."},
        {"name": "Vulnerability", "pref_label_fr": "Vulnérabilité", "pref_label_en": "Vulnerability", "alt_label_fr": "Faille de sécurité", "definition_fr": "Faiblesse logicielle exploitable répertoriée (CVE)."},
        {"name": "Weakness", "pref_label_fr": "Faiblesse", "pref_label_en": "Weakness", "alt_label_fr": "Type d'erreur logicielle", "definition_fr": "Famille d'erreur logicielle sous-jacente (CWE)."},
        {"name": "ThreatPattern", "pref_label_fr": "Schéma de Menace", "pref_label_en": "Threat Pattern", "alt_label_fr": "Mode opératoire d'attaque", "definition_fr": "Motif ou schéma d'attaque documenté (CAPEC)."},
        {"name": "TLPMarking", "pref_label_fr": "Marquage TLP", "pref_label_en": "TLP Marking", "alt_label_fr": "Niveau de confidentialité", "definition_fr": "Niveau de classification et de partage de l'information."}
    ]
    return [OWLClassSchema.model_validate(c) for c in raw_classes]


def get_validated_object_properties() -> list[OWLObjectPropertySchema]:
    raw_props = [
        {"name": "hasInstalledComponent", "domain": "Asset", "range_cls": "SoftwareComponent", "inverse_name": "isComponentOf", "pref_label_fr": "a pour composant", "pref_label_en": "has installed component", "comment_fr": "Associe un composant logiciel à un actif SI"},
        {"name": "isComponentOf", "domain": "SoftwareComponent", "range_cls": "Asset", "inverse_name": "hasInstalledComponent", "pref_label_fr": "est composant de", "pref_label_en": "is component of", "comment_fr": "Associe un actif SI au composant installé"},
        {"name": "hasVulnerability", "domain": "SoftwareComponent", "range_cls": "Vulnerability", "inverse_name": "isVulnerabilityOf", "pref_label_fr": "a pour vulnérabilité", "pref_label_en": "has vulnerability", "comment_fr": "Lie un composant à une vulnérabilité connue"},
        {"name": "isVulnerabilityOf", "domain": "Vulnerability", "range_cls": "SoftwareComponent", "inverse_name": "hasVulnerability", "pref_label_fr": "impacte le composant", "pref_label_en": "is vulnerability of", "comment_fr": "Lie une vulnérabilité au composant impacté"},
        {"name": "hasWeakness", "domain": "Vulnerability", "range_cls": "Weakness", "inverse_name": None, "pref_label_fr": "est de type faiblesse", "pref_label_en": "has weakness", "comment_fr": "Associe une vulnérabilité à un type d'erreur CWE"},
        {"name": "hasTLPMarking", "domain": "Thing", "range_cls": "TLPMarking", "inverse_name": None, "pref_label_fr": "a pour marquage TLP", "pref_label_en": "has TLP marking", "comment_fr": "Applique une classification TLP sur l'entité"}
    ]
    return [OWLObjectPropertySchema.model_validate(p) for p in raw_props]


def get_validated_datatype_properties() -> list[OWLDatatypePropertySchema]:
    raw_dt_props = [
        {"name": "assetId", "domain": "Asset", "datatype": XSD.string, "pref_label_fr": "identifiant d'actif", "pref_label_en": "asset identifier"},
        {"name": "hostname", "domain": "Asset", "datatype": XSD.string, "pref_label_fr": "nom d'hôte", "pref_label_en": "hostname"},
        {"name": "componentId", "domain": "SoftwareComponent", "datatype": XSD.string, "pref_label_fr": "identifiant de composant", "pref_label_en": "component identifier"},
        {"name": "cveId", "domain": "Vulnerability", "datatype": XSD.string, "pref_label_fr": "identifiant CVE", "pref_label_en": "CVE identifier"},
        {"name": "cvssScore", "domain": "Vulnerability", "datatype": XSD.float, "pref_label_fr": "score CVSS", "pref_label_en": "CVSS score"},
        {"name": "cweId", "domain": "Weakness", "datatype": XSD.string, "pref_label_fr": "identifiant CWE", "pref_label_en": "CWE identifier"}
    ]
    return [OWLDatatypePropertySchema.model_validate(dp) for dp in raw_dt_props]


def build_tbox_graph() -> Graph:
    g = Graph()
    g.bind("dkg", DKG_TBOX)
    g.bind("owl", OWL)
    g.bind("rdfs", RDFS)
    g.bind("skos", SKOS)

    classes = get_validated_classes()
    object_properties = get_validated_object_properties()
    datatype_properties = get_validated_datatype_properties()

    # EXG-TB-02 & EXG-TB-05
    for cls in classes:
        cls_uri = DKG_TBOX[cls.name]
        g.add((cls_uri, RDF.type, OWL.Class))
        g.add((cls_uri, RDFS.label, Literal(cls.name, lang="fr")))
        g.add((cls_uri, SKOS.prefLabel, Literal(cls.pref_label_fr, lang="fr")))
        g.add((cls_uri, SKOS.prefLabel, Literal(cls.pref_label_en, lang="en")))
        g.add((cls_uri, SKOS.altLabel, Literal(cls.alt_label_fr, lang="fr")))
        g.add((cls_uri, SKOS.definition, Literal(cls.definition_fr, lang="fr")))

    # EXG-TB-03 & EXG-TB-04
    for prop in object_properties:
        prop_uri = DKG_TBOX[prop.name]
        g.add((prop_uri, RDF.type, OWL.ObjectProperty))
        dom_uri = OWL.Thing if prop.domain == "Thing" else DKG_TBOX[prop.domain]
        rng_uri = DKG_TBOX[prop.range_cls]
        g.add((prop_uri, RDFS.domain, dom_uri))
        g.add((prop_uri, RDFS.range, rng_uri))
        g.add((prop_uri, RDFS.comment, Literal(prop.comment_fr, lang="fr")))
        g.add((prop_uri, SKOS.prefLabel, Literal(prop.pref_label_fr, lang="fr")))
        g.add((prop_uri, SKOS.prefLabel, Literal(prop.pref_label_en, lang="en")))
        if prop.inverse_name:
            g.add((prop_uri, OWL.inverseOf, DKG_TBOX[prop.inverse_name]))

    for dt_prop in datatype_properties:
        prop_uri = DKG_TBOX[dt_prop.name]
        g.add((prop_uri, RDF.type, OWL.DatatypeProperty))
        g.add((prop_uri, RDFS.domain, DKG_TBOX[dt_prop.domain]))
        g.add((prop_uri, RDFS.range, dt_prop.datatype))
        g.add((prop_uri, SKOS.prefLabel, Literal(dt_prop.pref_label_fr, lang="fr")))
        g.add((prop_uri, SKOS.prefLabel, Literal(dt_prop.pref_label_en, lang="en")))

    return g


def build_shacl_graph() -> Graph:
    g = Graph()
    g.bind("dkg", DKG_TBOX)
    g.bind("sh", SH)

    shacl_schema = SHACLCvssConstraintSchema.model_validate({"datatype": XSD.float})

    # EXG-QU-01 : Shapes couvrantes associées aux classes
    asset_shape = DKG_TBOX["AssetShape"]
    g.add((asset_shape, RDF.type, SH.NodeShape))
    g.add((asset_shape, SH.targetClass, DKG_TBOX["Asset"]))
    
    comp_shape = DKG_TBOX["SoftwareComponentShape"]
    g.add((comp_shape, RDF.type, SH.NodeShape))
    g.add((comp_shape, SH.targetClass, DKG_TBOX["SoftwareComponent"]))

    vuln_shape = DKG_TBOX["VulnerabilityShape"]
    g.add((vuln_shape, RDF.type, SH.NodeShape))
    g.add((vuln_shape, SH.targetClass, DKG_TBOX[shacl_schema.target_class]))
    
    # EXG-SH-01 : Node Shape explicitement nommée
    prop_cvss_shape = DKG_TBOX["CvssScorePropertyShape"]
    g.add((vuln_shape, SH.property, prop_cvss_shape))
    g.add((prop_cvss_shape, RDF.type, SH.PropertyShape))
    g.add((prop_cvss_shape, SH.path, DKG_TBOX[shacl_schema.path_property]))
    g.add((prop_cvss_shape, SH.datatype, shacl_schema.datatype))
    g.add((prop_cvss_shape, SH.maxInclusive, Literal(shacl_schema.max_inclusive, datatype=shacl_schema.datatype)))

    return g


def generate_markdown_doc(target_path: Path):
    lines = [
        "# 📚 Documentation du Socle Ontologique (Phase 1)",
        "",
        "> **Classification** : `TLP:AMBER` | **Domaine** : CyberSécurité & DKG",
        "",
        "---",
        "",
        "## 📖 1. Glossaire des Acronymes",
        "",
        "| Acronyme | Définition | Contextualisation |",
        "| :--- | :--- | :--- |",
        "| **TBox** | Terminological Box | Structure des classes et axiomes ontologiques |",
        "| **RBox** | Role Box | Propriétés, rôles et axiomes d'inversion |",
        "| **SKOS** | Simple Knowledge Organization System | Représentation lexicale et bilinguisme |",
        "| **SHACL** | Shapes Constraint Language | Validation de contraintes de qualité sous CWA |",
        "| **TLP** | Traffic Light Protocol | Protocole de partage de l'information |",
        "",
        "---",
        "",
        "## 📐 2. Architecture Graphique du Socle (Mermaid)",
        "",
        "```mermaid",
        "classDiagram",
        "    class Asset {",
        "        +string assetId",
        "        +string hostname",
        "    }",
        "    class SoftwareComponent {",
        "        +string componentId",
        "    }",
        "    class Vulnerability {",
        "        +string cveId",
        "        +float cvssScore",
        "    }",
        "    class Weakness {",
        "        +string cweId",
        "    }",
        "    class ThreatPattern",
        "    class TLPMarking",
        "",
        "    Asset \"1\" --> \"*\" SoftwareComponent : hasInstalledComponent",
        "    SoftwareComponent \"1\" --> \"1\" Asset : isComponentOf",
        "    SoftwareComponent \"1\" --> \"*\" Vulnerability : hasVulnerability",
        "    Vulnerability \"1\" --> \"*\" SoftwareComponent : isVulnerabilityOf",
        "    Vulnerability \"1\" --> \"*\" Weakness : hasWeakness",
        "    owl_Thing --> \"1\" TLPMarking : hasTLPMarking",
        "```",
        "",
        "---",
        "",
        "## 🏷️ 3. Résumé Synthétique des Classes TBox",
        "",
        "| Classe | Label FR (`skos:prefLabel`) | Label EN | Définition (`skos:definition`) |",
        "| :--- | :--- | :--- | :--- |",
        "| `Asset` | Actif | Asset | Ressource informatique du SI (serveur, poste, équipement réseau). |",
        "| `SoftwareComponent` | Composant Logiciel | Software Component | Composant logiciel, bibliothèque ou dépendance système. |",
        "| `Vulnerability` | Vulnérabilité | Vulnerability | Faiblesse logicielle exploitable répertoriée (CVE). |",
        "| `Weakness` | Faiblesse | Weakness | Famille d'erreur logicielle sous-jacente (CWE). |",
        "| `ThreatPattern` | Schéma de Menace | Threat Pattern | Motif ou schéma d'attaque documenté (CAPEC). |",
        "| `TLPMarking` | Marquage TLP | TLP Marking | Niveau de classification et de partage de l'information. |",
        "",
        "---",
        "",
        "## 🔗 4. Rôles et Inverses RBox",
        "",
        "| Propriété | Domaine | Portée | Inverse (`owl:inverseOf`) | Libellé FR |",
        "| :--- | :--- | :--- | :--- | :--- |",
        "| `hasInstalledComponent` | `Asset` | `SoftwareComponent` | `isComponentOf` | a pour composant |",
        "| `isComponentOf` | `SoftwareComponent` | `Asset` | `hasInstalledComponent` | est composant de |",
        "| `hasVulnerability` | `SoftwareComponent` | `Vulnerability` | `isVulnerabilityOf` | a pour vulnérabilité |",
        "| `isVulnerabilityOf` | `Vulnerability` | `SoftwareComponent` | `hasVulnerability` | impacte le composant |",
        "| `hasWeakness` | `Vulnerability` | `Weakness` | N/A | est de type faiblesse |",
        "| `hasTLPMarking` | `owl:Thing` | `TLPMarking` | N/A | a pour marquage TLP |",
        "",
        "---",
        "",
        "## 🛡️ 5. Validation SHACL (Contraintes de Surface)",
        "",
        "| Shape Cible | Propriété contrôlée | Datatype | Contrainte CWA |",
        "| :--- | :--- | :--- | :--- |",
        "| `dkg:VulnerabilityShape` | `dkg:cvssScore` | `xsd:float` | `sh:maxInclusive 10.0` |",
        ""
    ]
    with open(target_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    print("Exécution Phase 1 : Replay -> Safe Sync Master...")
    
    DIR_SNAPSHOT_P1.mkdir(parents=True, exist_ok=True)
    DIR_MASTER_TBOX.mkdir(parents=True, exist_ok=True)

    # Dérivation dynamique des noms d'artefacts via les constantes Path de config.py (EXG-OR-05)
    tbox_snapshot_ttl = DIR_SNAPSHOT_P1 / TBOX_MASTER_PATH.name
    tbox_snapshot_json = DIR_SNAPSHOT_P1 / TBOX_MASTER_PATH.with_suffix(".json").name
    tbox_snapshot_md = DIR_SNAPSHOT_P1 / TBOX_MASTER_PATH.with_suffix(".md").name
    shacl_snapshot_ttl = DIR_SNAPSHOT_P1 / SHACL_MASTER_PATH.name
    synthetic_snapshot_ttl = DIR_SNAPSHOT_P1 / "synthetic_qualification.ttl"

    # 1. Écriture initiale dans Snapshot (Principe de Replay)
    tbox_g = build_tbox_graph()
    tbox_g.serialize(destination=str(tbox_snapshot_ttl), format="turtle")
    tbox_g.serialize(destination=str(tbox_snapshot_json), format="json-ld")

    shacl_g = build_shacl_graph()
    shacl_g.serialize(destination=str(shacl_snapshot_ttl), format="turtle")

    generate_markdown_doc(tbox_snapshot_md)

    syn_g = Graph()
    syn_g.bind("dkg", DKG_TBOX)
    syn_g.bind("data", DKG_DATA)
    syn_g.add((DKG_DATA["asset-01"], RDF.type, DKG_TBOX["Asset"]))
    syn_g.serialize(destination=str(synthetic_snapshot_ttl), format="turtle")

    # 2. Synchronisation sécurisée vers Master_Transversal (EXG-OR-06)
    for file in DIR_SNAPSHOT_P1.glob("*.*"):
        shutil.copy(file, DIR_MASTER_TBOX / file.name)
        
    print(f"✅ Génération Snapshot validée : {DIR_SNAPSHOT_P1}")
    print(f"✅ Safe Sync Master effectuée   : {DIR_MASTER_TBOX}")


if __name__ == "__main__":
    main()
