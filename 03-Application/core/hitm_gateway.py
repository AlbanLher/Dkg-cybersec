# 03-Application/core/hitm_gateway.py
"""
GATEWAY — sas HITL & régimes d'écriture (M1/M2/HITL) — recette/EXG :
  EXG-MET-P8-DEM_3, DEM_5, DEM_6, RES_1 ; EXG-FWK-P8-soc_1 ;
  EXG-FWK-P1-GOU_22 (parse) ; EXG-FWK-P9-GTW_1, GTW_2 (P9 rév. 3).
Le sas tient la PREUVE unique des régimes (audit SHA-256 + UTC, §4 Design C1) ;
l'écriture physique reste au module propriétaire (anti-monolithe inc_1).
Deux interfaces :
  - CLI (pipelines P3-P8) : request_human_validation() — préservé à l'identique.
  - API/MCP (démonstrateur + registre MCP) : approve_and_merge / reject /
    reset_demo / record_write — fusion dans le WORKING SET uniquement
    (jamais le Master ni les seeds, EXG-MET-P8-RES_1).
Rév. 2026-11-23 — Design C1 (impl greffons 1-2 : SHACL sur M1 + record_write).
"""

import hashlib
import logging
import os
import re
from datetime import datetime, timezone
from pathlib import Path

from rdflib import Graph
from pyshacl import validate as _pyshacl_validate

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


# ------------------------------------------------------------------------------
# GREFFON 1 (Design C1, EXG-FWK-P9-GTW_2) : M1 = écriture SHACL-validée.
# L'état résultant (workset + delta) ne doit pas comporter de NOUVELLE violation
# par rapport au workset seul : les violations préexistantes ne sont pas imputées
# à l'opérateur (pas de faux rejet), seule l'aggravation bloque la fusion.
# ------------------------------------------------------------------------------
def _shacl_violation_count(graphe: Graph) -> int:
    """Nombre de sh:Violation sur un graphe donné (shapes SSOT config.py)."""
    shacl_path = settings.SHACL_MASTER_PATH
    if not shacl_path.exists():
        return 0  # pas de shapes SSOT : GOU_22 (parse) reste la seule garde (tracé)
    shapes = Graph().parse(shacl_path, format="turtle")
    conforms, _results_graph, results_text = _pyshacl_validate(
        data_graph=graphe, shacl_graph=shapes, inference="none", advanced=True)
    if conforms:
        return 0
    return sum(1 for ligne in results_text.splitlines()
               if "Constraint Violation" in ligne)


def validate_delta_shacl(delta_ttl: str) -> tuple:
    """GTW_2 — M1 opérateur : (workset + delta) au plus aussi violant que workset.

    Retour (ok: bool, detail: str) ; ok=False => detail = violations nouvelles
    (tronquées, lisibles IHM). Aucune écriture ici : fonction pure de contrôle.
    """
    try:
        ws = settings.WORKSET_TBOX_PATH
        base = Graph()
        if ws.exists():
            base.parse(ws, format="turtle")
        fusion = Graph()
        if ws.exists():
            fusion.parse(ws, format="turtle")
        fusion.parse(data=delta_ttl, format="turtle")
        n_base = _shacl_violation_count(base)
        n_fusion = _shacl_violation_count(fusion)
        if n_fusion <= n_base:
            return True, ""
        return False, (f"{n_fusion - n_base} violation(s) SHACL nouvelle(s) "
                       "introduite(s) par le delta — fusion refusée.")
    except Exception as err:
        # Une erreur du contrôle ne doit jamais ouvrir la porte : on refuse.
        logger.warning("Contrôle SHACL en erreur : %s", err)
        return False, f"Contrôle SHACL impossible ({err}) — fusion refusée."


def approve_and_merge(delta_ttl: str) -> dict:
    """
    EXG-MET-P8-DEM_3 : fusion UNIQUEMENT sur appel explicite (clic humain).
    Cible : WORKING SET (jamais le Master ni les seeds — EXG-MET-P8-RES_1).
    Idempotent : tous les sujets dkg: déclarés du delta déjà présents => NOOP tracé.
    GTW_2 : une écriture M1 est SHACL-validée (validate_delta_shacl) avant fusion.
    """
    if not delta_ttl.strip():
        _audit("HITL_APPROVE", "REJECT(empty)", delta_ttl)
        return {"status": "REJECTED", "message": "Delta TBox vide."}
    if not validate_delta(delta_ttl):
        _audit("HITL_APPROVE", "REJECT(unparsable)", delta_ttl)
        return {"status": "REJECTED",
                "message": "Delta TBox invalide (parse rdflib échoué) — fusion refusée."}

    ok_shacl, detail_shacl = validate_delta_shacl(delta_ttl)
    if not ok_shacl:
        _audit("HITL_APPROVE", "REJECT(shacl)", delta_ttl)
        return {"status": "REJECTED",
                "message": f"Delta refusé par le contrôle SHACL : {detail_shacl}"}

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
            "message": "Delta validé (rdflib + SHACL) et fusionné dans le WORKING "
                       "SET (TLP:AMBER). Validation humaine journalisée."}


def reject(delta_ttl: str) -> dict:
    """EXG-MET-P8-DEM_3 : le rejet est une issue explicite et traçable."""
    _audit("HITL_REJECT", "REJECT(by-operator)", delta_ttl)
    return {"status": "REJECTED",
            "message": "Proposition rejetée par l'opérateur — décision journalisée."}


# ------------------------------------------------------------------------------
# GREFFON 2 (Design C1 §3.1) : preuve unique des régimes M1/M2.
# Les modules propriétaires (cti_intake, scan_engine) délèguent ici la
# journalisation de LEUR écriture — une seule écriture (la leur), une seule
# preuve (ici). Format compatible + champ régime.
# ------------------------------------------------------------------------------
def record_write(regime: str, action: str, detail: str = "",
                 target: str = "") -> None:
    """GTW_2 — trace une écriture M1/M2 au journal unique, avec son régime.

    regime : "M1" (opérateur direct), "M2" (source externe), "HITL" (boucle).
    Exemples : record_write("M2", "CTI_INGEST", detail="<n> triplets",
                            target="WORKSET_CTI_BUFFER")
    """
    log_path = settings.WORKSET_HITL_AUDIT_LOG_PATH
    log_path.parent.mkdir(parents=True, exist_ok=True)
    fp = hashlib.sha256(detail.encode("utf-8")).hexdigest()[:12] if detail else "-"
    ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"[{ts}] {action} regime='{regime}' "
                f"detail='{detail}' delta_sha256={fp} target='{target}'\n")


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
