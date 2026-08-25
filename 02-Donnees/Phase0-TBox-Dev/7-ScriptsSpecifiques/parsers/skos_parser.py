import re
from pathlib import Path
from rdflib import Graph, Literal, Namespace, SKOS, RDF

EX = Namespace("http://example.org/dkg/ontology#")

def parse_markdown_lexicons(lexique_dir: Path, graph: Graph) -> Graph:
    """Ingère les définitions des lexiques Markdown et les convertit en SKOS."""
    md_files = list(lexique_dir.rglob("*.md"))
    for md_file in md_files:
        content = md_file.read_text(encoding="utf-8")
        blocks = re.split(r'\n(?=#{1,6}\s+)', content)
        
        for block in blocks:
            lines = [l.strip() for l in block.split('\n') if l.strip()]
            if not lines or not lines[0].startswith('#'):
                continue
            
            term_label = re.sub(r'^#{1,6}\s+', '', lines[0]).strip()
            term_id = re.sub(r'[^a-zA-Z0-9_]', '_', term_label)
            concept_uri = EX[f"Concept_{term_id}"]
            
            graph.add((concept_uri, RDF.type, SKOS.Concept))
            graph.add((concept_uri, SKOS.prefLabel, Literal(term_label, lang="fr")))
            
            for line in lines[1:]:
                if re.search(r'(synonyme|altlabel)', line, re.IGNORECASE):
                    syn_text = re.sub(r'^[*|-]\s*', '', line)
                    syn_text = re.sub(r'^\*\*(Synonymes?|skos:altLabel)\*\*\s*:\s*', '', syn_text, flags=re.IGNORECASE)
                    for syn in syn_text.split(','):
                        if syn.strip():
                            graph.add((concept_uri, SKOS.altLabel, Literal(syn.strip(), lang="fr")))
                elif "définition" in line.lower() or line.startswith("- "):
                    cleaned = re.sub(r'^[*|-]\s*', '', line)
                    cleaned = re.sub(r'^\*\*Définition\*\*\s*:\s*', '', cleaned, flags=re.IGNORECASE)
                    if cleaned.strip():
                        graph.add((concept_uri, SKOS.definition, Literal(cleaned.strip(), lang="fr")))
    return graph
