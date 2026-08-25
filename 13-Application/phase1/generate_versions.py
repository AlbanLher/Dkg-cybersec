from pathlib import Path
from rdflib import Graph
from rdflib.namespace import SKOS, OWL, RDF, RDFS
import json
from datetime import datetime

def generate_versions():
    # Charger la TBox
    graph = Graph()
    tbox_path = Path("12-Donnees/TBox_init/VAULT_CONSOLIDE.ttl")
    graph.parse(str(tbox_path), format="turtle")

    # Créer le dossier de sortie
    output_dir = Path("12-Donnees/TBox_init")
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. Générer LEXIQUE_CONSOLIDE.md
    md_lines = [
        "# Lexique & Ontologie - DKG",
        f"> *Généré le {datetime.now().strftime('%Y-%m-%d %H:%M')}*", "",
        "---",
        "",
        "## Lexique (Concepts Métiers)",
        "",
        "| Concept | Label | Définition |",
        "|---------|-------|------------|"
    ]

    for concept in graph.subjects(RDF.type, SKOS.Concept):
        label = graph.value(concept, SKOS.prefLabel, default="")
        definition = graph.value(concept, SKOS.definition, default="")
        md_lines.append(f"| {concept} | {label} | {definition} |")

    md_lines.extend([
        "",
        "---",
        "",
        "## Ontologie (Classes)",
        "",
        "```mermaid",
        "classDiagram"
    ])

    for cls in graph.subjects(RDF.type, OWL.Class):
        cls_name = str(cls).split("#")[-1]
        md_lines.append(f"    class {cls_name}")

    for cls in graph.subjects(RDF.type, OWL.Class):
        for super_cls in graph.objects(cls, RDFS.subClassOf):
            child = str(cls).split("#")[-1]
            parent = str(super_cls).split("#")[-1]
            md_lines.append(f"    {child} --|> {parent}")

    md_lines.extend([
        "```",
        "",
        "---",
        "",
        "## Statistiques",
        f"- Concepts SKOS: {len(list(graph.subjects(RDF.type, SKOS.Concept)))}",
        f"- Classes OWL: {len(list(graph.subjects(RDF.type, OWL.Class)))}"
    ])

    with open(output_dir / "LEXIQUE_CONSOLIDE.md", "w") as f:
        f.write("\n".join(md_lines))

    # 2. Générer ONTOLOGY_CONSOLIDE.json
    data = {
        "classes": [str(c) for c in graph.subjects(RDF.type, OWL.Class)],
        "properties": [str(p) for p in graph.subjects(RDF.type, OWL.ObjectProperty)]
    }
    with open(output_dir / "ONTOLOGY_CONSOLIDE.json", "w") as f:
        json.dump(data, f, indent=2)

    print("Généré: LEXIQUE_CONSOLIDE.md, ONTOLOGY_CONSOLIDE.json")

if __name__ == "__main__":
    generate_versions()
