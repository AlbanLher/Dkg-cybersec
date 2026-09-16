"""
03-Application/Phase6/generate_phase6_gateway.py
Pipeline d'exécution de la Phase 6 : Validation, Exécution et Synchronisation Snapshot.
"""

import sys
from pathlib import Path

# 1. Ancrage SSOT : Répertoire 03-Application dans sys.path
DIR_APP = Path(__file__).resolve().parent.parent
if str(DIR_APP) not in sys.path:
    sys.path.insert(0, str(DIR_APP))

# 2. Imports des modules standards et tiers
import json
import logging

# 3. Imports SSOT et sous-modules applicatifs
from config import (
    INPUT_P6_QUERY_PAYLOAD,
    DIR_SNAPSHOT_P6,
    PATH_P6_GATEWAY_LOG
)
from Phase6.p6_schemas import SPARQLQueryRequest
from Phase6.api_gateway import APIGateway

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def run_phase6_pipeline() -> None:
    logging.info("=== DÉBUT PIPELINE PHASE 6 : API GATEWAY & ISOLATION TLP ===")
    
    if not INPUT_P6_QUERY_PAYLOAD.exists():
        raise FileNotFoundError(f"Fichier de requêtes introuvable : {INPUT_P6_QUERY_PAYLOAD}")

    with open(INPUT_P6_QUERY_PAYLOAD, "r", encoding="utf-8") as f:
        payloads_raw = json.load(f)

    gateway = APIGateway(audit_log_path=PATH_P6_GATEWAY_LOG)
    execution_summary = []

    for idx, raw_item in enumerate(payloads_raw):
        logging.info(f"Traitement Payload #{idx + 1} - Client: {raw_item.get('client_id')}")
        
        # Validation Pydantic V2
        request_obj = SPARQLQueryRequest(**raw_item)
        
        # Exécution via la Gateway
        response_obj = gateway.execute_sparql(request_obj)
        execution_summary.append(response_obj.model_dump())

    # Replay/Snapshot - Enregistrement des résultats de recette
    snapshot_output = DIR_SNAPSHOT_P6 / "execution_results.json"
    with open(snapshot_output, "w", encoding="utf-8") as f:
        json.dump(execution_summary, f, indent=2, ensure_ascii=False)

    logging.info(f"Résultats exportés dans le Snapshot : {snapshot_output}")
    logging.info(f"Journal d'audit mis à jour : {PATH_P6_GATEWAY_LOG}")
    logging.info("=== FIN PIPELINE PHASE 6 : SUCCÈS ===")


if __name__ == "__main__":
    run_phase6_pipeline()
