from pathlib import Path
from rdflib import Graph

def validate_tbox():
    graph = Graph()
    graph.parse("12-Donnees/VAULT_CONSOLIDE.ttl", format="turtle")
    classes = list(graph.subjects(RDF.type, OWL.Class))
    print(f"✅ {len(classes)} classes OWL trouvées")

if __name__ == "__main__":
    validate_tbox()
