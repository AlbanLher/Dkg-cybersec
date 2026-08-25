import sys
import re
from pathlib import Path
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDF, SKOS, DCTERMS

EX = Namespace("http://example.org/dkg/lexique#")

def parse_markdown_lexicon(md_path: Path) -> Graph:
    """Parse un fichier Markdown et retourne un graphe RDF/SKOS."""
    g = Graph()
    g.bind("skos", SKOS)
    g.bind("dcterms", DCTERMS)
    g.bind("ex", EX)

    content = md_path.read_text(encoding="utf-8")
    
    # Création du ConceptScheme lié au nom du fichier
    scheme_name = md_path.stem.lower()
    concept_scheme_uri = EX[f"Scheme_{scheme_name}"]
    g.add((concept_scheme_uri, RDF.type, SKOS.ConceptScheme))
    g.add((concept_scheme_uri, DCTERMS.title, Literal(f"Lexique SKOS - {md_path.stem}", lang="fr")))

    # découpage par sections ###
    blocks = re.split(r'\n(?=###?\s+)', content)
    
    for block in blocks:
        lines = [line.strip() for line in block.split('\n') if line.strip()]
        if not lines or not lines[0].startswith('#'):
            continue
            
        term_label = re.sub(r'^###?\s+', '', lines[0]).strip()
        term_id = re.sub(r'[^a-zA-Z0-9_]', '_', term_label)
        concept_uri = EX[f"Concept_{term_id}"]
        
        g.add((concept_uri, RDF.type, SKOS.Concept))
        g.add((concept_uri, SKOS.inScheme, concept_scheme_uri))
        g.add((concept_uri, SKOS.prefLabel, Literal(term_label, lang="fr")))

        for line in lines[1:]:
            if line.startswith(('* **Définition**', '- **Définition**')):
                def_text = re.sub(r'^[*|-]\s*\*\*Définition\*\*\s*:\s*', '', line)
                g.add((concept_uri, SKOS.definition, Literal(def_text, lang="fr")))
                
            elif line.startswith(('* **Synonymes', '- **Synonymes')):
                syn_text = re.sub(r'^[*|-]\s*\*\*Synonymes[^*]*\*\*\s*:\s*', '', line)
                synonyms = [s.strip() for s in syn_text.split(',')]
                for syn in synonyms:
                    if syn and syn != "N/A":
                        g.add((concept_uri, SKOS.altLabel, Literal(syn, lang="fr")))
                        
            elif line.startswith(('* **Mapping SKOS**', '- **Mapping SKOS**')):
                mapping_text = re.sub(r'^[*|-]\s*\*\*Mapping SKOS\*\*\s*:\s*', '', line)
                en_labels = re.findall(r'"([^"]+)"@en', mapping_text)
                for en_label in en_labels:
                    g.add((concept_uri, SKOS.prefLabel, Literal(en_label, lang="en")))

    return g

def main():
    if len(sys.argv) < 2:
        print("⚠️ Usage: python md_to_skos.py <chemin_fichier_ou_dossier_input>")
        print("Exemple: python md_to_skos.py 02-Donnees/LexiquesOntologie/input-interne")
        sys.exit(1)

    input_path = Path(sys.argv[1]).resolve()
    
    # Résolution automatique du dossier vault de destination
    # Recherche du dossier racine LexiquesOntologie
    base_lexique_dir = None
    for p in [input_path] + list(input_path.parents):
        if p.name == "LexiquesOntologie":
            base_lexique_dir = p
            break
            
    if not base_lexique_dir:
        # Repli : crée un dossier vault local
        vault_dir = input_path.parent / "app-referential-vault"
    else:
        vault_dir = base_lexique_dir / "app-referential-vault"

    vault_dir.mkdir(parents=True, exist_ok=True)

    # Ingestion : fichier unique ou balayage de dossier
    md_files = [input_path] if input_path.is_file() else list(input_path.rglob("*.md"))

    if not md_files:
        print("❌ Aucun fichier .md trouvé.")
        sys.exit(1)

    for md_file in md_files:
        print(f"📖 Traitement : {md_file.relative_to(base_lexique_dir if base_lexique_dir else md_file.parent)}")
        graph = parse_markdown_lexicon(md_file)
        
        # Génération du fichier TTL dans le Vault
        output_ttl = vault_dir / f"{md_file.stem.lower()}.ttl"
        graph.serialize(destination=str(output_ttl), format="turtle")
        print(f"  └─ 🎯 Vault mis à jour : {output_ttl.name}")

if __name__ == "__main__":
    main()
