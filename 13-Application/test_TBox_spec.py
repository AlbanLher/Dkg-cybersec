#!/usr/bin/env python3
"""
Suite de tests de conformité automatisée pour le projet DKG-Cybersec.
Vérifie la TBox, les formats dérivés et la cohérence avec les spécifications.
"""

import json
from pathlib import Path
import pytest
from rdflib import RDF, RDFS, Graph, Namespace

BASE_DIR = Path(__file__).resolve().parent.parent
TBOX_DIR = BASE_DIR / "12-Donnees" / "TBox_init"
SPEC_DIR = BASE_DIR / "11-Principes_Architecture" / "Specifications"

TTL_FILE = TBOX_DIR / "TBox_Cybersec.ttl"
JSON_FILE = TBOX_DIR / "TBox_Cybersec.json"
MD_FILE = TBOX_DIR / "TBox_Cybersec.md"
SPEC_FILE = SPEC_DIR / "SpecificationNormativeSortiesFormatsTBox.md"

SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")


def test_tbox_ttl_structure():
    """Vérifie la validité RDF et la présence des classes requises Phase 1."""
    assert TTL_FILE.exists(), "Fichier TBox_Cybersec.ttl introuvable."
    g = Graph()
    g.parse(TTL_FILE, format="turtle")

    # Classes indispensables pour le README Phase 1
    classes_requises = ["Asset", "SoftwareComponent", "Vulnerability"]
    classes_presentes = [str(s).split("#")[-1] for s in g.subjects(RDF.type, None)]

    for c in classes_requises:
        assert (
            c in classes_presentes
        ), f"La classe {c} est absente du modèle TBox_Cybersec.ttl"


def test_spec_file_presence():
    """Vérifie que la spécification est bien présente dans le sous-repertoire Specifications."""
    assert SPEC_FILE.exists(), f"La spécification {SPEC_FILE} est introuvable."


def test_markdown_lexicon_and_diagrams():
    """Vérifie que le Markdown TBox contient bien le lexique, les acronymes et Mermaid."""
    assert MD_FILE.exists(), "TBox_Cybersec.md introuvable."
    content = MD_FILE.read_text(encoding="utf-8")

    assert "```mermaid" in content, "Diagrammes Mermaid absents du Markdown."
    assert "SKOS" in content and "RDF" in content, "Acronymes absents du Markdown."
    assert (
        "Synonymes / Acronymes (SKOS)" in content
    ), "Colonne de lexique SKOS absente."



if __name__ == "__main__":
    import sys
    import pytest

    # Lance pytest sur le fichier courant et retourne le code de sortie
    sys.exit(pytest.main(["-v", __file__]))
