from pathlib import Path
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import SKOS, OWL, RDF, RDFS
import json

EX_O = Namespace("http://example.org/cyber-ontology#")
EX_L = Namespace("http://example.org/dkg/lexique#")

def build_tbox():
    graph = Graph()
    graph.bind("ex-o", EX_O)
    graph.bind("ex-l", EX_L)
    graph.bind("owl", OWL)
    graph.bind("rdf", RDF)
    graph.bind("rdfs", RDFS)
    graph.bind("skos", SKOS)

    # 1. Charger CVE
    graph.parse("12-Donnees/1-Sources/2-Externes/cve_data.ttl", format="turtle")

    # 2. Créer les classes de base
    classes = {
        "Device": "Équipement physique ou virtuel",
        "Workstation": "Poste de travail",
        "NetworkDevice": "Équipement réseau",
        "Software": "Logiciel ou application",
        "Vulnerability": "Faiblesse exploitable dans un système"
    }

    for cls_name, definition in classes.items():
        cls_uri = EX_O[cls_name]
        graph.add((cls_uri, RDF.type, OWL.Class))
        graph.add((cls_uri, RDFS.label, Literal(cls_name, lang="fr")))
        graph.add((cls_uri, RDFS.comment, Literal(definition, lang="fr")))

    # Hiérarchie
    graph.add((EX_O.Workstation, RDFS.subClassOf, EX_O.Device))
    graph.add((EX_O.NetworkDevice, RDFS.subClassOf, EX_O.Device))

    # 3. Créer les propriétés
    properties = {
        "hasSoftware": {"domain": EX_O.Device, "range": EX_O.Software, "label": "a pour logiciel"},
        "hasIP": {"domain": EX_O.Device, "range": EX_O.IP_Address, "label": "a pour adresse IP"},
        "hasVulnerability": {"domain": EX_O.Software, "range": EX_O.Vulnerability, "label": "a pour vulnérabilité"}
    }

    for prop_name, prop_config in properties.items():
        prop_uri = EX_O[prop_name]
        graph.add((prop_uri, RDF.type, OWL.ObjectProperty))
        graph.add((prop_uri, RDFS.label, Literal(prop_config["label"], lang="fr")))
        graph.add((prop_uri, RDFS.domain, prop_config["domain"]))
        graph.add((prop_uri, RDFS.range, prop_config["range"]))

    # 4. Charger inventory.json
    with open("12-Donnees/1-Sources/1-Internes/inventory.json", "r") as f:
        inventory = json.load(f)

    # Créer le ConceptScheme
    scheme = EX_L.InternalLexicon
    graph.add((scheme, RDF.type, SKOS.ConceptScheme))
    graph.add((scheme, SKOS.prefLabel, Literal("Lexique Interne DKG")))

    # Ajouter les devices (comme instances)
    for device in inventory["devices"]:
        device_uri = EX_O[device["id"]]
        device_type = EX_O[device["type"]]

        graph.add((device_uri, RDF.type, device_type))
        graph.add((device_uri, RDFS.label, Literal(device["id"])))
        if "ip" in device:
            graph.add((device_uri, EX_O.hasIP, Literal(device["ip"])))

        for sw in device.get("software", []):
            sw_uri = EX_O[f"{sw['name']}_{sw['version'].replace('.', '_')}"]
            sw_type = EX_O[sw["name"]]

            graph.add((sw_uri, RDF.type, sw_type))
            graph.add((sw_uri, RDFS.label, Literal(f"{sw['name']} {sw['version']}")))
            graph.add((device_uri, EX_O.hasSoftware, sw_uri))

            # Lier à CVE si présent
            for cve in sw.get("cve", []):
                cve_uri = URIRef(f"https://cve.mitre.org/{cve}")
                graph.add((sw_uri, EX_O.hasVulnerability, cve_uri))

    # 5. Ajouter le lexique (concepts SKOS)
    for cls_name, definition in classes.items():
        concept_uri = EX_L[cls_name]
        graph.add((concept_uri, RDF.type, SKOS.Concept))
        graph.add((concept_uri, SKOS.inScheme, scheme))
        graph.add((concept_uri, SKOS.prefLabel, Literal(cls_name, lang="fr")))
        graph.add((concept_uri, SKOS.definition, Literal(definition, lang="fr")))
        graph.add((concept_uri, SKOS.exactMatch, EX_O[cls_name]))

    # 6. Sauvegarder
    output_dir = Path("12-Donnees/TBox_init")
    output_dir.mkdir(parents=True, exist_ok=True)
    graph.serialize(output_dir / "VAULT_CONSOLIDE.ttl", format="turtle")
    print("✅ TBox générée")

if __name__ == "__main__":
    build_tbox()
