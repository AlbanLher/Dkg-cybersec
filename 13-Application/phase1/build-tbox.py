from pathlib import Path
from rdflib import Graph, Namespace, RDF, OWL, Literal
from rdflib.namespace import SKOS

EX = Namespace("http://example.org/cyber-ontology#")
EX_L = Namespace("http://example.org/dkg/lexique#")

def build_tbox():
    graph = Graph()
    graph.bind("ex", EX)
    graph.bind("owl", OWL)
    graph.bind("rdf", RDF)
    graph.bind("skos", SKOS)

    # Charger CVE
    graph.parse("12-Donnees/1-Sources/2-Externes/cve_data.ttl", format="turtle")

    # Ajouter des concepts SKOS pour Vulnerability
    graph.add((EX_L.Vulnerability, RDF.type, SKOS.Concept))
    graph.add((EX_L.Vulnerability, SKOS.prefLabel, Literal("Vulnérabilité", lang="fr")))
    graph.add((EX_L.Vulnerability, SKOS.exactMatch, EX.Vulnerability))

    # Sauvegarder
    Path("12-Donnees").mkdir(exist_ok=True)
    graph.serialize("12-Donnees/VAULT_CONSOLIDE.ttl", format="turtle")
    print("✅ TBox générée")

if __name__ == "__main__":
    build_tbox()
