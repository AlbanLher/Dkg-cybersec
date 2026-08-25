import re
from pathlib import Path
from rdflib import Graph, SKOS, OWL, RDFS

def check_inputs_to_vault_coverage(root_dir: Path, vault_graph: Graph) -> dict:
    """Vérifie que 100% des concepts/classes d'entrée sont représentés dans le Vault."""
    dir_lexique = root_dir / "1-Lexique"
    
    # 1. Recensement des concepts sources MD
    source_terms = set()
    for md_file in dir_lexique.rglob("*.md"):
        content = md_file.read_text(encoding="utf-8")
        headers = re.findall(r'^#{1,6}\s+(.+)$', content, flags=re.MULTILINE)
        for h in headers:
            source_terms.add(h.strip().lower())
            
    # 2. Recensement des concepts présent dans le Vault
    vault_concepts = set()
    for _, _, label in vault_graph.triples((None, SKOS.prefLabel, None)):
        vault_concepts.add(str(label.value).lower())

    # 3. Calcul de couverture
    missing_terms = source_terms - vault_concepts
    coverage_rate = ((len(source_terms) - len(missing_terms)) / len(source_terms) * 100) if source_terms else 100.0

    report = {
        "source_count": len(source_terms),
        "vault_count": len(vault_concepts),
        "missing_count": len(missing_terms),
        "missing_terms": list(missing_terms),
        "coverage_rate": round(coverage_rate, 2)
    }
    return report
