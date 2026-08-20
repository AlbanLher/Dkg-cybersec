Montre un script Python qui extrait ces métadonnées depuis ontologie_v1.ttl pour construire les descriptions textuelles à vectoriser.

Voici le script Python complet basé sur **`rdflib`**. Il parcourt le fichier `ontologie_v1.ttl`, extrait les métadonnées sémantiques enrichies (`rdfs:label`, `skos:altLabel`, `rdfs:comment`, disjonctions et domaines/portées des propriétés) et applique le motif de sérialisation textuelle idéal pour la vectorisation (embeddings).

### Script Python : `generate_embeddings_text.py`

```Python

import os
from rdflib import Graph, Namespace, RDF, RDFS, OWL, SKOS, Literal

def extract_metadata_for_vectorization(ttl_path: str) -> list[dict]:
    # 1. Chargement du graphe RDF
    g = Graph()
    g.parse(ttl_path, format="turtle")

    # Namespaces
    CYBER = Namespace("http://example.org/cyber-ontology#")

    nodes_to_vectorize = []

    # Helper pour extraire les littéraux sous forme de liste de chaînes
    def get_literals(subject, predicate) -> list[str]:
        return [str(o) for o in g.objects(subject, predicate) if isinstance(o, Literal)]

    # Helper pour obtenir un nom court lisible depuis une URI
    def short_name(uri) -> str:
        uri_str = str(uri)
        if "#" in uri_str:
            return uri_str.split("#")[-1]
        elif "/" in uri_str:
            return uri_str.split("/")[-1]
        return uri_str

    # =========================================================================
    # A. EXTRACTION DES CLASSES (owl:Class)
    # =========================================================================
    classes = set(g.subjects(RDF.type, OWL.Class)).union(set(g.subjects(RDF.type, RDFS.Class)))

    for cls in classes:
        uri_name = short_name(cls)
        
        # Ignorer les nœuds anonymes / bnodes
        if not isinstance(cls, Literal) and uri_name.startswith("N"):
            continue

        labels = get_literals(cls, RDFS.label)
        alt_labels = get_literals(cls, SKOS.altLabel)
        comments = get_literals(cls, RDFS.comment)

        # Extraction des classes disjointes (owl:disjointWith)
        disjoints = [short_name(o) for o in g.objects(cls, OWL.disjointWith)]

        # Construction du texte sérialisé
        primary_label = labels[0] if labels else uri_name
        synonyms_str = f" (Synonymes/Acronymes: {', '.join(alt_labels)})" if alt_labels else ""
        definition_str = f" Définition: {comments[0]}" if comments else ""
        disjoint_str = f" Non-compatible / Disjoint de: {', '.join(disjoints)}." if disjoints else ""

        text_representation = (
            f"Concept: {primary_label}{synonyms_str}. "
            f"Type: Classe Ontologique ({uri_name})."
            f"{definition_str}"
            f"{disjoint_str}"
        )

        nodes_to_vectorize.append({
            "uri": str(cls),
            "identifier": uri_name,
            "type": "Class",
            "text_for_embedding": text_representation.strip()
        })

    # =========================================================================
    # B. EXTRACTION DES PROPRIÉTÉS (owl:DatatypeProperty & owl:ObjectProperty)
    # =========================================================================
    properties = set(g.subjects(RDF.type, OWL.ObjectProperty)).union(
        set(g.subjects(RDF.type, OWL.DatatypeProperty))
    )

    for prop in properties:
        uri_name = short_name(prop)
        prop_type = "Relation/Objet" if (prop, RDF.type, OWL.ObjectProperty) in g else "Attribut/Donnée"
        
        labels = get_literals(prop, RDFS.label)
        comments = get_literals(prop, RDFS.comment)
        domains = [short_name(o) for o in g.objects(prop, RDFS.domain)]
        ranges = [short_name(o) for o in g.objects(prop, RDFS.range)]

        primary_label = labels[0] if labels else uri_name
        definition_str = f" Description: {comments[0]}" if comments else ""
        domain_str = f" S'applique à (Domaine): {', '.join(domains)}." if domains else ""
        range_str = f" Pointe vers (Portée): {', '.join(ranges)}." if ranges else ""

        text_representation = (
            f"Propriété: {primary_label}. "
            f"Type: {prop_type} ({uri_name})."
            f"{definition_str}"
            f"{domain_str}"
            f"{range_str}"
        )

        nodes_to_vectorize.append({
            "uri": str(prop),
            "identifier": uri_name,
            "type": "Property",
            "text_for_embedding": text_representation.strip()
        })

    return nodes_to_vectorize

# =============================================================================
# EXÉCUTION & DÉMONSTRATION
# =============================================================================
if __name__ == "__main__":
    TTL_FILE = "ontologie_v1.ttl"

    # Vérification si le fichier existe, sinon génération d'un exemple fictif pour démo
    if not os.path.exists(TTL_FILE):
        print(f"⚠️ Fichier {TTL_FILE} non trouvé. Exécution sur exemple en mémoire...")
        sample_ttl = """
        @prefix cyber: <http://example.org/cyber-ontology#> .
        @prefix owl: <http://www.w3.org/2002/07/owl#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix skos: <http://www.w3.org/2004/02/skos/core#> .
        @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

        cyber:Vulnerability a owl:Class ;
            rdfs:label "Vulnérabilité Sécurité"@fr ;
            skos:altLabel "CVE", "Faille", "Flaw" ;
            rdfs:comment "Faiblesse dans un système d'information pouvant être exploitée."@fr ;
            owl:disjointWith cyber:Device .

        cyber:affectsDevice a owl:ObjectProperty ;
            rdfs:label "affecte l'équipement" ;
            rdfs:comment "Lie une vulnérabilité à l'équipement physique ou virtuel impacté." ;
            rdfs:domain cyber:Vulnerability ;
            rdfs:range cyber:Device .
        """
        with open("ontologie_v1.ttl", "w", encoding="utf-8") as f:
            f.write(sample_ttl)

    metadata_records = extract_metadata_for_vectorization(TTL_FILE)

    print(f"✅ {len(metadata_records)} concepts extraits pour vectorisation :\n")
    for record in metadata_records:
        print(f"📌 [{record['type']}] {record['identifier']}")
        print(f"   📄 Text Payload for Embedding:\n   \"{record['text_for_embedding']}\"\n")
```

### Résultat obtenu (Text Payloads prêts pour OpenAI / HuggingFace)

Ce script génère des chaînes textuelles enrichies que vous pouvez directement passer à votre modèle d'embedding (ex: `openai.Embedding.create()` ou `SentenceTransformer`) avant de les pousser dans Neo4j Vector Index :

Plaintext

```
📌 [Class] Vulnerability
   📄 Text Payload for Embedding:
   "Concept: Vulnérabilité Sécurité (Synonymes/Acronymes: CVE, Faille, Flaw). Type: Classe Ontologique (Vulnerability). Définition: Faiblesse dans un système d'information pouvant être exploitée. Non-compatible / Disjoint de: Device."

📌 [Property] affectsDevice
   📄 Text Payload for Embedding:
   "Propriété: affecte l'équipement. Type: Relation/Objet (affectsDevice). Description: Lie une vulnérabilité à l'équipement physique ou virtuel impacté. S'applique à (Domaine): Vulnerability. Pointe vers (Portée): Device."
```