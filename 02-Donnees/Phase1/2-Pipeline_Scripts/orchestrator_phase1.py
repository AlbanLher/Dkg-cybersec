import sys
from pathlib import Path
from rdflib import Graph, Namespace, RDF, RDFS, SKOS

script_dir = Path(__file__).resolve().parent
if str(script_dir) not in sys.path:
    sys.path.insert(0, str(script_dir))

from connectors.json_connector import JSONInventoryConnector
from reconciliation.entity_aligner import EntityAligner

EX = Namespace("http://example.org/dkg/ontology#")
INST = Namespace("http://example.org/dkg/instance#")

def run_phase1_ingestion():
    phase1_dir = script_dir.parent
    phase0_vault = phase1_dir.parent / "Phase0" / "3-App_Referential_Vault" / "VAULT_CONSOLIDE.ttl"
    
    input_json = phase1_dir / "1-Input_Instances" / "inventory.json"
    output_abox = phase1_dir / "3-Output_ABox" / "INSTANCES_ABOX.ttl"
    output_abox.parent.mkdir(parents=True, exist_ok=True)

    print("🚀 [Phase 1] Lancement du pipeline d'ingestion des instances...")

    abox_graph = Graph()
    abox_graph.bind("ex", EX)
    abox_graph.bind("inst", INST)
    abox_graph.bind("skos", SKOS)

    # 1. Extraction JSON -> RDF ABox
    print(f"  ├─ Parsing de {input_json.name}...")
    connector = JSONInventoryConnector(input_json)
    abox_graph = connector.extract_to_abox(abox_graph)

    # 2. Alignement & Normalisation avec la TBox Phase 0
    print("  ├─ Alignement des entités avec le Vault TBox...")
    aligner = EntityAligner(phase0_vault)
    abox_graph = aligner.align_abox(abox_graph)

    # 3. Sérialisation ABox
    abox_graph.serialize(destination=str(output_abox), format="turtle")
    
    # Rapport rapide
    eq_count = len(list(abox_graph.subjects(RDF.type, EX.Equipment)))
    soft_count = len(list(abox_graph.subjects(RDF.type, EX.Software)))
    
    print(f"  └─ ✅ Extrait : {eq_count} Équipement(s), {soft_count} Logiciel(s).")
    print(f"✅ Fichier ABox généré : {output_abox.relative_to(phase1_dir.parent)}")

if __name__ == "__main__":
    run_phase1_ingestion()
