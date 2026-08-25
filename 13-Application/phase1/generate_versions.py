from pathlib import Path
from rdflib import Graph, Literal
from rdflib.namespace import SKOS, OWL, RDF, RDFS
import json

def generate_versions():
    # 1. Charger la TBox
    graph = Graph()
    graph.parse("12-Donnees/TBox_init/VAULT_CONSOLIDE.ttl", format="turtle")

    # 2. Générer LEXIQUE_CONSOLIDE.md
    with open("12-Donnees/TBox_init/LEXIQUE_CONSOLIDE.md", "w") as f:
        f.write("# 📚 Lexique Consolidé\n\n")
        f.write("## Concepts SKOS\n\n")
        for concept in graph.subjects(RDF.type, SKOS.Concept):
            label = graph.value(concept, SKOS.prefLabel, default="")
            f.write(f"- **{concept}** : {label}\n")

        f.write("\n## Classes OWL\n\n")
        for cls in graph.subjects(RDF.type, OWL.Class):
            label = graph.value(cls, RDFS.label, default=str(cls).split("#")[-1])
            f.write(f"- **{cls}** : {label}\n")

    # 3. Générer ONTOLOGY_CONSOLIDE.json
    data = {"classes": [], "properties": []}
    for cls in graph.subjects(RDF.type, OWL.Class):
        data["classes"].append({
            "uri": str(cls),
            "label": str(graph.value(cls, RDFS.label, default=""))
        })
    for prop in graph.subjects(RDF.type, OWL.ObjectProperty):
        data["properties"].append(str(prop))

    with open("12-Donnees/TBox_init/ONTOLOGY_CONSOLIDE.json", "w") as f:
        json.dump(data, f, indent=2)

    print("✅ Généré: LEXIQUE_CONSOLIDE.md, ONTOLOGY_CONSOLIDE.json")

if __name__ == "__main__":
    generate_versions()
