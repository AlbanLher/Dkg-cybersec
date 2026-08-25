from pathlib import Path
from rdflib import Graph, Namespace, RDF, OWL
from rdflib.namespace import SKOS

EX = Namespace("http://example.org/cyber-ontology#")

def validate_tbox():
    graph = Graph()
    graph.parse("12-Donnees/VAULT_CONSOLIDE.ttl", format="turtle")
    
    classes = list(graph.subjects(RDF.type, OWL.Class))
    concepts = list(graph.subjects(RDF.type, SKOS.Concept))
    
    print(f"✅ Validation TBox:")
    print(f"   - {len(classes)} classes OWL")
    print(f"   - {len(concepts)} concepts SKOS")

if __name__ == "__main__":
    validate_tbox()
