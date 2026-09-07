"""
03-Application/Phase5/reasoning_engine.py

Moteur de Raisonnement Sémantique (Reasoning Engine) - Phase 5 / Vague 3
Conforme aux règles SSOT, Replay, Auto-Documentation et En-têtes Turtle.
"""

import logging
import sys
import time
import shutil
from pathlib import Path
from rdflib import Graph, Literal, RDF, RDFS, OWL, SKOS

# Ancrage dynamique du dossier 03-Application dans le PYTHONPATH
APP_DIR = Path(__file__).resolve().parent.parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))


from config import (
    ABOX_RED_PATH,
    ABOX_CTI_PATH,
    ABOX_INFERED_PATH,
    DIR_SNAPSHOT_P5,
    DIR_INFERED_RED,
    DOC_INFERED_MD_PATH,
    DKG_TBOX,
    DKG_CTI,
    DKG_DATA,
    SH,
    XSD
)

TB = "`" * 3  # Évite toute rupture de bloc Markdown/Triple-Backticks

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
        self._bind_namespaces(self.graph_input)
        self._bind_namespaces(self.graph_infered)

    def _bind_namespaces(self, graph: Graph):
        """Injecte l'intégralité des préfixes obligatoires."""
        graph.bind("dkg", DKG_TBOX)
        graph.bind("dkg-data", DKG_DATA)
        graph.bind("dkg-cti", DKG_CTI)
        graph.bind("sh", SH)
        graph.bind("xsd", XSD)
        graph.bind("rdfs", RDFS)
        graph.bind("skos", SKOS)
        graph.bind("rdf", RDF)
        graph.bind("owl", OWL)

    def load_graphs(self) -> None:
        """Charge la ABox Interne (TLP:RED) et la ABox CTI (TLP:CLEAR)."""
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
        """Règle R-01 : Qualification d'un Actif à Haut Risque (CISA KEV)."""
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
            self.graph_input.add(triple)

        added = len(self.graph_infered) - initial_count
        logger.info(f"Règle R-01 (CISA KEV) appliquée : {added} faits déduits.")
        return added

    def apply_rule_r02_silent_cascade(self) -> int:
        """Règle R-02 : Inférence du Chemin Cascade (Silent Cascade)."""
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
        """Exécute le pipeline de raisonnement."""
        start_time = time.time()
        logger.info("=== Démarrage du Moteur d'Inférence DKG (Phase 5) ===")

        self.load_graphs()
        self.apply_rule_r01_cisa_kev()
        self.apply_rule_r02_silent_cascade()

        execution_time = time.time() - start_time
        logger.info(f"Inférence terminée avec succès en {execution_time:.3f} secondes.")

        return execution_time

    def save_and_document(self) -> None:
        """Matérialise le graphe déduit et génère la documentation (Replay & Auto-Doc)."""
        DIR_SNAPSHOT_P5.mkdir(parents=True, exist_ok=True)
        DIR_INFERED_RED.mkdir(parents=True, exist_ok=True)

        snapshot_ttl = DIR_SNAPSHOT_P5 / ABOX_INFERED_PATH.name
        snapshot_md = DIR_SNAPSHOT_P5 / DOC_INFERED_MD_PATH.name

        # 1. Sauvegarde Turtle Snapshot
        self._bind_namespaces(self.graph_infered)
        self.graph_infered.serialize(destination=str(snapshot_ttl), format="turtle")
        logger.info(f"[📦] Snapshot TTL généré : {snapshot_ttl}")

        # 2. Génération Documentation Markdown
        md_content = f"""# 📑 Livrable Phase 5 - Raisonnement Sémantique & Inférences

**Classification :** `TLP:RED`  
**Nombre de faits déduits :** `{len(self.graph_infered)}`

---

## 📖 Glossaire & Table des Acronymes Métier

| Acronyme | Définition Complète | Contextualisation DKG |
| :--- | :--- | :--- |
| **CISA** | Cybersecurity and Infrastructure Security Agency | Agence fournissant le catalogue KEV. |
| **KEV** | Known Exploited Vulnerabilities | Base des vulnérabilités activement exploitées. |
| **RBox** | Relationship Box | Moteur d'inférence de propriétés et cascades. |
| **TLP** | Traffic Light Protocol | Protocole de ségrégation des données. |

---

## 🔄 Cascade d'Inférence Sémantique (R-01 & R-02)

{TB}mermaid
flowchart TD
    CVE[dkg:Vulnerability] -->|isCisaKev true| R1[Règle R-01 CISA KEV]
    R1 --> ASSET[dkg:HighRiskAsset]
    ASSET -->|connectsTo+| R2[Règle R-02 Silent Cascade]
    R2 --> TARGET[dkg:exposesToCascade Target]
{TB}

*Document généré automatiquement post-inférence.*
"""
        with open(snapshot_md, "w", encoding="utf-8") as f:
            f.write(md_content)
        logger.info(f"[📦] Snapshot MD généré : {snapshot_md}")

        # 3. Capitalisation Replay vers Master
        shutil.copy(snapshot_ttl, ABOX_INFERED_PATH)
        DOC_INFERED_MD_PATH.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(snapshot_md, DOC_INFERED_MD_PATH)
        logger.info(f"[✅] Synchronisation Master effectuée vers {DIR_INFERED_RED}")


def main():
    engine = ReasoningEngine()
    engine.run_inference()
    engine.save_and_document()


if __name__ == "__main__":
    main()
