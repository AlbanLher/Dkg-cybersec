import sys
from pathlib import Path
from rdflib import Graph, SKOS, RDFS, Namespace

# Ajouter le dossier courant 7-ScriptsSpecifiques au sys.path de Python
script_dir = Path(__file__).resolve().parent
if str(script_dir) not in sys.path:
    sys.path.insert(0, str(script_dir))

from rdflib import Graph, SKOS, RDFS, Namespace

# Imports relatifs aux sous-modules de 7-ScriptsSpecifiques
from parsers.skos_parser import parse_markdown_lexicons
from parsers.ttl_parser import parse_ttl_ontologies
from checkers.vault_coverage import check_inputs_to_vault_coverage
from checkers.neo4j_coverage import check_vault_to_cypher_coverage
from exporters.md_publisher import publish_documentation_and_reports

EX = Namespace("http://example.org/dkg/ontology#")

class Phase0Orchestrator:
    def __init__(self, root_dir: Path):
        self.root = root_dir
        self.dir_lexique = self.root / "1-Lexique"
        self.dir_ontologie = self.root / "2-Ontologie"
        self.dir_vault = self.root / "3-App_Referential_Vault"
        self.dir_graphe = self.root / "6-Graphe"

    def execute(self):
        print("🚀 [Phase 0] Lancement de l'Orchestration Structurelle...")
        
        # 1. Ingestion et Consolidation Structurelle
        graph = Graph()
        graph.bind("skos", SKOS)
        graph.bind("ex", EX)
        
        print("  ├─ Parsing des Lexiques Markdown...")
        graph = parse_markdown_lexicons(self.dir_lexique, graph)
        
        print("  ├─ Parsing des Ontologies Turtle (.ttl)...")
        graph = parse_ttl_ontologies(self.dir_ontologie, graph)

        # 2. Sérialisation Vault Consolidé
        vault_file = self.dir_vault / "VAULT_CONSOLIDE.ttl"
        graph.serialize(destination=str(vault_file), format="turtle")
        print(f"  ├─ Vault structurel sauvegardé : {vault_file.relative_to(self.root)}")

        # 3. Exécution des Vérificateurs de Couverture
        print("  ├─ Vérification 1 : Inputs -> Vault...")
        check1_res = check_inputs_to_vault_coverage(self.root, graph)

        cypher_file = self.dir_graphe / "graphe-global_schema.cypher"
        print("  ├─ Vérification 2 : Vault -> Projection Cypher...")
        check2_res = check_vault_to_cypher_coverage(graph, cypher_file)

        # 4. Publication des Documents et Rapports
        print("  └─ Génération de la documentation et du rapport...")
        publish_documentation_and_reports(self.root, graph, check1_res, check2_res)

        print("\n✅ [Phase 0 Terminée] Structure validée avec succès.")

if __name__ == "__main__":
    root_directory = Path(__file__).resolve().parent.parent
    orchestrator = Phase0Orchestrator(root_directory)
    orchestrator.execute()
