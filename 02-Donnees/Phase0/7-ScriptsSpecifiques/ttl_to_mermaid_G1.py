import sys
from rdflib import Graph, Namespace, RDF, RDFS, OWL

def ttl_to_mermaid(ttl_file):
    g = Graph()
    g.parse(ttl_file, format="turtle")
    
    classes = set()
    data_props = {}  # Class -> [props]
    obj_props = []   # (Subject, Property, Object)

    # 1. Extraire les classes
    for s in g.subjects(RDF.type, OWL.Class):
        c_name = str(s).split('#')[-1].split('/')[-1]
        classes.add(c_name)

    # 2. Extraire les propriétés de données (Datatype Properties)
    for s, p, o in g.triples((None, RDF.type, OWL.DatatypeProperty)):
        prop_name = str(s).split('#')[-1].split('/')[-1]
        domains = list(g.objects(s, RDFS.domain))
        for d in domains:
            domain_name = str(d).split('#')[-1].split('/')[-1]
            data_props.setdefault(domain_name, []).append(prop_name)

    # 3. Extraire les propriétés d'objets / relations (Object Properties)
    for s, p, o in g.triples((None, RDF.type, OWL.ObjectProperty)):
        prop_name = str(s).split('#')[-1].split('/')[-1]
        domains = list(g.objects(s, RDFS.domain))
        ranges = list(g.objects(s, RDFS.range))
        for d in domains:
            for r in ranges:
                d_name = str(d).split('#')[-1].split('/')[-1]
                r_name = str(r).split('#')[-1].split('/')[-1]
                obj_props.append((d_name, prop_name, r_name))

    # 4. Formater en Mermaid
    mermaid = ["classDiagram", "    direction LR"]
    
    for c in classes:
        mermaid.append(f"    class {c} {{")
        for dp in data_props.get(c, []):
            mermaid.append(f"        +{dp}")
        mermaid.append("    }")

    for src, rel, dst in obj_props:
        mermaid.append(f"    {src} --> {dst} : {rel}")

    return "\n".join(mermaid)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(ttl_to_mermaid(sys.argv[1]))
