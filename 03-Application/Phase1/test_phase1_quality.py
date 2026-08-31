import pytest
from pathlib import Path
from rdflib import RDF, RDFS, OWL, Namespace, SKOS


DKG_TBOX = Namespace("http://dkg.cybersec.org/tbox#")

def test_exg_tbox_01_uri_delimiter(tbox_graph):
    """EXG-TBOX-01: Verifie l'utilisation du delimiteur '#'."""
    for s, p, o in tbox_graph:
        if str(s).startswith("http://dkg.cybersec.org/"):
            assert "#" in str(s), f"URI non conforme (manque '#'): {s}"

def test_exg_tbox_02_owl_typing(tbox_graph):
    """EXG-TBOX-02: Verifie le typage owl:Class et owl:ObjectProperty."""
    classes = list(tbox_graph.subjects(RDF.type, OWL.Class))
    obj_props = list(tbox_graph.subjects(RDF.type, OWL.ObjectProperty))
    assert len(classes) >= 6, f"Nombre insuffisant de classes ({len(classes)})."
    assert len(obj_props) >= 5, f"Nombre insuffisant de proprietes ({len(obj_props)})."

def test_exg_tbox_03_domain_and_range(tbox_graph):
    """EXG-TBOX-03: Verifie rdfs:domain et rdfs:range sur les proprietes."""
    for prop in tbox_graph.subjects(RDF.type, OWL.ObjectProperty):
        domains = list(tbox_graph.objects(prop, RDFS.domain))
        ranges = list(tbox_graph.objects(prop, RDFS.range))
        assert len(domains) > 0, f"Propriete {prop} sans domain."
        assert len(ranges) > 0, f"Propriete {prop} sans range."

def test_exg_tbox_04_rbox_inverses(tbox_graph):
    """EXG-TBOX-04: Verifie les axiomes owl:inverseOf."""
    inverses = list(tbox_graph.triples((None, OWL.inverseOf, None)))
    assert len(inverses) >= 2, "Axiomes owl:inverseOf manquants."

def test_exg_qual_01_shacl_coverage(tbox_graph, shacl_graph):
    """EXG-QUAL-01: Verifie la presence de NodeShapes SHACL."""
    SH = Namespace("http://www.w3.org/ns/shacl#")
    shacl_target_classes = set(shacl_graph.objects(None, DKG_TBOX.targetClass))
    shacl_target_classes.update(shacl_graph.objects(None, SH.targetClass))
    
    tbox_classes = set(tbox_graph.subjects(RDF.type, OWL.Class))
    intersection = tbox_classes.intersection(shacl_target_classes)
    assert len(intersection) > 0, "Aucune classe TBox couverte par une Shape SHACL."

def test_spec_01_markdown_structure(master_dir):
    """SPEC-01: Verifie le Glossaire et Mermaid dans la doc MD."""
    md_file = master_dir / "DKG_TBox_Master.md"
    assert md_file.exists(), f"Fichier Markdown introuvable: {md_file}"
    content = md_file.read_text(encoding="utf-8")
    assert "Glossaire des Acronymes" in content, "Glossaire absent du Markdown."
    assert "```mermaid" in content, "Bloc Mermaid absent du Markdown."

def test_exg_org_02_master_snapshot_parity(master_dir):
    """EXG-ORG-02: Verifie la parite Master / Snapshot."""
    snapshot_dir = master_dir.parent.parent / "Snapshots_Phases" / "Phase_1_Socle"
    assert snapshot_dir.exists(), f"Repertoire snapshot introuvable: {snapshot_dir}"
    
    for master_file in master_dir.glob("*.*"):
        snap_file = snapshot_dir / master_file.name
        assert snap_file.exists(), f"Fichier absent du snapshot: {snap_file.name}"
        assert master_file.read_bytes() == snap_file.read_bytes(), f"Ecart sur {master_file.name}"


def test_exg_tbox_05_skos_completeness(tbox_graph):
    """EXG-TBOX-05: Vérifie la présence systématique des annotations SKOS sur les classes et propriétés."""
    # Sélection des classes et des propriétés d'objets
    entities = list(tbox_graph.subjects(RDF.type, OWL.Class)) + \
               list(tbox_graph.subjects(RDF.type, OWL.ObjectProperty))
    
    for entity in entities:
        # 1. Vérification du skos:prefLabel (au moins un label)
        pref_labels = list(tbox_graph.objects(entity, SKOS.prefLabel))
        assert len(pref_labels) >= 1, f"L'entité {entity} n'a pas de skos:prefLabel !"
        
        # 2. Vérification du skos:definition pour les classes
        if (entity, RDF.type, OWL.Class) in tbox_graph:
            definitions = list(tbox_graph.objects(entity, SKOS.definition))
            assert len(definitions) >= 1, f"La classe {entity} n'a pas de skos:definition !"
