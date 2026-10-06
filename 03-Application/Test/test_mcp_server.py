"""
03-Application/Test/test_mcp_server.py
Tests unitaires pour le serveur MCP (Model Context Protocol) central.
Valide l'enregistrement des ressources et l'exécution standardisée des outils (Tools).
"""

import sys
from pathlib import Path
import pytest

# Ajustement du path pour accéder au core
sys.path.append(str(Path(__file__).resolve().parent.parent / "core"))
from mcp_server import DKGMCPRegistry


@pytest.mark.non_regression
def test_mcp_resources_listing():
    """Vérifie que le registre expose bien les ressources de données (TLP:RED et CLEAR)."""
    resources = DKGMCPRegistry.list_resources()
    assert isinstance(resources, list), "Les ressources doivent être retournées sous forme de liste."
    assert len(resources) >= 2, "Le serveur doit exposer au moins les ressources internes et externes."
    
    uris = [r["uri"] for r in resources]
    assert "dkg://assets/internal-tlp-red" in uris, "La ressource interne TLP:RED est manquante."
    assert "dkg://cti/incoming-tlp-clear" in uris, "La ressource externe TLP:CLEAR est manquante."


@pytest.mark.non_regression
def test_mcp_tools_listing():
    """Vérifie que les outils indispensables de la Phase 8 et du simulateur sont enregistrés."""
    tools = DKGMCPRegistry.list_tools()
    assert isinstance(tools, list), "Les outils doivent être retournés sous forme de liste."
    
    tool_names = [t["name"] for t in tools]
    assert "run_simulation_benchmark" in tool_names, "L'outil simulateur doit être exposé."
    assert "run_frugal_filtering" in tool_names, "L'outil de filtrage frugal doit être exposé."
    assert "run_mitm_reconciliation" in tool_names, "L'outil Agent MITM doit être exposé."
    assert "run_soc_audit_pipeline" in tool_names, "L'outil d'orchestration SOC doit être exposé."


@pytest.mark.non_regression
def test_mcp_call_simulation_tool():
    """Teste l'appel direct de l'outil de simulation via le registre MCP avec un faible volume."""
    arguments = {"scale_factor": 100}
    result = DKGMCPRegistry.call_tool("run_simulation_benchmark", arguments)
    
    assert isinstance(result, dict), "Le résultat de l'outil MCP doit être un dictionnaire de métadonnées."
    assert result.get("status") == "SUCCESS", "L'exécution du banc d'essai via MCP doit réussir."
    assert result.get("triple_count") > 0, "Le nombre de triplets générés doit être supérieur à 0."


@pytest.mark.non_regression
def test_mcp_unknown_tool_raises_error():
    """Vérifie qu'un appel à un outil non enregistré lève bien une exception explicite."""
    with pytest.raises(ValueError, match="Outil MCP non reconnu"):
        DKGMCPRegistry.call_tool("outil_inexistant", {})
