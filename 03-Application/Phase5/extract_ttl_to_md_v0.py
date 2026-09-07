import sys
from pathlib import Path
from rdflib import Graph, RDF, RDFS, OWL, SKOS

def ttl_to_markdown(ttl_path: Path, output_md_path: Path):
    g = Graph()
    g.parse(str(ttl_path), format="turtle")
    
    md_lines = [
        f"# Extrait Sémantique : {ttl_path.name}",
        f"**Source** : `{ttl_path}`  ",
        f"**Nombre total de triplets** : `{len(g)}`  \n",
        "---",
        "## 1. Classes déclarées",
    ]
    
    # Extraction des Classes
    classes = set(g.subjects(RDF.type, OWL.Class)) | set(g.subjects(RDF.type, RDFS.Class))
    if classes:
        for cls in sorted(classes):
            label = g.value(cls, RDFS.label) or g.value(cls, SKOS.prefLabel) or cls.split("#")[-1]
            comment = g.value(cls, RDFS.comment) or g.value(cls, SKOS.definition) or "Aucune description"
            md_lines.append(f"* **`{cls.split('#')[-1]}`** (`{label}`): {comment}")
    else:
        md_lines.append("_Aucune classe explicitement déclarée._")
        
    md_lines.append("\n## 2. Propriétés")
    # Extraction des Propriétés
    props = set(g.subjects(RDF.type, OWL.ObjectProperty)) | set(g.subjects(RDF.type, OWL.DatatypeProperty))
    if props:
        for p in sorted(props):
            p_type = "ObjectProperty" if (p, RDF.type, OWL.ObjectProperty) in g else "DatatypeProperty"
            label = g.value(p, SKOS.prefLabel) or g.value(p, RDFS.label) or p.split("#")[-1]
            md_lines.append(f"* **`{p.split('#')[-1]}`** [{p_type}]: {label}")
    else:
        md_lines.append("_Aucune propriété explicitement déclarée._")

    md_lines.append("\n## 3. Échantillon de Triplets (Top 20)")
    md_lines.append("| Sujet | Prédicat | Objet |")
    md_lines.append("| :--- | :--- | :--- |")
    
    for i, (s, p, o) in enumerate(g):
        if i >= 20:
            break
        s_str = s.split("#")[-1] if "#" in str(s) else str(s).split("/")[-1]
        p_str = p.split("#")[-1] if "#" in str(p) else str(p).split("/")[-1]
        o_str = o.split("#")[-1] if "#" in str(o) else str(o).split("/")[-1]
        md_lines.append(f"| `{s_str}` | `{p_str}` | `{o_str}` |")

    output_md_path.write_text("\n".join(md_lines), encoding="utf-8")
    print(f"Extraction terminée : {output_md_path}")

if __name__ == "__main__":
    # Exemple d'usage sur les fichiers du projet
    base_dir = Path("./")
    ttl_files = list(base_dir.glob("**/*.ttl"))
    
    for ttl in ttl_files:
        md_out = ttl.with_suffix(".md")
        ttl_to_markdown(ttl, md_out)
