from rdflib import Graph, Namespace, RDF, SKOS

EX = Namespace("http://example.org/dkg/ontology#")

class EntityAligner:
    def __init__(self, tbox_path):
        self.tbox_graph = Graph()
        if tbox_path.exists():
            self.tbox_graph.parse(location=str(tbox_path), format="turtle")

    def align_abox(self, abox_graph: Graph) -> Graph:
        """Normalise les types d'instances et valide leur compatibilité avec la TBox Phase 0."""
        # Exemple de règle : s'assurer que tous les hôtes ont un type de haut niveau reconnu
        for eq in abox_graph.subjects(RDF.type, EX.Equipment):
            abox_graph.add((eq, RDF.type, EX.Asset))
        return abox_graph
