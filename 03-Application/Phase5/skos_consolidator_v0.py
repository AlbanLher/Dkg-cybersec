"""
03-Application/Phase5/skos_consolidator.py

Consolidateur Sémantique SKOS & TBox - Phase 5 / Vague 2 & 3
Conforme à SPEC-TECH-P05 et config.py.

Rôles principaux :
1. Charger les alignements générés par l'Agent MITM.
2. Appliquer les règles de réconciliation SPARQL CONSTRUCT (R-MITM-01).
3. Matérialiser le thésaurus SKOS réconcilié dans DKG_SKOS_Master.ttl / Master TBox[cite: 2].
"""

import logging
import sys
from pathlib import Path
from rdflib import Graph, URIRef, SKOS, RDF, RDFS, OWL

from config import (
    DIR_TBOX_AMBER,
    DIR_SNAPSHOT_P5,
    TBOX_MASTER_PATH,
    SKOS_MASTER_PATH,
    ABOX_RED_PATH,
    ABOX_CTI_PATH,
    DKG_TBOX,
    DKG_DATA,
    DKG_CTI
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("SKOSConsolidator")


class SKOSConsolidator:
    def __init__(self):
        self.master_graph = Graph()
        self.skos_output_path = DIR_TBOX_AMBER / "DKG_SKOS_Master.ttl"
        self._bind_namespaces()

    def _bind_namespaces(self):
        """Lie les espaces de noms officiels au graphe de restitution."""
        self.master_graph.bind("dkg", DKG_TBOX)
        self.master_graph.bind("dkg-data", DKG_DATA)
        self.master_graph.bind("dkg-cti", DKG_CTI)
        self.master_graph.bind("skos", SKOS)
        self.master_graph.bind("owl", OWL)
        self.master_graph.bind("rdfs", RDFS)

    def load_base_tbox(self) -> None:
        """Charge la TBox principale pour appuyer la consolidation[cite: 2]."""
        if Path(TBOX_MASTER_PATH).exists():
            self.master_graph.parse(str(TBOX_MASTER_PATH), format="turtle")
            logger.info(f"TBox Master chargée depuis {TBOX_MASTER_PATH}")
        else:
            logger.warning(f"Fichier TBox Master introuvable : {TBOX_MASTER_PATH}")

    def consolidate_alignment_graph(self, alignment_graph: Graph) -> int:
        """
        Exécute la règle R-MITM-01 pour déduire les équivalences exactes (`skos:exactMatch`)
        et intégrer le sous-graphe au graphe consolidated.
        """
        logger.info("Application de la règle de consolidation R-MITM-01...")
        query = f"""
        PREFIX dkg: <{DKG_TBOX}>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>

        CONSTRUCT {{
            ?entityA owl:sameAs ?entityB .
            ?entityA skos:exactMatch ?entityB .
        }}
        WHERE {{
            ?entityA dkg:alignmentScore ?score .
            ?entityA skos:exactMatch|owl:sameAs ?entityB .
            FILTER(?score >= 0.85)
        }}
        """
        results = alignment_graph.query(query)
        initial_count = len(self.master_graph)
        
        # Injection du sous-graphe aligné et des déductions
        self.master_graph += alignment_graph
        for triple in results:
            self.master_graph.add(triple)

        added = len(self.master_graph) - initial_count
        logger.info(f"Consolidation SKOS terminée : {added} triplets ajoutés/matérialisés.")
        return added

    def save_skos_master(self) -> None:
        """
        Sauvegarde le fichier SKOS/TBox consolidé dans le répertoire TLP:AMBER[cite: 2].
        """
        #snapshot_ttl = DIR_SNAPSHOT_P3 / ABOX_CTI_PATH.name
        #g.serialize(destination=str(snapshot_ttl), format="turtle")

        skos_output_path = DIR_SNAPSHOT_P5 / SKOS_MASTER_PATH.name
        self.master_graph.serialize(destination=str(skos_output_path), format="turtle")


        # self.skos_output_path.parent.mkdir(parents=True, exist_ok=True)
        # self.master_graph.serialize(destination=str(self.skos_output_path), format="turtle")



        logger.info(f"Artefact SKOS consolidé sauvegardé avec succès dans : {self.skos_output_path}")


def main():
    consolidator = SKOSConsolidator()
    consolidator.load_base_tbox()
    consolidator.save_skos_master()


if __name__ == "__main__":
    main()
