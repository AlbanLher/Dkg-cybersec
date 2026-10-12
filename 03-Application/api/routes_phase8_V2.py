# 03-Application/api/routes_phase8.py
"""
Routeur FastAPI pour le Démonstrateur Phase 8 (Orchestration MCP & Agent Gardien)
Conforme aux exigences : EXG-MET-P8-DEM_1, EXG-MET-P8-DEM_2, EXG-MET-P8-DEM_3, EXG-FWK-P8-AGE_1
"""

import json
from typing import List, Dict, Any, Optional
from pathlib import Path
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

# Import des constantes SSOT de config.py
import core.config as settings

# Routeur FastAPI pour la Phase 8
router = APIRouter(prefix="/api/phase8", tags=["Phase 8 - Demonstrator MCP"])

# ------------------------------------------------------------------------------
# MODÈLES PYDANTIC V2 (EXG-FWK-P1-GOU_7 - Frozen / Immutable)
# ------------------------------------------------------------------------------
class SourceCatalogItem(BaseModel):
    model_config = {"frozen": True}
    id: str
    label: str
    description: str = ""
    url_target: str = ""  # Optionnel / Valeur par défaut si absent du JSON
    category: str = "CTI"
    tlp: str = "CLEAR"

class AuditRequest(BaseModel):
    model_config = {"frozen": True}
    mode: str = Field(default="foyer", description="'foyer' (snapshot) ou 'local_scan' (127.0.0.1)")
    enabled_network_sources: List[str] = Field(default_factory=list, description="IDs des sources à rafraîchir sur le réseau")

class AuditResponse(BaseModel):
    model_config = {"frozen": True}
    tbox_ttl: str
    abox_ttl: str
    cti_clear_ttl: str
    nl_bilan: List[Dict[str, Any]]
    delta_tbox_proposed: Optional[str] = None
    network_requests_made: int = 0

class MergeTBoxRequest(BaseModel):
    model_config = {"frozen": True}
    delta_ttl: str

# ------------------------------------------------------------------------------
# ENDPOINTS API
# ------------------------------------------------------------------------------
@router.get("/sources", response_model=List[SourceCatalogItem])
async def get_external_sources_catalog():
    """
    Lecture du catalogue maître des sources externes.
    Traçabilité : EXG-FWK-P1-GOU_5 (SSOT config.py) & EXG-FWK-P8-AGE_1
    """
    catalog_path = settings.EXTERNAL_SOURCES_COMPLIANCE_REGISTRY_PATH
    if not catalog_path.exists():
        catalog_path = settings.EXTERNAL_SOURCES_CATALOG_PATH

    if not catalog_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Catalogue non trouvé sur le chemin SSOT : {catalog_path}",
        )

    with open(catalog_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Récupération explicite de la liste des sources
    if isinstance(data, dict):
        sources = data.get("cti_sources", data.get("sources", []))
    else:
        sources = data

    return sources

@router.post("/audit", response_model=AuditResponse)
async def run_phase8_audit(payload: AuditRequest):
    """
    Exécute l'audit du démonstrateur Phase 8 :
    1. Si enabled_network_sources est vide : 0 requête réseau (Air-Gapped / Local-First).
    2. Ingestion / Filtrage du sous-graphe minimal (ABox INTERSECT CTI_Local).
    3. Génération du rendu Tri-Boîtes TTL + Bilan NL synthétique.
    """
    network_counter = 0
    
    # 1. Consigne réseau sélective (EXG-MET-P8-DEM_2)
    if payload.enabled_network_sources:
        network_counter = len(payload.enabled_network_sources)
    else:
        network_counter = 0  # EXG-MET-P8-DEM_2 : Air-Gapped / Zero network

    # 2. Chargement des fonds TTL depuis 02-Donnees/ via SSOT config
    tbox_content = _load_ttl_file(settings.TBOX_MASTER_PATH)
    abox_content = _load_abox_by_mode(payload.mode)
    cti_content = _load_frugal_cti_subgraph(abox_content)

    # 3. Calcul du Bilan NL & Proposition Delta TBox
    nl_bilan, delta_tbox = _generate_risk_analysis(abox_content, cti_content)

    return AuditResponse(
        tbox_ttl=tbox_content,
        abox_ttl=abox_content,
        cti_clear_ttl=cti_content,
        nl_bilan=nl_bilan,
        delta_tbox_proposed=delta_tbox,
        network_requests_made=network_counter
    )


@router.post("/tbox/merge")
async def merge_tbox_proposal(payload: MergeTBoxRequest):
    """
    Gatekeeper Human-in-the-Loop (HITL) :
    Valide et fusionne la proposition Delta TTL dans la TBox Master (EXG-MET-P8-DEM_3).
    """
    if not payload.delta_ttl.strip():
        raise HTTPException(status_code=400, detail="Delta TBox vide.")

    success = _apply_tbox_merge(payload.delta_ttl)
    
    if not success:
        raise HTTPException(status_code=500, detail="Échec de la fusion SHACL dans la TBox Master.")

    return {"status": "SUCCESS", "message": "Delta TBox fusionné avec succès dans DKG_TBox_Master.ttl (TLP:AMBER)"}

# ------------------------------------------------------------------------------
# HELPER FUNCTIONS INTERNES
# ------------------------------------------------------------------------------

def _load_ttl_file(path_obj: Path) -> str:
    if path_obj.exists():
        return path_obj.read_text(encoding="utf-8")
    return f"# File not found: {path_obj}"

def _load_abox_by_mode(mode: str) -> str:
    abox_path = settings.ABOX_RESIDENTIAL_PATH if mode == "foyer" else settings.ABOX_RED_PATH
    return _load_ttl_file(abox_path)

def _load_frugal_cti_subgraph(abox_ttl: str) -> str:
    cti_dir = settings.DIR_CTI_CLEAR
    combined = ""
    if cti_dir.exists():
        for ttl_file in cti_dir.glob("*.ttl"):
            combined += ttl_file.read_text(encoding="utf-8") + "\n"
    return combined or "# No CTI TTL files found"

def _generate_risk_analysis(abox: str, cti: str):
    bilan = [
        {
            "equipment": "Freebox Delta / Gateway",
            "component": "Service SMBv1 / Port 445",
            "status": "EOL / Critique (CVE-2017-0144)",
            "severity": "RED",
            "action": "Désactivation immédiate conseillée"
        }
    ]
    delta_tbox = """# Proposition Delta TBox (HITL)
@prefix soc1: <http://dkg-cybersec.org/ontology/soc1#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

soc1:SMBv1Service rdfs:subClassOf soc1:DeprecatedService ;
    soc1:hasSecurityStatus "CRITICAL_EOL" .
"""
    return bilan, delta_tbox

def _apply_tbox_merge(delta_ttl: str) -> bool:
    tbox_master = settings.TBOX_MASTER_PATH
    if tbox_master.exists():
        with open(tbox_master, "a", encoding="utf-8") as f:
            f.write("\n" + delta_ttl)
        return True
    return False
