#!/usr/bin/env python3
"""
Suite de tests d'intégration et de validation normative - Phase 1.
Vérifie la conformité du dossier 12-Donnees/TBox_init/ par rapport aux exigences SPEC-01.
"""

import pytest
from pathlib import Path
from rdflib import Graph, RDF, RDFS, OWL, Namespace

# Définition des chemins vers le répertoire canonique TBox_init
BASE_DIR = Path(__file__).resolve().parent.parent
TBOX_DIR = BASE_DIR / "12-Donnees" / "TBox_init"
FILE_TTL = TBOX_DIR / "TBox_Cybersec.ttl"
FILE_MD = TBOX_DIR / "TBox_Cybersec.md"

DKG = Namespace("http://dkg.cybersec.org/tbox#")


@pytest.fixture(scope="module")
def tbox_graph():
    """Charge le graphe RDF de la TBox depuis le dossier TBox_init."""
    assert FILE_TTL.exists(), f"❌ Fichier introuvable : {FILE_TTL}. Exécutez generate_TBox_initiale.py au préalable."
    g = Graph()
    g.parse(FILE_TTL, format="turtle")
    return g


def test_exg_tbox_01_namespace_and_structure(tbox_graph):
    """EXG-TBOX-01: Vérification du namespace unique et des liaisons de préfixes."""
    namespaces = dict(tbox_graph.namespaces())
    assert "dkg" in namespaces, "Le préfixe 'dkg' doit être lié."
    assert str(namespaces["dkg"]) == "http://dkg.cybersec.org/tbox#", "Le namespace dkg doit se terminer par '#'."


def test_exg_tbox_02_classes_declaration(tbox_graph):
    """EXG-TBOX-02: Vérification de la déclaration des classes minimales requises."""
    expected_classes = {
        DKG["Asset"],
        DKG["SoftwareComponent"],
        DKG["Vulnerability"],
        DKG["Weakness"],
        DKG["ThreatPattern"]
    }
    
    declared_classes = set(tbox_graph.subjects(RDF.type, OWL.Class))
    for cls in expected_classes:
        assert cls in declared_classes, f"La classe {cls} n'est pas déclarée comme owl:Class."


def test_exg_tbox_03_object_properties_domain_range(tbox_graph):
    """EXG-TBOX-03: Vérification que chaque ObjectProperty possède un rdfs:domain et rdfs:range."""
    obj_properties = list(tbox_graph.subjects(RDF.type, OWL.ObjectProperty))
    assert len(obj_properties) > 0, "Aucune owl:ObjectProperty trouvée dans le graphe."

    for prop in obj_properties:
        domain = list(tbox_graph.objects(prop, RDFS.domain))
        range_ = list(tbox_graph.objects(prop, RDFS.range))
        
        assert len(domain) > 0, f"La propriété d'objet {prop} n'a pas de rdfs:domain défini."
        assert len(range_) > 0, f"La propriété d'objet {prop} n'a pas de rdfs:range défini."


def test_exg_tbox_04_rbox_inverse_axioms(tbox_graph):
    """EXG-TBOX-04: Vérification des axiomes de la RBox (owl:inverseOf)."""
    has_comp = DKG["hasInstalledComponent"]
    is_comp = DKG["isComponentOf"]

    # Vérification de la relation inverse réciproque
    inverses = list(tbox_graph.objects(is_comp, OWL.inverseOf))
    assert has_comp in inverses or is_comp in list(tbox_graph.objects(has_comp, OWL.inverseOf)), \
        f"L'axiome owl:inverseOf doit relier {has_comp} et {is_comp}."


def test_markdown_documentation_integrity():
    """Vérification de la présence et du contenu du fichier de documentation TBox_Cybersec.md."""
    assert FILE_MD.exists(), f"❌ Fichier Markdown introuvable dans : {FILE_MD}"
    
    content = FILE_MD.read_text(encoding="utf-8")
    
    # Validation du diagramme Mermaid
    assert "```mermaid" in content, "Le fichier Markdown doit inclure un bloc de diagramme Mermaid."
    assert "classDiagram" in content, "Le diagramme Mermaid doit être de type classDiagram."
    
    # Validation de la table d'acronymes
    assert "Glossaire & Acronymes Normatifs" in content, "Le fichier Markdown doit contenir le glossaire d'acronymes."
    assert "TBox" in content and "RBox" in content, "Les termes TBox et RBox doivent être présents dans le glossaire."


if __name__ == "__main__":
    # Exécution directe via pytest si appelé comme un script
    pytest.main(["-v", __file__])
