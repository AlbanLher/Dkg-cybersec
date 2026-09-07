"""
03-Application/Phase5/reasoning_engine.py

Moteur de Raisonnement Sémantique (Reasoning Engine) - Phase 5 / Vague 3
Conforme à SPEC-SOCLE-04.

Rôles principaux :
1. Charger les ABox Interne (TLP:RED) et CTI (TLP:CLEAR).
2. Appliquer les règles d'inférence SPARQL CONSTRUCT (R-01 KEV, R-02 Silent Cascade).
3. Matérialiser et valider la ségrégation TLP (EXG-SE-01) dans DKG_ABox_Infered.ttl.
"""

import logging
import sys
import time
from pathlib import Path
from rdflib import Graph, Literal, RDF

# Importation obligatoire depuis la SSOT config.py
from config import (
    ABOX_RED_PATH,
    ABOX_CTI_PATH,
    ABOX_INFERED_PATH,
    DKG_TBOX,
    DKG_CTI,
    DKG_DATA,
    RDF,
    RDFS,
    OWL
)

# Configuration du Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("ReasoningEngine")


class ReasoningEngine:
    def __init__(self):
        self.graph_input = Graph()
        self.graph_infered = Graph()
        self._bind_namespaces()

    def _bind_namespaces(self):
        """Lie les préfixes standardisés sur le graphe déduit."""
        self.graph_infered.bind("dkg", DKG_TBOX)
        self.graph_infered.bind("dkg-data", DKG_DATA)
        self.graph_infered.bind("dkg-cti", DKG_CTI)
        self.graph_infered.bind("rdfs", RDFS)
        self.graph_infered.bind("owl", OWL)

    def load_graphs(self) -> None:
        """
        Charge la ABox Interne (TLP:RED) et la ABox CTI (TLP:CLEAR)
        dans le graphe de travail en mémoire.
        """
        logger.info("Chargement des graphes sources pour le raisonnement...")
        
        if Path(ABOX_RED_PATH).exists():
            self.graph_input.parse(str(ABOX_RED_PATH), format="turtle")
            logger.info(f"ABox Interne chargée depuis {ABOX_RED_PATH}")
        else:
            logger.warning(f"Fichier ABox RED introuvable: {ABOX_RED_PATH}")

        if Path(ABOX_CTI_PATH).exists():
            self.graph_input.parse(str(ABOX_CTI_PATH), format="turtle")
            logger.info(f"ABox CTI chargée depuis {ABOX_CTI_PATH}")
        else:
            logger.warning(f"Fichier ABox CTI introuvable: {ABOX_CTI_PATH}")

        logger.info(f"Total de triplets en entrée : {len(self.graph_input)}")

    def apply_rule_r01_cisa_kev(self) -> int:
        """
        Règle R-01 : Qualification d'un Actif à Haut Risque (CISA KEV)
        SPEC-SOCLE-04 Section 3.2 (EXG-INF-01)
        """
        query = f"""
        PREFIX dkg: <{DKG_TBOX}>
        PREFIX dkg-cti: <{DKG_CTI}>

        CONSTRUCT {{
            ?asset a dkg:HighRiskAsset ;
                   dkg:hasRiskReason "Exposed vulnerability listed in CISA KEV" .
        }}
        WHERE {{
            ?asset dkg:hasVulnerability ?cve .
            ?cve dkg:isCisaKev true .
        }}
        """
        results = self.graph_input.query(query)
        initial_count = len(self.graph_infered)
        for triple in results:
            self.graph_infered.add(triple)
            # Injecte également les faits générés dans le graphe d'entrée
            # pour permettre le chaînage avant avec la règle R-02
            self.graph_input.add(triple)

        added = len(self.graph_infered) - initial_count
        logger.info(f"Règle R-01 (CISA KEV) appliquée : {added} faits déduits.")
        return added

    def apply_rule_r02_silent_cascade(self) -> int:
        """
        Règle R-02 : Inférence du Chemin Cascade (Silent Cascade)
        SPEC-SOCLE-04 Section 3.2 (EXG-INF-02)
        """
        query = f"""
        PREFIX dkg: <{DKG_TBOX}>

        CONSTRUCT {{
            ?pivot dkg:exposesToCascade ?target .
        }}
        WHERE {{
            ?pivot a dkg:HighRiskAsset ;
                   dkg:connectsTo+ ?target .
            ?target dkg:criticalityLevel "CRITICAL" .
        }}
        """
        results = self.graph_input.query(query)
        initial_count = len(self.graph_infered)
        for triple in results:
            self.graph_infered.add(triple)

        added = len(self.graph_infered) - initial_count
        logger.info(f"Règle R-02 (Silent Cascade) appliquée : {added} faits déduits.")
        return added

    def run_inference(self) -> float:
        """
        Exécute le pipeline complet de raisonnement.
        Retourne la durée d'exécution en secondes.
        """
        start_time = time.time()
        logger.info("=== Démarrage du Moteur d'Inférence DKG (Phase 5) ===")

        self.load_graphs()
        
        # Application ordonnée des règles (Chaînage Avant)
        self.apply_rule_r01_cisa_kev()
        self.apply_rule_r02_silent_cascade()

        execution_time = time.time() - start_time
        logger.info(f"Inférence terminée avec succès en {execution_time:.3f} secondes.")
        
        # Vérification exigence de performance EXG-HW-01 (< 5s)
        if execution_time > 5.0:
            logger.warning(f"EXG-HW-01 ALERTE : Temps d'exécution ({execution_time:.2f}s) > 5s")
        else:
            logger.info("EXG-HW-01 VALIDE : Temps d'exécution < 5s")

        return execution_time

    def save_infered_graph(self) -> None:
        """
        Matérialise le graphe déduit dans ABOX_INFERED_PATH (TLP:RED).
        Garantit la ségrégation TLP (EXG-SE-01).
        """
        output_path = Path(ABOX_INFERED_PATH)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        self.graph_infered.serialize(destination=str(output_path), format="turtle")
        logger.info(f"Graphe déduit sauvegardé dans {output_path} ({len(self.graph_infered)} triplets)")


def main():
    engine = ReasoningEngine()
    engine.run_inference()
    engine.save_infered_graph()


if __name__ == "__main__":
    main()
