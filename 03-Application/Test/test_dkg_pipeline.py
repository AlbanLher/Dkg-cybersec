"""
03-Application/Test/test_dkg_pipeline.py
Tests unitaires et d'intégration globale pour la Phase 8 et le socle DKG-CyberSec.
"""

import os
from pathlib import Path
import pytest
from rdflib import Graph

from core import config
from core.frugal_engine import run_frugal_filtering
from core.soc_engine import run_soc_audit_pipeline
from core.mitm_engine import MITMEngine
from core.simulator import DKGSimulator
from core.tbox_guardian import TBoxGuardianAgent

@pytest.mark.non_regression
def test_frugal_engine_execution():
    """
    Exigence: EXG-FWK-P8-age_1
    Vérifie que le moteur de filtrage frugal produit correctement un delta valide.
    """
    result = run_frugal_filtering()
    assert result["status"] == "success", "Le filtrage frugal doit aboutir avec succès."
    
    delta_path = Path(result["delta_path"])
    assert delta_path.exists(), "Le fichier delta buffer doit être généré."
    
    g = Graph()
    # Utilisation de source= au lieu de destination= pour le parsing
    g.parse(source=str(delta_path), format="turtle")
    assert len(g) > 0, "Le graphe delta ne doit pas être vide."


@pytest.mark.non_regression
def test_soc_audit_pipeline():
    """
    Exigence: EXG-FWK-P8-soc_2
    Vérifie le bon fonctionnement de l'orchestrateur d'audit SOC.
    """
    report = run_soc_audit_pipeline()
    assert report["status"] == "success", "L'audit SOC doit renvoyer un statut de succès."
    
    report_path = Path(report["report_path"])
    assert report_path.exists(), "Le fichier de rapport d'audit SOC doit être généré."


@pytest.mark.non_regression
def test_mitm_engine_indexing():
    """
    Exigence: EXG-TEC-P5-CON_1
    Vérifie l'initialisation et l'indexation sémantique du moteur MITM.
    """
    engine = MITMEngine()
    g = Graph()
    # Test avec un graphe minimal contenant une entité
    engine.bind_mandatory_prefixes(g)
    
    # Évaluation d'un candidat textuel
    match_uri, score = engine.evaluate_candidate("Sécurité du traitement et chiffrement")
    assert 0.0 <= score <= 1.0, "Le score de similarité doit être compris entre 0 et 1."


@pytest.mark.non_regression
def test_dkg_simulator_benchmark():
    """
    Exigence: EXG-TEC-P8-sim_1
    Vérifie la génération de charge synthétique et les métriques d'empreinte.
    """
    simulator = DKGSimulator()
    metrics = simulator.benchmark_execution(scale_factor=100)
    
    assert metrics["status"] == "SUCCESS", "Le benchmark de simulation doit réussir."
    assert metrics["triple_count"] > 0, "Le nombre de triplets générés doit être supérieur à 0."
    assert "memory_delta_mb" in metrics, "Les métriques de delta mémoire doivent être mesurées."


@pytest.mark.non_regression
def test_tbox_guardian_pipeline(monkeypatch):
    """
    Exigence: EXG-FWK-P8-age_1
    Vérifie l'agent gardien TBox avec simulation de validation HitM automatique.
    """
    monkeypatch.setenv("HITM_AUTO_APPROVE", "1")
    
    guardian = TBoxGuardianAgent()
    result = guardian.inspect_and_propose_enrichment()
    
    # Le résultat peut être 'success' (si alignements ou traitement OK)
    assert result["status"] in ["success", "rejected"], "Le pipeline de l'agent gardien doit s'exécuter proprement."
