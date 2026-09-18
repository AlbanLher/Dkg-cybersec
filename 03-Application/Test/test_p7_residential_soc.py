# [EXG-P7-01] [EXG-P7-04] [EXG-P7-05] Tests PyTest pour l'Assistant SOC Résidentiel
import pytest
from pathlib import Path
from config import INPUT_RESIDENTIAL_JSON_PATH, ABOX_RESIDENTIAL_PATH
from Phase7.residential_models import ResidentialFamilyEnvironment
from Phase7.residential_agent import run_residential_pipeline
from Phase7.external_cti_agent import ExternalCTIAgent
from Phase7.correlation_agent import CorrelationAgent

def test_residential_pydantic_immutability():
    """Valide l'exigence d'immutabilité des modèles Pydantic V2 (frozen=True)."""
    with open(INPUT_RESIDENTIAL_JSON_PATH, "r", encoding="utf-8") as f:
        import json
        raw = json.load(f)
    env = ResidentialFamilyEnvironment(**raw)
    
    with pytest.raises(Exception):
        env.network_environment.gateway_name = "NewGateway" # Doit lever une exception car frozen=True

def test_residential_pipeline_execution():
    """Valide la bonne exécution du pipeline de génération Turtle et Master Transversal."""
    t_snap, t_master = run_residential_pipeline()
    assert t_snap.exists()
    assert t_master.exists()
    
    content = t_snap.read_text(encoding="utf-8")
    assert "dkg-data" in content
    assert "asset_win10_01" in content

def test_correlation_agent_risks():
    """Valide la détection des chemins de compromission par l'agent de corrélation."""
    with open(INPUT_RESIDENTIAL_JSON_PATH, "r", encoding="utf-8") as f:
        import json
        raw = json.load(f)
    env = ResidentialFamilyEnvironment(**raw)
    
    cti_agent = ExternalCTIAgent()
    cti_entries = cti_agent.load_cti_database()
    
    correlation = CorrelationAgent()
    risks = correlation.analyze_risks(env, cti_entries)
    
    assert len(risks) > 0
    # Vérifie la présence de l'alerte critique sur le composant exposé WAN
    critical_risk = next((r for r in risks if r.risk_level == "CRITICAL"), None)
    assert critical_risk is not None
    assert "Plex" in critical_risk.description
