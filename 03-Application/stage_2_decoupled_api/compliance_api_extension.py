"""
03-Application/stage_2_decoupled_api/compliance_api_extension.py
Extension FastAPI pour exposer le rapport de conformité RGPD (Art. 32) 
et le bilan de ressources de l'agent gardien.
"""

import json
from pathlib import Path
from fastapi import APIRouter, HTTPException
from rdflib import Graph

import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))
import core.config

router = APIRouter(prefix="/api/v1/compliance", tags=["Phase 8 - Compliance & SOC Dashboard"])


@router.get("/report", summary="Restituer l'audit de conformité RGPD et le profil de ressources")
async def get_compliance_report():
    """
    Expose le statut de l'audit de conformité (Art. 32 RGPD) basé sur le sous-ensemble TLP:CLEAR 
    et les métriques d'exécution Green-by-Design.
    """
    try:
        # Chargement du rapport de profilage des ressources
        if not config.RESOURCE_PROFILE_REPORT_PATH.exists():
            raise HTTPException(status_code=404, detail="Rapport de profilage des ressources non disponible. Exécutez l'agent gardien.")
        
        with open(config.RESOURCE_PROFILE_REPORT_PATH, "r", encoding="utf-8") as f:
            profile_metrics = json.load(f)

        # Chargement du graphe des standards TLP:CLEAR
        g = Graph()
        if config.ABOX_COMPLIANCE_STANDARDS_CLEAR_PATH.exists():
            g.parse(str(config.ABOX_COMPLIANCE_STANDARDS_CLEAR_PATH), format="turtle")

        standards_list = []
        for subj, pred, obj in g:
            standards_list.append({
                "subject": str(subj),
                "predicate": str(pred),
                "object": str(obj)
            })

        return {
            "status": "success",
            "framework": "DKG-CyberSec Phase 8",
            "compliance_scope": "RGPD Article 32 (Sécurité du traitement)",
            "resource_profiling": profile_metrics,
            "standards_triplets_count": len(standards_list),
            "standards_sample": standards_list[:5]  # Aperçu frugal
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la génération du rapport de conformité : {str(e)}")
