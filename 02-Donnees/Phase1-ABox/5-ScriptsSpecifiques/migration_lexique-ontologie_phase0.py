"""
Script : migration_lexique-ontologie_phase0.py
Description :
    Migration stricte ISO-périmètre de la Phase 0 vers Referential_TBox/
    1. Source Lexique MD : Phase0/4-App_publication_md/Lexiques/PUBLICATION_LEXIQUE_GLOBAL.md
    2. Source Ontologies TTL : Phase0/3-App_Referential_Vault/
"""

import os
import re
from pathlib import Path
from rdflib import Graph, Namespace, RDF, RDFS, OWL, SKOS, Literal

# --- Ancrage automatique sur '02-Donnees' ---
CURRENT_SCRIPT_PATH = Path(__file__).resolve()

DATA_DIR = None
for parent in CURRENT_SCRIPT_PATH.parents:
    if parent.name == "02-Donnees":
        DATA_DIR = parent
        break

if not DATA_DIR:
    DATA_DIR = CURRENT_SCRIPT_PATH.parents[2]

# Arborescence réelle confirmée
PHASE0_DIR = DATA_DIR / "Phase0"
TBOX_DIR = DATA_DIR / "Referential_TBox"

# Exacts chemins d'accès GitHub/Disque
SOURCE_LEXIQUE_MD = PHASE0_DIR / "4-App_publication_md" / "Lexiques" / "PUBLICATION_LEXIQUE_GLOBAL.md"
SOURCE_VAULT_TTL = PHASE0_DIR / "3-App_Referential_Vault"

TBOX_MD_MASTER = TBOX_DIR / "App_Publication.md"
TBOX_TTL_OUTPUT = TBOX_DIR / "ONTOLOGY_TBOX.ttl"

EX = Namespace("http://example.org/dkg/ontology#")
SKOS_NS = Namespace("http://www.w3.org/2004/02/skos/core#")

def ensure_directories():
    TBOX_DIR.mkdir(parents=True, exist_ok=True)

def migrate_lexique_md():
    """Rapatrie PUBLICATION_LEXIQUE_GLOBAL.md et y insère les notions TBox/ABox."""
    ensure_directories()
    
    if not SOURCE_LEXIQUE_MD.exists():
        print(f"❌ Source Lexique introuvable à : {SOURCE_LEXIQUE_MD}")
        return False

    print(f"📥 Lecture de [{SOURCE_LEXIQUE_MD.relative_to(PHASE0_DIR)}]")
    content = SOURCE_LEXIQUE_MD.read_text(encoding="utf-8")

    tbox_def = "* **TBox (Terminological Box)** : Schéma formel du domaine définissant le vocabulaire, les concepts (Classes), leurs hiérarchies (Sous-classes) et les règles d'association (Propriétés/Relations). C'est le contrat de structure immuable du graphe.\n"
    abox_def = "* **ABox (Assertional Box)** : Données réelles et instances concrètes (équipements, adresses IP, identifiants CVE, règles de sécurité) constituant la mémoire opérationnelle.\n"

    if "TBox" not in content or "ABox" not in content:
        print("  ├─ ➕ Injection des notions TBox et ABox dans le Lexique...")
        first_bullet = re.search(r"(\n\*\s+\*\*)", content)
        if first_bullet:
            idx = first_bullet.start()
            content = content[:idx] + "\n" + tbox_def + abox_def + content[idx:]
        else:
            content = tbox_def + abox_def + "\n" + content

    TBOX_MD_MASTER.write_text(content, encoding="utf-8")
    print(f"  └─ ✅ Fichier maître [Referential_TBox/App_Publication.md] créé ({len(content)} car).")
    return True

def parse_markdown_lexicon_to_skos(graph: Graph):
    """Extrait les termes pour la TBox RDF machine."""
    if not TBOX_MD_MASTER.exists():
        return

    content = TBOX_MD_MASTER.read_text(encoding="utf-8")
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

    print(f"  └─ ✅ {count} concepts SKOS synchronisés depuis le Markdown.")

def executer_migration_phase0():
    print("🚀 Début de la migration Phase 0 -> Referential_TBox...")
    ensure_directories()
    
    # 1. Migration Lexique Markdown
    if not migrate_lexique_md():
        print("🛑 Migration annulée (Lexique MD introuvable).")
        return

    # 2. Consolidation Turtle (TTL) depuis 3-App_Referential_Vault
    print(f"🔄 Exploration des ontologies dans [{SOURCE_VAULT_TTL.relative_to(PHASE0_DIR)}]...")
    unified_graph = Graph()
    
    unified_graph.bind("ex", EX)
    unified_graph.bind("owl", OWL)
    unified_graph.bind("rdfs", RDFS)
    unified_graph.bind("skos", SKOS_NS)

    ttl_count = 0
    if SOURCE_VAULT_TTL.exists():
        for ttl_file in SOURCE_VAULT_TTL.rglob("*.ttl"):
            # Exclude Lexique TTL if they are in subdirectories or redundant
            if "Archive" not in ttl_file.parts:
                print(f"  ├─ Parsing TTL : {ttl_file.relative_to(PHASE0_DIR)}")
                try:
                    unified_graph.parse(location=str(ttl_file), format="turtle")
                    ttl_count += 1
                except Exception as e:
                    print(f"  ❌ Erreur de parsing sur {ttl_file.name} : {e}")
    else:
        print(f"⚠️ Répertoire Vault introuvable : {SOURCE_VAULT_TTL}")

    # 3. Synchronisation SKOS depuis le Lexique
    parse_markdown_lexicon_to_skos(unified_graph)

    # 4. Enregistrement final
    unified_graph.serialize(destination=str(TBOX_TTL_OUTPUT), format="turtle")
    
    classes_count = len(list(unified_graph.subjects(RDF.type, OWL.Class)))
    print(f"✅ Migration terminée avec succès !")
    print(f"  ├─ Master Markdown : {TBOX_MD_MASTER}")
    print(f"  └─ Master TTL : {TBOX_TTL_OUTPUT} ({ttl_count} fichiers fusionnés, {classes_count} classes OWL).")

if __name__ == "__main__":
    executer_migration_phase0()
