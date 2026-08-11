#!/usr/bin/env python3
import sys
from rdflib import Graph, Namespace, RDF

FOAF = Namespace("http://xmlns.com/foaf/0.1/")
CYBER = Namespace("http://example.org/cyber-ontology#")

def ttl_to_cypher(ttl_file):
    g = Graph()
    g.parse(ttl_file, format="turtle")

    cypher_statements = []

    # Parcourt tous les sujets de type :Vulnerability
    for vuln in g.subjects(RDF.type, CYBER.Vulnerability):
        # Récupération des propriétés
        cve_id = str(vuln).split("/")[-1]
        name = str(g.value(vuln, FOAF.name) or "")
        cvss = float(g.value(vuln, CYBER.cvssScore) or 0)
        desc = str(g.value(vuln, CYBER.description) or "").replace('"', '\\"')

        stmt = f'CREATE (c:Vulnerability {{id: "{cve_id}", name: "{name}", cvssScore: {cvss}, description: "{desc}"}});'
        cypher_statements.append(stmt)

    return "\n".join(cypher_statements)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python ttl_to_cypher.py <fichier.ttl>")
        sys.exit(1)
    print(ttl_to_cypher(sys.argv[1]))
