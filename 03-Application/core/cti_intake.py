# 03-Application/core/cti_intake.py
"""
Agent CTI / ingestion frugale (EXG-MET-P8-DEM_2, EXG-FWK-P8-AGE_1) :
sonde v-live des sources distantes (HEAD + sous-ensemble Green/discret),
extraction des CVE/acteurs du fonds seed vers le buffer workset TLP:CLEAR
(cumul idempotent), ratios de frugalité distant/local/RAM.
Extrait de api/routes_phase8.py lors du découpage v2 (logique inchangée).
"""
import re
from typing import List, Dict

import core.config as settings
from core.local_volumes import _read, _resolve_source_keywords

# --- Sources distantes réelles (v-live) ----------------------------------------
# Chaque entrée : url du flux public + stratégie de sous-ensemble.
#   monolithic : flux fichier unique (KEV) — téléchargé entier puis filtré
#                LOCALEMENT (les identifiants d'API restent publics) ;
#   per-cve    : API sélective — une requête PAR CVE publique concernée
#                (Green : quelques Ko ; discret : on ne divulgue rien) ;
#   head-only  : volume sondé sans corps téléchargé (STIX ~30 Mo : le
#                sous-ensemble vient de la sélection locale, 0 octet).
REMOTE_SOURCES = {
    "cisa_kev_2025": {
        "url": "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json",
        "mode": "monolithic",
        "note": "CISA KEV — catalogue public des vulnérabilités exploitées"},
    "nvd_cve_feed": {
        "url": "https://services.nvd.nist.gov/rest/json/cves/2.0",
        "mode": "per-cve",
        "note": "NVD API 2.0 — requêtes ciblées par CVE publique"},
    "mitre_attck_2026": {
        "url": "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack.json",
        "mode": "head-only",
        "note": "MITRE ATT&CK STIX — bundle volumineux, volume sondé seulement"},
    "anssi_2024": {
        "url": "https://www.cert.ssi.gouv.fr/alertes/",
        "mode": "head-only",
        "note": "CERT-FR — alertes publiques, volume sondé seulement"},
}

def _funds_cves_by_source() -> Dict[str, List[str]]:
    """CVE publiques du fonds seed par source (pour les requêtes ciblées).
    Seuls ces identifiants PUBLICS quittent le poste — jamais l'inventaire."""
    funds_path = settings.SEED_CTI_CLEAR_PATH
    if not funds_path.exists():
        return {}
    from rdflib import Graph
    g = Graph()
    g.parse(str(funds_path), format="turtle")
    q = """
    PREFIX dkg: <http://dkg.cybersec.org/tbox#>
    SELECT ?cve ?src WHERE { ?v a dkg:Vulnerability ; dkg:cveId ?cve ; dkg:providedBy ?src . }"""
    mapping: Dict[str, List[str]] = {}
    for row in g.query(q):
        mapping.setdefault(str(row.src), []).append(str(row.cve))
    return mapping

def _probe_remote_sources(source_ids: List[str]) -> List[dict]:
    """Sonde réelle des sources cochées : volume distant (HEAD) + sous-ensemble
    téléchargé. Repli hors-ligne : status='offline', volume = simulation.
    Retourne une sonde par source (affichée dans le volet TLP:CLEAR)."""
    probes = []
    cves_by_source = _funds_cves_by_source()
    try:
        import requests                                   # requis (v-live)
    except ImportError:
        return [{"source": s, "status": "offline", "remote_bytes": 0,
                 "downloaded_bytes": 0, "url": "", "detail": "lib requests absente"}
                for s in source_ids]
    for sid in source_ids:
        meta = REMOTE_SOURCES.get(sid)
        if not meta:
            continue
        probe = {"source": sid, "url": meta["url"], "status": "live",
                 "remote_bytes": 0, "downloaded_bytes": 0, "detail": ""}
        try:                                              # 1. volume distant
            r = requests.head(meta["url"], timeout=6, allow_redirects=True)
            cl = r.headers.get("Content-Length")
            if cl:
                probe["remote_bytes"] = int(cl)
            else:                                         # HEAD muet → GET stream
                with requests.get(meta["url"], timeout=6, stream=True) as rg:
                    probe["remote_bytes"] = int(rg.headers.get("Content-Length") or 0)
        except Exception as e:
            probe["status"] = "offline"
            probe["detail"] = f"hors-ligne ({str(e)[:48]}) — simulation locale"
            probes.append(probe)
            continue
        try:                                              # 2. sous-ensemble
            mode = meta["mode"]
            if mode == "per-cve":
                total = 0
                for cve in cves_by_source.get(sid, []):
                    rg = requests.get(f"{meta['url']}?cveId={cve}", timeout=8)
                    total += len(rg.content)
                probe["downloaded_bytes"] = total
                probe["detail"] = (f"{len(cves_by_source.get(sid, []))} requête(s) "
                                   "ciblée(s) — seules des CVE publiques sont envoyées")
            elif mode == "monolithic":
                rg = requests.get(meta["url"], timeout=15)
                probe["downloaded_bytes"] = len(rg.content)
                probe["detail"] = "flux monolithique téléchargé, filtré LOCALEMENT"
            else:                                          # head-only
                probe["downloaded_bytes"] = 0
                probe["detail"] = "volume sondé, 0 octet de corpus téléchargé"
        except Exception as e:
            probe["detail"] = f"sous-ensemble non téléchargé ({str(e)[:48]})"
        probes.append(probe)
    return probes

def _loaded_buffer_sources(buf) -> List[str]:
    """Ids des sources déjà chargées dans le buffer (marqueur # SOURCES:)."""
    if not buf.exists():
        return []
    m = re.search(r"^# SOURCES: (.*)$", buf.read_text(encoding="utf-8"),
                  flags=re.MULTILINE)
    return [s for s in m.group(1).split(",") if s] if m else []

def _append_source_cves(g, source_ids: List[str]) -> int:
    """FRUGALITÉ : extrait du fonds seed (TLP:CLEAR, lecture seule — RES_1)
    les CVE (affectsComponentId/affectsVersion) et les ACTEURS DE MENACE
    dont dkg:providedBy intersecte source_ids — avec leurs faiblesses liées
    (CWE) et catégories d'appareil ciblées — et les AJOUTE au volume local
    g. Idempotent (RDF set : jamais de doublon). Retourne le nb de CVE
    ajoutées cette fois. L'acteur de menace apporte des prédicats NON
    DÉCLARÉS (targetsDevice) : c'est le déclencheur du recallage TBox
    (GOU_22) — l'extraction est liée aux données internes, la TBox assure
    l'intégration cohérente."""
    funds_path = settings.SEED_CTI_CLEAR_PATH
    if not funds_path.exists() or not source_ids:
        return 0
    from rdflib import Graph, Namespace, RDF, URIRef
    DKG = Namespace("http://dkg.cybersec.org/tbox#")
    CTI = Namespace("http://dkg.cybersec.org/cti#")
    funds = Graph()
    funds.parse(str(funds_path), format="turtle")
    q = """
    PREFIX dkg: <http://dkg.cybersec.org/tbox#>
    SELECT ?v ?src ?w WHERE {
      ?v a dkg:Vulnerability ; dkg:providedBy ?src .
      OPTIONAL { ?v dkg:exploitsWeakness ?w }
    }"""
    q_actor = """
    PREFIX dkg: <http://dkg.cybersec.org/tbox#>
    SELECT ?a ?src WHERE {
      ?a a dkg:ThreatActor ; dkg:providedBy ?src .
    }"""
    wanted = set(source_ids)
    subjects, cves = set(), set()
    for row in funds.query(q):
        if str(row.src) in wanted:
            subjects.add(row.v)
            cves.add(row.v)
            if row.w is not None:
                subjects.add(row.w)               # CWE exploitée
    for row in funds.query(q_actor):
        if str(row.src) in wanted:
            subjects.add(row.a)
            for o in funds.objects(row.a, DKG.targetsDevice):
                subjects.add(o)                  # catégorie ciblée (IoTCamera)
    # CWE -> CAPEC : le motif d'attaque accompagne la faiblesse chargée
    for s in list(subjects):
        for p, o in funds.predicate_objects(s):
            if isinstance(o, URIRef) and str(o).startswith(str(CTI)):
                subjects.add(o)
    for s in subjects:
        for p, o in funds.predicate_objects(s):
            g.add((s, p, o))
    return len(cves)


def build_cti_buffer(source_ids: List[str]) -> dict:
    """Corps de POST /cti/select : enrichit le buffer workset et
    renvoie le volume TTL + ratios v-live (distant/local/RAM)."""
    buf = settings.WORKSET_CTI_BUFFER_PATH
    buf.parent.mkdir(parents=True, exist_ok=True)
    loaded = _loaded_buffer_sources(buf)            # cumul déjà présent
    new_sources = [s for s in source_ids if s not in loaded]
    # Sonde distante des NOUVELLES sources uniquement (frugalité : une
    # source déjà dans le capital local n'est pas re-consultée).
    probes = (_probe_remote_sources(new_sources) if new_sources else [])
    all_sources = loaded + [s for s in new_sources] # ordre d'arrivée
    from rdflib import Graph
    g = Graph()
    # BINDING de namespaces : la sérialisation doit émettre dkg: (pas ns1:)
    # — le Gardien TBox (GOU_22) scanne le buffer pour les prédicats
    # non déclarés ; un préfixe anonyme (ns1:) le rendrait aveugle.
    from rdflib import Namespace
    g.bind("dkg", Namespace("http://dkg.cybersec.org/tbox#"))
    g.bind("dkg-cti", Namespace("http://dkg.cybersec.org/cti#"))
    g.bind("dkg-data", Namespace("http://dkg.cybersec.org/data#"))
    if loaded:
        try:
            g.parse(str(buf), format="turtle")
        except Exception:
            pass                                  # buffer corrompu -> repart à zéro
    added = _append_source_cves(g, new_sources) if new_sources else 0
    # Bulletins des sources chargées (commentaires — traçabilité du volume)
    _, bulletins = _resolve_source_keywords(all_sources)
    body = g.serialize(format="turtle")
    # MESSAGE DIDACTIQUE FRUGALITÉ (v-live) : la source cochée est réellement
    # consultée en ligne — volume du magasin distant sondé (HEAD), sous-ensemble
    # téléchargé (Green & discret : seuls des CVE PUBLIQUES sont demandées,
    # le filtrage « pertinent pour nous » reste LOCAL), sélection persistée
    # en local (fichier buffer) et tenue en RAM (graphe actif).
    funds_bytes = (settings.SEED_CTI_CLEAR_PATH.stat().st_size
                   if settings.SEED_CTI_CLEAR_PATH.exists() else 0)
    local_bytes = len(ttl_bytes) if (ttl_bytes := body.encode("utf-8")) else 0
    ram_bytes = local_bytes          # représentation du graphe en mémoire
    remote_total = sum(p["remote_bytes"] for p in probes)
    downloaded_total = sum(p["downloaded_bytes"] for p in probes)
    header = ("# Volume CTI local TLP:CLEAR (frugalité — cumul conservé, "
              "décocher ne supprime rien, /reset purge)\n"
              f"# SOURCES: {','.join(all_sources)}\n")
    for p in probes:
        if p["status"] == "live":
            header += (f"# 🌐 {p['source']} — site distant consulté : "
                       f"{p['remote_bytes']:,} octets sondés | "
                       f"⬇️ téléchargé : {p['downloaded_bytes']:,} octets"
                       f" ({100 * p['downloaded_bytes'] / p['remote_bytes']:.2f}% du flux"
                       if p["remote_bytes"] else
                       f"# 🌐 {p['source']} — site distant consulté | "
                       f"⬇️ téléchargé : {p['downloaded_bytes']:,} octets")
            header += f")\n" if p["remote_bytes"] else "\n"
            if p["detail"]:
                header += f"#    ↳ {p['detail']}\n"
        else:
            header += (f"# 🌐 {p['source']} — HORS-LIGNE ({p['detail']}) : "
                       f"volume simulé depuis le fonds local\n")
    header += ("# 🔒 Discrétion : seuls des identifiants CVE PUBLICS sont envoyés aux "
               "API — l'inventaire interne (TLP:RED) ne quitte jamais le poste\n")
    if remote_total:
        header += (f"# 📊 RATIOS — distant sondé : {remote_total:,} octets | "
                   f"téléchargé : {downloaded_total:,} | "
                   f"persisté en local : {local_bytes:,} "
                   f"({100 * local_bytes / max(remote_total, 1):.2f}% du distant) | "
                   f"RAM : {ram_bytes:,} octets\n")
    else:
        header += (f"# 💾 Local (fichier buffer) : {local_bytes:,} octets "
                   f"(simulation fonds : {funds_bytes:,}) | "
                   f"🧠 RAM : {ram_bytes:,} octets\n")
    header += f"# Triplets: {len(g)} | CVE ajoutées cette fois: {added}\n"
    bulletin_lines = "\n".join(
        "# " + b.replace("\r", " ").replace("\n", " ") for b in bulletins)
    ttl = header + (bulletin_lines + "\n" if bulletin_lines else "") + body
    buf.write_text(ttl, encoding="utf-8")
    return {"cti_clear_ttl": ttl, "buffer_path": str(buf),
            "sources_volume_bytes": funds_bytes,
            "local_volume_bytes": local_bytes,
            "ram_volume_bytes": ram_bytes,
            "remote_volume_bytes": remote_total,
            "downloaded_volume_bytes": downloaded_total,
            "remote_probes": probes,
            "sources_loaded": all_sources, "buffer_triples": len(g),
            "buffer_bytes": len(ttl.encode("utf-8")), "cves_added": added}
