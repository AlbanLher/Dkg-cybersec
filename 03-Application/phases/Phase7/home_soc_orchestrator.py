import sys
from pathlib import Path
import logging

# Ajout du dossier parent (03-Application) au chemin Python pour importer config
sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import (
    ABOX_RESIDENTIAL_PATH, 
    INPUT_RESIDENTIAL_JSON_PATH, 
    SECURE_ABOX_RESIDENTIAL_PATH, 
    SECURE_INPUT_RESIDENTIAL_PATH
)

# Import des agents locaux et externes
from local_inventory_agent import LocalInventoryAgent
from external_cti_agent import ExternalCTIAgent

logger = logging.getLogger("HomeSOCOrchestrator")


class AdvisorAgent:
    """Agent Conseil : Analyse les risques et arbitre les installations du foyer."""
    def __init__(self, assets, cti_entries):
        self.assets = assets
        self.cti_entries = cti_entries

    def evaluate_risks(self) -> list:
        reports = []
        logger.info("Analyse croisée (Actifs Foyer vs CTI Externe) en cours...")

        for asset in self.assets:
            risk_level = "FAIBLE"
            recommendations = []
            matched_threats = []

            # Recherche de correspondances et traçabilité sémantique
            for service in asset.exposed_services:
                for cti in self.cti_entries:
                    if service.lower() in cti.affected_product.lower() or cti.affected_product.lower() in service.lower():
                        risk_level = "CRITIQUE (BLOQUÉ)"
                        # On stocke sous forme de dictionnaire structuré propre
                        matched_threats.append({
                            "cve": cti.cve_id,
                            "component": cti.affected_product,
                            "service_matched": service
                        })
                        recommendations.append(f"Mettre à jour d'urgence ou fermer le service {service} (Menace CISA KEV : {cti.cve_id})")

            if not matched_threats and asset.zone == "WAN":
                risk_level = "MOYEN"
                recommendations.append("Surveiller l'exposition WAN de cet actif.")

            # Dédoublonnage propre des menaces par CVE
            unique_threats = {t["cve"]: t for t in matched_threats}.values()

            reports.append({
                "asset_name": asset.name,
                "ip": asset.ip_address,
                "zone": asset.zone,
                "risk_level": risk_level,
                "matched_threats": list(unique_threats),
                "recommendations": recommendations if recommendations else ["Aucune vulnérabilité active détectée."]
            })

        return reports


class HomeSOCOrchestrator:
    def __init__(self):
        self.inventory_agent = LocalInventoryAgent()
        self.cti_agent = ExternalCTIAgent()

    def run_full_audit(self, source: str = "local"):
        logger.info(f"=== Lancement de l'Orchestration SOC Résidentiel (Source: {source}) ===")

        # Injection dynamique de la source dans l'agent d'inventaire
        if source == "family":
            self.inventory_agent.input_path = INPUT_RESIDENTIAL_JSON_PATH
            self.inventory_agent.output_turtle_path = ABOX_RESIDENTIAL_PATH
        else:
            self.inventory_agent.input_path = SECURE_INPUT_RESIDENTIAL_PATH
            self.inventory_agent.output_turtle_path = SECURE_ABOX_RESIDENTIAL_PATH

        # 1. Chargement et validation de l'inventaire
        env = self.inventory_agent.load_and_validate_inventory()
        if not env:
            logger.error(f"Échec critique : Impossible de charger l'inventaire ({source}).")
            return []

        # Export de l'ABox Turtle correspondante
        self.inventory_agent.export_to_abox_turtle(env)

        # 2. Récupération des flux CTI live (TLP:CLEAR)
        cti_entries = self.cti_agent.fetch_all_cti()

        # 3. Exécution de l'Agent Conseil / Corrélation
        advisor = AdvisorAgent(env.household_assets, cti_entries)
        diagnostic_reports = advisor.evaluate_risks()

        logger.info("=== Audit SOC du Foyer terminé avec succès ===")
        return diagnostic_reports

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    orchestrator = HomeSOCOrchestrator()
    orchestrator.run_full_audit()
