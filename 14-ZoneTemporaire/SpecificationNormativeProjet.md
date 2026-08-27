- **EXG-PROJ-01 (Architecture TBox/ABox)** : Séparation stricte entre le schéma conceptuel (`TBox_init/`) et les données instanciées (`ABox`).
    
- **EXG-PROJ-02 (Conformité des Artefacts)** : Tout livrable de modélisation doit être accompagné de sa source Turtle (`.ttl`), de sa sérialisation machine (`.json`) et de sa documentation humain (`.md`).
    
- **EXG-PROJ-03 (Validation Automatisée)** : Aucun changement d'ontologie ou de script d'ingestion ne doit être commité sans validation préalable par la suite de tests `pytest`.
    
- **EXG-PROJ-04 (Gestion de la Traçabilité & Provenance)** : Les données SI (`graph:private`) et les flux OSINT (`graph:public`) doivent être strictement étanches.