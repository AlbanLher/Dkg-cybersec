#!/usr/bin/env python3
"""build-tbox.py - Version finale avec débogage et lexique garanti"""

import json
import re
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

# Chemins alternatifs pour les lexiques
LEXIQUE_PATHS = [
    ROOT / "12-Donnees" / "Referential_TBox",
    ROOT / "12-Donnees" / "1-Sources" / "2-Externes",
    ROOT / "12-Donnees",
    ROOT / "12-Donnees" / "1-Sources",
]

CYBER = Namespace("http://example.org/cyber-ontology#")
CVE_NS = Namespace("https://cve.mitre.org/")

# ========== FONCTIONS DE LECTURE ==========
def read_inventory():
    """Lire inventory.json avec validation flexible"""
    inv_path = SOURCES_INTERNES / "inventory.json"
    if not inv_path.exists():
        raise FileNotFoundError(f"Fichier introuvable: {inv_path}")

    with open(inv_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if not isinstance(data, dict):
        raise ValueError("inventory.json doit être un objet JSON")

    devices = data.get('devices', data.get('equipments', data.get('assets', [])))

    validated_devices = []
    for idx, device in enumerate(devices):
        if not isinstance(device, dict):
            print(f"⚠️  Entrée {idx} invalide: {device}")
            continue

        name = device.get('name') or device.get('hostname') or device.get('id') or device.get('device_name')
        if not name:
            print(f"⚠️  Entrée {idx} sans nom: {device}")
            continue

        validated_device = {
            'name': str(name),
            'ip': device.get('ip') or device.get('address') or device.get('ip_address'),
            'type': device.get('type') or device.get('device_type') or 'unknown',
            'software': []
        }

        raw_software = device.get('software', device.get('apps', device.get('components', [])))
        for sw in raw_software:
            if not isinstance(sw, dict):
                continue
            sw_name = sw.get('name') or sw.get('software') or sw.get('app')
            if not sw_name:
                continue
            validated_sw = {
                'name': str(sw_name),
                'version': sw.get('version') or sw.get('ver') or '',
                'cvss': sw.get('cvss', sw.get('vulnerabilities', []))
            }
            validated_device['software'].append(validated_sw)

        validated_devices.append(validated_device)

    return {'devices': validated_devices}

def read_lexicons():
    """Lire les fichiers de lexique - recherche étendue"""
    graphs = []
    lexique_files = ["LEXIQUE_TECHNIQUE.ttl", "LEXIQUE_COMPATIBLE.ttl", "LEXIQUE_PUBLIQUE.ttl", "LEXIQUE_PRIVEE.ttl"]

    print("🔍 Recherche des fichiers de lexique...")
    for lex_path in LEXIQUE_PATHS:
        if not lex_path.exists():
            continue
        for name in lexique_files:
            path = lex_path / name
            if path.exists():
                g = Graph()
                try:
                    g.parse(str(path), format='turtle')
                    graphs.append(g)
                    print(f"   ✅ Trouvé: {path}")
                except Exception as e:
                    print(f"   ⚠️  Erreur parsing {path}: {e}")
    return graphs

# ========== EXTRACTION SKOS ==========
def extract_concepts(graphs):
    """Extraire les concepts SKOS avec débogage"""
    if not graphs:
        print("⚠️  Aucun graphe de lexique chargé !")
        return {}

    concepts = {}
    total_concepts = 0

    for g in graphs:
        g_concepts = list(g.subjects(SKOS.Concept, None))
        print(f"   Grape avec {len(g_concepts)} concepts")
        total_concepts += len(g_concepts)

        for uri in g_concepts:
            s = str(uri)
            if s not in concepts:
                concepts[s] = {'prefLabel': [], 'altLabel': [], 'definition': [], 'inScheme': set()}
            d = concepts[s]

            for label in g.objects(uri, SKOS.prefLabel):
                if label.language == 'fr':
                    d['prefLabel'].append(str(label))

            for label in g.objects(uri, SKOS.altLabel):
                if label.language == 'fr':
                    clean = re.sub(r'[\*]+', '', str(label)).replace('Synonymes / Acronymes :', '').strip()
                    if clean and clean not in d['altLabel']:
                        d['altLabel'].append(clean)

            for defn in g.objects(uri, SKOS.definition):
                if defn.language == 'fr':
                    d['definition'].append(str(defn))

            for scheme in g.objects(uri, SKOS.inScheme):
                d['inScheme'].add(str(scheme))

    print(f"   ✅ {total_concepts} concepts SKOS extraits au total")
    return concepts

# ========== GÉNÉRATION MARKDOWN - CORRIGÉE ==========
def generate_markdown(concepts):
    """Générer LEXIQUE_CONSOLIDE.md - version corrigée pour afficher TOUS les concepts"""
    lines = [
        "# 📚 Lexique Consolidé - Dkg-cybersec",
        "",
        f"**Généré:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"**Concepts:** {len(concepts)}",
        "",
        "## 📋 Table des Matières",
        ""
    ]

    # Si aucun concept, afficher un message
    if not concepts:
        lines.extend([
            "⚠️  **Aucun concept SKOS trouvé**",
            "",
            "Vérifiez que :",
            "- Les fichiers LEXIQUE_*.ttl existent",
            "- Ils sont dans 12-Donnees/Referential_TBox/ ou 12-Donnees/1-Sources/2-Externes/",
            "- Ils sont valides (format Turtle)",
            ""
        ])
        return "\n".join(lines)

    # Organiser par schéma
    schemes = {}
    for uri, data in concepts.items():
        for scheme in data['inScheme']:
            schemes.setdefault(scheme, []).append((uri, data))

    # Si aucun schéma, afficher tous les concepts dans une section unique
    if not schemes:
        lines.append("## Tous les Concepts")
        lines.append("")
        for uri, data in sorted(concepts.items(), key=lambda x: x[1]['prefLabel'][0] if x[1]['prefLabel'] else x[0]):
            _add_concept(lines, uri, data)
        return "\n".join(lines)

    scheme_titles = {
        "http://example.org/dkg/lexique#Scheme_LEXIQUE_TECHNIQUE": "📖 Lexique Technique",
        "http://example.org/dkg/lexique#Scheme_LEXIQUE_PUBLIQUE": "🌐 Lexique Public",
        "http://example.org/dkg/lexique#Scheme_LEXIQUE_PRIVEE": "🔒 Lexique Privé"
    }

    for scheme in sorted(schemes.keys()):
        title = scheme_titles.get(scheme, scheme.split('#')[-1])
        anchor = title.lower().replace(' ', '-').replace('📖', '').replace('🌐', '').replace('🔒', '')
        lines.append(f"- [{title}](#{anchor})")

    lines.extend(["", "---", ""])

    # Générer les sections
    for scheme in sorted(schemes.keys()):
        title = scheme_titles.get(scheme, scheme.split('#')[-1])
        lines.append(f"## {title}")
        lines.append("")

        for uri, data in sorted(schemes[scheme], key=lambda x: x[1]['prefLabel'][0] if x[1]['prefLabel'] else x[0]):
            _add_concept(lines, uri, data)

        lines.append("")

    # Ajouter le diagramme des relations
    lines.extend([
        "---",
        "",
        "## 🔗 Diagramme des Relations",
        "",
        "```mermaid",
        "graph TD",
        "    Device[Device/Équipement] -->|hasSoftware| Software[Software/Logiciel]",
        "    Software -->|hasVulnerability| Vulnerability[Vulnerability/Vulnérabilité]",
        "    Device -->|hasVulnerability| Vulnerability",
        "    Vulnerability -->|cvssScore| CVSS[Score CVSS]",
        "    Device -->|hasIP| IP[Adresse IP]",
        "```",
        ""
    ])

    return "\n".join(lines)

def _add_concept(lines, uri, data):
    """Ajouter un concept au markdown"""
    if not data['prefLabel']:
        return

    pref = data['prefLabel'][0]
    clean_pref = pref.replace('[', '').replace(']', '').strip()
    lines.append(f"### {clean_pref}")
    lines.append("")

    lines.append("| **Aspect** | **Valeur** |")
    lines.append("|------------|------------|")

    # Terme Officiel
    if data['prefLabel']:
        lines.append(f"| **Terme Officiel** | {data['prefLabel'][0]} |")

    # Synonymes
    if data['altLabel']:
        alts = data['altLabel'][:5]  # Limiter à 5
        lines.append(f"| **Synonymes** | {', '.join(alts)} |")

    # URI Ontologie
    uri_ont = None
    for defn in data['definition']:
        if m := re.search(r'`([^`]+)`', defn):
            uri_ont = m.group(1)
            break
    if uri_ont:
        lines.append(f"| **URI Ontologie** | `{uri_ont}` |")

    # Domaine
    domaine = None
    for defn in data['definition']:
        if m := re.search(r'\*\*Domaine :\*\* ([^\*]+)', defn):
            domaine = m.group(1).strip()
            break
    if domaine:
        lines.append(f"| **Domaine** | {domaine} |")

    # Définition Métier
    definition = None
    for defn in data['definition']:
        if m := re.search(r'\*\*Définition Métier :\*\* ([^\*]+)(?=\*\*|\Z)', defn, re.DOTALL):
            definition = m.group(1).strip()
            if len(definition) > 200:
                definition = definition[:200] + "..."
            break
    if definition:
        lines.append(f"| **Définition Métier** | {definition} |")

    # Exemple
    exemple = None
    for defn in data['definition']:
        if m := re.search(r'\*\*Exemple d\'Usage :\*\* ([^\*]+)', defn, re.DOTALL):
            exemple = m.group(1).strip()
            break
    if exemple:
        lines.append(f"| **Exemple** | {exemple} |")

    # Erreurs Fréquentes
    if data['hiddenLabel']:
        errors = [l for l in data['hiddenLabel'] if l][:3]
        if errors:
            lines.append(f"| **Erreurs Fréquentes** | {', '.join(errors)} |")

    lines.append("")

# ========== GÉNÉRATION ONTOLOGIE ==========
def generate_ontology(inventory, lex_graphs):
    """Générer VAULT_CONSOLIDE.ttl"""
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
        'version': (OWL.DatatypeProperty, CYBER.Software, XSD.string, 'version'),
    }
    for name, (prop_type, domain, range_, label) in props.items():
        uri = CYBER[name]
        consolidated.add((uri, RDF.type, prop_type))
        consolidated.add((uri, RDFS.label, Literal(label, lang='fr')))
        consolidated.add((uri, RDFS.domain, domain))
        consolidated.add((uri, RDFS.range, range_))

    for device in inventory.get('devices', []):
        if 'name' not in device:
            print(f"⚠️  Device sans name: {device}")
            continue

        dev_name = device['name'].replace('-', '_').replace('.', '_').replace(' ', '_')
        dev_uri = CYBER[dev_name]

        consolidated.add((dev_uri, RDF.type, CYBER.Device))
        consolidated.add((dev_uri, FOAF.name, Literal(device['name'])))

        if device.get('ip'):
            consolidated.add((dev_uri, CYBER.hasIP, Literal(device['ip'])))

        for sw in device.get('software', []):
            if 'name' not in sw:
                print(f"⚠️  Software sans name: {sw}")
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
                    print(f"⚠️  CVE sans id: {cve}")
                    continue

                cve_uri = CVE_NS[cve['id']]
                consolidated.add((cve_uri, RDF.type, CYBER.Vulnerability))
                consolidated.add((cve_uri, FOAF.name, Literal(cve['id'])))

                if 'score' in cve:
                    try:
                        consolidated.add((cve_uri, CYBER.cvssScore, Literal(float(cve['score']))))
                    except (ValueError, TypeError):
                        print(f"⚠️  Score CVE invalide: {cve['score']}")

                if 'description' in cve:
                    desc = str(cve['description'])[:200]
                    consolidated.add((cve_uri, RDFS.comment, Literal(desc, lang='fr')))

                consolidated.add((sw_uri, CYBER.hasVulnerability, cve_uri))
                consolidated.add((dev_uri, CYBER.hasVulnerability, cve_uri))

    return consolidated

# ========== FONCTION PRINCIPALE ==========
def main():
    """Fonction principale avec débogage"""
    print("🚀 Construction TBox - Dkg-cybersec")
    print("=" * 50)

    try:
        TBOX_OUT.mkdir(parents=True, exist_ok=True)

        print("\n📖 Lecture des données...")
        inventory = read_inventory()
        print(f"   ✅ {len(inventory.get('devices', []))} équipements validés")

        print("\n📚 Lecture des lexiques...")
        lex_graphs = read_lexicons()

        if not lex_graphs:
            print("⚠️  AUCUN FICHIER DE LEXIQUE TROUVÉ !")
            print("   Cherché dans:")
            for p in LEXIQUE_PATHS:
                print(f"   - {p} (existe: {p.exists()})")
            print("\n   Vérifiez que les fichiers LEXIQUE_*.ttl existent dans l'un de ces répertoires.")
            return 1

        print("\n🔍 Extraction des concepts SKOS...")
        concepts = extract_concepts(lex_graphs)

        if not concepts:
            print("⚠️  AUCUN CONCEPT SKOS EXTRAIT !")
            print("   Vérifiez que vos fichiers TTL contiennent bien des concepts SKOS (skos:Concept)")
            return 1

        print("\n📝 Génération des fichiers...")
        ontology = generate_ontology(inventory, lex_graphs)
        ontology.serialize(destination=str(TBOX_OUT / "VAULT_CONSOLIDE.ttl"), format='turtle')
        print(f"   ✅ VAULT_CONSOLIDE.ttl")

        md = generate_markdown(concepts)
        with open(TBOX_OUT / "LEXIQUE_CONSOLIDE.md", 'w', encoding='utf-8') as f:
            f.write(md)
        print(f"   ✅ LEXIQUE_CONSOLIDE.md")

        print("\n✅ Terminé! Fichiers dans:", TBOX_OUT)

    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0

if __name__ == "__main__":
    exit(main())
