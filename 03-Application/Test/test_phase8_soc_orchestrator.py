"""
tests/test_soc_orchestrator.py
Tests unitaires et d'intégration pour la Phase 8 (SOC Orchestrator & Frugal Filter).
"""

import os
import pytest
from pathlib import Path
from rdflib import Graph

# Configuration de l'environnement de test pour automatiser le HitM
os.environ["HITM_AUTO_APPROVE"] = "1"

from frugal_filter import run_frugal_filtering
from soc_orchestrator import run_soc_audit_pipeline
from config import DELTA_BUFFER_PATH, ABOX_MASTER_PATH, MAX_TRIPLES_IN_MEMORY

def test_frugal_filter_execution():
    """Vérifie que le filtre frugal génère un delta valide sans saturer la RAM."""
    delta_file = run_frugal_filtering()
    assert delta_file.exists(), "Le fichier delta buffer doit être généré."
    
    g = Graph()
    g.parse(destination=str(delta_file), format="turtle")
    assert len(g) > 0, "Le delta ne doit pas être vide."
    assert len(g) <= MAX_TRIPLES_IN_MEMORY, "Le delta respecte la limite Green Dev."

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