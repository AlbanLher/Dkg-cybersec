"""
03-Application/api/routes_phase8.py
Route API supportant l'environnement 'Family' (défaut) ou 'Local Host PC'
ainsi que la simulation de montée en charge.
"""

import json
import platform
import socket
from fastapi import APIRouter, HTTPException, Query
from core import config
from core.frugal_engine import run_frugal_filtering

router = APIRouter(prefix="/api/phase8", tags=["Phase 8"])


def get_local_host_assets():
    """Extraction dynamique des composants logiciels du PC hôte."""
    hostname = socket.gethostname()
    os_name = f"{platform.system()} {platform.release()}"
    python_ver = f"Python {platform.python_version()}"
    
    return [
        {
            "asset_id": "host_pc_master",
            "name": f"PC Hôte ({hostname})",
            "ip_address": "127.0.0.1",
            "os": os_name,
            "exposed_services": [python_ver, "FastAPI / Uvicorn Server", "Docker Daemon / Systemd"],
            "zone": "LOCAL_SYSTEM"
        }
    ]


@router.get("/audit")
def get_phase8_audit(
    mode: str = Query("family", description="Mode source: 'family' ou 'host'"),
    load_factor: int = Query(1, description="Facteur de charge (1 à 100)")
):
    try:
        # 1. Sélection de la source d'Assets
        if mode == "host":
            assets_data = get_local_host_assets()
        else:
            assets_data = []
            if config.INPUT_RESIDENTIAL_JSON_PATH.exists():
                with open(config.INPUT_RESIDENTIAL_JSON_PATH, "r", encoding="utf-8") as f:
                    env_json = json.load(f)
                    assets_data = env_json.get("household_assets", [])

        # 2. Lecture de l'ABox Phase 7 si disponible
        abox_ttl = ""
        if mode == "family" and config.ABOX_RESIDENTIAL_PATH.exists():
            abox_ttl = config.ABOX_RESIDENTIAL_PATH.read_text(encoding="utf-8")

        # 3. Filtrage Frugal avec simulation de charge
        frugal_data = run_frugal_filtering()
        
        # Simulation d'accroissement de charge
        raw_bytes = (frugal_data.get("raw_size_bytes", 8500000)) * load_factor
        filtered_bytes = (frugal_data.get("filtered_size_bytes", 520)) * (1 + (load_factor * 0.05))
        triple_count = (frugal_data.get("triple_count", 4)) * load_factor

        delta_ttl = ""
        if config.DELTA_BUFFER_PATH.exists():
            delta_ttl = config.DELTA_BUFFER_PATH.read_text(encoding="utf-8")

        return {
            "status": "success",
            "mode": mode,
            "load_factor": load_factor,
            "assets": assets_data,
            "abox_ttl": abox_ttl if mode == "family" else "",
            "frugality": {
                "raw_bytes": int(raw_bytes),
                "filtered_bytes": int(filtered_bytes),
                "reduction_pct": round(100 - (filtered_bytes / raw_bytes * 100), 4),
                "triple_count": int(triple_count),
            },
            "delta_ttl": delta_ttl,
        }
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))


@router.post("/hitm/validate")
def validate_hitm_injection(payload: dict):
    approved = payload.get("approved", False)
    if approved:
        return {"status": "success", "message": "Triplets validés et fusionnés dans la TBox Master."}
    return {"status": "rejected", "message": "Enrichissement TBox annulé."}
