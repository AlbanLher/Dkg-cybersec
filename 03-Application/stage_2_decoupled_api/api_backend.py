import sys
from pathlib import Path

# 1. Ajout du dossier Phase7 au chemin Python pour trouver les agents et l'orchestrateur
phase7_path = Path(__file__).resolve().parent.parent / "Phase7"
sys.path.append(str(phase7_path))

# 2. Ajout du dossier parent (03-Application) pour trouver config.py
sys.path.append(str(Path(__file__).resolve().parent.parent))

from config import INPUT_RESIDENTIAL_JSON_PATH, ABOX_RESIDENTIAL_PATH, SECURE_INPUT_RESIDENTIAL_PATH, SECURE_ABOX_RESIDENTIAL_PATH
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Query
from home_soc_orchestrator import HomeSOCOrchestrator
from local_inventory_agent import LocalInventoryAgent
from external_cti_agent import ExternalCTIAgent

app = FastAPI(
    title="DKG-CyberSec SOC API (Phase 7)",
    description="API REST agnostique pour l'assistant SOC du foyer et l'analyse de risque résidentiel.",
    version="1.0.0"
)

# Activation de CORS pour permettre à un front-end JavaScript (React/Vue/HTML natif) d'interroger l'API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {
        "project": "DKG-CyberSec SOC Dashboard",
        "phase": "Phase 7 - Résidentiel & Micro-Agents",
        "status": "🟢 Opérationnel",
        "endpoints": ["/api/v1/inventory", "/api/v1/cti", "/api/v1/audit"]
    }

@app.get("/api/v1/inventory")
def get_inventory(source: str = Query("local", description="Source de l'inventaire : 'local' (.private) ou 'family' (cas d'école)")):
    """Récupère l'inventaire validé des actifs du foyer selon la source demandée."""
    agent = LocalInventoryAgent()
    
    # Si l'utilisateur demande explicitement le cas d'école et que le fichier public existe
    if source == "family":
        agent.input_path = INPUT_RESIDENTIAL_JSON_PATH
        agent.output_turtle_path = ABOX_RESIDENTIAL_PATH
    
    env = agent.load_and_validate_inventory()
    if not env:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la lecture de l'inventaire ({source}).")
    return {"source_mode": source, **env.model_dump()}

@app.get("/api/v1/cti")
def get_external_cti():
    """Récupère les flux CTI externes live et catalogués."""
    agent = ExternalCTIAgent()
    entries = agent.fetch_all_cti()
    # Transformation des objets pour sérialisation JSON
    serialized = [
        {
            "cve_id": e.cve_id,
            "severity": e.severity,
            "cvss_score": e.cvss_score,
            "affected_product": e.affected_product,
            "description": e.description,
            "is_cisa_kev": e.is_cisa_kev,
            "source_type": e.source_type
        }
        for e in entries
    ]
    return {"total": len(serialized), "entries": serialized}


@app.get("/api/v1/audit")
def run_soc_audit(source: str = Query("local", description="Source : 'local' ou 'family'")):
    """Exécute l'audit SOC global du foyer selon la source active."""
    try:
        orchestrator = HomeSOCOrchestrator()
        audit_results = orchestrator.run_full_audit(source=source)
        
        return {
            "status": "success",
            "source_mode": source,
            "audit_data": audit_results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'audit SOC ({source}) : {str(e)}")

from local_host_scanner import LocalHostScanner

@app.post("/api/v1/scan-local")
def trigger_local_scan():
    """Déclenche le scan du poste local et met à jour le fichier TLP:RED dans .private/."""
    try:
        scanner = LocalHostScanner()
        data = scanner.scan_current_host()
        return {
            "status": "success",
            "message": "Scan du poste local effectué avec succès (TLP:RED stocké en zone sécurisée).",
            "scanned_data": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du scan local : {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api_backend:app", host="127.0.0.1", port=8000, reload=True)
