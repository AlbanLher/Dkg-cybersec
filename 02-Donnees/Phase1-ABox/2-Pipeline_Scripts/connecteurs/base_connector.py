from abc import ABC, abstractmethod
from pathlib import Path
from rdflib import Graph, Namespace

EX = Namespace("http://example.org/dkg/ontology#")
INST = Namespace("http://example.org/dkg/instance#")

class BaseConnector(ABC):
    def __init__(self, file_path: Path):
        self.file_path = file_path

    @abstractmethod
    def extract_to_abox(self, graph: Graph) -> Graph:
        """Extrait les instances depuis le fichier source et alimente le graphe ABox."""
        pass
