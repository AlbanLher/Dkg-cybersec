#!/usr/bin/env python3
"""build-tbox.py - Version définitive adaptée à VOS fichiers"""

import json, re
from pathlib import Path
from datetime import datetime
from rdflib import Graph, Literal, Namespace, XSD
from rdflib.namespace import RDF, RDFS, OWL, SKOS, FOAF

# ========== CONFIGURATION ==========
SCRIPT_DIR = Path(__file__).parent
ROOT = SCRIPT_DIR.parent.parent
SOURCES_INTERNES = ROOT / "12-Donnees" / "1-Sources" / "1-Internes"
SOURCES_EXTERNES = ROOT / "12-Donnees" / "1-Sources" / "2-Externes"
TBOX_OUT = ROOT / "12-Donnees" / "TBox_init"

CYBER = Namespace("http://example.org/cyber-ontology#")
CVE_NS = Namespace("https://cve.mitre.org/")

# ========== LECTURE DES LEXIQUES - CORRIGÉE ==========
def read_lexicons():
    """Lire TOUS les fichiers LEXIQUE_*.ttl dans les répertoires sources"""
    graphs = []
    lexique_files = ["LEXIQUE_PROJET.ttl", "LEXIQUE_FIRST.ttl", "LEXIQUE_TECHNIQUE.ttl", "LEXIQUE_COMPATIBLE.ttl"]

    search_paths = [SOURCES_INTERNES, SOURCES_EXTERNES]

    print("🔍 Recherche des fichiers de lexique...")
    for path in search_paths:
        if not path.exists():
            print(f"   Répertoire inexistant: {path}")
            continue
        for name in lexique_files:
            file_path = path / name
            if file_path.exists():
                g = Graph()
                try:
                    g.parse(str(file_path), format='turtle')
                    graphs.append(g)
                    print(f"   ✅ Trouvé: {file_path}")
                except Exception as e:
                    print(f"   ⚠️  Erreur: {file_path} - {e}")

    if not graphs:
        print("❌ AUCUN FICHIER LEXIQUE TROUVÉ !")
        print("   Vérifiez que les fichiers existent bien dans:")
        for path in search_paths:
            print(f"   - {path} (existe: {path.exists()})")
            if path.exists():
                print(f"     Contenu: {list(path.glob('LEXIQUE*'))}")

    return graphs

def read_inventory():
    inv_path = SOURCES_INTERNES / "inventory.json"
    if not inv_path.exists():
        raise FileNotFoundError(f"Fichier introuvable: {inv_path}")
    with open(inv_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# ========== EXTRACTION SKOS ==========
def extract_concepts(graphs):
    if not graphs:
        return {}

    concepts = {}
    for g in graphs:
        for uri in g.subjects(SKOS.Concept, None):
            s = str(uri)
            if s not in concepts:
                concepts[s] = {'prefLabel': [], 'altLabel': [], 'definition': []}
            d = concepts[s]
            for label in g.objects(uri, SKOS.prefLabel):
                if label.language == 'fr':
                    d['prefLabel'].append(str(label))
            for label in g.objects(uri, SKOS.altLabel):
                if label.language == 'fr':
                    clean = re.sub(r'[\*]+', '', str(label)).strip()
                    if clean and clean not in d['altLabel']:
                        d['altLabel'].append(clean)
            for defn in g.objects(uri, SKOS.definition):
                if defn.language == 'fr':
                    d['definition'].append(str(defn))
    return concepts

# ========== GÉNÉRATION MARKDOWN ==========
def generate_markdown(concepts):
    if not concepts:
        return "# ⚠️ Aucun concept SKOS trouvé\n\nVérifiez que vos fichiers LEXIQUE_*.ttl contiennent bien des concepts avec skos:Concept"

    lines = [
        "# 📚 Lexique Consolidé - Dkg-cybersec",
        "",
        f"**Généré:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"**Concepts:** {len(concepts)}",
        ""
    ]

    # Trier par prefLabel
    sorted_concepts = sorted(concepts.items(),
                           key=lambda x: x[1]['prefLabel'][0] if x[1]['prefLabel'] else x[0])

    for uri, data in sorted_concepts:
        if not data['prefLabel']:
            continue
        pref = data['prefLabel'][0]
        lines.append(f"## {pref}")
        lines.append("")
        if data['altLabel']:
            lines.append(f"**Synonymes:** {', '.join(data['altLabel'][:5])}")
        if data['definition']:
            defn = data['definition'][0]
            if len(defn) > 300:
                defn = defn[:300] + "..."
            lines.append(f"**Définition:** {defn}")
        lines.append("")

    return "\n".join(lines)

# ========== GÉNÉRATION ONTOLOGIE ==========
def generate_ontology(inventory, lex_graphs):
    consolidated = Graph()
    for prefix, ns in [('cyber', CYBER), ('cve', CVE_NS), ('skos', SKOS),
                       ('foaf', FOAF), ('owl', OWL), ('rdfs', RDFS), ('xsd', XSD)]:
        consolidated.bind(prefix, ns)

    for g in lex_graphs:
        consolidated += g

    for name, label in [('Device', 'Équipement'), ('Software', 'Logiciel'), ('Vulnerability', 'Vulnérabilité')]:
        uri = CYBER[name]
        consolidated.add((uri, RDF.type, OWL.Class))
        consolidated.add((uri, RDFS.label, Literal(label, lang='fr')))

    props = {
        'hasSoftware': (OWL.ObjectProperty, CYBER.Device, CYBER.Software, 'a pour logiciel'),
        'hasVulnerability': (OWL.ObjectProperty, CYBER.Device, CYBER.Vulnerability, 'a pour vulnérabilité'),
        'hasIP': (OWL.DatatypeProperty, CYBER.Device, XSD.string, 'a pour IP'),
        'cvssScore': (OWL.DatatypeProperty, CYBER.Vulnerability, XSD.float, 'score CVSS'),
    }
    for name, (ptype, domain, range_, label) in props.items():
        uri = CYBER[name]
        consolidated.add((uri, RDF.type, ptype))
        consolidated.add((uri, RDFS.label, Literal(label, lang='fr')))
        consolidated.add((uri, RDFS.domain, domain))
        consolidated.add((uri, RDFS.range, range_))

    for device in inventory.get('devices', []):
        if 'name' not in device:
            continue
        dev_uri = CYBER[device['name'].replace('-', '_').replace('.', '_')]
        consolidated.add((dev_uri, RDF.type, CYBER.Device))
        consolidated.add((dev_uri, FOAF.name, Literal(device['name'])))
        if device.get('ip'):
            consolidated.add((dev_uri, CYBER.hasIP, Literal(device['ip'])))

        for sw in device.get('software', []):
            if 'name' not in sw:
                continue
            sw_name = sw['name'].replace(' ', '_').replace('.', '_')
            sw_version = sw.get('version', '').replace('.', '_')
            sw_uri = CYBER[f"{sw_name}_{sw_version}"] if sw_version else CYBER[sw_name]
            consolidated.add((sw_uri, RDF.type, CYBER.Software))
            consolidated.add((sw_uri, FOAF.name, Literal(sw['name'])))
            if sw.get('version'):
                consolidated.add((sw_uri, CYBER.version, Literal(sw['version'])))
            consolidated.add((dev_uri, CYBER.hasSoftware, sw_uri))

            for cve in sw.get('cvss', []):
                if 'id' not in cve:
                    continue
                cve_uri = CVE_NS[cve['id']]
                consolidated.add((cve_uri, RDF.type, CYBER.Vulnerability))
                consolidated.add((cve_uri, FOAF.name, Literal(cve['id'])))
                if 'score' in cve:
                    try:
                        consolidated.add((cve_uri, CYBER.cvssScore, Literal(float(cve['score']))))
                    except:
                        pass
                if 'description' in cve:
                    desc = str(cve['description'])[:200]
                    consolidated.add((cve_uri, RDFS.comment, Literal(desc, lang='fr')))
                consolidated.add((sw_uri, CYBER.hasVulnerability, cve_uri))
                consolidated.add((dev_uri, CYBER.hasVulnerability, cve_uri))

    return consolidated

# ========== MAIN ==========
def main():
    print("🚀 Construction TBox - Dkg-cybersec")
    print("=" * 50)

    TBOX_OUT.mkdir(parents=True, exist_ok=True)

    lex_graphs = read_lexicons()
    if not lex_graphs:
        return 1

    inventory = read_inventory()
    concepts = extract_concepts(lex_graphs)

    if not concepts:
        print("⚠️  Aucun concept SKOS extrait !")
        print("   Vérifiez que vos fichiers contiennent bien des triplets comme:")
        print("   ex:Concept_X skos:prefLabel 'Un concept'@fr .")
        return 1

    print(f"\n✅ {len(concepts)} concepts extraits")
    print(f"✅ {len(inventory.get('devices', []))} équipements")

    ontology = generate_ontology(inventory, lex_graphs)
    ontology.serialize(destination=str(TBOX_OUT / "VAULT_CONSOLIDE.ttl"), format='turtle')
    print(f"✅ VAULT_CONSOLIDE.ttl généré")

    md = generate_markdown(concepts)
    with open(TBOX_OUT / "LEXIQUE_CONSOLIDE.md", 'w', encoding='utf-8') as f:
        f.write(md)
    print(f"✅ LEXIQUE_CONSOLIDE.md généré")

    print(f"\n✅ Terminé ! Fichiers dans: {TBOX_OUT}")
    return 0

if __name__ == "__main__":
    exit(main())
