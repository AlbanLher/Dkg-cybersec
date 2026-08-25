import sys
from pathlib import Path
from rdflib import Graph, Namespace, RDF, RDFS

script_dir = Path(__file__).resolve().parent
if str(script_dir) not in sys.path:
    sys.path.insert(0, str(script_dir))

from regex_extractor import RegexEntityExtractor
from llm_extractor import LLMTripletExtractor

EX = Namespace("http://example.org/dkg/ontology#")
INST = Namespace("http://example.org/dkg/instance#")

class HybridNERPipeline:
    def __init__(self):
        self.regex_extractor = RegexEntityExtractor()
        self.llm_extractor = LLMTripletExtractor()

    def process_document(self, text: str, source_id: str, graph: Graph) -> Graph:
        print(f"  ├─ [NER Step 1] Extraction déterministe Regex...")
        graph = self.regex_extractor.extract_from_text(text, source_id, graph)

        print(f"  ├─ [NER Step 2] Extraction contextualisée LLM...")
        graph = self.llm_extractor.extract_to_graph(text, graph)

        return graph

if __name__ == "__main__":
    sample_text = """
    Rapport d'audit du serveur SRV-WEB-01 (IP: 192.168.1.50, MAC: 00:1A:2B:3C:4D:5E).
    Le serveur exécute Apache_2_4_49 qui est affecté par la vulnérabilité critique CVE-2021-41773.
    """

    graph = Graph()
    graph.bind("ex", EX)
    graph.bind("inst", INST)

    pipeline = HybridNERPipeline()
    graph = pipeline.process_document(sample_text, "report_001", graph)

    output_path = Path("02-Donnees/Phase1/3-Output_ABox/NER_INSTANCES_ABOX.ttl")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    graph.serialize(destination=str(output_path), format="turtle")

    print(f"✅ Extraction terminée et enregistrée dans : {output_path}")
