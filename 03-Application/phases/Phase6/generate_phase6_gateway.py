"""
03-Application/phases/Phase6/generate_phase6_gateway.py
Pipeline d'exécution de la Phase 6 : Validation & Exécution des payloads SPARQL.

Rév. 2026-11-25 (étape 3, vague 3) — v2.3 : RELOGEMENT de la passerelle P6
hors de Snapshots_Phases (zone vouée à l abrogation) vers la zone Master
TLP_GREEN_API_Gateway : journal d audit HAB_3 (PATH_P6_GATEWAY_LOG) et
résultats de recette (PATH_P6_EXECUTION_RESULTS) vivent désormais au
Master Transversal. Écriture DIRECTE (GOU_2 v2.3), plus de relais snapshot.
"""

import sys
from pathlib import Path

# 1. Ancrage SSOT : Répertoire 03-Application dans sys.path
DIR_APP = Path(__file__).resolve().parent.parent.parent
if str(DIR_APP) not in sys.path:
    sys.path.insert(0, str(DIR_APP))

# 2. Imports des modules standards et tiers
import json
import logging

# 3. Imports SSOT et sous-modules applicatifs
from core.config import (
    INPUT_P6_QUERY_PAYLOAD,
    PATH_P6_GATEWAY_LOG,
    PATH_P6_EXECUTION_RESULTS
)
from phases.Phase6.p6_schemas import SPARQLQueryRequest
from phases.Phase6.api_gateway import APIGateway

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

    # Capitalisation directe au Master TLP:GREEN (GOU_2 v2.3, relogement acté)
    results_output = PATH_P6_EXECUTION_RESULTS
    results_output.parent.mkdir(parents=True, exist_ok=True)
    with open(results_output, "w", encoding="utf-8") as f:
        json.dump(execution_summary, f, indent=2, ensure_ascii=False)

    logging.info(f"Résultats de recette écrits au Master TLP:GREEN : {results_output}")
    logging.info(f"Journal d'audit mis à jour : {PATH_P6_GATEWAY_LOG}")
    logging.info("=== FIN PIPELINE PHASE 6 : SUCCÈS ===")


if __name__ == "__main__":
    run_phase6_pipeline()
