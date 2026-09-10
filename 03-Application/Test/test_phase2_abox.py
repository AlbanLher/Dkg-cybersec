#!/usr/bin/env python3
"""
test_phase2_quality.py
Suite de tests d'intégration, d'intégrité référentielle et de recette SHACL (Phase 2).
Aligné sur les spécifications SPEC-SOCLE, SPEC-TECH et SPEC-METIER.
Respect strict de la règle SSOT : uniquement des constantes issues de config.py.
"""

import sys
from pathlib import Path
import pytest
from rdflib import Graph
from pyshacl import validate

# 1. Ancrage sys.path vers 03-Application/ pour importer config.py (EXG-OR-05)
APP_DIR = Path(__file__).resolve().parent.parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

# Import exclusif des constantes déclarées dans config.py
from config import (
    TBOX_MASTER_PATH,
    SHACL_MASTER_PATH,
    ABOX_MASTER_PATH,
    DKG_TBOX,
    DKG_DATA,
    DIR_SNAPSHOT_P2,
    DIR_MASTER_ABOX,
)


@pytest.fixture(scope="module")
def full_graph() -> Graph:
    """Charge l'ensemble TBox + ABox dans un graphe RDF global pour les tests d'intégration."""
    g = Graph()
    assert TBOX_MASTER_PATH.exists(), f"Fichier TBox Master introuvable : {TBOX_MASTER_PATH}"
    assert ABOX_MASTER_PATH.exists(), f"Fichier ABox Master introuvable : {ABOX_MASTER_PATH}"
    
    g.parse(str(TBOX_MASTER_PATH), format="turtle")
    g.parse(str(ABOX_MASTER_PATH), format="turtle")
    return g


def test_exg_uc_abox_tlp_marking(full_graph: Graph):
    """Vérifie l'application et la présence explicite du marquage TLP:RED sur les actifs (SPEC-METIER)."""
    query = """
    PREFIX dkg: <http://dkg.cybersec.org/tbox#>
    PREFIX data: <http://dkg.cybersec.org/data#>

    SELECT ?tlp WHERE {
        ?asset a dkg:Asset ;
               dkg:hasTLPMarking ?tlp .
        ?tlp a dkg:TLPMarking .
    }
    """
    res = [str(row[0]) for row in full_graph.query(query)]
    expected_tlp_red = str(DKG_DATA["TLP-RED"])
    assert expected_tlp_red in res, f"Marquage TLP:RED introuvable sur les actifs. Trouvé: {res}"


def test_exg_uc_abox_01_namespace_integrity(full_graph: Graph):
    """EXG-UC-ABOX-01 : Validation de l'isolation stricte des Namespaces TBox (tbox#) et Data (data#)."""
    query = """
    PREFIX dkg: <http://dkg.cybersec.org/tbox#>
    SELECT ?s WHERE {
        ?s a ?type .
        FILTER(STRSTARTS(STR(?type), "http://dkg.cybersec.org/tbox#"))
        FILTER(!STRSTARTS(STR(?s), "http://dkg.cybersec.org/data#"))
    }
    """
    res = list(full_graph.query(query))
    assert len(res) == 0, f"Instances hors namespace dkg-data détectées : {[row[0] for row in res]}"


def test_exg_uc_abox_03_cyber_chain_completeness(full_graph: Graph):
    """
    EXG-UC-ABOX-03 : Complétude de la chaîne CTI Traversante.
    Asset -> SoftwareComponent -> Vulnerability -> Weakness -> ThreatPattern
    Utilise le prédicat normé dkg:exploitsWeakness (SPEC-TECH-UC01).
    """
    query = """
    PREFIX dkg: <http://dkg.cybersec.org/tbox#>
    SELECT ?asset ?comp ?cve ?cwe ?capec WHERE {
        ?asset a dkg:Asset ;
               dkg:hasInstalledComponent ?comp .
        ?comp a dkg:SoftwareComponent ;
              dkg:hasVulnerability ?cve .
        ?cve a dkg:Vulnerability ;
             dkg:exploitsWeakness ?cwe .
        ?cwe a dkg:Weakness ;
             dkg:hasThreatPattern ?capec .
        ?capec a dkg:ThreatPattern .
    }
    """
    res = list(full_graph.query(query))
    assert len(res) > 0, "La chaîne CTI complète (Asset -> Component -> CVE -> CWE -> CAPEC) est absente !"


def test_exg_fwk_02_01_referential_integrity(full_graph: Graph):
    """EXG-FWK-02-01 : Intégrité référentielle globale (0 instance ou ressource orpheline non typée)."""
    query = """
    PREFIX dkg: <http://dkg.cybersec.org/tbox#>
    SELECT ?s ?p ?o WHERE {
        ?s ?p ?o .
        FILTER(isURI(?o))
        FILTER(STRSTARTS(STR(?o), "http://dkg.cybersec.org/data#"))
        FILTER NOT EXISTS { ?o a ?type }
    }
    """
    res = list(full_graph.query(query))
    assert len(res) == 0, f"URIs d'instances orphelines non déclarées dans dkg-data : {res}"


def test_exg_qual_02_03_shacl_validation(full_graph: Graph):
    """EXG-QUAL-02 / EXG-QUAL-03 : Validation SHACL sous CWA (0 violation tolérée)."""
    assert SHACL_MASTER_PATH.exists(), f"Fichier SHACL Master introuvable : {SHACL_MASTER_PATH}"
    shacl_graph = Graph().parse(str(SHACL_MASTER_PATH), format="turtle")
    
    conforms, report_graph, report_text = validate(
        data_graph=full_graph,
        shacl_graph=shacl_graph,
        inference="rdfs",
        abort_on_first=False,
        meta_shacl=False,
    )
    
    assert conforms, f"Violations SHACL détectées lors de la recette ABox Phase 2 :\n{report_text}"


def test_exg_org_02_phase2_master_snapshot_parity():
    """
    EXG-OR-06 : Vérification de la parité stricte entre Snapshot Phase 2 et Master ABox.
    Garantit l'absence de dérive entre les livrables d'archivage et le Master transversal.
    """
    assert DIR_SNAPSHOT_P2.exists(), f"Répertoire Snapshot Phase 2 introuvable : {DIR_SNAPSHOT_P2}"
    assert DIR_MASTER_ABOX.exists(), f"Répertoire Master ABox introuvable : {DIR_MASTER_ABOX}"

    # Vérification ciblée sur l'ABox TTL et sa documentation MD
    snapshot_files = [
        f for f in DIR_SNAPSHOT_P2.iterdir()
        if f.is_file() and f.name in {ABOX_MASTER_PATH.name, ABOX_MASTER_PATH.with_suffix(".md").name}
    ]

    assert len(snapshot_files) > 0, "Aucun fichier ABox/Doc valide trouvé dans le Snapshot Phase 2 !"

    for snap_file in snapshot_files:
        master_file = DIR_MASTER_ABOX / snap_file.name
        assert master_file.exists(), f"Fichier synchronisé absent du Master ABox : {master_file}"
        
        # Comparaison contenu texte normalisé (fin de ligne CRLF -> LF)
        snap_content = snap_file.read_text(encoding="utf-8").strip().replace("\r\n", "\n")
        master_content = master_file.read_text(encoding="utf-8").strip().replace("\r\n", "\n")
        
        assert snap_content == master_content, f"Désynchronisation détectée sur {snap_file.name} entre Snapshot et Master !"
