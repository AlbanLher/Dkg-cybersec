from pathlib import Path
from rdflib import Graph, Namespace, RDF, OWL
from rdflib.namespace import SKOS

EX = Namespace("http://example.org/cyber-ontology#")

def build_tbox():
    graph = Graph()
    graph.bind("ex", EX)
    graph.bind("owl", OWL)
    graph.bind("rdf", RDF)
    
    # Charger CVE
    graph.parse("12-Donnees/1-Sources/2-Externes/cve_data.ttl", format="turtle")
    
    # Sauvegarder
    Path("12-Donnees").mkdir(exist_ok=True)
    graph.serialize("12-Donnees/VAULT_CONSOLIDE.ttl", format="turtle")
    print("✅ TBox générée dans 12-Donnees/VAULT_CONSOLIDE.ttl")

if __name__ == "__main__":
    build_tbox()
