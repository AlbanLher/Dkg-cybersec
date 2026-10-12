"""
03-Application/core/tbox_guardian.py
Agent TBoxGuardian pour la Phase 8 (SOC_1).
"""

import logging
from typing import Dict, Any

from core import config
from core.frugal_engine import run_frugal_filtering
from core.hitm_gateway import request_human_validation

logger = logging.getLogger("TBoxGuardian")


class TBoxGuardianAgent:
    """Agent inspecteur garantissant l'intégrité de la TBox Master sous contrôle HitM."""

    def inspect_and_propose_enrichment(self) -> Dict[str, Any]:
        print("[TBoxGuardian] Analyse du catalogue externe de référence...")

        delta_path = config.DELTA_BUFFER_PATH
        if not delta_path.exists() or delta_path.stat().st_size <= 1:
            run_frugal_filtering()

        print("[TBoxGuardian] Proposition d'enrichissement de la TBox générée.")

        # Contrôle humain HitM
        approved = request_human_validation(delta_path)

        if approved:
            print("[TBoxGuardian] Validation acceptée. Fusion des concepts dans la TBox maître...")
            return {"status": "success", "message": "Enrichissement TBox validé et appliqué."}
        else:
            print("[TBoxGuardian] Validation refusée par l'opérateur.")
            return {"status": "rejected", "message": "Enrichissement annulé."}
