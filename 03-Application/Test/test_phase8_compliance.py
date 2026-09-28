"""
03-Application/Test/test_phase8_compliance.py
Tests unitaires pour la Phase 8 : Agent Gardien, Filtrage Frugal, 
Génération du subset Turtle TLP:CLEAR et Validation des Ressources.
"""

import sys
from pathlib import Path
import pytest
from rdflib import Graph

# Assure l'accès au SSOT config
sys.path.append(str(Path(__file__).resolve().parent.parent))
import core.config

from Phase8.compliance_steward_agent import ExternalReferenceStewardAgent


def test_registry_exists():
    """Vérifie que le fichier de registre de traçabilité existe (EXG-P8-01)."""
    assert config.EXTERNAL_SOURCES_COMPLIANCE_REGISTRY_PATH.exists(), "Le registre externe des sources est introuvable."


def test_steward_agent_execution():
    """Exécute l'agent gardien, vérifie la production du subset et le respect du Green-by-Design."""
    steward = ExternalReferenceStewardAgent()
    metrics = steward.execute_frugal_extraction()

    # Vérification des métriques de sobriété (EXG-GREEN-01)
    assert metrics["status"] == "SUCCESS"
    assert metrics["execution_time_ms"] < 2000, "L'extraction frugale dépasse le seuil de tolérance temporel."
    assert metrics["concepts_extracted"] > 0, "Aucun concept n'a été extrait du registre."

    # Vérification de l'existence du fichier Turtle TLP:CLEAR généré
    assert config.ABOX_COMPLIANCE_STANDARDS_CLEAR_PATH.exists(), "Le fichier Turtle TLP:CLEAR n'a pas été généré."

    # Vérification de la validité du graphe RDF généré
    g = Graph()
    g.parse(str(config.ABOX_COMPLIANCE_STANDARDS_CLEAR_PATH), format="turtle")
    assert len(g) > 0, "Le graphe Turtle généré est vide."

    # Vérification du rapport de profilage des ressources
    assert config.RESOURCE_PROFILE_REPORT_PATH.exists(), "Le rapport de profilage des ressources est manquant."
