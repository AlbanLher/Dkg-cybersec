# 03-Application/core/local_volumes.py
"""
Accès SSOT aux volumes locaux (EXG-FWK-P1-GOU_5 : chemins centralisés config.py).
Lecture des ABox selon le terrain (foyer/hote simulés, scan réel .private/),
volume CTI local actif (buffer workset cumulatif), résolution catalogue.
Extrait de api/routes_phase8.py lors du découpage v2 (logique inchangée).
Traçability :  XG-MET-P8-RES_1, EXG-FWK-P8-AGE_1
"""
import json
import re
from typing import List, Optional

import core.config as settings
from core import confrontation

def _read(path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else f"# File not found: {path}"

def _local_cti_active() -> Optional[str]:
    """FRUGALITÉ : volume CTI local chargé (buffer workset cumulatif).
    Retourne le texte du buffer s'il contient des données réellement
    chargées ; le placeholder '# CTI buffer vide' (état initial/reset)
    ne compte PAS comme volume actif -> None."""
    buf = settings.WORKSET_CTI_BUFFER_PATH
    if not buf.exists():
        return None
    text = _read(buf)
    if not text.strip() or "CTI buffer vide" in text:
        return None
    return text

def _load_abox_by_mode(mode: str) -> str:
    """EXG-MET-P8-RES_1 : ABox = SEED (foyer/hote simulés) ou SCAN RÉEL.
    mode='scan' (v-real) : ABox du poste réel (TLP:RED, .private/ — produite
    par POST /scan sur clic HITL). Jamais purgée par le reset : fait
    d'observation durable. Absente => marqueur visible (démo continue sur
    le message, le bilan signalera l'ABox non chargée).
    EXG-CONF_1 + FRUGALITÉ : si le volume CTI LOCAL contient des données
    chargées, CONFRONTATION_1 s'exécute sur le graphe EN MÉMOIRE contre ce
    buffer (seeds intacts, jamais le réseau) : les findings naissent du
    raisonnement sur le capital local accumulé, reliés par skos:exactMatch.
    Volume vide (initial/reset) : inventaire pur sérialisé tel quel."""
    if mode == "scan":
        path = settings.SECURE_ABOX_HOST_SCAN_PATH
        ttl = _read(path)
        if ttl.startswith("# File not found"):
            return ("# ⚠️ Aucun scan du poste enregistré — cliquez "
                    "« Scanner mon poste » (consentement HITL, TLP:RED).\n")
        return ttl
    path = settings.SEED_ABOX_FOYER_PATH if mode == "foyer" else settings.SEED_ABOX_HOTE_PATH
    abox_ttl = _read(path)
    cti = _local_cti_active()
    if cti is None:
        return abox_ttl
    from rdflib import Graph
    try:
        g = Graph()
        g.parse(data=abox_ttl, format="turtle")
        # règle RBox contre le VOLUME LOCAL (buffer cumulatif) — jamais
        # d'écriture des seeds ; décocher une source ne purge rien (R3 :
        # seul /reset vide le buffer).
        confrontation.run_confrontation(
            g, funds_path=settings.WORKSET_CTI_BUFFER_PATH)
        return g.serialize(format="turtle")
    except FileNotFoundError:
        # Fonds CTI non posé : on rend l'inventaire pur + un marqueur visible
        return (abox_ttl + "\n# ⚠️ EXG-CONF_1 : fonds CTI (TLP:CLEAR) introuvable — "
                "confrontation impossible, inventaire pur restitué.\n")
    except Exception:
        # ABox non parsable : contenu brut restitué (le bilan signalera l'erreur)
        return abox_ttl

def _resolve_source_keywords(source_ids: List[str]) -> tuple:
    """17.7 : ids + acronymes + labels du catalogue SSOT + bulletins bruts."""
    keywords = set(source_ids)
    bulletins = []
    try:
        with open(settings.EXTERNAL_SOURCES_COMPLIANCE_REGISTRY_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        for s in (data.get("cti_sources", data.get("sources", [])) or []):
            sid = s.get("id", "")
            keywords.update({sid, s.get("acronym", ""), s.get("label", ""), s.get("name", "")} - {""})
            if sid in source_ids and s.get("content"):
                bulletins.append(f"# --- {sid} ({s.get('acronym','')}) ---\n# {s.get('label','')}\n"
                                 f"# {s['content']}")
    except Exception:
        pass
    return sorted(k for k in keywords if k), bulletins

def _select_cti_subset(keywords: List[str]) -> str:
    """Sous-graphe CTI CLEAR local filtré par mots-clés (id/acronyme/label)."""
    cti_dir = settings.DIR_CTI_CLEAR
    kws = [k.lower() for k in keywords if k]
    parts = [f"# Sous-graphe CTI sélectionné : {keywords or '(aucun)'}"]
    matched_any = False
    if cti_dir.exists():
        for ttl_file in sorted(cti_dir.glob("*.ttl")):
            content = ttl_file.read_text(encoding="utf-8")
            if (not kws) or any(k in content.lower() for k in kws):
                matched_any = True
                parts.append(f"# --- {ttl_file.name} ---\n{content}")
    if not matched_any and cti_dir.exists():
        # Repli transparent (EXG-FWK-P8-AGE_1) : fonds local complet chargé.
        parts.append("# ⚠️ Aucun mot-clé de source trouvé dans les fichiers CTI "
                     "locaux — chargement du fonds complet (frugalité réduite).")
        for ttl_file in sorted(cti_dir.glob("*.ttl")):
            parts.append(f"# --- {ttl_file.name} (repli fonds complet) ---\n"
                         + ttl_file.read_text(encoding="utf-8"))
    return "\n\n".join(parts) if len(parts) > 1 else parts[0]
