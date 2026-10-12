# 03-Application/api/routes_phase8.py
"""
Routeur FastAPI Phase 8 — adaptateur HTTP (EXG-MET-P8-DEM_6 : 0 logique de
gouvernance ici, tout délégué à core/hitm_gateway.py).
EXG-MET-P8-DEM_1 (Tri-Boîtes), DEM_2 (Air-Gapped), DEM_3 (HITL), DEM_4
(pédagogie), EXG-FWK-P8-AGE_1 (Local-First, SPARQL sur graphe),
EXG-MET-P8-RES_1 (Seed/Reset), EXG-FWK-P1-GOU_22 (vocabulaire vs TBox réf.).
Lectures : TBox/RBox = WORKING SET ; ABox = SEEDS ; CTI = buffer workset.
"""

import json
import re
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

import core.config as settings
from core.hitm_gateway import (approve_and_merge, reject, reset_demo,
                               ensure_workset_initialized)

router = APIRouter(prefix="/api/phase8", tags=["Phase 8 - Demonstrator MCP"])

# ------------------------------------------------------------------------------
# MODÈLES PYDANTIC V2 (frozen)
# ------------------------------------------------------------------------------
class SourceCatalogItem(BaseModel):
    model_config = {"frozen": True}
    id: str
    label: str
    description: str = ""
    url_target: str = ""
    category: str = "CTI"
    tlp: str = "CLEAR"

class AuditRequest(BaseModel):
    model_config = {"frozen": True}
    mode: str = Field(default="foyer")
    enabled_network_sources: List[str] = Field(default_factory=list)

class AuditResponse(BaseModel):
    model_config = {"frozen": True}
    tbox_ttl: str
    abox_ttl: str
    cti_clear_ttl: str
    nl_bilan: List[Dict[str, Any]]
    delta_tbox_proposed: Optional[str] = None
    network_requests_made: int = 0

class MergeTBoxRequest(BaseModel):
    model_config = {"frozen": True}
    delta_ttl: str

class CtiSelectRequest(BaseModel):
    model_config = {"frozen": True}
    source_ids: List[str] = Field(default_factory=list)

# ------------------------------------------------------------------------------
# ENDPOINTS
# ------------------------------------------------------------------------------
@router.get("/tbox")
async def get_tbox():
    # EXG-MET-P8-DEM_1 : TBox de référence (workset), affichée dès l'ouverture.
    ensure_workset_initialized()
    return {"tbox_ttl": _read(settings.WORKSET_TBOX_PATH), "tbox_source": "workset"}

@router.get("/rbox")
async def get_rbox():
    # EXG-FWK-P8-AGE_1 : règles locales (workset), zéro requête réseau.
    ensure_workset_initialized()
    return {"rbox_ttl": _read(settings.WORKSET_RULES_PATH)}

@router.post("/cti/select")
async def select_cti_sources(payload: CtiSelectRequest):
    # EXG-MET-P8-DEM_2 : sélection locale uniquement, aucun réseau.
    keywords, bulletins = _resolve_source_keywords(payload.source_ids)
    subset = _select_cti_subset(keywords)
    if bulletins:
        subset = ("# Bulletins bruts des sources cochées (TLP:CLEAR)\n"
                  + "\n\n".join(bulletins) + "\n\n" + subset)
    buf = settings.WORKSET_CTI_BUFFER_PATH
    buf.parent.mkdir(parents=True, exist_ok=True)
    buf.write_text(subset, encoding="utf-8")
    return {"cti_clear_ttl": subset, "buffer_path": str(buf)}

@router.get("/sources", response_model=List[SourceCatalogItem])
async def get_external_sources_catalog():
    catalog_path = settings.EXTERNAL_SOURCES_COMPLIANCE_REGISTRY_PATH
    if not catalog_path.exists():
        catalog_path = settings.EXTERNAL_SOURCES_CATALOG_PATH
    if not catalog_path.exists():
        raise HTTPException(status_code=404,
            detail=f"Catalogue non trouvé sur le chemin SSOT : {catalog_path}")
    with open(catalog_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    sources = data.get("cti_sources", data.get("sources", [])) if isinstance(data, dict) else data
    return sources if sources is not None else []

@router.post("/audit", response_model=AuditResponse)
async def run_phase8_audit(payload: AuditRequest):
    # EXG-MET-P8-DEM_2 : 0 coche => 0 requête réseau (Air-Gapped).
    ensure_workset_initialized()
    network_counter = len(payload.enabled_network_sources) if payload.enabled_network_sources else 0
    tbox_content = _read(settings.WORKSET_TBOX_PATH)
    abox_content = _load_abox_by_mode(payload.mode)
    cti_content = (_read(settings.WORKSET_CTI_BUFFER_PATH)
                   if settings.WORKSET_CTI_BUFFER_PATH.exists()
                   else "# CTI buffer vide — sélectionnez des sources TLP:CLEAR.")
    nl_bilan, delta_tbox = _generate_risk_analysis(abox_content, cti_content)
    return AuditResponse(tbox_ttl=tbox_content, abox_ttl=abox_content,
        cti_clear_ttl=cti_content, nl_bilan=nl_bilan,
        delta_tbox_proposed=delta_tbox, network_requests_made=network_counter)

@router.post("/tbox/merge")
async def merge_tbox_proposal(payload: MergeTBoxRequest):
    # EXG-MET-P8-DEM_3 + DEM_6 : délégation PURE à la passerelle.
    result = approve_and_merge(payload.delta_ttl)
    if result["status"] == "REJECTED":
        raise HTTPException(status_code=422, detail=result["message"])
    return result

@router.post("/tbox/reject")
async def reject_tbox_proposal(payload: MergeTBoxRequest):
    # EXG-MET-P8-DEM_3 : issue [Rejeter] explicite et traçable.
    return reject(payload.delta_ttl)

@router.post("/reset")
async def reset_demonstrator():
    # EXG-MET-P8-RES_1 : retour au point de départ garanti (seeds intacts).
    return reset_demo()

@router.get("/tbox/graph")
async def get_tbox_graph():
    """EXG-MET-P8-DEM_4b : vue Mermaid de la TBox de référence. Local-only (GOU_13).
    JAMAIS de 500 : erreur visible dans le graphe (durcissement 17.6)."""
    from rdflib import Graph, RDF, OWL, RDFS
    ensure_workset_initialized()
    try:
        g = Graph()
        g.parse(settings.WORKSET_TBOX_PATH, format="turtle")
    except Exception as e:
        return {"mermaid": 'classDiagram\n    class ERREUR_PARSE_TBOX\n'
                f'    ERREUR_PARSE_TBOX : +cause "{_sanitize(e)}"'}
    def localname(u):
        s = str(u)
        return s.split("#")[-1].split("/")[-1] if "#" in s or "/" in s else s
    classes, members, relations = set(), [], []
    for c in g.subjects(RDF.type, OWL.Class):
        n = localname(c)
        if n and n[0].isupper():
            classes.add(n)
    for p in g.subjects(RDF.type, OWL.DatatypeProperty):
        dom, rng = g.value(p, RDFS.domain), g.value(p, RDFS.range)
        if dom is not None and rng is not None:
            members.append(f"    {localname(dom)} : +{localname(p)} "
                           f"{localname(rng).replace('XMLSchema#','xsd:')}")
    for p in g.subjects(RDF.type, OWL.ObjectProperty):
        dom, rng = g.value(p, RDFS.domain), g.value(p, RDFS.range)
        if dom is not None and rng is not None and localname(dom) in classes:
            r = localname(rng)
            classes.add(r)
            relations.append(f'    {localname(dom)} "*" --> "1" {r} : {localname(p)}')
    body = "\n".join([f"    class {c}" for c in sorted(classes)] + members + relations)
    return {"mermaid": "classDiagram\n" + body + "\n"}

@router.get("/abox/graph")
async def get_abox_graph(mode: str = "foyer"):
    """EXG-MET-P8-DEM_4b : vue Mermaid de l'ABox active (seed selon le mode)."""
    from rdflib import Graph, RDF, RDFS
    abox_ttl = _load_abox_by_mode(mode)
    if abox_ttl.startswith("# File not found") or not abox_ttl.strip():
        return {"mermaid": 'classDiagram\n    class ABOX_INTROUVABLE\n'
                f'    ABOX_INTROUVABLE : +mode "{mode}"'}
    try:
        g = Graph()
        g.parse(data=abox_ttl, format="turtle")
    except Exception as e:
        cause = _sanitize(e)
        return {"mermaid": "classDiagram\n    class ERREUR_PARSE_ABOX\n"
                f"    ERREUR_PARSE_ABOX : +cause \"{cause}\"\n"
                "    note for ERREUR_PARSE_ABOX \"Corriger le prefixe manquant dans le ttl\""}
    def ln(u):
        s = str(u); return s.split("#")[-1].split("/")[-1]
    instances, seen = [], set()
    for cls in sorted(set(g.objects(None, RDF.type)), key=str):
        cn = ln(cls)
        if not cn or not cn[0].isupper():
            continue
        if cn not in seen:
            seen.add(cn)
            instances.append(f"    class {cn}")
        for inst in sorted(set(g.subjects(RDF.type, cls)), key=str):
            label = g.value(inst, RDFS.label)
            name = _sanitize(label) if label else _sanitize(ln(inst))
            instances.append(f'    {cn} : +"{name}"')
    return {"mermaid": "classDiagram\n" + "\n".join(instances) + "\n"}

@router.get("/frugality")
async def get_frugality(mode: str = "foyer"):
    """EXG-FWK-P8-AGE_2 (abaque Green-Dev) : volumes chargés vs volume
    disponible (magasin seeds + workset, .private/ exclu), ratio, et TOP
    des entités les plus conséquentes du graphe actif. Lecture pure (AGE_1)."""
    ensure_workset_initialized()                                       # RES_1
    abox = _load_abox_by_mode(mode)                                    # RES_1
    cti = (_read(settings.WORKSET_CTI_BUFFER_PATH)
           if settings.WORKSET_CTI_BUFFER_PATH.exists() else "")        # AGE_1
    return _generate_frugality_metrics(abox, cti)

# ------------------------------------------------------------------------------
# HELPERS (un seul exemplaire de chacun)
# ------------------------------------------------------------------------------
@router.get("/superposition/graph")
async def get_superposition_graph(mode: str = "foyer", equipment: str = ""):
    """EXG-MET-P8-DEM_4b : superposition TBox/ABox/CTI pour UNE alerte du
    bilan. Graphe VERTICAL (flowchart TD) ; code couleur TLP : données
    internes TLP:RED (rose), fonds CTI externe TLP:CLEAR (vert), marquage
    TLP affiché dans chaque nœud. Lecture pure — aucune écriture (DEM_3)."""
    ensure_workset_initialized()                                       # RES_1
    abox = _load_abox_by_mode(mode)                                    # RES_1
    cti = (_read(settings.WORKSET_CTI_BUFFER_PATH)
           if settings.WORKSET_CTI_BUFFER_PATH.exists() else "")        # AGE_1
    return {"mermaid": _generate_superposition_mermaid(abox, cti, equipment)}

# ------------------------------------------------------------------------------
# HELPERS (un seul exemplaire de chacun)
# ------------------------------------------------------------------------------
def _read(path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else f"# File not found: {path}"

def _load_abox_by_mode(mode: str) -> str:
    # EXG-MET-P8-RES_1 : ABox de démo = SEED (lecture seule, réinitialisable).
    # Le scan réel 127.0.0.1 (.private/) reste un mode ultérieur hors didactique.
    path = settings.SEED_ABOX_FOYER_PATH if mode == "foyer" else settings.SEED_ABOX_HOTE_PATH
    return _read(path)

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

def _sanitize(s) -> str:
    """Assainit pour injection dans un classDiagram Mermaid (labels + erreurs)."""
    return (str(s).replace('"', "'").replace(":", " ").replace("\n", " ")
            .replace("\r", " ").replace("{", "(").replace("}", ")").strip()[:200])

def _generate_risk_analysis(abox: str, cti: str):
    """
    Exécute EXG-FWK-P8-AGE_1 : bilan NL calculé par SPARQL sur le graphe ABox
    (Local-First, ordre de sérialisation indépendant). Regex INTERDITE sur le
    contenu des .ttl ; échec de parse = ligne visible (jamais silencieux).
    Delta HITL proposé UNIQUEMENT sur écart réel vs la TBox DE RÉFÉRENCE
    (§25 base saine : 0 proposition au premier audit ; les écarts viennent du
    CTI coché — exploitsWeakness, isCisaKev). Jamais d'écriture auto (DEM_3).
    """
    from rdflib import Graph
    bilan = []
    cti_lower = cti.lower()

    g = None
    try:
        g = Graph()
        g.parse(data=abox, format="turtle")
    except Exception as parse_err:
        bilan.append({
            "equipment": "ABox locale", "component": "-",
            "linkage": "formel",
            "status": f"⚠️ ABox non parsable (rdflib) : {str(parse_err)[:120]} — bilan impossible",
            "severity": "AMBER", "action": "Corriger le .ttl (préfixe manquant ?)"
        })

    if g is not None:
        q = """
        PREFIX dkg: <http://dkg.cybersec.org/tbox#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?v ?vlabel ?score ?comp ?clabel ?asset ?alabel WHERE {
          ?v a dkg:Vulnerability .
          OPTIONAL { ?v rdfs:label ?vlabel }
          OPTIONAL { ?v dkg:cvssScore ?score }
          OPTIONAL { ?v dkg:isVulnerabilityOf ?comp .
                     OPTIONAL { ?comp rdfs:label ?clabel }
                     OPTIONAL { ?comp dkg:isComponentOf ?asset .
                                OPTIONAL { ?asset rdfs:label ?alabel } } }
        }"""
        for row in g.query(q):
            vid = str(row.v).split("#")[-1].split("/")[-1]
            vlabel = str(row.vlabel) if row.vlabel else vid
            clabel = str(row.clabel) if row.clabel else (
                str(row.comp).split("#")[-1].split("/")[-1] if row.comp else "-")
            alabel = str(row.alabel) if row.alabel else (
                str(row.asset).split("#")[-1].split("/")[-1] if row.asset else "Équipement inconnu")
            try:
                score = float(str(row.score))
            except (TypeError, ValueError):
                score = None
            cited = vid.lower() in cti_lower or vlabel.lower() in cti_lower
            bilan.append({
                "equipment": alabel,
                "component": f"{clabel} — {vlabel} ({vid})",
                "linkage": "formel",                     # DEM_4 : graphe formel
                "status": (f"Confirmé par CTI locale — CVSS {score}" if cited and score
                           else (f"Exposition locale — CVSS {score} (CTI locale silencieuse)"
                                 if score else "Exposition locale (score inconnu)")),
                "severity": ("RED" if score and score >= 9.0
                             else ("AMBER" if score and score >= 7.0 else "CLEAR")),
                "action": "Mise à jour du composant conseillée (patch éditeur)"
            })

        if any(k in cti_lower for k in ("smbv1", "smb v1", "end-of-life", "eol")):
            q_eol = """
            PREFIX dkg: <http://dkg.cybersec.org/tbox#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT ?asset ?alabel ?svc WHERE {
              ?asset dkg:exposesService ?svc .
              FILTER (CONTAINS(LCASE(STR(?svc)), "smb"))
              OPTIONAL { ?asset rdfs:label ?alabel }
            }"""
            for row in g.query(q_eol):
                alabel = str(row.alabel) if row.alabel else (
                    str(row.asset).split("#")[-1].split("/")[-1])
                bilan.append({
                    "equipment": alabel,
                    "component": f"{str(row.svc)} — Service SMBv1 / Port 445",
                    "linkage": "implicite",               # DEM_4 : liaison par mot-clé
                    "status": "EOL / Critique (CVE-2017-0144, confirmé CTI locale)",
                    "severity": "RED",
                    "action": "Désactivation immédiate conseillée"
                })

    if not bilan:
        bilan.append({
            "equipment": "ABox locale", "component": "-",
            "status": "Aucune vulnérabilité détectée dans l'ABox chargée",
            "severity": "CLEAR", "action": "Maintenir la veille CTI locale"
        })

    # Proposition HITL (EXG-FWK-P1-GOU_22) : vocabulaire utilisé (ABox + fonds
    # CTI coché) absent de la TBox DE RÉFÉRENCE (workset). Base saine §25 :
    # exposesService/hasThreatPattern y sont déclarés => 0 proposition au
    # premier audit ; le Gardien n'apparaît qu'avec du CTI NOUVEAU coché.
    tbox_ref = _read(settings.WORKSET_TBOX_PATH)
    props_used = (set(re.findall(r"dkg:([a-z]\w+)\s", abox))
                  | set(re.findall(r"dkg:([a-z]\w+)\s", cti)))
    props_declared = set(re.findall(r"^dkg:([a-z]\w+)\s+a\s+owl:(?:Object|Datatype)Property",
                                    tbox_ref, flags=re.M))
    missing = sorted(props_used - props_declared - {"hasTLPMarking"})
    tmpl = {
        "exploitsWeakness": ("dkg:exploitsWeakness a owl:ObjectProperty ;\n"
            "    rdfs:domain dkg:Vulnerability ; rdfs:range dkg:Weakness ;\n"
            '    skos:prefLabel "exploits weakness"@en, "exploite la faiblesse"@fr .'),
        "isCisaKev": ("dkg:isCisaKev a owl:DatatypeProperty ;\n"
            "    rdfs:domain dkg:Vulnerability ; rdfs:range xsd:boolean ;\n"
            '    skos:prefLabel "is CISA KEV"@en, "référencé CISA KEV"@fr .'),
    }
    delta_parts = [tmpl[p] for p in missing if p in tmpl]
    if delta_parts:
        header = ("@prefix dkg: <http://dkg.cybersec.org/tbox#> .\n"
                  "@prefix owl: <http://www.w3.org/2002/07/owl#> .\n"
                  "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n"
                  "@prefix skos: <http://www.w3.org/2004/02/skos/core#> .\n"
                  "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n")
        delta_tbox = ("# Delta TBox proposé (Gatekeeper HITL)\n"
                      "# Justification EXG-FWK-P1-GOU_22 : propriétés du fonds CTI\n"
                      "# (TLP:CLEAR coché) non déclarées dans la TBox de référence.\n"
                      + header + "\n" + "\n\n".join(delta_parts) + "\n")
        return bilan, delta_tbox
    return bilan, None


def _generate_superposition_mermaid(abox: str, cti: str, equipment: str) -> str:
    """EXG-MET-P8-DEM_4b : chaîne de raisonnement VERTICALE de l'alerte :
    Asset (TLP:RED) -> composant -> vulnérabilité -> faiblesse, reliée au
    fonds CTI externe (TLP:CLEAR) via skos:exactMatch. Tout est SPARQL sur
    graphe (EXG-FWK-P8-AGE_1) ; un lien CTI non déclaré en TBox porte ⚠️
    (EXG-FWK-P1-GOU_22) — la rupture de raisonnement d'un rejet y est visible.
    """
    from rdflib import Graph, RDF, RDFS, Namespace
    DKG = Namespace("http://dkg.cybersec.org/tbox#")
    SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")

    def ln(u):
        s = str(u)
        return s.split("#")[-1].split("/")[-1]

    g = Graph()                                                        # AGE_1
    try:
        g.parse(data=abox, format="turtle")                            # AGE_1
    except Exception as e:
        return 'flowchart TD\n    ERR["⚠️ ABox non parsable — ' + _sanitize(e) + '"]'

    # 1. Actif ciblé : label exact, puis localname, puis repli approché (AGE_1)
    asset = None
    for s in g.subjects(RDF.type, DKG.Asset):
        label = str(g.value(s, RDFS.label) or "")
        if label == equipment or ln(s) == equipment:
            asset = s
            break
    if asset is None:
        for s in g.subjects(RDF.type, DKG.Asset):
            label = str(g.value(s, RDFS.label) or ln(s))
            if equipment and equipment.lower() in label.lower():
                asset = s
                break
    if asset is None:
        return ('flowchart TD\n    NF["Aucun actif trouvé pour : '
                + _sanitize(equipment)
                + ' — cliquez [Vue superposition] depuis une carte du bilan."]')

    # 2. Vocabulaire déclaré dans la TBox de référence (workset) — GOU_22
    tbox_ref = _read(settings.WORKSET_TBOX_PATH)                      # GOU_22
    declared = set(re.findall(r"^dkg:([a-z]\w+)\s+a\s+owl:(?:Object|Datatype)Property",
                              tbox_ref, flags=re.M))                  # GOU_22

    # 3. Fonds CTI coché (buffer workset) — TLP:CLEAR                 # AGE_1
    g_cti = Graph()
    if cti.strip():
        try:
            g_cti.parse(data=cti, format="turtle")                    # AGE_1
        except Exception:
            g_cti = Graph()

    # 4. Construction des nœuds/arêtes : internes = rouge, CTI = vert (DEM_4b)
    nodes, edges = [], []  # (id, texte, classe) / (src, label, dst, pointillé)
    a_label = _sanitize(g.value(asset, RDFS.label) or ln(asset))
    nodes.append(("A0", f"🖥️ TLP:RED · Asset<br/>{a_label}", "intern"))
    for svc in sorted(set(g.objects(asset, DKG.exposesService)), key=str):
        sid = f"S{len(nodes)}"
        nodes.append((sid, f"🖥️ TLP:RED · Service exposé<br/>{_sanitize(svc)}", "intern"))
        edges.append(("A0", "exposesService", sid, False))
    for comp in sorted(set(g.objects(asset, DKG.hasInstalledComponent)), key=str):
        cid = f"C{len(nodes)}"
        cname = _sanitize(g.value(comp, RDFS.label) or ln(comp))
        cver = _sanitize(g.value(comp, DKG.version) or "")
        nodes.append((cid, f"🖥️ TLP:RED · Composant<br/>{cname} {cver}".strip(), "intern"))
        edges.append(("A0", "hasInstalledComponent", cid, False))
        for vuln in sorted(set(g.objects(comp, DKG.hasVulnerability)), key=str):
            vid = f"V{len(nodes)}"
            vname = _sanitize(g.value(vuln, RDFS.label) or ln(vuln))
            score = g.value(vuln, DKG.cvssScore)
            score_txt = f" — CVSS {score}" if score else ""
            nodes.append((vid, f"🖥️ TLP:RED · Vulnérabilité<br/>{vname}{score_txt}", "intern"))
            edges.append((cid, "hasVulnerability", vid, False))
            # Superposition : correspondant externe du fonds CTI (TLP:CLEAR)
            ext = None
            for m in g.objects(vuln, SKOS.exactMatch):
                ext = m
                break
            if ext is None:
                cve = g.value(vuln, DKG.cveId)
                if cve is not None:
                    for s2 in g_cti.subjects(DKG.cveId, None):
                        if str(g_cti.value(s2, DKG.cveId)) == str(cve):
                            ext = s2
                            break
            if ext is not None:
                xid = f"X{len(nodes)}"
                nodes.append((xid, f"🌐 TLP:CLEAR · CTI externe<br/>{_sanitize(ln(ext))}", "extern"))
                edges.append((vid, "skos:exactMatch", xid, True))
                for w in sorted(set(g_cti.objects(ext, DKG.exploitsWeakness)), key=str):
                    warn = "" if "exploitsWeakness" in declared \
                        else " ⚠️ non déclarée en TBox"                # GOU_22
                    yid = f"Y{len(nodes)}"
                    nodes.append((yid, f"🌐 TLP:CLEAR · Faiblesse CTI<br/>{_sanitize(ln(w))}", "extern"))
                    edges.append((xid, f"exploitsWeakness{warn}", yid, True))
            for w in sorted(set(g.objects(vuln, DKG.hasWeakness)), key=str):
                wid = f"W{len(nodes)}"
                nodes.append((wid, f"🖥️ TLP:RED · Faiblesse<br/>{_sanitize(ln(w))}", "intern"))
                edges.append((vid, "hasWeakness", wid, False))

    # 5. Nature de la liaison (DEM_4 + §37.2) : formelle si le graphe relie
    # explicitement l'actif à une vulnérabilité (chain SPARQL) ; implicite
    # si la chaîne s'arrête au littéral exposesService (mot-clé).
    has_formal_vuln = any(nid.startswith("V") for nid, _, _ in nodes)
    if has_formal_vuln:
        lines = ["flowchart TD"]
        lines.append('    L0["✓ LIAISON FORMELLE — raisonnement SPARQL sur le graphe"]:::formal')
    else:
        lines = ["flowchart TD"]
        lines.append('    L0["⚠️ LIAISON IMPLICITE — détection par mot-clé, lien ABox↔CTI non formalisé (candidate Gardien ABox §37)"]:::implicit')
    for nid, txt, cls in nodes:
        lines.append(f'    {nid}["{txt}"]:::{cls}')
    for src, lbl, dst, dashed in edges:
        arrow = "-.->" if dashed else "-->"
        lines.append(f"    {src} {arrow}|{lbl}| {dst}")
    lines.append("    classDef intern fill:#450a0a,stroke:#f43f5e,color:#ffe4e6")
    lines.append("    classDef extern fill:#052e16,stroke:#10b981,color:#d1fae5")
    lines.append("    classDef formal fill:#052e16,stroke:#34d399,color:#d1fae5")
    lines.append("    classDef implicit fill:#450a0a,stroke:#fb7185,color:#ffe4e6")
    return "\n".join(lines) + "\n"


def _generate_frugality_metrics(abox: str, cti: str) -> dict:
    """EXG-FWK-P8-AGE_2 — abaque Green-Dev : volumes chargés vs dispo.
    VOLUME CHARGÉ = ce que la session manipule réellement (workset TBox +
    ABox active + buffer CTI). VOLUME DISPONIBLE = l'intégralité du magasin
    de données (seeds + workset, .private/ exclu car TLP:RED). Le ratio
    démontre la frugalité : la démo charge une petite part du socle.
    TOP entités : les plus grosses instances du graphe actif, calculées
    par SPARQL (nb de triplets par sujet) — jamais de regex sur .ttl (GOU_22).
    """
    from rdflib import Graph, RDF, RDFS, Literal                        # AGE_2

    loaded = {
        "tbox_workset_bytes": len(_read(settings.WORKSET_TBOX_PATH).encode()),
        "abox_bytes": len(abox.encode()),
        "cti_bytes": len(cti.encode()),
        "rules_workset_bytes": len(_read(settings.WORKSET_RULES_PATH)
                                   .encode()) if settings.WORKSET_RULES_PATH.exists() else 0,
    }
    loaded_total = sum(loaded.values())

    # Volume disponible : magasin de données complet (seeds + workset),
    # fichiers .ttl uniquement (AGE_1) ; .private/ exclu (TLP:RED, DEM_4c).
    # Robustesse GOU_5 : AUCUN attribut de répertoire inventé — on dérive
    # les répertoires des chemins de FICHIERS garantis par la config, et
    # on déduplique (résolu) pour ne pas compter deux fois un même .ttl.
    _file_attrs = (                                                  # AGE_1
        "WORKSET_TBOX_PATH", "WORKSET_RULES_PATH",
        "WORKSET_CTI_BUFFER_PATH",
        "SEED_TBOX_PATH", "SEED_RULES_PATH",
        "SEED_ABOX_FOYER_PATH", "SEED_ABOX_HOTE_PATH",
    )
    seen, ttl_files = set(), []
    for attr in _file_attrs:
        p = getattr(settings, attr, None)
        if p is None or not getattr(p, "exists", lambda: False)():
            continue                       # attribut absent sur ce déploiement
        ttl_files.append(p)
        seen.add(p.resolve())
    for attr in _file_attrs:                                          # voisins .ttl
        p = getattr(settings, attr, None)
        if p is None or not p.exists():
            continue
        for f in p.parent.glob("*.ttl"):                             # même dossier
            if ".private" in f.parts:                                # DEM_4c
                continue
            if f.resolve() not in seen:
                seen.add(f.resolve())
                ttl_files.append(f)
    available_total = sum(f.stat().st_size for f in ttl_files)
    available_total = max(available_total, 1)

    # TOP entités : nb de triplets par sujet, graphe actif = ABox + CTI.
    g = Graph()
    parse_errors = []                                                 # AGE_2
    for src in (abox, cti):                                            # AGE_1
        if src.strip():
            try:
                g.parse(data=src, format="turtle")
            except Exception as exc:                                  # AGE_2
                # v3.1 (12/10) : ne plus avaler silencieusement. Un chemin
                # de repli `_read` (« # File not found: ... ») ou un .ttl
                # corrompu donnait un graphe VIDE sans erreur visible
                # (constaté via top_entities == []).
                parse_errors.append(str(exc)[:160])
    top = []
    for subj in set(g.subjects()):
        if isinstance(subj, Literal):  # v3.1 : URIRef/BNode SOUS-CLASSES de str !
            continue
        n = sum(1 for _ in g.predicate_objects(subj))
        label = g.value(subj, RDFS.label)
        name = str(label) if label else str(subj).split("#")[-1].split("/")[-1]
        top.append({"entity": name, "triplets": n})
    top.sort(key=lambda e: -e["triplets"])

    ratio = round(100.0 * loaded_total / available_total, 2)
    return {
        "loaded": loaded,                      # octets par volet
        "loaded_total_bytes": loaded_total,
        "available_total_bytes": available_total,
        "loaded_vs_available_pct": ratio,      # abaque Green-Dev (AGE_2)
        "top_entities": top[:5],               # fenêtre des cas conséquents
        "graph_parse_errors": parse_errors,    # AGE_2 — v3.1 : visibilité
        "graph_is_empty": len(g) == 0,          # AGE_2 — v3.1 : alarme didactique
    }
