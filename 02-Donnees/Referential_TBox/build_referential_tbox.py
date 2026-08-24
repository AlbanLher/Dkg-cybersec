from pathlib import Path
from rdflib import Graph, Namespace, RDF, RDFS, OWL, SKOS

# Chemins de base
BASE_DIR = Path(__file__).resolve().parent.parent
PHASE0_ONTOLOGIES = BASE_DIR / "Phase0" / "2-Ontologie"
TBOX_OUTPUT_DIR = BASE_DIR / "Referential_TBox"
TBOX_OUTPUT_FILE = TBOX_OUTPUT_DIR / "ONTOLOGY_TBOX.ttl"

# Repertoires cibles et exclus
TARGET_SUBDIRS = ["External_Input", "Internal_Input"]
EXCLUDED_DIR = "Archive"

EX = Namespace("http://example.org/dkg/ontology#")

def build_unified_tbox():
    print("🔄 Consolidation de la TBox Transverse depuis les sources Phase 0...")
    
    unified_graph = Graph()
    
    # Binding des préfixes standards
    unified_graph.bind("ex", EX)
    unified_graph.bind("owl", OWL)
    unified_graph.bind("rdfs", RDFS)
    unified_graph.bind("skos", SKOS)

    ttl_files = []

    # 1. Collecte des fichiers TTL uniquement dans External_Input et Internal_Input
    for subdir_name in TARGET_SUBDIRS:
        target_path = PHASE0_ONTOLOGIES / subdir_name
        if target_path.exists():
            for ttl_file in target_path.rglob("*.ttl"):
                # S'assurer qu'aucun fichier contenu dans un dossier nommé Archive ne soit inclus
                if EXCLUDED_DIR not in ttl_file.parts:
                    ttl_files.append(ttl_file)
        else:
            print(f"⚠️ Repertoire introuvable : {target_path}")

    if not ttl_files:
        print(f"❌ Aucun fichier TTL valide trouvé dans {TARGET_SUBDIRS}.")
        return

    # 2. Parsing et fusion des ontologies valides
    for ttl_file in ttl_files:
        rel_path = ttl_file.relative_to(PHASE0_ONTOLOGIES)
        print(f"  ├─ Fusion de [{rel_path}]...")
        try:
            unified_graph.parse(location=str(ttl_file), format="turtle")
        except Exception as e:
            print(f"  ❌ Erreur lors du parsing de {ttl_file.name}: {e}")

    # 3. Sérialisation de la TBox Unifiée
    TBOX_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    unified_graph.serialize(destination=str(TBOX_OUTPUT_FILE), format="turtle")
    
    # Statistiques du graphe TBox
    classes_count = len(list(unified_graph.subjects(RDF.type, OWL.Class))) + \
                    len(list(unified_graph.subjects(RDF.type, RDFS.Class)))
    props_count = len(list(unified_graph.subjects(RDF.type, OWL.ObjectProperty))) + \
                  len(list(unified_graph.subjects(RDF.type, OWL.DatatypeProperty))) + \
                  len(list(unified_graph.subjects(RDF.type, RDF.Property)))

    print(f"  └─ ✅ TBox Unifiée générée : {classes_count} Classe(s), {props_count} Propriété(s).")
    print(f"✅ Fichier destination : {TBOX_OUTPUT_FILE.relative_to(BASE_DIR.parent)}")

if __name__ == "__main__":
    build_unified_tbox()
