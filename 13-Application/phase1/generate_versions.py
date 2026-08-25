from pathlib import Path
from rdflib import Graph, Literal
from rdflib.namespace import SKOS, OWL, RDF, RDFS
import json
from datetime import datetime

def generate_versions():
    # Charger la TBox
    graph = Graph()
    graph.parse("12-Donnees/TBox_init/VAULT_CONSOLIDE.ttl", format="turtle")

    # Générer LEXIQUE_CONSOLIDE.md
    with open("12-Donnees/TBox_init/LEXIQUE_CONSOLIDE.md", "w") as f:
        f.write(f"""# Lexique & Ontologie - DKG
Généré le {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Lexique (Concepts Métiers)

| Concept | Label | Définition |
|---------|-------|------------|
""")

        for concept in graph.subjects(RDF.type, SKOS.Concept):
            label = graph.value(concept, SKOS.prefLabel, default="")
            definition = graph.value(concept, SKOS.definition, default="")
            f.write(f"| {concept} | {label} | {definition} |\n")

        f.write("""

## Ontologie (Classes)

```mermaid
classDiagram
""")

        for cls in graph.subjects(RDF.type, OWL.Class):
            cls_name = str(cls).split("#")[-1]
            f.write(f"    class {cls_name}\n")

        for cls in graph.subjects(RDF.type, OWL.Class):
            for super_cls in graph.objects(cls, RDFS.subClassOf):
                child = str(cls).split("#")[-1]
                parent = str(super_cls).split("#")[-1]
                f.write(f"    {child} --|> {parent}\n")

        f.write("""}
""")
        # Générer JSON
        data = {"classes": [str(c) for c in graph.subjects(RDF.type, OWL.Class)]}
        with open("12-Donnees/TBox_init/ONTOLOGY_CONSOLIDE.json", "w") as f:
            json.dump(data, f, indent=2)

    print("Généré: LEXIQUE_CONSOLIDE.md, ONTOLOGY_CONSOLIDE.json")


if __name__ == "main":
    generate_version()
