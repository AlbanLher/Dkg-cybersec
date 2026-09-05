def test_exg_qual_01_shacl_coverage(tbox_graph, shacl_graph):
    """EXG-QUAL-01: Verifie la presence de NodeShapes SHACL."""
    SH = Namespace("http://www.w3.org/ns/shacl#")
    
    # Extraire uniquement les cibles via le vrai prédicat SHACL
    shacl_target_classes = set(shacl_graph.objects(None, SH.targetClass))
    tbox_classes = set(tbox_graph.subjects(RDF.type, OWL.Class))
    
    intersection = tbox_classes.intersection(shacl_target_classes)
    
    # Message de debug en cas d'échec pour afficher les ensembles
    assert len(intersection) > 0, (
        f"Aucune classe TBox couverte.\n"
        f"Classes TBox trouvées ({len(tbox_classes)}): {tbox_classes}\n"
        f"Cibles SHACL trouvées ({len(shacl_target_classes)}): {shacl_target_classes}"
    )
