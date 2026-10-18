# =============================================================================
# core/confrontation.py — TLP:AMBER (RBox applicative P8/P9)
# CONFRONTATION_1 : la SEULE porte d'entrée des vulnérabilités dans le graphe
# local (standard P9 : le scan/seed ne produit que de l'inventaire).
# Calé sur le SSOT core.config : SEED_ABOX_HOTE_PATH / SEED_ABOX_FOYER_PATH /
# SEED_CTI_CLEAR_PATH (fonds TLP:CLEAR = DKG_ABox_CTI_External.ttl),
# WORKSET_ABOX_RED (écriture findings), namespaces DKG_DATA/DKG_CTI.
#
# Aucune écriture des seeds (RES_1). Les findings produits sont écrits dans
# le WORKSET (seul espace écrit par la démo) sous
# WORKSET_ABOX_RED/DKG_ABox_Findings_Confrontation.ttl — purgeables (R3).
#
# API :
#   load_inventory(mode)                  -> Graph  (ABox seed, inventaire pur)
#   run_confrontation(g, funds_path=None,
#                     sources=None)      -> dict   (findings + stats) ;
#       sources = ids des sources CTI cochées (catalogue P7). Chaque CVE du
#       fonds porte dkg:providedBy ; la confrontation n'utilise QUE les CVE
#       dont la provenance intersecte les sources cochées (EXG-MET-P8-DEM_2 :
#       la collecte dépend de la source cochée). sources=None/[] => tout le
#       fonds (comportement catalogue complet).
#   purge_findings(g)                     -> int
#   findings_ttl(mode)                    -> str    (sérialisation findings)
#   find_findings(g)                      -> list[dict]  (pour le bilan NL)
# =============================================================================
"""
Traçabilté : EXG-FWK-P8-AGE_1, EXG-MET-P8-RES_1, + EXG-CONF_1
(P9 anticipé — non encore déclaré en spec)
"""



from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

from rdflib import Graph, Namespace
from rdflib.namespace import RDF

from core import config

DKG = Namespace(str(config.DKG_TBOX))
DKG_DATA = Namespace(str(config.DKG_DATA))
DKG_CTI = Namespace(str(config.DKG_CTI))

# Marqueur des findings PRODUITS par la confrontation (purge R3) :
# IRI locale dérivée de la CVE du fonds — n'existe jamais dans un seed.
LOCAL_CVE_PREFIX = str(DKG_DATA["Local-"])

# --- La règle CONFRONTATION_1 (vivant commenté dans DKG_Rules_DemoRef.ttl) ---
# Le code ne fait que l'EXÉCUTER : toute évolution métier se fait en RBox.
CONFRONTATION_1 = """
PREFIX dkg: <http://dkg.cybersec.org/tbox#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
CONSTRUCT {
  ?localCve a dkg:Vulnerability ;
      dkg:cveId ?cveId ;
      rdfs:label ?lbl ;
      dkg:cvssScore ?score ;
      dkg:hasTLPMarking ?tlp ;
      skos:exactMatch ?ctiCve .
  ?comp dkg:hasVulnerability ?localCve .
  ?localCve dkg:isVulnerabilityOf ?comp .
}
WHERE {
  ?ctiCve a dkg:Vulnerability ;
      dkg:cveId ?cveId ;
      rdfs:label ?lbl ;
      dkg:cvssScore ?score ;
      dkg:affectsComponentId ?cid ;
      dkg:affectsVersion ?ver .
  ?comp a dkg:SoftwareComponent ;
      dkg:componentId ?cid ;
      dkg:version ?ver .
  ?comp dkg:isComponentOf ?asset .
  ?asset dkg:hasTLPMarking ?tlp .
  BIND(IRI(CONCAT("http://dkg.cybersec.org/data#Local-", ?cveId)) AS ?localCve)
  FILTER NOT EXISTS {
    ?existing dkg:cveId ?cveId .
    FILTER(STRSTARTS(STR(?existing), "http://dkg.cybersec.org/data#Local-"))
  }
}
"""

_COUNT_LOCAL = """
PREFIX dkg: <http://dkg.cybersec.org/tbox#>
SELECT (COUNT(?v) AS ?n) WHERE {
  ?v a dkg:Vulnerability .
  FILTER(STRSTARTS(STR(?v), "http://dkg.cybersec.org/data#"))
}
"""


def load_inventory(mode: str = "foyer") -> Graph:
    """Charge l'ABox seed du mode demandé (lecture seule — RES_1).
    mode='foyer' -> SEED_ABOX_FOYER_PATH ; 'hote' -> SEED_ABOX_HOTE_PATH."""
    path = (config.SEED_ABOX_FOYER_PATH if mode == "foyer"
            else config.SEED_ABOX_HOTE_PATH)
    g = Graph()
    g.parse(str(path), format="turtle")
    return g


def count_local_vulnerabilities(g: Graph) -> int:
    """Garde recette R1 : 0 attendu sur l'inventaire pur (avant CTI)."""
    for row in g.query(_COUNT_LOCAL):
        return int(row[0])
    return 0


def run_confrontation(g: Graph,
                      funds_path: Optional[Path] = None,
                      sources: Optional[List[str]] = None) -> Dict[str, Any]:
    """CTI COCHÉ : exécution de CONFRONTATION_1 contre le fonds CLEAR
    (SEED_CTI_CLEAR_PATH) — sans jamais polluer l'ABox locale.

    EXG-CONF_1 : le fonds est parsé dans un graphe TEMPORAIRE ; la règle
    s'exécute sur l'union (inventaire + fonds) ; seuls les findings
    produits (IRI dkg-data:Local-*) sont ajoutés à g. Aucune instance du
    fonds (namespace dkg.cti) n'entre dans le graphe local.

    sources (EXG-MET-P8-DEM_2) : ids des sources cochées. Chaque CVE du
    fonds porte dkg:providedBy (une ou plusieurs provenances) ; seules les
    CVE dont AU MOINS une provenance ∈ sources participent à la règle.
    sources=None/[] => tout le fonds (aucun filtre).
    Retourne les stats + findings pour l'IHM (compteurs avant/après)."""
    path = Path(funds_path) if funds_path else config.SEED_CTI_CLEAR_PATH
    if not path.exists():
        raise FileNotFoundError(
            f"Fonds CTI introuvable : {path} — déposer DKG_ABox_CTI_External.ttl "
            f"dans {config.DIR_SEED_CTI_CLEAR} (seed TLP:CLEAR)."
        )
    before = count_local_vulnerabilities(g)

    # Le fonds vit dans un graphe séparé — il ne fusionne JAMAIS dans g.
    funds_g = Graph()
    funds_g.parse(str(path), format="turtle")
    funds_triples = len(funds_g)

    # --- Filtre de provenance (la collecte dépend de la source cochée) ------
    vuln_subjects = set(funds_g.subjects(RDF.type, DKG.Vulnerability))
    selected = set(vuln_subjects)                      # défaut : tout le fonds
    sources_filter = sorted(set(sources)) if sources else []
    if sources_filter:
        selected = set()
        q_prov = """
        PREFIX dkg: <http://dkg.cybersec.org/tbox#>
        SELECT ?v ?src WHERE { ?v a dkg:Vulnerability ; dkg:providedBy ?src . }
        """
        for row in funds_g.query(q_prov):
            if str(row.src) in sources_filter:
                selected.add(row.v)
        # CVE sans providedBy = connaissance CTI non attribuée à une source :
        # on l'exclut du filtre strict (elle n'appartient à aucune coche).

    # Union éphémère (lecture seule) pour l'évaluation de la règle.
    union = Graph()
    for triple in g:
        union.add(triple)
    for triple in funds_g:
        s = triple[0]
        if s in vuln_subjects and s not in selected:
            continue           # CVE d'une source NON cochée : ignorée
        union.add(triple)

    # Exécution de CONFRONTATION_1 sur l'union ; seuls les findings
    # produits entrent dans le graphe local g.
    findings_g = union.query(CONFRONTATION_1).graph
    produced = len(set(findings_g.subjects(RDF.type, DKG.Vulnerability)))
    for triple in findings_g:
        g.add(triple)

    return {
        "funds_path": str(path),
        "funds_triples": funds_triples,
        "sources_filter": sources_filter,       # [] => tout le fonds
        "findings_produced": produced,
        "local_vulnerabilities_before": before,
        "local_vulnerabilities": count_local_vulnerabilities(g),
        "findings": find_findings(g),
    }


def purge_findings(g: Graph) -> int:
    """R3 : retire tout ce que la confrontation a produit (findings locaux
    + fonds CLEAR). Le graphe retourne à l'inventaire pur."""
    removed = 0
    to_remove = []
    for s, p, o in g:
        s_str, o_str = str(s), str(o)
        if s_str.startswith(LOCAL_CVE_PREFIX) or o_str.startswith(LOCAL_CVE_PREFIX):
            to_remove.append((s, p, o))
        elif s_str.startswith(str(DKG_CTI)) or o_str.startswith(str(DKG_CTI)):
            to_remove.append((s, p, o))
    for t in to_remove:
        g.remove(t)
        removed += 1
    return removed


def find_findings(g: Graph) -> List[Dict[str, Any]]:
    """Liste les findings locaux (produits) au format bilan NL
    (clés equipment/component/status/severity/action — AGE_1/DEM_1)."""
    q = """
    PREFIX dkg: <http://dkg.cybersec.org/tbox#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    SELECT ?equip ?compName ?cveId ?score ?cti WHERE {
      ?cve a dkg:Vulnerability ;
          dkg:cveId ?cveId ; dkg:cvssScore ?score ;
          skos:exactMatch ?cti .
      FILTER(STRSTARTS(STR(?cve), "http://dkg.cybersec.org/data#Local-"))
      ?cve dkg:isVulnerabilityOf ?comp .
      ?comp rdfs:label ?compName ; dkg:isComponentOf ?asset .
      ?asset rdfs:label ?equip .
    } ORDER BY DESC(?score)
    """
    items = []
    for row in g.query(q):
        items.append({
            "equipment": str(row.equip),
            "component": str(row.compName),
            "cve_id": str(row.cveId),
            "cvss": float(row.score),
            "cti_iri": str(row.cti),
            "status": "confrontation CTI (TLP:CLEAR)",
            "severity": "RED" if float(row.score) >= 9.0 else "AMBER",
            "action": (f"Mettre à jour {row.compName} (CVE {row.cveId}, "
                       f"CVSS {float(row.score)} — voir fonds CTI {row.cti})"),
            "linkage": "formel",
        })
    return items


def findings_ttl(mode: str = "foyer") -> str:
    """Sérialise l'ABox + findings pour l'IHM (vue RED consolidée)."""
    g = load_inventory(mode)
    run_confrontation(g)
    return g.serialize(format="turtle")
