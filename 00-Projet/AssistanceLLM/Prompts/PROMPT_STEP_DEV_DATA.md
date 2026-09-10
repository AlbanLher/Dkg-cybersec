# 🔧 Prompt 2/3 — Code, Data Pipeline & Tests PyTest (`[CONTEXT: DEV-DATA]`)

## 📌 Fichiers à joindre obligatoirement dans votre message :
1. `03-Application/config.py`
2. `00-Projet/PhaseX/Phase_Content.md` & `SPEC-0X_....md` (Générés au Prompt 1)
3. Scripts d'infrastructures existants à faire évoluer (ex: `mitm_agent.py`, `reasoning_engine.py`)

## Périmètre d'Action
- Répertoires : `03-Application/PhaseX/`, `03-Application/Test/`, `02-Donnees/Snapshots_Phases/`
- Objectif : Implémenter le code métier, générer/ingérer les données RDF, exécuter le moteur d'inférence/alignement et valider via PyTest + SHACL.

## 📋 Directives & Check-list Qualité Code
- [ ] **SSOT Strict :** 100% des objets `Path` et `Namespace` proviennent EXCLUSIVEMENT de `config.py`. Aucun `open("string")` ou chaîne littérale.
- [ ] **Conformité Pydantic V2 :** Utilisation de `ConfigDict(frozen=True)` pour l'immutabilité des payloads.
- [ ] **Validité Turtle & En-tête :** Ajout systématique des 7 préfixes standard (`dkg:`, `dkg-data:`, `dkg-cti:`, `sh:`, `xsd:`, `rdfs:`, `skos:`).
- [ ] **Validation SHACL CWA :** Intégration du contrôle PySHACL sous Closed World Assumption sur le graphe unifié.
- [ ] **PyTest Suite :** Rédaction d'un jeu de tests unitaires/intégration couvrant 100% des règles (incluant les cas aux limites float/bounding).
- [ ] **Pydantic V2 / SSOT **: Interdire l'utilisation de constantes en dur pour les seuils de confiance (ex: seuil d'ambiguïté 0.65≤Score<0.85) ou les espaces de noms ; ceux-ci doivent obligatoirement être déclarés dans config.py.

## 📤 Livrables Attendus
1. Scripts applicatifs sous `03-Application/PhaseX/`
2. Artefacts RDF `.ttl` générés sous `02-Donnees/Snapshots_Phases/PhaseX.../`
3. Fichier de recette `03-Application/Test/test_phaseX.md` / `test_phaseX.py`