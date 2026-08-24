import os
import re
from pathlib import Path
from rdflib import Graph, Namespace, RDF, RDFS, OWL, SKOS, Literal

# --- Ancrage automatique sur le dossier racine '02-Donnees' ---
CURRENT_SCRIPT_PATH = Path(__file__).resolve()

DATA_DIR = None
for parent in CURRENT_SCRIPT_PATH.parents:
    if parent.name == "02-Donnees":
        DATA_DIR = parent
        break

if not DATA_DIR:
    # Fallback si l'arborescence diffère
    DATA_DIR = CURRENT_SCRIPT_PATH.parents[2]

# Emplacements des répertoires TBox et Phase 0
PHASE0_DIR = DATA_DIR / "Phase0"
TBOX_DIR = DATA_DIR / "Referential_TBox"

# Sources & Destinations précises
SOURCE_LEXIQUE_MD = PHASE0_DIR / "4-App_publication_md" / "PUBLICATION_LEXIQUE_GLOBAL.md"
TBOX_MD_MASTER = TBOX_DIR / "App_Publication.md"
TBOX_TTL_OUTPUT = TBOX_DIR / "ONTOLOGY_TBOX.ttl"

# Espaces de noms RDF
EX = Namespace("http://example.org/dkg/ontology#")
SKOS_NS = Namespace("http://www.w3.org/2004/02/skos/core#")

def ensure_directories():
    """S'assure que le répertoire cible Referential_TBox existe sur le disque."""
    TBOX_DIR.mkdir(parents=True, exist_ok=True)

def migrate_and_enrich_lexicon():
    """
    Rapatrie PUBLICATION_LEXIQUE_GLOBAL.md vers App_Publication.md
    et y intègre le cadrage TBox/ABox si ces termes n'y figurent pas encore.
    """
    ensure_directories()
    
    if not SOURCE_LEXIQUE_MD.exists():
        print(f"⚠️ Fichier source introuvable : {SOURCE_LEXIQUE_MD}")
        # Si le fichier exact n'est pas trouvé, on cherche un fichier .md équivalent dans le dossier
        alt_mds = list((PHASE0_DIR / "4-App_publication_md").glob("*.md")) if (PHASE0_DIR / "4-App_publication_md").exists() else []
        if alt_mds:
            source_file = alt_mds[0]
            print(f"🔄 Utilisation du fichier alternatif trouvé : {source_file.name}")
        else:
            print("❌ Aucun fichier Markdown source trouvé dans Phase0/4-App_publication_md.")
            return
    else:
        source_file = SOURCE_LEXIQUE_MD

    print(f"📥 Portage de [{source_file.name}] vers [{TBOX_MD_MASTER.name}]...")
    content = source_file.read_text(encoding="utf-8")

    # Vérification et injection du cadrage TBox / ABox dans le lexique si absent
    tbox_abox_definitions = """
* **TBox (Terminological Box)** : Schéma formel du domaine définissant le vocabulaire, les concepts (Classes), leurs hiérarchies (Sous-classes) et les règles d'association (Propriétés/Relations). C'est le contrat de structure immuable du graphe.
* **ABox (Assertional Box)** : Données réelles et instances concrètes (équipements, adresses IP, identifiants CVE, règles de sécurité) constituant la mémoire opérationnelle.
"""

    if "TBox" not in content or "ABox" not in content:
        print("  ├─ ➕ Injection du cadrage conceptuel (TBox / ABox) dans le Lexique...")
        # Insertion après le premier titre principal ou au début du document
        if "# " in content:
            parts = content.split("# ", 1)
            content = f"# {parts[0]}\n\n## Cadrage Conceptuel (TBox / ABox)\n{tbox_abox_definitions}\n\n# {parts[1]}"
        else:
            content = f"# Cadrage Conceptuel (TBox / ABox)\n{tbox_abox_definitions}\n\n" + content

    TBOX_MD_MASTER.write_text(content, encoding="utf-8")
    print(f"  └─ ✅ Fichier maître humain créé : {TBOX_MD_MASTER}")

def parse_markdown_lexicon_to_skos(graph: Graph):
    """Parse le Markdown maître et injecte les concepts SKOS dans le graphe TBox."""
    if not TBOX_MD_MASTER.exists():
        return

    print(f"📄 Parsing sémantique des termes du lexique depuis {TBOX_MD_MASTER.name}...")
    content = TBOX_MD_MASTER.read_text(encoding="utf-8")
    
    # Capture des paires **Terme** : Définition
    matches = re.findall(r"\*\*(.*?)\*\*\s*:\s*(.*)", content)
    
    count = 0
    for term, definition in matches:
        term_clean = term.strip()
        def_clean = definition.strip()
        if not term_clean or len(term_clean) > 80:
            continue
            
        term_slug = re.sub(r"\W+", "_", term_clean).strip("_")
        concept_uri = EX[f"Concept_{term_slug}"]

        graph.add((concept_uri, RDF.type, SKOS_NS.Concept))
        graph.add((concept_uri, SKOS_NS.prefLabel, Literal(term_clean, lang="fr")))
        graph.add((concept_uri, SKOS_NS.definition, Literal(def_clean, lang="fr")))
        count += 1

    print(f"  └─ ✅ {count} concepts SKOS du lexique intégrés au graphe TBox.")

def build_unified_tbox():
    """Séquence principale d'assemblage de la TBox Master."""
    ensure_directories()
    
    # 1. Portage du Markdown unifié de Phase 0 avec le cadrage TBox/ABox
    migrate_and_enrich_lexicon()

    print("🔄 Assemblage de la TBox Master (ONTOLOGY_TBOX.ttl)...")
    unified_graph = Graph()
    
    unified_graph.bind("ex", EX)
    unified_graph.bind("owl", OWL)
    unified_graph.bind("rdfs", RDFS)
    unified_graph.bind("skos", SKOS_NS)

    # 2. Parsing des ontologies .ttl de Phase 0 (Internal_Input & External_Input)
    phase0_ontologies = PHASE0_DIR / "2-Ontologie"
    target_subdirs = ["External_Input", "Internal_Input"]
    
    ttl_count = 0
    for subdir in target_subdirs:
        path = phase0_ontologies / subdir
        if path.exists():
            for ttl_file in path.rglob("*.ttl"):
                if "Archive" not in ttl_file.parts:
                    print(f"  ├─ Parsing TTL : {ttl_file.relative_to(PHASE0_DIR)}")
                    try:
                        unified_graph.parse(location=str(ttl_file), format="turtle")
                        ttl_count += 1
                    except Exception as e:
                        print(f"  ❌ Erreur de parsing sur {ttl_file.name} : {e}")

    # 3. Synchronisation des concepts du lexique Markdown vers le graphe TTL
    parse_markdown_lexicon_to_skos(unified_graph)

    # 4. Sérialisation finale
    unified_graph.serialize(destination=str(TBOX_TTL_OUTPUT), format="turtle")
    
    classes_count = len(list(unified_graph.subjects(RDF.type, OWL.Class)))
    props_count = len(list(unified_graph.subjects(RDF.type, OWL.ObjectProperty))) + \
                  len(list(unified_graph.subjects(RDF.type, OWL.DatatypeProperty)))

    print(f"✅ TBox unifiée générée avec succès ({ttl_count} fichiers TTL fusionnés) -> {TBOX_TTL_OUTPUT}")
    print(f"📊 Bilan TBox : {classes_count} Classe(s) OWL, {props_count} Propriété(s).")

if __name__ == "__main__":
    build_unified_tbox()
