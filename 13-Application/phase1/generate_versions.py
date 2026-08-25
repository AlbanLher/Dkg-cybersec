from pathlib import Path
from rdflib import Graph

def generate_versions():
    graph = Graph()
    graph.parse("12-Donnees/VAULT_CONSOLIDE.ttl", format="turtle")
    # Générer .md et .json (à implémenter)
    print("✅ Versions générées")

if __name__ == "__main__":
    generate_versions()
