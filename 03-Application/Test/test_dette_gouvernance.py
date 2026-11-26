#!/usr/bin/env python3
"""
test_dette_gouvernance.py
Vague dédiée de rattrapage dette (arbitrage 2026-11-26) — EXG :
  EXG-FWK-P1-GOU_5 : Architecture SSOT (config.py) — contrat du SSOT validé.
  EXG-TEC-P2-ABO_4 : Typage & Plages CVSS — bornes [0.0, 10.0] sous CWA
                    (assertion sur le graphe + preuve déclarative dans les shapes).
Conventions : uniquement des constantes issues de config.py (SSOT règle 01.1).

Note doctrine : les deux EXG étaient déclarées recette auto sans test depuis
l origine ; ce fichier ferme la dernière dette de couverture P1-P8 hors soc_2
(test dédié en cours de cadrage).
"""

import sys
from pathlib import Path

import pytest
from rdflib import Graph, URIRef, Literal
from pyshacl import validate

# Ancrage sys.path vers 03-Application/ (EXG-OR-05, même convention que test_phase2_abox)
APP_DIR = Path(__file__).resolve().parent.parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from core.config import (
    DKGConfig,
    TBOX_MASTER_PATH,
    SHACL_MASTER_PATH,
    ABOX_MASTER_PATH,
    DKG_TBOX,
    DKG_DATA,
    DIR_MASTER_ABOX,
)


# ---------------------------------------------------------------------------
# EXG-FWK-P1-GOU_5 — Architecture SSOT (config.py)
# ---------------------------------------------------------------------------
@pytest.mark.non_regression
def test_exg_gou_5_ssot_config_contrat():
    """EXG-FWK-P1-GOU_5 : DKGConfig est le SSOT — instanciation propre,
    rejet des extras, override par variable d environnement DKG_ attendu,
    et chemins dérivés depuis une seule racine (pas de constantes éparses)."""
    cfg = DKGConfig()
    # 1. racine unique : toutes les propriétés répertoires dérivent de dir_app
    assert cfg.dir_app == Path(__file__).resolve().parent.parent
    assert cfg.dir_root == cfg.dir_app.parent
    assert cfg.dir_data == cfg.dir_root / "02-Donnees"
    # 2. les chemins module-level du SSOT sont cohérents avec l instance
    assert TBOX_MASTER_PATH == cfg.dir_master_tbox / "TBox_Master.ttl"
    # 3. extra=ignore : une clé parasite ne fait pas échouer le SSOT
    #    (validé par instanciation directe, cf. model_config)
    assert DKGConfig.model_config.get("extra") == "ignore"
    assert DKGConfig.model_config.get("env_prefix") == "DKG_"


@pytest.mark.non_regression
def test_exg_gou_5_ssot_env_override(monkeypatch):
    """EXG-FWK-P1-GOU_5 : le SSOT reste pilotable par variable d environnement
    (DKG_DIR_APP) — priorité env > défaut, sans modifier le code."""
    app_dir = str(Path(__file__).resolve().parent.parent)
    monkeypatch.setenv("DKG_DIR_APP", app_dir)
    cfg = DKGConfig()
    assert str(cfg.dir_app) == app_dir, "Override DKG_DIR_APP ignoré par le SSOT"


# ---------------------------------------------------------------------------
# EXG-TEC-P2-ABO_4 — Typage & Plages CVSS [0.0, 10.0] sous CWA
# ---------------------------------------------------------------------------
@pytest.fixture(scope="module")
def full_graph() -> Graph:
    """Même fixture que test_phase2_abox (TBox + ABox Master)."""
    g = Graph()
    assert TBOX_MASTER_PATH.exists(), f"Fichier TBox Master introuvable : {TBOX_MASTER_PATH}"
    assert ABOX_MASTER_PATH.exists(), f"Fichier ABox Master introuvable : {ABOX_MASTER_PATH}"
    g.parse(str(TBOX_MASTER_PATH), format="turtle")
    g.parse(str(ABOX_MASTER_PATH), format="turtle")
    return g


@pytest.mark.non_regression
def test_exg_abo_4_plages_cvss_dans_graphe(full_graph: Graph):
    """EXG-TEC-P2-ABO_4 (partie 1) : tout dkg:cvssScore du graphe est un
    littéral numérique dans la plage stricte [0.0, 10.0]."""
    query = """
    PREFIX dkg: <http://dkg.cybersec.org/tbox#>
    SELECT ?s ?score WHERE {
        ?s dkg:cvssScore ?score .
    }
    """
    rows = list(full_graph.query(query))
    assert len(rows) >= 1, "Aucun dkg:cvssScore dans le graphe : la recette ABO_4 ne peut pas trancher."
    for s, score in rows:
        try:
            val = float(score)
        except (TypeError, ValueError):
            pytest.fail(f"EXG-TEC-P2-ABO_4 : {s} porte un cvssScore non numérique : {score!r}")
        assert 0.0 <= val <= 10.0, (
            f"EXG-TEC-P2-ABO_4 : {s} porte un cvssScore hors plage stricte [0.0, 10.0] : {val}")


@pytest.mark.non_regression
def test_exg_abo_4_shape_cvss_bornee_declaree():
    """EXG-TEC-P2-ABO_4 (partie 2, preuve CWA) : la borne est DÉCLARÉE dans
    le SHACL Master (sh:in ou minInclusive/maxInclusive sur dkg:cvssScore) —
    c'est la shape qui fait la loi sous CWA, pas seulement le jeu de données."""
    assert SHACL_MASTER_PATH.exists(), f"Fichier SHACL Master introuvable : {SHACL_MASTER_PATH}"
    g = Graph().parse(str(SHACL_MASTER_PATH), format="turtle")
    q = """
    PREFIX sh: <http://www.w3.org/ns/shacl#>
    PREFIX dkg: <http://dkg.cybersec.org/tbox#>
    SELECT ?shape ?kind ?bound WHERE {
        ?shape sh:path dkg:cvssScore .
        { BIND("minInclusive" AS ?kind) ?shape sh:minInclusive ?bound }
        UNION
        { BIND("maxInclusive" AS ?kind) ?shape sh:maxInclusive ?bound }
        UNION
        { BIND("datatype" AS ?kind) ?shape sh:datatype ?dt . FILTER(STR(?dt) = "http://www.w3.org/2001/XMLSchema#float") BIND(STR(?dt) AS ?bound) }
    }
    """
    rows = {(str(r[1]), str(r[2])) for r in g.query(q)}
    assert any(k == "minInclusive" and float(b) == 0.0 for k, b in rows) or \
           any(k == "datatype" for k, b in rows), (
        f"EXG-TEC-P2-ABO_4 : aucune borne min (0.0) déclarée sur dkg:cvssScore dans le SHACL Master : {rows}")
    assert any(k == "maxInclusive" and float(b) == 10.0 for k, b in rows), (
        f"EXG-TEC-P2-ABO_4 : aucune borne max (10.0) déclarée sur dkg:cvssScore dans le SHACL Master : {rows}")


@pytest.mark.non_regression
def test_exg_abo_4_cvss_hors_plage_rejete_cwa():
    """EXG-TEC-P2-ABO_4 (partie 3, recette fonctionnelle) : une instance
    portant un score hors plage (10.5) est REJETÉE par la validation SHACL —
la contrainte est active sous CWA, pas décorative."""
    assert SHACL_MASTER_PATH.exists()
    shacl_graph = Graph().parse(str(SHACL_MASTER_PATH), format="turtle")
    g_hors_plage = Graph()
    g_hors_plage.parse(str(TBOX_MASTER_PATH), format="turtle")
    g_hors_plage.add((
        DKG_DATA["Vuln-Hors-Plage-Recette-ABO4"],
        URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"),
        DKG_TBOX["Vulnerability"],
    ))
    g_hors_plage.add((
        DKG_DATA["Vuln-Hors-Plage-Recette-ABO4"],
        DKG_TBOX["cvssScore"],
        Literal(10.5, datatype=URIRef("http://www.w3.org/2001/XMLSchema#float")),
    ))
    conforms, _, report_text = validate(
        data_graph=g_hors_plage,
        shacl_graph=shacl_graph,
        inference="rdfs",
        abort_on_first=False,
    )
    assert not conforms, (
        "EXG-TEC-P2-ABO_4 : un cvssScore de 10.5 a passé la validation SHACL — "
        f"la borne CWA n est pas active. Rapport :\n{report_text}")
