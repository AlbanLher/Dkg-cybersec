"""
03-Application/Phase5/skos_consolidator.py

Consolidateur Sémantique SKOS & TBox - Phase 5
Conforme aux règles SSOT, Replay, Auto-Documentation et SKOS intégré à TBox Master.
"""

import logging
import sys
import shutil
from pathlib import Path
from rdflib import Graph, SKOS, RDF, RDFS, OWL, SH, XSD

# Ancrage dynamique du dossier 03-Application dans le PYTHONPATH
APP_DIR = Path(__file__).resolve().parent.parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from config import (
    DIR_TBOX_AMBER,
    DIR_SNAPSHOT_P5,
    TBOX_MASTER_PATH,
    TBOX_MASTER_MD_PATH,
    DKG_TBOX,
    DKG_DATA,
    DKG_CTI
)

TB = "`" * 3  # Évite toute rupture de bloc Markdown

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("SKOSConsolidator")


class SKOSConsolidator:
    def __init__(self):
        self.master_graph = Graph()
        self._bind_namespaces(self.master_graph)

    def _bind_namespaces(self, graph: Graph):
        """Injecte tous les préfixes obligatoires."""
        graph.bind("dkg", DKG_TBOX)
        graph.bind("dkg-data", DKG_DATA)
        graph.bind("dkg-cti", DKG_CTI)
        graph.bind("sh", SH)
        graph.bind("xsd", XSD)
        graph.bind("rdfs", RDFS)
        graph.bind("skos", SKOS)
        graph.bind("owl", OWL)
        graph.bind("rdf", RDF)

    def load_base_tbox(self) -> None:
        """Charge la TBox principale (qui intègre SKOS)."""
        if Path(TBOX_MASTER_PATH).exists():
            self.master_graph.parse(str(TBOX_MASTER_PATH), format="turtle")
            logger.info(f"TBox Master chargée depuis {TBOX_MASTER_PATH}")
        else:
            logger.warning(f"Fichier TBox Master introuvable : {TBOX_MASTER_PATH}")

    def consolidate_alignment_graph(self, alignment_graph: Graph) -> int:
        """Exécute la règle R-MITM-01 et intègre les déductions au graphe TBox Master."""
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
""".strip()

        results = alignment_graph.query(query)
        initial_count = len(self.master_graph)

        self.master_graph += alignment_graph
        for triple in results:
            self.master_graph.add(triple)

        added = len(self.master_graph) - initial_count
        logger.info(f"Consolidation SKOS terminée : {added} triplets ajoutés/matérialisés dans TBox Master.")
        return added

    def save_and_document(self) -> None:
        """Sauvegarde la TBox Master enrichie selon le Principe de Replay et Auto-Doc."""
        DIR_SNAPSHOT_P5.mkdir(parents=True, exist_ok=True)
        DIR_TBOX_AMBER.mkdir(parents=True, exist_ok=True)

        snapshot_ttl = DIR_SNAPSHOT_P5 / TBOX_MASTER_PATH.name
        snapshot_md = DIR_SNAPSHOT_P5 / TBOX_MASTER_MD_PATH.name

        master_ttl = TBOX_MASTER_PATH
        master_md = TBOX_MASTER_MD_PATH

        # 1. Sauvegarde Turtle avec en-têtes
        self._bind_namespaces(self.master_graph)
        self.master_graph.serialize(destination=str(snapshot_ttl), format="turtle")
        logger.info(f"[📦] Snapshot TBox Master TTL sauvegardé : {snapshot_ttl}")

        # 2. Génération de la documentation Markdown Miroir
        md_content = f"""# 📑 Livrable Phase 5 - Consolidation SKOS au sein de TBox Master

**Classification :** `TLP:AMBER`  
**Nombre de triplets dans TBox Master :** `{len(self.master_graph)}`

---

## 📖 Glossaire & Table des Acronymes Métier

| Acronyme | Définition Complète | Contextualisation DKG |
| :--- | :--- | :--- |
| **OWL** | Web Ontology Language | Langage d'équivalence sémantique (`owl:sameAs`). |
| **SKOS** | Simple Knowledge Organization System | Normalisation du thésaurus (directement intégré dans TBox Master). |
| **SSOT** | Single Source of Truth | Source unique de vérité (`config.py`). |
| **TBox** | Terminology Box | Définition du schéma sémantique, des règles et des concepts. |

---

## 🔄 Flux de Consolidation SKOS / TBox Master

{TB}mermaid
flowchart TD
    ALIGN[Alignement Agent MITM] --> CONSOL[Règle R-MITM-01]
    TBOX_IN[DKG_TBox_Master.ttl] --> CONSOL
    CONSOL -->|skos:exactMatch / owl:sameAs| TBOX_OUT[DKG_TBox_Master.ttl Enrichi]
{TB}

*Document généré automatiquement post-consolidation SKOS dans TBox Master.*
"""
        with open(snapshot_md, "w", encoding="utf-8") as f:
            f.write(md_content)
        logger.info(f"[📦] Snapshot TBox Master MD généré : {snapshot_md}")

        # 3. Capitalisation Replay vers Master
        shutil.copy(snapshot_ttl, master_ttl)
        shutil.copy(snapshot_md, master_md)
        logger.info(f"[✅] Synchronisation TBox Master effectuée dans {DIR_TBOX_AMBER}")


def main():
    consolidator = SKOSConsolidator()
    consolidator.load_base_tbox()
    consolidator.save_and_document()


if __name__ == "__main__":
    main()
