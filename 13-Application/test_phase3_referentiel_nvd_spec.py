#!/usr/bin/env python3
"""
Suite de tests de validation normative - Phase 2 (ABox).
Vérifie la conformité du dossier 12-Donnees/ABox_init/ par rapport aux exigences SPEC-02.
"""

import pytest
from pathlib import Path
from rdflib import Graph, RDF, RDFS, OWL, Namespace

BASE_DIR = Path(__file__).resolve().parent.parent
ABOX_DIR = BASE_DIR / "12-Donnees" / "ABox_init"
FILE_TTL = ABOX_DIR / "ABox_Cybersec.ttl"
FILE_MD = ABOX_DIR / "ABox_Cybersec.md"

DKG = Namespace("http://dkg.cybersec.org/tbox#")
DKG_INST = Namespace("http://dkg.cybersec.org/abox#")


@pytest.fixture(scope="module")
def abox_graph():
    """Charge le graphe RDF de l'ABox depuis le dossier ABox_init."""
    assert FILE_TTL.exists(), f"❌ Fichier introuvable : {FILE_TTL}. Exécutez generate_ABox_initiale.py au préalable."
    g = Graph()
    g.parse(FILE_TTL, format="turtle")
    return g


def test_exg_abox_01_namespaces_and_instances(abox_graph):
    """EXG-ABOX-01: Vérification du namespace d'instances et de la présence d'individus."""
    instances = list(abox_graph.subjects(RDF.type, None))
    assert len(instances) > 0, "L'ABox doit contenir des instances."
    
    inst_namespaces = {str(s).split("#")[0] + "#" for s in instances if "#" in str(s)}
    assert "http://dkg.cybersec.org/abox#" in inst_namespaces, "Les instances doivent utiliser le namespace dkg-inst."


def test_exg_abox_02_typing_and_classes(abox_graph):
    """EXG-ABOX-02: Vérification que toutes les instances sont typées avec des classes TBox validées."""
    assets = list(abox_graph.subjects(RDF.type, DKG["Asset"]))
    comps = list(abox_graph.subjects(RDF.type, DKG["SoftwareComponent"]))
    vulns = list(abox_graph.subjects(RDF.type, DKG["Vulnerability"]))

    assert len(assets) >= 1, "Il doit y avoir au moins une instance de dkg:Asset."
    assert len(comps) >= 1, "Il doit y avoir au moins une instance de dkg:SoftwareComponent."
    assert len(vulns) >= 1, "Il doit y avoir au moins une instance de dkg:Vulnerability."


def test_exg_abox_03_relationships_integrity(abox_graph):
    """EXG-ABOX-03: Vérification de l'intégrité des relations entre instances."""
    has_comp_triples = list(abox_graph.triples((None, DKG["hasInstalledComponent"], None)))
    assert len(has_comp_triples) > 0, "Des relations hasInstalledComponent doivent relier Assets et Composants."

    has_vuln_triples = list(abox_graph.triples((None, DKG["hasVulnerability"], None)))
    assert len(has_vuln_triples) > 0, "Des relations hasVulnerability doivent relier Composants et CVEs."


def test_exg_abox_04_rbox_inverse_consistency(abox_graph):
    """EXG-ABOX-04: Vérification de la réciprocité de la relation inverse (isComponentOf)."""
    for asset, _, comp in abox_graph.triples((None, DKG["hasInstalledComponent"], None)):
        is_comp_triples = list(abox_graph.triples((comp, DKG["isComponentOf"], asset)))
        assert len(is_comp_triples) > 0, f"L'inférence inverse isComponentOf manque entre {comp} et {asset}."


def test_abox_markdown_report_integrity():
    """Vérification du rapport Markdown ABox_Cybersec.md."""
    assert FILE_MD.exists(), f"❌ Rapport Markdown introuvable dans : {FILE_MD}"
    content = FILE_MD.read_text(encoding="utf-8")
    
    assert "```mermaid" in content, "Le rapport ABox doit intégrer un diagramme Mermaid."
    assert "Métriques du Jeu d'Instances" in content, "Le rapport ABox doit inclure la section métriques."


if __name__ == "__main__":
    pytest.main(["-v", __file__])
