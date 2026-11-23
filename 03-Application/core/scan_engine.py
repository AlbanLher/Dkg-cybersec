# 03-Application/core/scan_engine.py
"""
Terrain « scan » (v-real) : orchestration du scan NON INTRUSIF du poste réel
(TLP:RED). HITL : ne s'exécute que sur clic explicite — le consentement est
journalisé dans l'audit trail (format gateway _audit, EXG-MET-P8-DEM_7).
Chaîne : LocalHostScanner (JSON .private/) → HostScanAboxAgent
(ABox TTL conforme TBox §29.1). La confrontation, le Gardien TBox et le HITL
s'appliquent ensuite à l'identique des seeds simulés.
Extrait de api/routes_phase8.py lors du découpage v2 (logique inchangée).
"""
from datetime import datetime, timezone
from pathlib import Path

import core.config as settings


def scan_orchestrate() -> dict:
    """Scan + matérialisation ABox + journalisation du consentement HITL.
    Lève RuntimeError (message propre à l'IHM) en cas d'échec."""
    # 0. Modules du scan réel (imports canoniques, layout core/ — règle A4)
    from core.local_host_scanner import LocalHostScanner
    from core.agent_local_host_abox import HostScanAboxAgent

    # 1. Journalisation du consentement HITL (format gateway _audit)
    log = settings.WORKSET_HITL_AUDIT_LOG_PATH
    log.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with open(log, "a", encoding="utf-8") as f:
        f.write(f"[{ts}] SCAN_APPROVE user_click='scan' delta_sha256=- "
                "detail='scan local non intrusif du poste (TLP:RED .private/)'\n")

    # 2. Scan + matérialisation ABox
    LocalHostScanner().scan_current_host()
    result = HostScanAboxAgent().run()
    if result.get("status") != "SUCCESS":
        raise RuntimeError(str(result.get("message")))
    result["mode"] = "scan"
    result["message"] = ("Scan TLP:RED enregistré dans .private/ — audit "
                        "« Poste réel » disponible. Le reset ne le purge pas.")
    return result
