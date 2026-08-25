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

    # Charger CVE
    graph.parse("12-Donnees/1-Sources/2-Externes/cve_data.ttl", format="turtle")

    # Charger inventory.json (avec vérification)
    inventory_path = Path("12-Donnees/1-Sources/1-Internes/inventory.json")
    if not inventory_path.exists():
        print(f"❌ Fichier introuvable: {inventory_path}")
        return

    try:
        with open(inventory_path, "r") as f:
            inventory = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Erreur JSON dans {inventory_path}: {e}")
        return

    # Créer le ConceptScheme
    scheme = EX_L.InternalLexicon
    graph.add((scheme, RDF.type, SKOS.ConceptScheme))
    graph.add((scheme, SKOS.prefLabel, Literal("Lexique Interne DKG")))

    # Ajouter les devices
    for device in inventory.get("devices", []):
        device_uri = EX_O[device["id"]]
        device_type = EX_O[device["type"]]

        graph.add((device_type, RDF.type, OWL.Class))
        graph.add((device_type, RDFS.label, Literal(device["type"])))

        graph.add((device_uri, RDF.type, device_type))
        graph.add((device_uri, RDFS.label, Literal(device["id"])))
        if "ip" in device:
            graph.add((device_uri, EX_O.hasIP, Literal(device["ip"])))

        concept_uri = EX_L[device["type"]]
        graph.add((concept_uri, RDF.type, SKOS.Concept))
        graph.add((concept_uri, SKOS.inScheme, scheme))
        graph.add((concept_uri, SKOS.prefLabel, Literal(device["type"])))
        graph.add((concept_uri, SKOS.exactMatch, device_type))

        for sw in device.get("software", []):
            sw_uri = EX_O[f"{sw['name']}_{sw['version'].replace('.', '_')}"]
            sw_type = EX_O[sw["name"]]

            graph.add((sw_type, RDF.type, OWL.Class))
            graph.add((sw_type, RDFS.label, Literal(sw["name"])))

            graph.add((sw_uri, RDF.type, sw_type))
            graph.add((sw_uri, RDFS.label, Literal(f"{sw['name']} {sw['version']}")))
            graph.add((device_uri, EX_O.hasSoftware, sw_uri))

            sw_concept = EX_L[sw["name"]]
            graph.add((sw_concept, RDF.type, SKOS.Concept))
            graph.add((sw_concept, SKOS.inScheme, scheme))
            graph.add((sw_concept, SKOS.prefLabel, Literal(sw["name"])))
            graph.add((sw_concept, SKOS.exactMatch, sw_type))

    output_dir = Path("12-Donnees/TBox_init")
    output_dir.mkdir(parents=True, exist_ok=True)
    graph.serialize(output_dir / "VAULT_CONSOLIDE.ttl", format="turtle")
    print("✅ TBox générée")

if __name__ == "__main__":
    build_tbox()
