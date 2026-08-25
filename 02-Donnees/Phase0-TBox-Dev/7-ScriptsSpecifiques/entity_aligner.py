from rdflib import Graph, Namespace, RDF, RDFS, SKOS, OWL
from typing import Optional

class EntityAligner:
    def __init__(self, tbox_path: Path):
        self.tbox_graph = Graph()
        self.tbox_graph.parse(str(tbox_path), format="turtle")
        self.skos_schemes = self._load_skos_schemes()
        self.owl_classes = self._load_owl_classes()

    def _load_skos_schemes(self) -> dict:
        """Charge les schémas SKOS pour la résolution de synonymes"""
        schemes = {}
        for scheme in self.tbox_graph.subjects(RDF.type, SKOS.ConceptScheme):
            for concept in self.tbox_graph.objects(scheme, SKOS.hasTopConcept):
                pref_label = self._get_pref_label(concept)
                alt_labels = self._get_alt_labels(concept)
                schemes[str(scheme)] = {
                    "concepts": {str(concept): {"prefLabel": pref_label, "altLabels": alt_labels}}
                }
        return schemes

    def align_abox(self, abox_graph: Graph) -> Graph:
        """Aligne les instances ABox avec la TBox"""
        # 1. Résolution des synonymes via SKOS
        abox_graph = self._resolve_skos_synonyms(abox_graph)

        # 2. Validation des types
        abox_graph = self._validate_types(abox_graph)

        # 3. Déduplication
        abox_graph = self._deduplicate_instances(abox_graph)

        return abox_graph
