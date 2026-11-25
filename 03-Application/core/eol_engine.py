# 03-Application/core/eol_engine.py
"""
MOTEUR — intégration EOL (source) — recette/EXG :
  EXG-FWK-P9-EOL_1, EXG-FWK-P9-EOL_2, EXG-FWK-P9-EOL_3 (+ FRG_1,
  EXG-FWK-P9-GTW_2 : écriture M2 tracée au sas hitm_gateway.record_write).
Ingestion EOL frugale par delta : sonde la source déclarée au registre
(stand-by), extrait du fonds de recette local (offline-first, jamais de
crash hors-ligne), fusionne en cumul idempotent dans le volume EOL de
l ABox Externe (TLP:CLEAR, namespace dkg-eol, jamais dkg-data), ratios
de frugalité distant/local/RAM. Mécanique clonée de cti_intake.py
(design C2 A3). Rév. 2026-11-24 — V3.
Interdits (loi de séparation inc_1) : aucune dépendance applicative
(fastapi, api, phases bannis par ce module) ; aucune écriture hors
ABox Externe ; jamais les seeds ni le scan réel.
"""
import re
from typing import Dict, List

import core.config as settings
from core.hitm_gateway import record_write

# --- Namespace EOL (EOL_2 : séparation par origine, jamais dkg-data) ---------
DKG_EOL_URI = "http://dkg.cybersec.org/eol#"
DKG_URI = "http://dkg.cybersec.org/tbox#"


def _load_registry_eol_entry() -> Dict:
    """V0 — lit l entrée EOL du registre des sources (stand-by réactivé).
    Repli introuvable : entrée minimale offline-first (jamais de crash)."""
    import json
    entry: Dict = {"id": settings.EOL_SOURCE_ID,
                   "label": "Catalogue End-of-Life (stand-by)", "url": "",
                   "mode": "fonds-local"}
    try:
        with open(settings.EXTERNAL_SOURCES_COMPLIANCE_REGISTRY_PATH,
                  "r", encoding="utf-8") as f:
            data = json.load(f)
        for bucket in ("eol_sources", "sources", "cti_sources"):
            for s in (data.get(bucket) or []):
                if isinstance(s, dict) and s.get("id") == settings.EOL_SOURCE_ID:
                    entry.update(s)
                    break
    except Exception:
        pass
    return entry


def _probe_remote(entry: Dict) -> Dict:
    """Sonde v-live de la source (HEAD). Hors-ligne -> status offline,
    volume simulé depuis le fonds local (FRG_1, jamais de crash)."""
    probe = {"source": settings.EOL_SOURCE_ID, "url": entry.get("url", ""),
             "status": "offline", "remote_bytes": 0, "downloaded_bytes": 0,
             "detail": ""}
    url = entry.get("url") or ""
    if not url:
        probe["detail"] = "stand-by sans url — recette sur fonds local"
        return probe
    try:
        import requests                                   # requis (v-live)
        r = requests.head(url, timeout=6, allow_redirects=True)
        probe["status"] = "live"
        probe["remote_bytes"] = int(r.headers.get("Content-Length") or 0)
        probe["detail"] = "volume distant sondé (HEAD), 0 octet téléchargé"
    except Exception as e:
        probe["detail"] = f"hors-ligne ({str(e)[:48]}) — volume simulé depuis le fonds local"
    return probe


def _loaded_volume_sources(vol) -> List[str]:
    """Ids des sources déjà chargées dans le volume EOL (marqueur # SOURCES:)."""
    if not vol.exists():
        return []
    m = re.search(r"^# SOURCES: (.*)$",
                  vol.read_text(encoding="utf-8"), flags=re.MULTILINE)
    return [s for s in m.group(1).split(",") if s] if m else []


def _ingest_fonds(g) -> int:
    """FRUGALITÉ — ingestion par delta : extrait du fonds de recette local
    (TLP:CLEAR, lecture seule) les instances dkg-eol:EndOfLife AVEC leurs
    triplets (eolDate xsd:date, sourceNote, supportStatus, TLP, provenance)
    et les AJOUTE au volume g. Sélection SPARQL, jamais de regex sur .ttl.
    Idempotent (RDF set : jamais de doublon). Retourne le nb d instances
    ajoutées cette fois."""
    funds_path = settings.EOL_FONDS_RECETTE_PATH
    if not funds_path.exists():
        return 0
    from rdflib import Graph
    funds = Graph()
    try:
        funds.parse(str(funds_path), format="turtle")
    except Exception:
        return -1                    # fonds corrompu : marqueur visible, pas de crash
    q = """
    PREFIX dkg-eol: <http://dkg.cybersec.org/eol#>
    SELECT ?e WHERE { ?e a dkg-eol:EndOfLife . }"""
    eols = [row.e for row in funds.query(q)]
    added = 0
    for e in eols:
        before = len(g)
        for p, o in funds.predicate_objects(e):
            g.add((e, p, o))
        if len(g) > before:
            added += 1
    return added


def ingest_eol_source() -> dict:
    """Corps de POST /eol/ingest : enrichit le volume EOL de l ABox
    Externe (TLP:CLEAR) et renvoie le volume TTL + ratios v-live
    (distant sondé / téléchargé / local / RAM — mêmes champs que CTI)."""
    vol = settings.ABOX_EXTERNE_EOL_PATH
    vol.parent.mkdir(parents=True, exist_ok=True)
    loaded = _loaded_volume_sources(vol)               # cumul déjà présent
    new_sources = ([settings.EOL_SOURCE_ID]
                   if settings.EOL_SOURCE_ID not in loaded else [])
    entry = _load_registry_eol_entry()
    probe = _probe_remote(entry) if new_sources else {"source": settings.EOL_SOURCE_ID,
                                                      "status": "stand-by",
                                                      "remote_bytes": 0,
                                                      "downloaded_bytes": 0,
                                                      "url": "", "detail": ""}
    all_sources = loaded + new_sources                  # ordre d arrivée
    from rdflib import Graph, Namespace
    g = Graph()
    # BINDING : la sérialisation doit émettre dkg: et dkg-eol: (pas ns1:).
    g.bind("dkg", Namespace(DKG_URI))
    g.bind("dkg-eol", Namespace(DKG_EOL_URI))
    if loaded:
        try:
            g.parse(str(vol), format="turtle")
        except Exception:
            pass                                  # volume corrompu -> repart à zéro
    added = _ingest_fonds(g)
    fonds_notice = ""
    if added == -1:
        added = 0
        fonds_notice = ("# ⚠️ Fonds EOL de recette non parsable (rdflib) — "
                        "ingestion ignorée, cumul local conservé\n")
    body = g.serialize(format="turtle")
    funds_bytes = (settings.EOL_FONDS_RECETTE_PATH.stat().st_size
                   if settings.EOL_FONDS_RECETTE_PATH.exists() else 0)
    local_bytes = len((ttl_bytes := body.encode("utf-8")))
    ram_bytes = local_bytes
    remote_total = probe.get("remote_bytes", 0)
    downloaded_total = probe.get("downloaded_bytes", 0)
    header = ("# Volume EOL TLP:CLEAR — ABox Externe (frugalité : cumul conservé, "
              "ingestion par delta idempotente, offline-first)\n"
              f"# SOURCES: {','.join(all_sources)}\n")
    if probe.get("status") == "live":
        header += (f"# 🌐 {probe['source']} — site distant consulté : "
                   f"{remote_total:,} octets sondés | "
                   f"⬇️ téléchargé : {downloaded_total:,} octets\n")
        if probe.get("detail"):
            header += f"#    ↳ {probe['detail']}\n"
    else:
        header += (f"# 🌐 {probe['source']} — STAND-BY / HORS-LIGNE "
                   f"({probe.get('detail', 'fonds local')}) : "
                   f"volume simulé depuis le fonds de recette local\n")
    header += (f"# 📊 RATIOS — distant sondé : {remote_total:,} octets | "
               f"téléchargé : {downloaded_total:,} | "
               f"persisté en local : {local_bytes:,} | RAM : {ram_bytes:,} octets\n")
    header += f"# Triplets: {len(g)} | instances EOL ajoutées cette fois: {added}\n"
    header += fonds_notice
    ttl = header + body
    vol.write_text(ttl, encoding="utf-8")
    # EOL_1 / GTW_2 : l écriture M2 (ingestion au volume EOL de l ABox
    # Externe) est tracée au JOURNAL UNIQUE du sas. Un cumul sans ajout
    # n est pas une ingestion, donc pas de trace.
    if added:
        record_write("M2", "EOL_INGEST",
                     detail=f"{added} instances EOL ajoutées, {len(g)} triplets, "
                            f"source: {settings.EOL_SOURCE_ID}",
                     target="ABOX_EXTERNE_EOL")
    return {"eol_clear_ttl": ttl, "volume_path": str(vol),
            "sources_fonds_bytes": funds_bytes,
            "local_volume_bytes": local_bytes,
            "ram_volume_bytes": ram_bytes,
            "remote_volume_bytes": remote_total,
            "downloaded_volume_bytes": downloaded_total,
            "remote_probe": probe,
            "sources_loaded": all_sources, "volume_triples": len(g),
            "volume_bytes": len(ttl.encode("utf-8")), "eol_records_added": added}
