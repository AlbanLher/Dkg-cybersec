# 03-Application/core/audit_engine.py
"""
Moteur d'audit SOC  bilan NL par SPARQL sur le graphe ABox (Local-First) et
détection Gardien TBox du vocabulaire non déclaré .
Contrôle Gardien de la couche lexicale SKOS (EXG-FWK-P1-GOU_18 — contrôle
proposé par le Gardien, exigence dédiée en formalisation côté
SPC-FWK-P8_Agent_Gardien_RefExt rév. 2) : toute classe/propriété de la
TBox de référence sans skos:prefLabel FR+EN ou sans skos:definition
génère un delta d'annotation HITL (jamais fusionné automatiquement).
Extrait de api/routes_phase8.py lors du découpage v2 ; contrôle SKOS v3.
GREFFON EOL_3 (Brique C2 V4, EXG-FWK-P9-EOL_3 + EOL_2/FRG_1) : les findings
sont enrichis par jointure SPARQL composant ABox - instance dkg-eol du
volume EOL de l ABox Externe (TLP:CLEAR), jamais par regex sur le .ttl ;
les findings sans correspondance EOL restent strictement inchangés.
Traçabilité : EXG-MET-P8-DEM_1 (bilan NL), EXG-FWK-P1-GOU_22
(vocabulaire non déclaré → proposition delta), EXG-FWK-P1-GOU_18
(couche SKOS), EXG-MET-P8-DEM_7 (adaptateur pur).
"""
import re
from typing import Optional, Tuple, List, Dict, Any

import core.config as settings
from core.local_volumes import _read


# --- Contrôle Gardien GOU_18 : couche lexicale SKOS --------------------------
_SKOS_CHECK = """
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
SELECT ?e ?kind ?pl ?d WHERE {
  ?e a ?kind .
  FILTER (?kind IN (owl:Class, owl:ObjectProperty, owl:DatatypeProperty))
  OPTIONAL { ?e skos:prefLabel ?pl }
  OPTIONAL { ?e skos:definition ?d }
}
"""

_LABEL_QUERY = """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?e ?lbl ?cmt WHERE {
  OPTIONAL { ?e rdfs:label ?lbl }
  OPTIONAL { ?e rdfs:comment ?cmt }
}
"""

# --- Greffon EOL_3 (Brique C2) : jointure SPARQL composant-instance dkg-eol --
# Correspondance en deux étages (lecture seule sur l UNION des graphes) :
#   1. strict : même nom de produit ET même version ;
#   2. repli : composant sans version connue (unknown/absente).
# Toute correspondance porte la date EOL sourcée et son triplet source
# (dkg:sourceNote) — jamais de regex sur le .ttl EOL (EOL_2/AGE_1).
_EOL_LINK_STRICT = """
PREFIX dkg: <http://dkg.cybersec.org/tbox#>
PREFIX dkg-eol: <http://dkg.cybersec.org/eol#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?comp ?clabel ?cv ?pv ?sv ?asset ?alabel ?ed ?sn ?st WHERE {
  ?comp a dkg:SoftwareComponent ; rdfs:label ?clabel ; dkg:version ?cv .
  ?e a dkg-eol:EndOfLife ; dkg:productName ?pn ; dkg:componentVersion ?pv ;
     dkg:supportStatus ?st ; dkg:eolDate ?ed ; dkg:sourceNote ?sn .
  FILTER (LCASE(STR(?clabel)) = LCASE(STR(?pn)))
  FILTER (LCASE(STR(?cv)) = LCASE(STR(?pv)))
  OPTIONAL { ?e dkg:successorVersion ?sv }
  OPTIONAL { ?comp dkg:isComponentOf ?asset .
             OPTIONAL { ?asset rdfs:label ?alabel } }
}
"""

_EOL_LINK_LOOSE = """
PREFIX dkg: <http://dkg.cybersec.org/tbox#>
PREFIX dkg-eol: <http://dkg.cybersec.org/eol#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?comp ?clabel ?cv ?pv ?sv ?asset ?alabel ?ed ?sn ?st WHERE {
  ?comp a dkg:SoftwareComponent ; rdfs:label ?clabel .
  OPTIONAL { ?comp dkg:version ?cv }
  FILTER (!BOUND(?cv) || LCASE(STR(?cv)) = "unknown")
  ?e a dkg-eol:EndOfLife ; dkg:productName ?pn ;
     dkg:supportStatus ?st ; dkg:eolDate ?ed ; dkg:sourceNote ?sn .
  FILTER (LCASE(STR(?clabel)) = LCASE(STR(?pn)))
  OPTIONAL { ?e dkg:componentVersion ?pv }
  OPTIONAL { ?e dkg:successorVersion ?sv }
  OPTIONAL { ?comp dkg:isComponentOf ?asset .
             OPTIONAL { ?asset rdfs:label ?alabel } }
}
"""


def _localname(uri) -> str:
    s = str(uri)
    return s.split("#")[-1].split("/")[-1]


def _skos_annotation_delta(tbox_ttl: str) -> Optional[str]:
    """EXG-FWK-P1-GOU_18 (contrôle Gardien) : propose un delta d'annotation
    SKOS pour toute entité déclarée non conforme. Contrôle 100% SPARQL sur
    le graphe parsé (AGE_1 — zéro regex sur le .ttl), échec de parse =
    aucun delta + aucune exception silencieuse (déjà tracé par le bilan).
    Le delta est une PROPOSITION : les labels sont moules depuis le
    rdfs:label existant ou le nom local — l'humain garde la décision
    (DEM_3 : jamais d'écriture automatique)."""
    from rdflib import Graph
    g = Graph()
    try:
        g.parse(data=tbox_ttl, format="turtle")
    except Exception:
        return None                                  # TBox non parsable : bilan le trace

    missing: Dict[str, set] = {}
    entity_labels: Dict[str, set] = {}
    entity_defs: Dict[str, bool] = {}
    for row in g.query(_SKOS_CHECK):
        uri = str(row.e)
        lacks = missing.setdefault(uri, set())
        if row.pl is not None:
            lang = str(getattr(row.pl, "language", "") or "").lower()
            entity_labels.setdefault(uri, set()).add(lang)
        if row.d is not None:
            entity_defs[uri] = True
    for uri, lacks in missing.items():
        langs = entity_labels.get(uri, set())
        if "en" not in langs:
            lacks.add("prefLabel@en")
        if "fr" not in langs:
            lacks.add("prefLabel@fr")
        if uri not in entity_defs:
            lacks.add("definition")
    missing = {u: l for u, l in missing.items() if l}
    if not missing:
        return None

    # Base de rédaction : rdfs:label/comment existants sinon nom local.
    labels = {}
    for row in g.query(_LABEL_QUERY):
        labels.setdefault(str(row.e), {})
        if row.lbl is not None and "lbl" not in labels[str(row.e)]:
            labels[str(row.e)]["lbl"] = str(row.lbl)
        if row.cmt is not None:
            labels[str(row.e)].setdefault("cmt", str(row.cmt))

    parts = []
    for uri, lacks in sorted(missing.items()):
        name = _localname(uri)
        info = labels.get(uri, {})
        base_en = info.get("lbl", name)
        lines = [f"dkg:{name}"]
        if "prefLabel@en" in lacks:
            lines.append(f'    skos:prefLabel "{base_en}"@en ;')
        if "prefLabel@fr" in lacks:
            lines.append(f'    skos:prefLabel "{base_en}"@fr ;')
        if "definition" in lacks:
            def_src = info.get("cmt", "À compléter par l'analyste (proposition Gardien).")
            lines.append(f'    skos:definition "{def_src}"@fr ;')
        parts.append(" ;\n".join([lines[0]] + [l.rstrip(" ;") for l in lines[1:]])
                     + " .")

    header = ("@prefix dkg: <http://dkg.cybersec.org/tbox#> .\n"
              "@prefix skos: <http://www.w3.org/2004/02/skos/core#> .\n")
    return ("# Delta d'annotation SKOS proposé (Gardien TBox — EXG-FWK-P1-GOU_18)\n"
            "# Entités déclarées sans couche lexicale complète (prefLabel FR/EN,\n"
            "# définition). Proposition HITL : à valider/amender/rejeter.\n"
            + header + "\n" + "\n\n".join(parts) + "\n")


def _generate_risk_analysis(abox: str, cti: str, eol: str = "") -> Tuple[List[Dict[str, Any]], Optional[str]]:
    """
    Exécute EXG-FWK-P8-AGE_1 : bilan NL calculé par SPARQL sur le graphe ABox
    (Local-First, ordre de sérialisation indépendant). Regex INTERDITE sur le
    contenu des .ttl ; échec de parse = ligne visible (jamais silencieux).
    EXG-CONF_1 : les findings de confrontation (présents dans l'ABox passée
    quand le CTI est coché) sont détectés par la même requête SPARQL — aucun
    code dédié : le delta avant/après CTI est automatique.
    GREFFON EOL_3 (Brique C2 V4) : le paramètre eol (texte TTL du volume EOL
    de l ABox Externe) est OPTIONNEL et se replie sur le SSOT
    settings.ABOX_EXTERNE_EOL_PATH — les appelants existants (routes, tests)
    restent inchangés. Toute correspondance composant-instance dkg-eol
    enrichit le finding concerné (statut support + date EOL sourcée + triplet
    source dkg:sourceNote) ; les findings sans correspondance EOL ainsi que
    les non-audits restent strictement inchangés (non-régression).
    Delta HITL proposé UNIQUEMENT sur écart réel vs la TBox DE RÉFÉRENCE
    (§25 base saine : 0 proposition au premier audit ; les écarts viennent du
    CTI coché — exploitsWeakness, isCisaKev). Jamais d'écriture auto (DEM_3).
    Contrôle GOU_18 : le delta inclut aussi les annotations SKOS manquantes.
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
        # GREFFON EOL_3 (Brique C2 V4) : correspondances composant ABox -
        # instance dkg-eol du volume EOL (TLP:CLEAR), jointure SPARQL sur
        # l UNION LOCALE des graphes, en lecture seule — aucune écriture,
        # jamais de regex sur le .ttl EOL. Volume absent ou non parsable =
        # ligne visible, jamais de crash ni de suppression silencieuse.
        eol_hits: Dict[str, Dict[str, Any]] = {}
        eol_notice = ""
        eol_ttl = eol if eol else _read(settings.ABOX_EXTERNE_EOL_PATH)
        if eol_ttl and "File not found" not in eol_ttl:
            try:
                g_eol = Graph()
                g_eol.parse(data=eol_ttl, format="turtle")
                ug = g + g_eol
                seen: set = set()
                for q_link in (_EOL_LINK_STRICT, _EOL_LINK_LOOSE):
                    for row in ug.query(q_link):
                        cu = str(row.comp)
                        if cu in seen:
                            continue
                        seen.add(cu)
                        eol_hits[cu] = {
                            "label": str(row.clabel),
                            "asset": (str(row.alabel) if row.alabel else
                                      (str(row.asset).split("#")[-1]
                                       .split("/")[-1] if row.asset
                                       else "Équipement inconnu")),
                            "eol_date": str(row.ed),
                            "source_note": str(row.sn),
                            "support_status": str(row.st),
                            "version_installed": (str(row.cv)
                                                  if row.cv is not None
                                                  else "inconnue"),
                            "version_eol": (str(row.pv)
                                            if row.pv is not None else ""),
                            "successor_version": (str(row.sv)
                                                 if row.sv is not None
                                                 else "consulter la feuille de route éditeur")}
            except Exception as parse_err:
                eol_notice = (f"⚠️ Volume EOL non parsable (rdflib) : "
                              f"{str(parse_err)[:120]} — enrichissement EOL ignoré")
        comp_covered: set = set()

        q = """
        PREFIX dkg: <http://dkg.cybersec.org/tbox#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        SELECT ?v ?vlabel ?score ?comp ?clabel ?asset ?alabel ?exact WHERE {
          ?v a dkg:Vulnerability .
          OPTIONAL { ?v rdfs:label ?vlabel }
          OPTIONAL { ?v dkg:cvssScore ?score }
          OPTIONAL { ?v skos:exactMatch ?exact }
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
            # EXG-CONF_1 : finding né de la confrontation (exactMatch vers CTI)
            # = confirmation FORMELLE par le fonds TLP:CLEAR.
            if getattr(row, "exact", None) is not None:
                status = (f"Révélé par confrontation CTI (TLP:CLEAR) — CVSS {score}"
                          if score else "Révélé par confrontation CTI (TLP:CLEAR)")
                severity = ("RED" if score and score >= 9.0
                            else ("AMBER" if score and score >= 7.0 else "CLEAR"))
                action = "Mise à jour du composant conseillée (patch éditeur)"
            elif cited and score:
                status = f"Confirmé par CTI locale — CVSS {score}"
                severity = ("RED" if score >= 9.0
                            else ("AMBER" if score >= 7.0 else "CLEAR"))
                action = "Mise à jour du composant conseillée (patch éditeur)"
            else:
                status = (f"Exposition locale — CVSS {score} (CTI locale silencieuse)"
                          if score else "Exposition locale (score inconnu)")
                severity = ("RED" if score and score >= 9.0
                            else ("AMBER" if score and score >= 7.0 else "CLEAR"))
                action = "Mise à jour du composant conseillée (patch éditeur)"
            finding = {
                "equipment": alabel,
                "component": f"{clabel} — {vlabel} ({vid})",
                "linkage": "formel",                     # DEM_4 : graphe formel
                "status": status, "severity": severity, "action": action
            }
            # GREFFON EOL_3 (Brique C2) : composant du finding en fin de
            # support → statut étoffé CVE/KEV + EOL sourcée (date EOL + note
            # de la source publique), action recalée sur la migration. Le
            # triplet source (dkg:sourceNote) voyage avec le finding.
            hit = eol_hits.get(str(row.comp)) if row.comp else None
            if hit:
                comp_covered.add(str(row.comp))
                finding["status"] = (
                    f"{status} ; Fin de support (EOL) : {hit['eol_date']} "
                    f"({hit['support_status']}) — version installée : "
                    f"{hit['version_installed']} ; successeur supporté : "
                    f"{hit['successor_version']} — source : "
                    f"{hit['source_note'][:90]}")
                finding["action"] = ("Migration vers un composant supporté "
                                     "requise (fin de support confirmée par "
                                     "la source EOL publique)")
                finding["eol_date"] = hit["eol_date"]
                finding["eol_source_note"] = hit["source_note"]
                finding["eol_version_installed"] = hit["version_installed"]
                finding["eol_successor_version"] = hit["successor_version"]
            bilan.append(finding)

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

        # GREFFON EOL_3 (Brique C2) : un composant en fin de support SANS
        # vulnérabilité connue dans l ABox audité produit quand même un
        # finding EOL autonome (date sourcée + triplet source) — la fin de
        # support est un risque en soi (plus de correctifs).
        for cu, hit in sorted(eol_hits.items()):
            if cu in comp_covered:
                continue
            bilan.append({
                "equipment": hit["asset"],
                "component": (f"{hit['label']}"
                              if hit["version_installed"] == "inconnue"
                              else f"{hit['label']} "
                                   f"(version installée : {hit['version_installed']})"),
                "linkage": "formel",
                "status": (f"Fin de support confirmée (EOL) : {hit['eol_date']} "
                           f"({hit['support_status']}) ; successeur supporté : "
                           f"{hit['successor_version']} — source : "
                           f"{hit['source_note'][:90]}"),
                "severity": "AMBER",
                "action": "Migration vers un composant supporté requise",
                "eol_date": hit["eol_date"],
                "eol_source_note": hit["source_note"],
                "eol_version_installed": hit["version_installed"],
                "eol_successor_version": hit["successor_version"]
            })
        if eol_notice:
            bilan.append({
                "equipment": "ABox locale", "component": "-",
                "status": eol_notice, "severity": "AMBER",
                "action": "Corriger le volume EOL (DKG_EOL_Source.ttl)"
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
    props_used = (set(re.findall(r"(?:dkg:|tbox#)([a-z]\w+)\s", abox))
                  | set(re.findall(r"(?:dkg:|tbox#)([a-z]\w+)\s", cti)))
    props_declared = set(re.findall(r"^dkg:([a-z]\w+)\s+a\s+owl:(?:Object|Datatype)Property",
                                    tbox_ref, flags=re.M))
    missing = sorted(props_used - props_declared - {"hasTLPMarking"})
    # Templates GOU_22 : désormais conformes GOU_18 (prefLabel FR/EN +
    # définition) — le Gardien ne propose jamais une entité sans couche SKOS.
    tmpl = {
        "exploitsWeakness": ("dkg:exploitsWeakness a owl:ObjectProperty ;\n"
            "    rdfs:domain dkg:Vulnerability ; rdfs:range dkg:Weakness ;\n"
            '    skos:prefLabel "exploits weakness"@en, "exploite la faiblesse"@fr ;\n'
            '    skos:definition "Relie une vulnérabilité à la faiblesse (CWE) '
            "qu'elle exploite.\"@fr ."),
        "isCisaKev": ("dkg:isCisaKev a owl:DatatypeProperty ;\n"
            "    rdfs:domain dkg:Vulnerability ; rdfs:range xsd:boolean ;\n"
            '    skos:prefLabel "is CISA KEV"@en, "référencé CISA KEV"@fr ;\n'
            '    skos:definition "Indique que la vulnérabilité figure au catalogue '
            "CISA KEV (exploitée activement).\"@fr ."),
        "targetsDevice": ("dkg:targetsDevice a owl:ObjectProperty ;\n"
            "    rdfs:domain dkg:ThreatActor ; rdfs:range dkg:DeviceCategory ;\n"
            '    skos:prefLabel "targets device category"@en, "cible la catégorie d\'appareil"@fr ;\n'
            "    skos:definition \"Relie un acteur de menace à la catégorie "
            "d'appareil qu'il recrute (ex. botnet -> caméras IP).\"@fr ."),
    }
    delta_parts = [tmpl[p] for p in missing if p in tmpl]
    delta_sections = []
    if delta_parts:
        header = ("@prefix dkg: <http://dkg.cybersec.org/tbox#> .\n"
                  "@prefix owl: <http://www.w3.org/2002/07/owl#> .\n"
                  "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n"
                  "@prefix skos: <http://www.w3.org/2004/02/skos/core#> .\n"
                  "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n")
        delta_sections.append(
            "# Delta TBox proposé (Gatekeeper HITL)\n"
            "# Justification EXG-FWK-P1-GOU_22 : propriétés du fonds CTI\n"
            "# (TLP:CLEAR coché) non déclarées dans la TBox de référence.\n"
            + header + "\n" + "\n\n".join(delta_parts))

    # Contrôle Gardien GOU_18 : annotations SKOS manquantes dans la TBox de
    # référence (proposition HITL d'annotation — jamais de fusion ici).
    skos_delta = _skos_annotation_delta(tbox_ref)
    if skos_delta:
        delta_sections.append(skos_delta)

    if delta_sections:
        return bilan, "\n\n".join(delta_sections) + "\n"
    return bilan, None
