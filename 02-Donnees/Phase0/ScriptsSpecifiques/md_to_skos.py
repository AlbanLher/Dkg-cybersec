import re
from rdflib import Graph, Namespace, Literal, RDF, RDFS, URIRef
from rdflib.namespace import SKOS, DCTERMS

def parse_md_to_skos(md_file_path: str, ttl_file_path: str):
    g = Graph()
    
    # Namespaces
    CYBER = Namespace("http://example.org/cyber-ontology#")
    LEX = Namespace("http://example.org/cyber-lexicon#")
    
    g.bind("skos", SKOS)
    g.bind("cyber", CYBER)
    g.bind("lex", LEX)

    with open(md_file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Découpage par section de concept
    sections = content.split("### ")
    
    for section in sections[1:]:  # Sauter le titre principal
        lines = section.strip().split("\n")
        header = lines[0]
        
        # Extraction de l'ID du concept et du nom
        match = re.match(r"\[(.*?)\]\s*(.*)", header)
        if not match:
            continue
            
        concept_id, pref_label = match.groups()
        concept_uri = LEX[concept_id.strip()]
        
        g.add((concept_uri, RDF.type, SKOS.Concept))
        g.add((concept_uri, SKOS.prefLabel, Literal(pref_label.strip(), lang="fr")))

        # Parsing des lignes de métadonnées
        for line in lines[1:]:
            if "**Identifiant URI :**" in line:
                uri_str = line.split("`")[1]
                g.add((concept_uri, RDFS.isDefinedBy, URIRef(f"http://example.org/cyber-ontology#{uri_str.split(':')[-1]}")))
            elif "**Jargon & Acronymes (altLabel) :**" in line:
                synonyms = line.split(":**")[1].split(",")
                for syn in synonyms:
                    g.add((concept_uri, SKOS.altLabel, Literal(syn.strip(), lang="fr")))
            elif "**Définition Métier :**" in line:
                definition = line.split(":**")[1].strip()
                g.add((concept_uri, SKOS.definition, Literal(definition, lang="fr")))

    g.serialize(destination=ttl_file_path, format="turtle")
    print(f"✅ Conversion réussie : {md_file_path} -> {ttl_file_path}")

if __name__ == "__main__":
    parse_md_to_skos(
        "00-Governance_and_Ontology/LEXIQUE_METIER.md", 
        "00-Governance_and_Ontology/lexique_metier.ttl"
    )
