"""
03-Application/Test/test_phase8_soc_orchestrator.py
Tests unitaires et d'intégration pour la Phase 8 (SOC Orchestrator & Frugal Filter).
"""

import os
import sys
from pathlib import Path
import pytest
from rdflib import Graph

# Assure l'accès au répertoire parent 03-Application/
sys.path.append(str(Path(__file__).resolve().parent.parent))

# Configuration de l'environnement de test pour automatiser le HitM
os.environ["HITM_AUTO_APPROVE"] = "1"

from core.config import ABOX_MASTER_PATH
# Ajustez l'import ci-dessous si frugal_filter et soc_orchestrator sont dans Phase8 ou core
from core.frugal_engine import run_frugal_filtering
from core.soc_engine import run_soc_audit_pipeline


def test_frugal_filter_execution():
    """Vérifie que le filtre frugal génère un delta valide sans saturer la RAM."""
    delta_file = run_frugal_filtering()
    assert delta_file.exists(), "Le fichier delta buffer doit être généré."
    
    g = Graph()
    g.parse(destination=str(delta_file), format="turtle")
    assert len(g) > 0, "Le delta ne doit pas être vide."
    
    # Vérification de la limite de mémoire si configurée dans config, sinon valeur par défaut
    max_triples = getattr(config, "MAX_TRIPLES_IN_MEMORY", 50000)
    assert len(g) <= max_triples, "Le delta respecte la limite Green Dev."


def test_soc_orchestrator_pipeline(monkeypatch):
    """Vérifie le cycle complet d'orchestration avec approbation HitM simulée."""
    # S'assure que le mode auto-approve est bien pris en compte
    monkeypatch.setenv("HITM_AUTO_APPROVE", "1")
    
    report = run_soc_audit_pipeline()
    assert report["status"] == "SUCCESS", "Le pipeline d'audit doit aboutir avec succès."
    assert report["hitm_approved"] is True, "Le contrôle HitM doit être validé."
    assert report["merged"] is True, "Le delta doit être fusionné."
    
    # Vérification que le fichier de sortie ABox master contient bien des données
    assert ABOX_MASTER_PATH.exists()
    target_g = Graph()
    target_g.parse(destination=str(ABOX_MASTER_PATH), format="turtle")
    assert len(target_g) > 0
