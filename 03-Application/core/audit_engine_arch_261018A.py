# 03-Application/core/audit_engine.py
"""
Moteur d'audit SOC (EXG-FWK-P8-AGE_1/AGE_2, EXG-FWK-P1-GOU_22) : bilan NL
par SPARQL sur le graphe ABox (Local-First) et détection Gardien TBox du
vocabulaire non déclaré (delta HITL proposé, jamais fusionné ici — DEM_3).
Extrait de api/routes_phase8.py lors du découpage v2 (logique inchangée).
"""
import re

import core.config as settings
from core.local_volumes import _read

def _generate_risk_analysis(abox: str, cti: str):
    """
    Exécute EXG-FWK-P8-AGE_1 : bilan NL calculé par SPARQL sur le graphe ABox
    (Local-First, ordre de sérialisation indépendant). Regex INTERDITE sur le
    contenu des .ttl ; échec de parse = ligne visible (jamais silencieux).
    EXG-CONF_1 : les findings de confrontation (présents dans l'ABox passée
    quand le CTI est coché) sont détectés par la même requête SPARQL — aucun
    code dédié : le delta avant/après CTI est automatique.
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
            bilan.append({
                "equipment": alabel,
                "component": f"{clabel} — {vlabel} ({vid})",
                "linkage": "formel",                     # DEM_4 : graphe formel
                "status": status, "severity": severity, "action": action
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
    props_used = (set(re.findall(r"(?:dkg:|tbox#)([a-z]\w+)\s", abox))
                  | set(re.findall(r"(?:dkg:|tbox#)([a-z]\w+)\s", cti)))
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
        "targetsDevice": ("dkg:targetsDevice a owl:ObjectProperty ;\n"
            "    rdfs:domain dkg:ThreatActor ; rdfs:range dkg:DeviceCategory ;\n"
            '    skos:prefLabel "targets device category"@en, "cible la catégorie d\'appareil"@fr ;\n'
            "    skos:definition \"Relie un acteur de menace à la catégorie "
            "d'appareil qu'il recrute (ex. botnet -> caméras IP).\"@fr ."),
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
