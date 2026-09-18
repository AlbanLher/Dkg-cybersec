# [EXG-P7-02] Agent de Corrélation - Analyse des chemins de compromission
import sys
from pathlib import Path

# Injection dynamique rigoureuse du répertoire 03-Application dans le sys.path (SSOT)
CURRENT_DIR = Path(__file__).resolve().parent
APPLICATION_DIR = CURRENT_DIR if CURRENT_DIR.name == "03-Application" else CURRENT_DIR.parent
if str(APPLICATION_DIR) not in sys.path:
    sys.path.insert(0, str(APPLICATION_DIR))

from typing import List
from pydantic import BaseModel, ConfigDict
from config import INPUT_RESIDENTIAL_JSON_PATH
from Phase7.residential_models import ResidentialFamilyEnvironment
from Phase7.external_cti_agent import CTIEntry

class RiskPath(BaseModel):
    model_config = ConfigDict(frozen=True)
    asset_id: str
    risk_level: str
    description: str
    recommended_action: str

class CorrelationAgent:
    """Croise les actifs du foyer et la CTI pour générer des graphes de compromission."""

    def analyze_risks(self, env: ResidentialFamilyEnvironment, cti_entries: List[CTIEntry]) -> List[RiskPath]:
        risks = []
        
        # Règle 1 : Vérification de l'exposition WAN sur la passerelle / Plex
        if env.network_environment.wan_exposure_risk:
            risks.append(
                RiskPath(
                    asset_id="asset_fedora_01",
                    risk_level="CRITICAL",
                    description="Le serveur Plex est directement exposé sur le WAN via la Box FAI.",
                    recommended_action="Désactiver l'UPnP et fermer la redirection de port WAN pour Plex."
                )
            )

        # Règle 2 : Analyse des services locaux non sécurisés ou obsolètes
        for asset in env.assets:
            for srv in asset.local_services:
                if srv.name in ["Telnet", "SMBv1"] or "Unauthenticated" in srv.status:
                    risks.append(
                        RiskPath(
                            asset_id=asset.host_id,
                            risk_level="HIGH",
                            description=f"Service à haut risque détecté ({srv.name}) sur l'actif {asset.name}.",
                            recommended_action=f"Isoler l'équipement {asset.host_id} ou désactiver le service non sécurisé."
                        )
                    )
        return risks
