from pathlib import Path
from rdflib import Graph
import json

def generate_versions():
    # Charger TBox
    graph = Graph()
    graph.parse("12-Donnees/VAULT_CONSOLIDE.ttl", format="turtle")
    
    # Générer .json
    data = {"concepts": [], "classes": []}
    for s, p, o in graph:
        data.setdefault(str(s), {})[str(p)] = str(o)
    
    Path("12-Donnees").mkdir(exist_ok=True)
    with open("12-Donnees/VAULT_CONSOLIDE.json", "w") as f:
        json.dump(data, f, indent=2)
    
    print("✅ Versions générées: .ttl, .json")

if __name__ == "__main__":
    generate_versions()
