# 03-Application/agents/local_host_abox_agent.py
# =============================================================================
# HostScanAboxAgent — matérialise le scan réel du poste en ABox TTL (TLP:RED).
# Chaîne : local_host_scanner.py (JSON .private/) → Pydantic frozen → rdflib
# → DKG_ABox_HostScan.ttl (.private/ — jamais versionné, jamais purgé par le
# reset : fait d'observation durable).
# Vocabulaire STRICTEMENT conforme à la TBox de référence (§29.1) : la
# confrontation P9 (CONFRONTATION_1), le bilan SPARQL et le Gardien TBox
# fonctionnent sur cette ABox exactement comme sur les seeds simulés.
# =============================================================================
import sys
import json
import logging
from pathlib import Path
from typing import List
from pydantic import BaseModel, Field
from rdflib import Graph, Literal, RDF, RDFS, Namespace, URIRef

sys.path.append(str(Path(__file__).resolve().parent.parent))
from core.config import (SECURE_INPUT_HOST_SCAN_PATH,
                         SECURE_ABOX_HOST_SCAN_PATH)

logger = logging.getLogger("HostScanAboxAgent")

DKG = Namespace("http://dkg.cybersec.org/tbox#")
DKG_DATA = Namespace("http://dkg.cybersec.org/data#")


# --- Modèles Pydantic V2 (frozen, extra ignore) -------------------------------
class ScannedComponentModel(BaseModel):
    component_id: str
    name: str
    version: str = "unknown"
    support_status: str = "unknown"
    model_config = {"frozen": True, "extra": "ignore"}


class ScannedAssetModel(BaseModel):
    asset_id: str
    name: str
    ip_address: str = "127.0.0.1"
    os: str = "Unknown"
    exposed_services: List[str] = Field(default_factory=list)
    zone: str = "LAN-SECURE"
    model_config = {"frozen": True, "extra": "ignore"}


class HostScanModel(BaseModel):
    household_assets: List[ScannedAssetModel]
    software_components: List[ScannedComponentModel] = Field(default_factory=list)
    model_config = {"frozen": True, "extra": "ignore"}


class HostScanAboxAgent:
    """JSON scan réel → ABox TTL (TLP:RED) dans .private/ (SSOT config.py)."""

    def __init__(self):
        self.input_path = SECURE_INPUT_HOST_SCAN_PATH
        self.output_path = SECURE_ABOX_HOST_SCAN_PATH

    def load_and_validate(self) -> HostScanModel | None:
        if not self.input_path.exists():
            logger.error(f"Scan introuvable : {self.input_path} — lancer le scan d'abord.")
            return None
        try:
            with open(self.input_path, encoding="utf-8") as f:
                raw = json.load(f)
            model = HostScanModel(
                household_assets=raw.get("household_assets", []),
                software_components=raw.get("software_components", []))
            logger.info(f"[SUCCESS] {len(model.household_assets)} actif(s), "
                        f"{len(model.software_components)} composant(s) validés.")
            return model
        except Exception as e:
            logger.error(f"Validation Pydantic du scan échouée : {e}")
            return None

    def export_to_abox_turtle(self, scan: HostScanModel) -> bool:
        """ABox conforme TBox §29.1 — même vocabulaire que les seeds
        (assetId/hostname/ipAddress/exposesService/componentId/version/
        hasTLPMarking) : la règle CONFRONTATION_1 s'applique telle quelle."""
        try:
            g = Graph()
            g.bind("dkg", DKG)
            g.bind("dkg-data", DKG_DATA)
            g.bind("xsd", Namespace("http://www.w3.org/2001/XMLSchema#"))

            tlp_red = DKG_DATA["TLP-RED"]
            g.add((tlp_red, RDF.type, DKG.TLPMarking))
            g.add((tlp_red, RDFS.label, Literal("TLP:RED", lang="en")))

            for asset in scan.household_assets:
                a = DKG_DATA["Asset-Host-Scan"]
                g.add((a, RDF.type, DKG.Asset))
                g.add((a, DKG.assetId, Literal(asset.asset_id)))
                g.add((a, RDFS.label, Literal(asset.name, lang="fr")))
                g.add((a, DKG.hostname, Literal(asset.name.split("(")[-1].rstrip(")") or asset.asset_id)))
                g.add((a, DKG.ipAddress, Literal(asset.ip_address)))
                g.add((a, DKG.hasOperatingSystem, Literal(asset.os)))
                for svc in asset.exposed_services:
                    g.add((a, DKG.exposesService, Literal(svc)))
                g.add((a, DKG.hasTLPMarking, tlp_red))
                # Composants logiciels détectés (componentId comp-* — le
                # format du fonds CTI : matching de confrontation possible)
                for i, comp in enumerate(scan.software_components):
                    c = DKG_DATA[f"Comp-Scan-{i}"]
                    g.add((c, RDF.type, DKG.SoftwareComponent))
                    g.add((c, DKG.componentId, Literal(comp.component_id)))
                    g.add((c, RDFS.label, Literal(comp.name, lang="fr")))
                    g.add((c, DKG.version, Literal(comp.version)))
                    g.add((c, DKG.supportStatus, Literal(comp.support_status)))
                    g.add((c, DKG.isComponentOf, a))
                    g.add((a, DKG.hasInstalledComponent, c))

            self.output_path.parent.mkdir(parents=True, exist_ok=True)
            g.serialize(destination=str(self.output_path), format="turtle")
            logger.info(f"[SUCCESS] ABox scan réel exportée : {self.output_path}")
            return True
        except Exception as e:
            logger.error(f"Export ABox scan échoué : {e}")
            return False

    def run(self) -> dict:
        """Pipeline complet : validation + export. Retourne le résumé."""
        scan = self.load_and_validate()
        if scan is None:
            return {"status": "ERROR", "message": "Scan JSON absent ou invalide."}
        if not self.export_to_abox_turtle(scan):
            return {"status": "ERROR", "message": "Échec de l'export ABox."}
        return {"status": "SUCCESS",
                "assets": len(scan.household_assets),
                "components": len(scan.software_components),
                "abox_path": str(self.output_path)}


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    print(json.dumps(HostScanAboxAgent().run(), indent=2, ensure_ascii=False))
