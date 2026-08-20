#!/usr/bin/env python3
"""
Convertit un fichier TTL (CVE) en requêtes Cypher pour Neo4j.
Usage: python ttl_to_cypher.py cve_data.ttl > cve_import.cypher
"""
import re

def ttl_to_cypher(ttl_file):
    with open(ttl_file, "r") as f:
        content = f.read()

    # Extraire les triples
    triples = re.findall(r'cve:([^\s]+)\s+a\s+:([^\s]+)\s*;\s*foaf:name\s*"([^"]+)"\s*;\s*:cvssScore\s*([^\s;]+)\s*;\s*:description\s*"([^"]+)"', content)

    cypher = []
    for cve_id, cve_type, name, cvss, desc in triples:
        cypher.append(f'CREATE (c:Vulnerability {{id: "{cve_id}", name: "{name}", cvssScore: {cvss}, description: "{desc.replace('"', '\\"')}"}})')
    print(cypher)
    return "\n".join(cypher)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python ttl_to_cypher.py <fichier.ttl>")
        sys.exit(1)
    print(ttl_to_cypher(sys.argv[1]))
