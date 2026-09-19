import sys, os, pytest
from pathlib import Path

# Ajustement du chemin pour inclure le répertoire Phase7
sys.path.append(str(Path(__file__).resolve().parent.parent / "Phase7"))

from home_soc_orchestrator import HomeSOCOrchestrator, AdvisorAgent
from local_inventory_agent import LocalInventoryAgent
from external_cti_agent import ExternalCTIAgent


# Détermine si on est dans un environnement CI (ex: GitHub Actions) ou si le dossier .private est absent
IS_CI = os.getenv("CI", "false").lower() == "true"
PRIVATE_DIR_EXISTS = Path(".private").exists()


@pytest.mark.skipif(IS_CI or not PRIVATE_DIR_EXISTS, reason="Fichiers d'inventaire privés non disponibles dans le runner CI GitHub")
def test_local_inventory_loading():
    """Vérifie le chargement de l'inventaire en mode local (uniquement en local)."""
    agent = LocalInventoryAgent()
    env_model = agent.load_and_validate_inventory()
    
    # Vérification du modèle global et de sa liste d'actifs interne
    assert hasattr(env_model, "household_assets")
    assert isinstance(env_model.household_assets, list)
    assert len(env_model.household_assets) > 0

def test_family_inventory_loading():
    """Vérifie le chargement de l'inventaire en mode cas d'école (famille)."""
    orchestrator = HomeSOCOrchestrator()
    # Simulation du mode family via l'orchestrator ou injection du chemin
    assets = orchestrator.run_full_audit(source="family") # Test global de l'orchestrateur
    assert isinstance(assets, list)

def test_external_cti_feed():
    """Vérifie la récupération et la structure des données CTI externes (CISA KEV)."""
    agent = ExternalCTIAgent()
    cti_entries = agent.fetch_all_cti()
    assert isinstance(cti_entries, list)
    assert len(cti_entries) > 0
    first_entry = cti_entries[0]
    assert hasattr(first_entry, "cve_id")
    assert hasattr(first_entry, "affected_product")

def test_advisor_agent_risk_evaluation():
    """Vérifie le moteur de corrélation sémantique et d'évaluation des risques via l'orchestrateur."""
    orchestrator = HomeSOCOrchestrator()
    reports = orchestrator.run_full_audit(source="local")
    
    assert isinstance(reports, list)
    for report in reports:
        assert "asset_name" in report
        assert "risk_level" in report
        assert "matched_threats" in report
        assert "recommendations" in report
