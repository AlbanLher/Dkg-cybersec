# 03-Application/core/hitm_gateway.py
"""
Passerelle Human-in-the-Middle (HitM) souveraine (Phase 8).
EXG-MET-P8-DEM_5 (audit trail), EXG-MET-P8-DEM_6 (capacité centrale),
EXG-MET-P8-RES_1 (Seed/Reset). Deux interfaces :
  - CLI (pipelines) : request_human_validation() — préservé à l'identique.
  - API (démonstrateur) : approve_and_merge / reject / reset_demo — fusion
    idempotente dans le WORKING SET uniquement (jamais le Master ni les seeds).
"""

import hashlib
import logging
import os
import re
from datetime import datetime, timezone
from pathlib import Path

from rdflib import Graph

import core.config as settings

logger = logging.getLogger("hitm_gateway")


# ==============================================================================
# INTERFACE CLI (préservée à l'identique — pipelines Phase 3-8)
# ==============================================================================
def request_human_validation(delta_path: Path) -> bool:
    print(f"\n[HitM Gateway] === CONTRÔLE HUMAIN REQUIS ===")
    print(f"[HitM Gateway] Analyse du fichier de delta : {delta_path}")

    # Affichage du contenu du delta à valider
    if delta_path.exists():
        print("\n" + "─" * 50)
        print("📄 PROPOSITION D'INJECTION DANS LE GRAPHE (SOC_1) :")
        with open(delta_path, "r", encoding="utf-8") as f:
            content = f.read()
            print(content if content.strip() else "  (Delta vide / Aucun ajout)")
        print("─" * 50 + "\n")

    if os.getenv("HITM_AUTO_APPROVE") == "1":
        print("[HitM Gateway] Mode automatique activé (CI/Test) -> Validation accordée.")
        return True

    response = input("[HitM Gateway] Souhaitez-vous valider l'injection de ces triplets dans la TBox Master ? (oui/non) : ").strip().lower()
    return response in ["oui", "o", "yes", "y"]


# ==============================================================================
# INTERFACE API — DÉMONSTRATEUR (EXG-MET-P8-DEM_5/DEM_6, RES_1)
# ==============================================================================
def _audit(action: str, decision: str, delta_ttl: str) -> None:
    """EXG-MET-P8-DEM_5 : événement horodaté UTC + empreinte SHA-256 du delta."""
    log_path = settings.WORKSET_HITL_AUDIT_LOG_PATH
    log_path.parent.mkdir(parents=True, exist_ok=True)
    fp = hashlib.sha256(delta_ttl.encode("utf-8")).hexdigest()[:12] if delta_ttl else "-"
    ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"[{ts}] {action} user_click='{decision}' delta_sha256={fp}\n")


def validate_delta(delta_ttl: str) -> bool:
    """EXG-FWK-P1-GOU_22 : tout delta doit être parsable rdflib avant fusion."""
    try:
        Graph().parse(data=delta_ttl, format="turtle")
        return True
    except Exception as err:
        logger.warning("Delta non parsable : %s", err)
        return False


def approve_and_merge(delta_ttl: str) -> dict:
    """
    EXG-MET-P8-DEM_3 : fusion UNIQUEMENT sur appel explicite (clic humain).
    Cible : WORKING SET (jamais le Master ni les seeds — EXG-MET-P8-RES_1).
    Idempotent : tous les sujets dkg: déclarés du delta déjà présents => NOOP tracé.
    """
    if not delta_ttl.strip():
        _audit("HITL_APPROVE", "REJECT(empty)", delta_ttl)
        return {"status": "REJECTED", "message": "Delta TBox vide."}
    if not validate_delta(delta_ttl):
        _audit("HITL_APPROVE", "REJECT(unparsable)", delta_ttl)
        return {"status": "REJECTED",
                "message": "Delta TBox invalide (parse rdflib échoué) — fusion refusée."}

    # EXG-MET-P8-DEM_3/GOU_5 : détection idempotente insensible à la forme
    # sérialisée de owl: (préfixe "owl:" OU URI complète
    # <http://www.w3.org/2002/07/owl#...>) — tout delta parsable déjà fusionné
    # est détecté, jamais réécrit en doublon.
    decl = r"^(dkg:\w+)\s+a\s+(?:owl:|<https?://www\.w3\.org/2002/07/owl#)"
    working = settings.WORKSET_TBOX_PATH
    existing = working.read_text(encoding="utf-8") if working.exists() else ""
    subjects = re.findall(decl, delta_ttl, flags=re.M)
    already = [s for s in subjects
               if re.search(rf"^{re.escape(s)}\s+a\s+"
                            rf"(?:owl:|<https?://www\.w3\.org/2002/07/owl#)",
                            existing, flags=re.M)]
    if subjects and len(already) == len(subjects):
        _audit("HITL_APPROVE", "NOOP(already-merged)", delta_ttl)
        return {"status": "NOOP",
                "message": "Propriété(s) déjà déclarée(s) dans le working set — "
                           "fusion idempotente, aucun doublon écrit."}

    working.parent.mkdir(parents=True, exist_ok=True)
    with open(working, "a", encoding="utf-8") as f:
        f.write("\n" + delta_ttl)
    _audit("HITL_APPROVE", "APPROVE", delta_ttl)
    return {"status": "SUCCESS",
            "message": "Delta validé (rdflib) et fusionné dans le WORKING SET "
                       "(TLP:AMBER). Validation humaine journalisée."}


def reject(delta_ttl: str) -> dict:
    """EXG-MET-P8-DEM_3 : le rejet est une issue explicite et traçable."""
    _audit("HITL_REJECT", "REJECT(by-operator)", delta_ttl)
    return {"status": "REJECTED",
            "message": "Proposition rejetée par l'opérateur — décision journalisée."}


def reset_demo() -> dict:
    """EXG-MET-P8-RES_1 : recopie seed -> working set ; seeds JAMAIS modifiés."""
    pairs = [
        (settings.SEED_TBOX_DEMO_PATH, settings.WORKSET_TBOX_PATH),
        (settings.SEED_RULES_DEMO_PATH, settings.WORKSET_RULES_PATH),
    ]
    copied = []
    for src, dst in pairs:
        if not src.exists():
            raise FileNotFoundError(f"Seed manquant : {src} — posez le pack §29.")
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
        copied.append(dst.name)
    if settings.WORKSET_CTI_BUFFER_PATH.exists():
        settings.WORKSET_CTI_BUFFER_PATH.write_text(
            "# CTI buffer vide — sélectionnez des sources TLP:CLEAR.\n", encoding="utf-8")
    if settings.WORKSET_HITL_AUDIT_LOG_PATH.exists():
        settings.WORKSET_HITL_AUDIT_LOG_PATH.unlink()
    _audit("HITL_RESET", "WORKSET-RESTORED", "")
    return {"status": "SUCCESS",
            "message": f"Working set restauré depuis les seeds ({', '.join(copied)}) — "
                       "buffer CTI purgé, audit réinitialisé."}


def ensure_workset_initialized() -> None:
    """Au premier accès API : working set absent => reset automatique depuis les seeds."""
    if not settings.WORKSET_TBOX_PATH.exists():
        reset_demo()
