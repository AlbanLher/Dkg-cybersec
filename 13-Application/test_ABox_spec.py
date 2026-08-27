#!/usr/bin/env python3
"""
Suite de Tests de Validation Normative pour l'ABox Privée (Phase 2).
Vérifie :
  - 12-Donnees/ABox_init/ABox_Cybersec.ttl (Syntaxe, URIs, alignement TBox)
  - 12-Donnees/ABox_init/ABox_Cybersec.md (Doc, Lexique et Mermaid)
Conforme à : 11-Principes_Architecture/Specifications/SpecificationNormativeIngestionABox.md
"""

from pathlib import Path
import pytest
from rdflib import RDF, RDFS, OWL, Graph, Namespace

# Dynamic base path resolution
BASE_DIR = Path(__file__).resolve().parent.parent
ABOX_TTL = BASE_DIR / "12-Donnees" / "ABox_init" / "ABox_Cybersec.ttl"
ABOX_MD = BASE_DIR / "12-Donnees" / "ABox_init" / "ABox_Cybersec.md"

DKG = Namespace("http://dkg.cybersec.org/tbox#")
ABOX = Namespace("http://dkg.cybersec.org/abox#")


@pytest.fixture(scope="module")
def abox_graph():
    """Charge le graphe ABox pour l'ensemble de la session de test."""
    assert ABOX_TTL.exists(), f"Le fichier ABox maître est introuvable : {ABOX_TTL}"
    g = Graph()
    g.parse(ABOX_TTL, format="turtle")
    return g


def test_abox_01_ttl_validity_and_header(abox_graph):
    """TEST-ABOX-01 : Vérifie la validité RDF, le namespace et la déclaration de l'ontologie ABox."""
    assert len(abox_graph) > 0, "Le graphe ABox ne contient aucun triplet."

    # Vérification de l'import OWL vers la TBox
    abox_ont = ABOX[""]
    assert (abox_ont, RDF.type, OWL.Ontology) in abox_graph, "Ontologie ABox non déclarée."
    assert (abox_ont, OWL.imports, DKG[""]) in abox_graph, "Import OWL de la TBox manquant."


def test_abox_02_asset_instantiation_and_alignment(abox_graph):
    """TEST-ABOX-02 : Vérifie qu'au moins un Asset est instancié et correctement rattaché à un composant."""
    assets = list(abox_graph.subjects(RDF.type, DKG.Asset))
    assert len(assets) > 0, "Aucune instance de type dkg:Asset n'a été trouvée."

    for asset in assets:
        # Vérifie qu'un asset a un label RDFS
        labels = list(abox_graph.objects(asset, RDFS.label))
        assert len(labels) > 0, f"L'Asset {asset} n'a pas de rdfs:label."

        # Vérifie qu'au moins un composant est installé (dkg:hasInstalledComponent)
        components = list(abox_graph.objects(asset, DKG.hasInstalledComponent))
        assert len(components) > 0, f"L'Asset {asset} n'a aucun dkg:SoftwareComponent rattaché."


def test_abox_03_no_orphan_components(abox_graph):
    """TEST-ABOX-03 : Vérifie qu'aucun SoftwareComponent n'existe sans être rattaché à un Asset."""
    software_components = list(abox_graph.subjects(RDF.type, DKG.SoftwareComponent))
    assert len(software_components) > 0, "Aucun dkg:SoftwareComponent instancié."

    for sw in software_components:
        parent_assets = list(abox_graph.subjects(DKG.hasInstalledComponent, sw))
        assert len(parent_assets) > 0, f"Le composant logiciel {sw} est orphelin (non rattaché à un Asset)."


def test_abox_04_md_file_existence_and_content():
    """TEST-ABOX-04 : Vérifie l'existence de ABox_Cybersec.md et du tableau d'inventaire."""
    assert ABOX_MD.exists(), f"Le fichier de restitution Markdown est introuvable : {ABOX_MD}"
    content = ABOX_MD.read_text(encoding="utf-8")

    assert "# Restitution Visuelle ABox" in content, "Titre principal manquant dans le fichier Markdown."
    assert "| Type DKG | Identifiant Instance (URI) |" in content, "Tableau synthétique des instances manquant."


def test_abox_05_md_mermaid_diagram():
    """TEST-ABOX-05 : Vérifie la présence du diagramme de graphe Mermaid.js (EXG-ABOX-VIS-01)."""
    content = ABOX_MD.read_text(encoding="utf-8")

    assert "```mermaid" in content, "Bloc de code Mermaid.js introuvable dans ABox_Cybersec.md."
    assert "graph TD" in content, "Orientation 'graph TD' Mermaid manquant."
    assert "hasInstalledComponent" in content, "La relation 'hasInstalledComponent' doit figurer dans le graphe Mermaid."


if __name__ == "__main__":
    import sys
    sys.exit(pytest.main(["-v", __file__]))
