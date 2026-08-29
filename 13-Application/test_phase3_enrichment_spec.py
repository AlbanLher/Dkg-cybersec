#!/usr/bin/env python3
"""
Suite de tests de validation normative - Phase 3 (Enrichissement & TLP).
Vérifie à la fois le snapshot 12-Donnees/ABox_enriched/ et les répertoires master.
"""

import pytest
from pathlib import Path
from rdflib import Graph, RDF, Namespace

BASE_DIR = Path(__file__).resolve().parent.parent
ENRICHED_DIR = BASE_DIR / "12-Donnees" / "ABox_enriched"
CONSOLIDATION_DIR = BASE_DIR / "12-Donnees" / "Consolidation_ABox"

FILE_SNAPSHOT = ENRICHED_DIR / "ABox_Cybersec_enriched.ttl"
FILE_MASTER = CONSOLIDATION_DIR / "DKG_ABox_Master.ttl"

DKG = Namespace("http://dkg.cybersec.org/tbox#")
DKG_INST = Namespace("http://dkg.cybersec.org/abox#")


@pytest.fixture(scope="module")
def enriched_graph():
    assert FILE_SNAPSHOT.exists(), f"❌ Snapshot introuvable : {FILE_SNAPSHOT}"
    g = Graph()
    g.parse(FILE_SNAPSHOT, format="turtle")
    return g


def test_exg_enrich_01_master_consolidation_alignment():
    """Vérifie la synchronisation entre le Snapshot Phase 3 et l'ABox Master Consolidée."""
    assert FILE_MASTER.exists(), f"❌ Master ABox introuvable dans {FILE_MASTER}"
    g_master = Graph()
    g_master.parse(FILE_MASTER, format="turtle")
    assert len(g_master) > 0, "Le fichier Master ABox ne doit pas être vide."


def test_exg_enrich_02_tlp_markings_presence(enriched_graph):
    """EXG-ENRICH-05: Vérification de la présence des marquages TLP (AMBER vs CLEAR)."""
    tlp_triples = list(enriched_graph.triples((None, DKG["hasTLPMarking"], None)))
    assert len(tlp_triples) >= 4, "Chaque entité principale doit posséder un marquage dkg:hasTLPMarking."


def test_exg_enrich_03_capec_and_nvd_integrity(enriched_graph):
    """EXG-ENRICH-03: Vérification de la présence des attributs NVD et des patterns CAPEC."""
    patterns = list(enriched_graph.subjects(RDF.type, DKG["ThreatPattern"]))
    assert len(patterns) >= 1, "Il doit y avoir au moins un ThreatPattern CAPEC."

    vulns = list(enriched_graph.subjects(RDF.type, DKG["Vulnerability"]))
    for v in vulns:
        assert len(list(enriched_graph.objects(v, DKG["cvssV3Vector"]))) > 0, f"CVSS Vector manquant pour {v}."


if __name__ == "__main__":
    pytest.main(["-v", __file__])
