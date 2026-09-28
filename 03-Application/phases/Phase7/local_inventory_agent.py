import sys
from pathlib import Path
import json
import logging
from pydantic import BaseModel, Field
from typing import List, Optional
from rdflib import Graph, Literal, RDF, URIRef, Namespace

# Ajout du dossier parent (03-Application) au chemin Python pour importer config
sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import (
    INPUT_RESIDENTIAL_JSON_PATH, 
    ABOX_RESIDENTIAL_PATH, 
    SECURE_INPUT_RESIDENTIAL_PATH, 
    SECURE_ABOX_RESIDENTIAL_PATH,
    DKG_DATA, 
    DKG_TBOX
)

logger = logging.getLogger("LocalInventoryAgent")

# -------------------------------------------------------------------------
# MODÈLE PYDANTIC V2 (Immuable frozen=True + Parser défensif implicite)
# -------------------------------------------------------------------------
class ResidentialAssetModel(BaseModel):
    asset_id: str
    name: str
    ip_address: str
    os: str
    exposed_services: List[str] = Field(default_factory=list)
    zone: str = "LAN"

    model_config = {"frozen": True, "extra": "ignore"}

class HouseholdEnvironmentModel(BaseModel):
    household_assets: List[ResidentialAssetModel] = Field(default_factory=list)

    model_config = {"frozen": True, "extra": "ignore"}


class LocalInventoryAgent:
    def __init__(self):
        # Utilisation conditionnelle : pointe vers .private/ si présent, sinon fallback sur le chemin public
        self.input_path = SECURE_INPUT_RESIDENTIAL_PATH if SECURE_INPUT_RESIDENTIAL_PATH.exists() else INPUT_RESIDENTIAL_JSON_PATH
        self.output_turtle_path = SECURE_ABOX_RESIDENTIAL_PATH if SECURE_INPUT_RESIDENTIAL_PATH.exists() else ABOX_RESIDENTIAL_PATH

    def _safe_get(self, dictionary: dict, key: str, default=None):
        """Parser défensif pour contrer toute anomalie de clé manquante."""
        val = dictionary.get(key, default)
        return val if val is not None else default

    def load_and_validate_inventory(self) -> Optional[HouseholdEnvironmentModel]:
        """Charge et valide l'inventaire brut du foyer via Pydantic V2."""
        if not self.input_path.exists():
            logger.error(f"Fichier d'inventaire introuvable : {self.input_path}")
            return None
        
        try:
            with open(self.input_path, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
            
            # Normalisation défensive des données brutes
            assets_raw = self._safe_get(raw_data, "household_assets", [])
            cleaned_assets = []
            
            for item in assets_raw:
                cleaned_item = {
                    "asset_id": self._safe_get(item, "asset_id", "unknown_id"),
                    "name": self._safe_get(item, "name", "Unnamed Asset"),
                    "ip_address": self._safe_get(item, "ip_address", "0.0.0.0"),
                    "os": self._safe_get(item, "os", "Unknown OS"),
                    "exposed_services": self._safe_get(item, "exposed_services", []),
                    "zone": self._safe_get(item, "zone", "LAN")
                }
                cleaned_assets.append(cleaned_item)

            validated_env = HouseholdEnvironmentModel(household_assets=cleaned_assets)
            logger.info(f"[SUCCESS] {len(validated_env.household_assets)} actifs validés avec succès.")
            return validated_env

        except Exception as e:
            logger.error(f"Erreur critique lors de la validation Pydantic de l'inventaire : {e}")
            return None

    def export_to_abox_turtle(self, env: HouseholdEnvironmentModel) -> bool:
        """Exporte l'environnement validé sous forme de graphe RDF/Turtle (ABox TLP:RED)."""
        try:
            g = Graph()
            g.bind("dkg_data", DKG_DATA)
            g.bind("dkg_tbox", DKG_TBOX)

            for asset in env.household_assets:
                asset_uri = DKG_DATA[asset.asset_id]
                
                # Déclaration du type d'actif
                g.add((asset_uri, RDF.type, DKG_TBOX.ResidentialAsset))
                g.add((asset_uri, DKG_TBOX.hasAssetName, Literal(asset.name)))
                g.add((asset_uri, DKG_TBOX.hasIpAddress, Literal(asset.ip_address)))
                g.add((asset_uri, DKG_TBOX.hasOperatingSystem, Literal(asset.os)))
                g.add((asset_uri, DKG_TBOX.hasNetworkZone, Literal(asset.zone)))

                for service in asset.exposed_services:
                    g.add((asset_uri, DKG_TBOX.exposesService, Literal(service)))

            # Sauvegarde dans le chemin géré par le SSOT (config.py)
            self.output_turtle_path.parent.mkdir(parents=True, exist_ok=True)
            g.serialize(destination=str(self.output_turtle_path), format="turtle")
            logger.info(f"[SUCCESS] ABox résidentielle exportée vers : {self.output_turtle_path}")
            return True

        except Exception as e:
            logger.error(f"Erreur lors de la génération du fichier Turtle ABox : {e}")
            return False


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    
    print("=== Démarrage de l'Agent d'Inventaire Local (Phase 7) ===")
    agent = LocalInventoryAgent()
    
    environment = agent.load_and_validate_inventory()
    if environment:
        success = agent.export_to_abox_turtle(environment)
        if success:
            print("=== Inventaire traité et ABox Turtle générée avec succès ===")
        else:
            print("=== Échec de l'export Turtle ===")
    else:
        print("=== Échec de la validation de l'inventaire ===")
