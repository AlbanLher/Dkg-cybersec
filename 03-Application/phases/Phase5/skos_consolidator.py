#!/usr/bin/env python3
"""
03-Application/phases/Phase5/skos_consolidator.py

Consolidateur Sémantique SKOS - Phase 5
Script de consolidation R-MITM-01 (SPC-TEC-P5-CONSO_01 §3, EXG-TEC-P5-CON_2) :
matérialise les alignements validés (skos:exactMatch / owl:sameAs) de l'agent
MITM dans l'artefact dédié DKG_SKOS_Master.ttl (TLP:AMBER).

Rév. 2026-11-25 (étape 3, vague 3) — PROTECTION TBOX MASTER v2.3 :
CE SCRIPT NE TOUCHE PLUS JAMAIS DKG_TBox_Master.ttl. L'ancienne version
resérialisait la TBox Master ENTIÈRE (copie miroir depuis snapshot) alors
que la TBox est un artefact M1 opérateur vivant (sas), jamais régénéré par
script, et que son main() était inert (chargeait puis resérialisait sans
rien consolider — roulette de reformatage à chaque rejeu).
Vérité v2.3 conformément à la spec : l'artefact produit = DKG_SKOS_Master.ttl
(registre DÉRIVÉ des alignements consolidés, delta rejouable) — la TBox
Master reste l'œuvre de l'opérateur via les sas prévus (Gardien HITL,
jamais d'écriture automatique, DEM_3).
"""

import logging
import sys
from pathlib import Path
from rdflib import Graph, SKOS, RDF, RDFS, OWL, SH, XSD

# Ancrage dynamique du dossier 03-Application dans le PYTHONPATH
APP_DIR = Path(__file__).resolve().parent.parent.parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from core.config import (
    DIR_TBOX_AMBER,
    DKG_SKOS_MASTER_PATH,
    DKG_SKOS_MASTER_MD_PATH,
    MITM_ALIGNMENT_DEMO_PATH,
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
        self.consolidated_graph = Graph()
        self._bind_namespaces(self.consolidated_graph)

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

    def consolidate_alignment_graph(self, alignment_graph: Graph) -> int:
        """Exécute la règle R-MITM-01 : matérialise les identifiants
        réconciliés (propagation owl:sameAs / skos:exactMatch) pour tout
        alignement validé (score >= 0.85), dans le registre consolidé.
        L'entité reste indépendante si l'alignement n'est pas validé
        (EXG-TEC-P5-CON_2 : consolidation au lieu de duplication)."""
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
        initial_count = len(self.consolidated_graph)

        # Le registre capitalise le delta d'alignement TEL QUEL + les
        # déductions R-MITM-01 — jamais une copie de la TBox Master.
        self.consolidated_graph += alignment_graph
        for triple in results:
            self.consolidated_graph.add(triple)

        added = len(self.consolidated_graph) - initial_count
        logger.info(f"Consolidation SKOS terminée : {added} triplets ajoutés/matérialisés dans {DKG_SKOS_MASTER_PATH.name}.")
        return added

    def save_and_document(self) -> None:
        """Écriture DIRECTE du registre consolidé (GOU_2 v2.3) :
        DKG_SKOS_Master.ttl + documentation miroir, mêmes toit et geste.
        La TBox Master n'est ni lue à des fins de copie, ni réécrite."""
        DIR_TBOX_AMBER.mkdir(parents=True, exist_ok=True)

        # 1. Écriture DIRECTE du registre Turtle (delta des alignements)
        self._bind_namespaces(self.consolidated_graph)
        self.consolidated_graph.serialize(destination=str(DKG_SKOS_MASTER_PATH), format="turtle")
        logger.info(f"[✅] Registre SKOS écrit en direct (TLP:AMBER) : {DKG_SKOS_MASTER_PATH}")

        # 2. Documentation Markdown miroir, même toit, même geste
        md_content = f"""# 📑 Livrable Phase 5 - Registre de Consolidation SKOS (DKG_SKOS_Master)

**Classification :** `TLP:AMBER`  
**Nombre de triplets dans le registre consolidé :** `{len(self.consolidated_graph)}`

---

## 📖 Glossaire & Table des Acronymes Métier

| Acronyme | Définition Complète | Contextualisation DKG |
| :--- | :--- | :--- |
| **OWL** | Web Ontology Language | Langage d'équivalence sémantique (`owl:sameAs`). |
| **SKOS** | Simple Knowledge Organization System | Normalisation du thésaurus (alignements `skos:exactMatch`). |
| **SSOT** | Single Source of Truth | Source unique de vérité (`core/config.py`). |
| **TBox** | Terminology Box | Définition du schéma sémantique — artefact opérateur vivant, hors de portée de ce script. |

---

## 🔄 Flux de Consolidation SKOS (R-MITM-01, spec SPC-TEC-P5-CONSO_01)

{TB}mermaid
flowchart TD
    ALIGN[SKOSConsolidator] --> CONSOL[Règle R-MITM-01<br/>score >= 0.85]
    MITM[Alignement Agent MITM<br/>DKG_MITM_*.ttl] --> CONSOL
    CONSOL -->|skos:exactMatch / owl:sameAs| OUT[DKG_SKOS_Master.ttl<br/>registre consolidé TLP:AMBER]
{TB}

*Document généré automatiquement post-consolidation SKOS. La TBox Master (sas opérateur) n'est jamais réécrite par ce script.*
"""
        with open(DKG_SKOS_MASTER_MD_PATH, "w", encoding="utf-8") as f:
            f.write(md_content)
        logger.info(f"[✅] Documentation registre écrite en direct : {DKG_SKOS_MASTER_MD_PATH}")


def main():
    consolidator = SKOSConsolidator()

    # Entrée : l'artefact d'alignement produit par l'agent MITM (démo/recette)
    if not Path(MITM_ALIGNMENT_DEMO_PATH).exists():
        logger.error(
            f"Artefact d'alignement MITM introuvable : {MITM_ALIGNMENT_DEMO_PATH} — "
            "rien à consolider. Lance d'abord l'agent MITM (aucune tolérance silencieuse)."
        )
        sys.exit(1)

    alignment_graph = Graph()
    alignment_graph.parse(str(MITM_ALIGNMENT_DEMO_PATH), format="turtle")
    logger.info(f"Alignement MITM chargé depuis : {MITM_ALIGNMENT_DEMO_PATH}")

    consolidator.consolidate_alignment_graph(alignment_graph)
    consolidator.save_and_document()


if __name__ == "__main__":
    main()
