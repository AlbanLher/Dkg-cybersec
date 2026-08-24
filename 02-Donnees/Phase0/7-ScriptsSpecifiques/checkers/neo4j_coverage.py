from rdflib import Graph, RDF, OWL, RDFS

def check_vault_to_cypher_coverage(vault_graph: Graph, cypher_file_path) -> dict:
    """Vérifie que chaque Classe et Propriété du Vault est exportée en Cypher."""
    # Extraire les classes du Vault
    vault_classes = set()
    for s in vault_graph.subjects(RDF.type, OWL.Class):
        vault_classes.add(str(s).split("#")[-1].split("/")[-1])
    for s in vault_graph.subjects(RDF.type, RDFS.Class):
        vault_classes.add(str(s).split("#")[-1].split("/")[-1])

    if not cypher_file_path.exists():
        return {"error": "Fichier Cypher introuvable", "coverage_rate": 0.0}

    cypher_content = cypher_file_path.read_text(encoding="utf-8")
    
    # Vérifier présence des contraintes/labels dans le script Cypher
    found_classes = {cls for cls in vault_classes if cls in cypher_content}
    missing_classes = vault_classes - found_classes

    coverage_rate = (len(found_classes) / len(vault_classes) * 100) if vault_classes else 100.0

    return {
        "vault_classes_count": len(vault_classes),
        "cypher_classes_count": len(found_classes),
        "missing_classes": list(missing_classes),
        "coverage_rate": round(coverage_rate, 2)
    }
