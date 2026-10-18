# 03-Application/api/routes_phase8.py
"""
Routeur FastAPI Phase 8 — adaptateur HTTP FIN  : 0 logique métier ici).
Tout est délégué aux modules core/ (découpage v2) :
  core/local_volumes.py   — accès SSOT aux volumes locaux 
  core/cti_intake.py      — agent CTI v-live + buffer frugal 
  core/audit_engine.py    — bilan SPARQL + Gardien TBox 
  core/mermaid_views.py   — vues Mermaid (DEM_4b) — présentation pure
  core/frugality_metrics.py — abaque Green-Dev 
  core/scan_terrain.py    — terrain « scan » réel (HITL journalisé)
  core/hitm_gateway.py   — Gatekeeper HITL  — inchangé
Lectures : TBox/RBox = WORKING SET ; ABox = SEEDS ou scan .private/ ;
CTI = buffer workset (cumul frugal, seul /reset purge — RES_1).
Traçabilité : EXG-MET-P8-DEM_1, EXG-MET-P8-DEM_2, EXG-MET-P8-DEM_3, EXG-MET-P8-DEM_4b,
              EXG-MET-P8-RES_1, EXG-FWK-P8-AGE_1, EXG-FWK-P8-AGE_2, EXG-FWK-P1-GOU_22, 
              EXG-FWK-P1-GOU_5, EXG-FWK-P1-GOU_13, + EXG-MET-P8-DEM_7
"""
import json
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

import core.config as settings
from core.hitm_gateway import (approve_and_merge, reject, reset_demo,
                               ensure_workset_initialized)
from core.local_volumes import (_read, _load_abox_by_mode,
                                 _resolve_source_keywords)
from core.cti_intake import build_cti_buffer
from core.audit_engine import _generate_risk_analysis
from core.mermaid_views import (tbox_graph_mermaid, abox_graph_mermaid,
                                 _generate_superposition_mermaid)
from core.frugality_metrics import _generate_frugality_metrics
from core.scan_terrain import scan_orchestrate

router = APIRouter(prefix="/api/phase8", tags=["Phase 8 - Demonstrator MCP"])

# ------------------------------------------------------------------------------
# MODÈLES PYDANTIC V2 (frozen) — contrats API uniquement
# ------------------------------------------------------------------------------
class SourceCatalogItem(BaseModel):
    model_config = {"frozen": True}
    id: str
    label: str
    description: str = ""
    url_target: str = ""
    category: str = "CTI"
    tlp: str = "CLEAR"

class AuditRequest(BaseModel):
    model_config = {"frozen": True}
    mode: str = Field(default="foyer")
    enabled_network_sources: List[str] = Field(default_factory=list)

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

class CtiSelectRequest(BaseModel):
    model_config = {"frozen": True}
    source_ids: List[str] = Field(default_factory=list)

# ------------------------------------------------------------------------------
# ENDPOINTS — aiguillage pur : valider, déléguer, renvoyer
# ------------------------------------------------------------------------------
@router.get("/tbox")
async def get_tbox():
    # EXG-MET-P8-DEM_1 : TBox de référence (workset), affichée dès l'ouverture.
    ensure_workset_initialized()
    return {"tbox_ttl": _read(settings.WORKSET_TBOX_PATH), "tbox_source": "workset"}

@router.get("/rbox")
async def get_rbox():
    # EXG-FWK-P8-AGE_1 : règles locales (workset), zéro requête réseau.
    ensure_workset_initialized()
    return {"rbox_ttl": _read(settings.WORKSET_RULES_PATH)}

@router.post("/cti/select")
async def select_cti_sources(payload: CtiSelectRequest):
    """EXG-MET-P8-DEM_2 + FRUGALITÉ v-live : délégation à l'agent CTI
    (sonde distante des NOUVELLES sources, buffer cumulatif idempotent,
    ratios distant/local/RAM). Repli hors-ligne silencieux (GOU_13)."""
    return build_cti_buffer(payload.source_ids)

@router.get("/sources", response_model=List[SourceCatalogItem])
async def get_external_sources_catalog():
    catalog_path = settings.EXTERNAL_SOURCES_COMPLIANCE_REGISTRY_PATH
    if not catalog_path.exists():
        catalog_path = settings.EXTERNAL_SOURCES_CATALOG_PATH
    if not catalog_path.exists():
        raise HTTPException(status_code=404,
            detail=f"Catalogue non trouvé sur le chemin SSOT : {catalog_path}")
    with open(catalog_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    sources = data.get("cti_sources", data.get("sources", [])) if isinstance(data, dict) else data
    return sources if sources is not None else []

@router.post("/audit", response_model=AuditResponse)
async def run_phase8_audit(payload: AuditRequest):
    # EXG-MET-P8-DEM_2 : 0 coche => 0 requête réseau (Air-Gapped).
    ensure_workset_initialized()
    network_counter = len(payload.enabled_network_sources) if payload.enabled_network_sources else 0
    tbox_content = _read(settings.WORKSET_TBOX_PATH)
    # EXG-CONF_1 : CONFRONTATION_1 s'applique au chargement du terrain ; le
    # bilan SPARQL détecte naturellement les findings du capital local.
    abox_content = _load_abox_by_mode(payload.mode)
    cti_content = (_read(settings.WORKSET_CTI_BUFFER_PATH)
                   if settings.WORKSET_CTI_BUFFER_PATH.exists()
                   else "# CTI buffer vide — sélectionnez des sources TLP:CLEAR.")
    nl_bilan, delta_tbox = _generate_risk_analysis(abox_content, cti_content)
    return AuditResponse(tbox_ttl=tbox_content, abox_ttl=abox_content,
        cti_clear_ttl=cti_content, nl_bilan=nl_bilan,
        delta_tbox_proposed=delta_tbox, network_requests_made=network_counter)

@router.post("/tbox/merge")
async def merge_tbox_proposal(payload: MergeTBoxRequest):
    # EXG-MET-P8-DEM_3 + DEM_6 : délégation PURE à la passerelle HITL.
    result = approve_and_merge(payload.delta_ttl)
    if result["status"] == "REJECTED":
        raise HTTPException(status_code=422, detail=result["message"])
    return result

@router.post("/tbox/reject")
async def reject_tbox_proposal(payload: MergeTBoxRequest):
    # EXG-MET-P8-DEM_3 : issue [Rejeter] explicite et traçable.
    return reject(payload.delta_ttl)

@router.post("/reset")
async def reset_demonstrator():
    # EXG-MET-P8-RES_1 : retour au point de départ garanti (seeds intacts).
    # Le scan réel (.private/) n'est PAS purgé — fait d'observation durable.
    return reset_demo()

# ------------------------------------------------------------------------------
# SCAN RÉEL DU POSTE (v-real — 3e terrain, à côté de foyer/hote simulés)
# ------------------------------------------------------------------------------
@router.post("/scan")
async def scan_local_host():
    """Terrain « scan » : délégation à core/scan_terrain (HITL journalisé,
    EXG-MET-P8-DEM_7). Le routeur ne fait que traduire l'échec en HTTP."""
    try:
        return scan_orchestrate()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scan échoué : {str(e)[:120]}")

@router.get("/tbox/graph")
async def get_tbox_graph():
    """EXG-MET-P8-DEM_4b : vue Mermaid de la TBox de référence. Local-only (GOU_13).
    JAMAIS de 500 : erreur visible dans le graphe (durcissement 17.6)."""
    ensure_workset_initialized()
    return tbox_graph_mermaid()

@router.get("/abox/graph")
async def get_abox_graph(mode: str = "foyer"):
    """EXG-MET-P8-DEM_4b : vue Mermaid de l'ABox du terrain (inventaire pur —
    EXG-CONF_1 : la confrontation est un raisonnement d'audit, pas un état)."""
    return abox_graph_mermaid(mode)

@router.get("/frugality")
async def get_frugality(mode: str = "foyer"):
    """EXG-FWK-P8-AGE_2 (abaque Green-Dev) : volumes chargés vs volume
    disponible, ratio, TOP entités. Lecture pure (AGE_1)."""
    ensure_workset_initialized()                                        # RES_1
    abox = _load_abox_by_mode(mode)                                     # RES_1
    cti = (_read(settings.WORKSET_CTI_BUFFER_PATH)
           if settings.WORKSET_CTI_BUFFER_PATH.exists() else "")        # AGE_1
    return _generate_frugality_metrics(abox, cti)

# ------------------------------------------------------------------------------
# SUPERPOSITION (EXG-MET-P8-DEM_4b)
# ------------------------------------------------------------------------------
@router.get("/superposition/graph")
async def get_superposition_graph(mode: str = "foyer", equipment: str = ""):
    """EXG-MET-P8-DEM_4b : superposition TBox/ABox/CTI pour UNE alerte du
    bilan (lecture pure — aucune écriture, DEM_3). Reflète le VOLUME LOCAL
    accumulé : décocher une source ne supprime pas les données chargées."""
    ensure_workset_initialized()                                        # RES_1
    cti = (_read(settings.WORKSET_CTI_BUFFER_PATH)
           if settings.WORKSET_CTI_BUFFER_PATH.exists() else "")        # AGE_1
    abox = _load_abox_by_mode(mode)
    return {"mermaid": _generate_superposition_mermaid(abox, cti, equipment)}
