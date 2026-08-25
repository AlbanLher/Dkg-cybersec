from pathlib import Path
from rdflib import Graph

def build_tbox():
    graph = Graph()
    # Charger inventory.json (à implémenter)
    # Charger cve_data.ttl
    graph.parse("12-Donnees/1-Sources/2-Externes/cve_data.ttl", format="turtle")
    graph.serialize("12-Donnees/VAULT_CONSOLIDE.ttl", format="turtle")
    print("✅ TBox générée")

if __name__ == "__main__":
    build_tbox()
