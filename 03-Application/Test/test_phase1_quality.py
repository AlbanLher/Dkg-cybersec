import sys
from pathlib import Path
import pytest

# 1. Résolution de la racine pour l'import SSOT (EXG-OR-05)
APP_DIR = Path(__file__).resolve().parent.parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

# Importation directe et exclusive des clés config.py (EXG-OR-05)
from core.config import (
    DIR_MASTER_TBOX,
    TBOX_MASTER_PATH,
    DKG_TBOX,
    RDF,
    RDFS,
    OWL,
    SKOS,
    SH
)

@pytest.mark.non_regression
def test_exg_tb_01_uri_delimiter(tbox_graph):
    """EXG-FWK-P1-T-R_1 : Vérifie le namespace unique et le séparateur '#'."""
    # EXG-FWK-P1-T-R_1
    for s, p, o in tbox_graph:
        if str(s).startswith(str(DKG_TBOX)):
            assert "#" in str(s), f"URI non conforme (manque '#'): {s}"

@pytest.mark.non_regression
def test_exg_tb_02_owl_typing(tbox_graph):
    """EXG-TB-02  /  EXG-FWK-P1-T-R_2   : Vérifie le typage owl:Class et owl:ObjectProperty."""
    classes = list(tbox_graph.subjects(RDF.type, OWL.Class))
    obj_props = list(tbox_graph.subjects(RDF.type, OWL.ObjectProperty))
    assert len(classes) >= 6, f"Nombre insuffisant de classes ({len(classes)})."
    assert len(obj_props) >= 5, f"Nombre insuffisant de propriétés ({len(obj_props)})."

@pytest.mark.non_regression
def test_exg_tb_03_domain_and_range(tbox_graph):
    """EXG-TB-03 / EXG-FWK-P1-T-R_3  : Vérifie la présence de rdfs:domain et rdfs:range."""
    for prop in tbox_graph.subjects(RDF.type, OWL.ObjectProperty):
        domains = list(tbox_graph.objects(prop, RDFS.domain))
        ranges = list(tbox_graph.objects(prop, RDFS.range))
        assert len(domains) > 0, f"Propriété {prop} sans rdfs:domain."
        assert len(ranges) > 0, f"Propriété {prop} sans rdfs:range."

@pytest.mark.non_regression
def test_exg_tb_04_rbox_inverses(tbox_graph):
    """EXG-TB-04  /  EXG-FWK-P1-T-R_4  : Vérifie la déclaration des axiomes d'inversion owl:inverseOf."""
    inverses = list(tbox_graph.triples((None, OWL.inverseOf, None)))
    assert len(inverses) >= 2, "Axiomes owl:inverseOf manquants."

@pytest.mark.non_regression
def test_exg_tb_05_skos_completeness(tbox_graph):
    """EXG-FWK-P1-GOU_18    : Vérifie les annotations SKOS sur classes et propriétés."""
    entities = list(tbox_graph.subjects(RDF.type, OWL.Class)) + \
               list(tbox_graph.subjects(RDF.type, OWL.ObjectProperty))
    
    for entity in entities:
        pref_labels = list(tbox_graph.objects(entity, SKOS.prefLabel))
        assert len(pref_labels) >= 1, f"L'entité {entity} n'a pas de skos:prefLabel !"
        
        if (entity, RDF.type, OWL.Class) in tbox_graph:
            definitions = list(tbox_graph.objects(entity, SKOS.definition))
            assert len(definitions) >= 1, f"La classe {entity} n'a pas de skos:definition !"

@pytest.mark.non_regression
def test_exg_qu_01_shacl_coverage(tbox_graph, shacl_graph):
    """EXG-QU-01    /  EXG-FWK-P1-T-R_6   : Vérifie la couverture des classes TBox par des NodeShapes SHACL."""
    shacl_target_classes = set(shacl_graph.objects(None, SH.targetClass))
    tbox_classes = set(tbox_graph.subjects(RDF.type, OWL.Class))
    
    intersection = tbox_classes.intersection(shacl_target_classes)
    assert len(intersection) > 0, (
        f"Aucune classe TBox couverte.\n"
        f"Classes TBox ({len(tbox_classes)}): {tbox_classes}\n"
        f"Cibles SHACL ({len(shacl_target_classes)}): {shacl_target_classes}"
    )

def test_markdown_documentation_structure(master_dir):
    """
    exigence : EXG-FWK-P1-GOU_3
    Vérifie la présence du Glossaire, du schéma Mermaid et des tableaux dans le Markdown."""
    md_file = master_dir / TBOX_MASTER_PATH.with_suffix(".md").name
    assert md_file.exists(), f"Fichier Markdown introuvable: {md_file}"
    content = md_file.read_text(encoding="utf-8")
    assert "Glossaire des Acronymes" in content, "Glossaire absent du Markdown."
    assert "```mermaid" in content, "Bloc Mermaid absent du Markdown."
    assert "Résumé Synthétique des Classes TBox" in content, "Tableau des classes absent du Markdown."


def test_exg_fwk_p1_gou_2_figeage_par_tag_rejeu_par_checkout(master_dir):
    """EXG-FWK-P1-GOU_2 (doctrine P9, registre v2.3) : le figeage des
    livrables P1 est porte par le TAG git phase1-v1 — l historique EST le
    snapshot, le rejeu se fait par checkout du tag (jamais par copie de
    fichiers). Le Master est la reference vivante : les artefacts du socle
    y vivent complets et parsables de facon autonome."""
    import subprocess
    from rdflib import Graph
    # 1. figeage : le tag existe (git resoud le repo depuis n importe
    #    quel chemin interieur ; ancrage = repertoire Master, SSOT).
    tags = subprocess.run(["git", "tag", "-l", "phase1-v1"],
                           capture_output=True, text=True,
                           cwd=str(DIR_MASTER_TBOX)).stdout.strip()
    assert tags == "phase1-v1", (f"Tag de figeage phase1-v1 absent (doctrine "
                                 f"GOU_2 v2.3) — sortie git : {tags!r}")
    # 2. Master complet et parsable : socle vivant, artefacts presents.
    for ttl_artefact in (TBOX_MASTER_PATH,
                         DIR_MASTER_TBOX / "DKG_SHACL_Master.ttl",
                         DIR_MASTER_TBOX / "synthetic_qualification.ttl"):
        assert ttl_artefact.exists(), f"Artefact du socle absent du Master : {ttl_artefact}"
        Graph().parse(str(ttl_artefact), format="turtle")   # parse autonome
    assert (DIR_MASTER_TBOX / TBOX_MASTER_PATH.with_suffix(".md").name).exists(), \
        "Documentation Markdown du socle absente du Master."
