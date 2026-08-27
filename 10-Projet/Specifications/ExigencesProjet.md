Pour étendre l'approche normative formalisée dans `11-Principes_Architecture/Specifications/` à l'ensemble du projet, voici les règles exigibles à intégrer dans le `README.md` principal :

- **EXG-PROJ-01 (Architecture TBox/ABox)** : Séparation stricte entre le schéma conceptuel (`TBox_init/`) et les données instanciées (`ABox`).
    
- **EXG-PROJ-02 (Conformité des Artefacts)** : Tout livrable de modélisation doit être accompagné de sa source Turtle (`.ttl`), de sa sérialisation machine (`.json`) et de sa documentation humain (`.md`).
    
- **EXG-PROJ-03 (Validation Automatisée)** : Aucun changement d'ontologie ou de script d'ingestion ne doit être commité sans validation préalable par la suite de tests `pytest`

- **EXG-PROJ-04 (Gestion de la Traçabilité & Provenance)** : Les données SI (`graph:private`) et les flux OSINT (`graph:public`) doivent être strictement étanches.

 - **EXG-PROJ-05 (Données publique - Common)**Identifier et mettre en oeuvre les données publique comme les standards et les communs pour être pertinent et efficace

- **EXG-PROJ-06 (Assurer la confidentialité des données internes privée)**  (avec différents niveaux de confidentialité). 
  Ce projet (POC ) simule les données privées avec l'étiquette "pseudo-confidentielle" pour satisfaire le besoin didactique. Mais explicite ajustement a faire pour accéder a cette confidentialité.  
- 
- **EXG-PROJ-07 (Faible ressource IT )**  l'agent doit pouvoir tourner en local sur une machine ACER Aspire 515-40 avec 16Go RAM et peut faire a ppel a des ressource cloud pour le fine tuning de modèle si nécessaire.
