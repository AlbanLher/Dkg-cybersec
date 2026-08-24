from pathlib import Path
from rdflib import Graph

def parse_ttl_ontologies(onto_dir: Path, graph: Graph) -> Graph:
    """Ingère l'ensemble des ontologies et schémas TTL structurels."""
    ttl_files = list(onto_dir.rglob("*.ttl"))
    for ttl_file in ttl_files:
        if "VAULT_CONSOLIDE" not in ttl_file.name:
            try:
                graph.parse(location=str(ttl_file), format="turtle")
            except Exception as e:
                print(f"⚠️ Erreur de parsing TTL sur {ttl_file.name} : {e}")
    return graph
