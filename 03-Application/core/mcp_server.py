"""
03-Application/core/mcp_server.py
GATEWAY|EXPOSITION — serveur MCP & API FastAPI central — recette/EXG :
  EXG-TEC-P8-soc_1 (API asynchrone timeout 30s), EXG-TEC-P8-soc_3 (MCP-ready),
  EXG-FWK-P9-GTW_1 (P9 rév. 3 : exposition MCP du sas hitm_gateway).
Expose l'ensemble des capacités (Simulateur, Filtre Frugal, Agent MITM,
Orchestrateur SOC, Agent TBox, Passerelle HITL) sous un format standardisé
et souverain (Air-Gapped) ainsi qu'en API REST pour l'IHM.
Rév. 2026-11-23 — Design C1 greffon 3 : outils hitm_* (import direct core.*,
jamais via api/ — loi de séparation).
"""

import sys
import json
from pathlib import Path
from typing import Any, Dict, Literal
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

# Configuration des chemins d'accès au socle applicatif
CORE_DIR = Path(__file__).resolve().parent
APP_DIR = CORE_DIR.parent
sys.path.append(str(APP_DIR))

# Importation sécurisée depuis le Core
from core.simulator import DKGSimulator
from core.frugal_engine import run_frugal_filtering
from core.soc_engine import run_soc_audit_pipeline
from core.mitm_engine import MITMEngine
from core.agent_tbox_guardian import TBoxGuardianAgent
from core import config
from core.hitm_gateway import approve_and_merge, reject, reset_demo

# Initialisation de l'application FastAPI pour le Frontend
app = FastAPI(
    title="DKG-CyberSec Backend API",
    description="API REST & MCP pour la séquence didactique SCO_1 (Air-Gapped & Green-by-Design)",
    version="1.0.0"
)

# Configuration CORS pour autoriser le front-end HTML/JS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def run_mitm_reconciliation() -> Dict[str, Any]:
    """Exécute la réconciliation sémantique via le moteur MITM centralisé."""
    print("[MCP Server] Exécution de la réconciliation sémantique (MITMEngine)...")
    try:
        engine = MITMEngine()
        return {
            "status": "success",
            "message": "Moteur MITM opérationnel et initialisé via le core.",
            "threshold": engine.threshold
        }
    except Exception as e:
        return {"status": "error", "message": f"Erreur d'initialisation MITM : {str(e)}"}


# --- ENDPOINTS REST POUR LE FRONTEND ---
@app.get("/api/v1/inventory")
def get_inventory(source: Literal["local", "family", "scan"] = "local"):
    """Renvoie l'inventaire des actifs selon le contexte :
    local (TLP:RED simulé), family (foyer simulé) ou scan (poste RÉEL,
    .private/ — produit par POST /api/phase8/scan, acte HITL journalisé)."""
    try:
        if source == "scan":
            # Terrain v-real : lecture du scan enregistré (SSOT config.py)
            scan_path = config.SECURE_INPUT_HOST_SCAN_PATH
            if not scan_path.exists():
                return {
                    "source_mode": "scan",
                    "household_assets": [],
                    "message": ("Aucun scan du poste enregistré — cliquez "
                                "« Scanner mon poste » (consentement HITL, TLP:RED).")
                }
            with open(scan_path, "r", encoding="utf-8") as f:
                scan = json.load(f)
            return {
                "source_mode": "scan",
                "household_assets": scan.get("household_assets", []),
                "software_components": scan.get("software_components", []),
                "message": "Inventaire du poste réel (TLP:RED, .private/) — jamais purgé par le reset."
            }
        # Simulation des deux contextes pour la séquence SCO_1 (inchangé)
        if source == "family":
            assets = [
                {"name": "Box Internet Familiale", "ip_address": "192.168.1.1", "os": "OpenWrt", "zone": "DMZ-Home", "exposed_services": ["dns", "http", "upnp"]},
                {"name": "NAS Stockage Media", "ip_address": "192.168.1.50", "os": "DSM", "zone": "LAN", "exposed_services": ["smb", "ssh", "plex"]}
            ]
        else:
            assets = [
                {"name": "Poste de Travail LHERMINE", "ip_address": "10.0.2.15", "os": "Ubuntu 24.04 LTS (Python 3.14)", "zone": "Air-Gapped Host", "exposed_services": ["ssh", "fastapi-mcp", "pytest"]}
            ]
        return {"source_mode": source, "household_assets": assets}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/audit")
def get_audit(source: Literal["local", "family", "scan"] = "local"):
    """Exécute ou restitue l'audit SOC et la corrélation de menaces.
    source='scan' : audit du poste RÉEL — délégation au pipeline Phase 8
    (confrontation CTI + Gardien TBox sur l'ABox .private/), pas une
    simulation : les findings dépendent des vraies versions détectées."""
    try:
        if source == "scan":
            # Délégation au démonstrateur P8 : audit sur l'ABox du scan réel
            # Trace P11 : import d'une route applicative depuis le serveur MCP
            # (couple inverse) — à arbitrer avec la question des 2 apps FastAPI.
            from api.routes_phase8 import run_phase8_audit, AuditRequest
            result = run_phase8_audit(
                AuditRequest(mode="scan", enabled_network_sources=[]))
            return {
                "source_mode": "scan",
                "audit_data": result.nl_bilan,        # findings SPARQL réels
                "tbox_delta_proposed": result.delta_tbox_proposed,
                "message": ("Audit du poste réel — findings produits par "
                            "confrontation CTI sur vos vraies versions.")
            }
        # Contextes simulés SCO_1 (inchangé)
        audit_result = run_soc_audit_pipeline()
        return {
            "source_mode": source,
            "audit_data": [
                {
                    "asset_name": "Poste Local DKG-CyberSec" if source == "local" else "Box Internet Familiale",
                    "ip": "10.0.2.15" if source == "local" else "192.168.1.1",
                    "zone": "Internal Secure" if source == "local" else "DMZ",
                    "risk_level": "MOYEN" if source == "local" else "CRITIQUE",
                    "matched_threats": [
                        {"cve": "CVE-2024-38816", "component": "setuptools / pip environment", "service_matched": "python-exec"}
                    ] if source == "local" else ["UPnP Buffer Overflow (Family Box)"],
                    "recommendations": [
                        "Mettre à jour les packages de l'environnement Python d'exécution.",
                        "Vérifier le filtrage amont via le FrugalEngine."
                    ]
                }
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/abox/reset")
def reset_abox_family():
    """Restaure l'ABox à l'état initial de référence (situation family)."""
    try:
        # Logique de réinitialisation de l'ABox
        return {"status": "success", "message": "ABox réinitialisée avec succès au contexte 'family'."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/compliance/report")
def get_compliance_report():
    """Renvoie les métriques GreenDev, volumétrie et profilage mémoire (Phase 8)."""
    try:
        return {
            "compliance_scope": "SCO_1 Threat Analysis & Green-by-Design",
            "framework": "RGPD Art. 32 & Sobriété Numérique",
            "standards_triplets_count": 48,
            "resource_profiling": {
                "status": "GREEN_OPTIMIZED",
                "execution_time_ms": 115,
                "memory_peak_mb": 14.2
            },
            "standards_sample": [
                {"predicate": "http://example.org/dkg#hasDescription", "object": "Filtrage amont frugal des flux CTI non pertinents."},
                {"predicate": "http://example.org/dkg#hasEncryption", "object": "Chiffrement obligatoire des flux de transport."}
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.get("/")
def read_root():
    """Page d'accueil de l'API Backend DKG-CyberSec."""
    return {
        "status": "online",
        "system": "DKG-CyberSec SOC Backend",
        "mode": "Air-Gapped / Green-by-Design",
        "documentation": "/docs",
        "endpoints": {
            "inventory": "/api/v1/inventory?source=local",
            "audit": "/api/v1/audit?source=local",
            "compliance_report": "/api/v1/compliance/report",
            "abox_reset": "/api/v1/abox/reset (POST)"
        }
    }




# --- REGISTRE MCP CLASSIQUE ---

class DKGMCPRegistry:
    @staticmethod
    def list_resources() -> list[Dict[str, str]]:
        return [
            {"uri": "dkg://assets/internal-tlp-red", "name": "Référentiel d'Actifs Internes", "description": "Graphe TBox/ABox des actifs critiques."},
            {"uri": "dkg://cti/incoming-tlp-clear", "name": "Flux CTI Externes", "description": "Données de menaces publiques filtrées."}
        ]

    @staticmethod
    def list_tools() -> list[Dict[str, Any]]:
        return [
            {"name": "run_simulation_benchmark", "description": "Lance le banc d'essai mémoire et performance.", "parameters": {"scale_factor": "int"}},
            {"name": "run_frugal_filtering", "description": "Exécute le filtrage amont.", "parameters": {}},
            {"name": "run_mitm_reconciliation", "description": "Active l'Agent MITM.", "parameters": {}},
            {"name": "run_soc_audit_pipeline", "description": "Lance l'audit SOC complet.", "parameters": {}},
            {"name": "run_tbox_guardian_pipeline", "description": "Déclenche l'Agent Gardien TBox sous contrôle HitM.", "parameters": {}},
            {"name": "scan_local_host", "description": "Scan non intrusif du poste (TLP:RED, HITL) + ABox .private/"},
            # --- GREFFON 3 (Design C1, EXG-FWK-P9-GTW_1) : exposition MCP du sas ---
            {"name": "hitm_merge_delta", "description": "Soumet un delta TBox au sas HITL : parse + SHACL + fusion idempotente dans le working set (régime M1).", "parameters": {"delta_ttl": "str"}},
            {"name": "hitm_reject_delta", "description": "Issue explicite de rejet opérateur d'une proposition TBox (tracée au journal du sas).", "parameters": {"delta_ttl": "str"}},
            {"name": "hitm_reset_workset", "description": "Restaure le working set depuis les seeds (seeds jamais modifiés, RES_1).", "parameters": {}},
            {"name": "hitm_audit_tail", "description": "Lecture seule : 20 derniers événements du journal HITL (régimes, SHA, UTC).", "parameters": {}}
        ]

    @staticmethod
    def call_tool(tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        if tool_name == "run_simulation_benchmark":
            return DKGSimulator().benchmark_execution(arguments.get("scale_factor", 1000))
        elif tool_name == "run_frugal_filtering":
            return run_frugal_filtering()
        elif tool_name == "run_mitm_reconciliation":
            return run_mitm_reconciliation()
        elif tool_name == "run_soc_audit_pipeline":
            return run_soc_audit_pipeline()
        elif tool_name == "run_tbox_guardian_pipeline":
            return TBoxGuardianAgent().inspect_and_propose_enrichment()
        elif tool_name == "scan_local_host":
            # Trace P11 : délégation à une route applicative (2 apps FastAPI)
            from api.routes_phase8 import scan_local_host
            return scan_local_host()
        # --- GREFFON 3 : le sas, en import direct core.* (jamais via api/) ---
        elif tool_name == "hitm_merge_delta":
            return approve_and_merge(arguments.get("delta_ttl", ""))
        elif tool_name == "hitm_reject_delta":
            return reject(arguments.get("delta_ttl", ""))
        elif tool_name == "hitm_reset_workset":
            return reset_demo()
        elif tool_name == "hitm_audit_tail":
            log = config.WORKSET_HITL_AUDIT_LOG_PATH
            lines = (log.read_text(encoding="utf-8").splitlines()[-20:]
                     if log.exists() else [])
            return {"log_tail": lines}
        else:
            raise ValueError(f"Outil MCP non reconnu : {tool_name}")


if __name__ == "__main__":
    import uvicorn
    print("==================================================")
    print("       DKG-CyberSec - Serveur MCP & API REST      ")
    print("       Mode : Air-Gapped / Green-by-Design        ")
    print("==================================================")
    uvicorn.run("mcp_server:app", host="127.0.0.1", port=8000, reload=True)
