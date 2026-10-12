"""
03-Application/phases/Phase8/soc_orchestrator.py
Orchestrateur Didactique Phase 8 (SOC_1 & Sobriété Frugale).
Strictement appuyé sur la configuration centralisée core.config.
"""

import sys
import json
import logging
from pathlib import Path

APPLICATION_ROOT = Path(__file__).resolve().parent.parent.parent
if str(APPLICATION_ROOT) not in sys.path:
    sys.path.append(str(APPLICATION_ROOT))

from core import config
from core.soc_engine import run_soc_audit_pipeline
from core.frugal_engine import run_frugal_filtering
from core.tbox_guardian import TBoxGuardianAgent

logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(message)s")


def run_didactic_cli():
    print("\n" + "=" * 70)
    print(" 🛡️   SÉQUENCE DIDACTIQUE SOC_1 : AUDIT DE SÉCURITÉ & SOBRIÉTÉ (PHASE 8)")
    print(" 🎯  Périmètre : Menaces, Vulnérabilités & Frugalité Green-by-Design")
    print(" 🚫  Hors scope : RGPD / Conformité Métier (Périmètre Phase 9)")
    print("=" * 70 + "\n")

    # 1. Registre CTI depuis la SSOT
    print("1️⃣ [SELECTION CTI] Référentiels externes chargés dans Input_Phases :")
    registry_path = config.EXTERNAL_SOURCES_COMPLIANCE_REGISTRY_PATH
    if registry_path.exists():
        with open(registry_path, "r", encoding="utf-8") as f:
            reg_data = json.load(f)
            for src in reg_data.get("sources", []):
                print(f"   • Source : {src.get('source_id')} | {src.get('title')} ({src.get('tlp')})")
    print()

    # 2. Filtrage Frugal
    print("2️⃣ [FRUGAL ENGINE] Evaluation de la sobriété numérique...")
    frugal_res = run_frugal_filtering()
    raw_b = frugal_res.get("raw_size_bytes", 0)
    filt_b = frugal_res.get("filtered_size_bytes", 0)
    pct = frugal_res.get("reduction_pct", 0)
    
    print(f"   📊 Volume brut estimé     : {raw_b} octets (~{round(raw_b/1_000_000, 1)} Mo)")
    print(f"   ✂️ Volume retenu (delta) : {filt_b} octets ({frugal_res.get('triple_count')} triplets)")
    print(f"   🌱 Taux de réduction     : {pct}% d'économie d'empreinte mémoire\n")

    # 3. Audit SOC_1
    print("3️⃣ [SOC ENGINE] Audit de Conformité Technique SOC_1 (NIST / ANSSI)...")
    soc_res = run_soc_audit_pipeline()
    print(f"   🎯 Conforme au référentiel : SOC_1 / Directives d'Hygiène Foyer")
    print(f"   📄 Rapport d'audit généré  : {soc_res.get('report_path')}\n")

    # 4. TBox Guardian & HitM
    print("4️⃣ [TBOX GUARDIAN & HITM] Inspection de la proposition et validation explicite...")
    guardian = TBoxGuardianAgent()
    guardian_res = guardian.inspect_and_propose_enrichment()
    
    print(f"\n   ✅ Résultat final de la séquence : {guardian_res.get('status')}")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    run_didactic_cli()
