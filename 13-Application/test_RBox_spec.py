#!/usr/bin/env python3
"""
Suite de Tests de Validation Normative pour la RBox Publique (Phase 3).
Vérifie :
  - 12-Donnees/TLP-CLEAR_RBox_NVD-CWE/RBox_Cybersec.ttl (Syntaxe, score CVSS, classification CWE)
  - 12-Donnees/TLP-CLEAR_RBox_NVD-CWE/RBox_Cybersec.md (Diagramme Mermaid)
Conforme à : SpecificationNormativeEnrichissementRBox.md
Classification : TLP:CLEAR
"""

from pathlib import Path
import pytest
from rdflib import RDF, RDFS, OWL, Graph, Namespace

BASE_DIR = Path(__file__).resolve().parent.parent
RBOX_DIR = BASE_DIR / "12-Donnees" / "TLP-CLEAR_RBox_NVD-CWE"
RBOX_TTL = RBOX_DIR / "RBox_Cybersec.ttl"
RBOX_MD = RBOX_DIR / "RBox_Cybersec.md"

DKG = Namespace("http://dkg.cybersec.org/tbox#")
RBOX = Namespace("http://dkg.cybersec.org/rbox#")


@pytest.fixture(scope="module")
def rbox_graph():
    """Charge le graphe RBox."""
    assert RBOX_TTL.exists(), f"Le fichier RBox est introuvable : {RBOX_TTL}"
    g = Graph()
    g.parse(RBOX_TTL, format="turtle")
    return g


def test_rbox_01_ttl_validity_and_header(rbox_graph):
    """TEST-RBOX-01 : Valide le fichier Turtle et l'entête OWL."""
    assert len(rbox_graph) > 0, "Le graphe RBox est vide."
    rbox_ont = RBOX[""]
    assert (rbox_ont, RDF.type, OWL.Ontology) in rbox_graph, "Ontologie RBox non déclarée."
    assert (rbox_ont, OWL.imports, DKG[""]) in rbox_graph, "Import OWL de la TBox manquant."


def test_rbox_02_vulnerabilities_and_cvss(rbox_graph):
    """TEST-RBOX-02 : Vérifie qu'au moins une CVE existe avec un score CVSS."""
    cves = list(rbox_graph.subjects(RDF.type, DKG.Vulnerability))
    assert len(cves) > 0, "Aucune vulnérabilité trouvée dans la RBox."

    for cve in cves:
        scores = list(rbox_graph.objects(cve, DKG.cvssScore))
        assert len(scores) > 0, f"Score CVSS manquant pour {cve}"


def test_rbox_03_cve_to_cwe_link(rbox_graph):
    """TEST-RBOX-03 : Vérifie la liaison dkg:classifiedUnder vers un dkg:Weakness."""
    cves = list(rbox_graph.subjects(RDF.type, DKG.Vulnerability))
    for cve in cves:
        cwes = list(rbox_graph.objects(cve, DKG.classifiedUnder))
        assert len(cwes) > 0, f"La vulnérabilité {cve} n'est reliée à aucun CWE."
        for cwe in cwes:
            assert (cwe, RDF.type, DKG.Weakness) in rbox_graph, f"L'entité {cwe} n'est pas typée dkg:Weakness."


def test_rbox_04_markdown_and_mermaid_validity():
    """TEST-RBOX-04 : Vérifie la présence du fichier RBox_Cybersec.md et du bloc Mermaid."""
    assert RBOX_MD.exists(), f"Fichier de restitution RBox introuvable : {RBOX_MD}"
    content = RBOX_MD.read_text(encoding="utf-8")

    assert "```mermaid" in content, "Bloc Mermaid manquant dans RBox_Cybersec.md"
    assert "classifiedUnder" in content, "La relation classifiedUnder doit figurer dans le diagramme."


if __name__ == "__main__":
    import sys
    sys.exit(pytest.main(["-v", __file__]))
