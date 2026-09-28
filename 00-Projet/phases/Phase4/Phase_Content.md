# 📋 Phase 4 : Extraction NER & Ingestion CTI Non Structurée

> **Statut** : En cours
> **Date de début** : 01/09/2026
> **Date de clôture** : [JJ/MM/AAAA]

## 🎯 1. Objectifs & Périmètre

- **But principal** : Traiter les sources de renseignement non structurées (bulletins de sécurité, avis PDF, blogs) pour extraire automatiquement les entités et relations cyber grâce à un modèle NER, puis les intégrer sous forme de triplets RDF validés dans la ABox CTI (`TLP:CLEAR`).

**📌 Hypothèse de Cadrage — Conformité au Socle TBox/RBox (Phase 4)** :

_L'ingestion CTI non structurée via NER traite exclusivement les entités et relations strictement conformes au socle TBox/RBox existant (`TLP:AMBER`). Tout besoin d'extension ontologique (découverte de nouveaux concepts ou affinement de relations) est explicitement différé à la **Phase 5**, où le moteur de raisonnement et l'évolution dynamique de la TBox/RBox seront traités de manière consolidée._



- **Livrables attendus** :
    - Spécification technique `SPEC-04_Unstructured_CTI_NER.md`.
    - Script d'extraction NER et de mapping RDF `ner_cti_extractor.py`.
    - Suite de tests de validation NLP/SHACL `test_phase4_ner_validation.py`.
    - Mise à jour du graphe externe `DKG_ABox_CTI_External.ttl`.

## 🛠️ 2. Traçabilité des Livrables par Brique

### A. Spécification & Gouvernance (SPEC Framework)

- **Spécification associée** : [`SPEC-04_Unstructured_CTI_NER.md`](https://www.google.com/search?q=../../01-Principes_Sp%C3%A9cifications/Specifications_Framework/SPEC-04_Unstructured_CTI_NER.md)
    
- **Exigences couvertes** :
    - `EXG-NER-01` : Extraction et classification d'entités cyber conformes à la TBox Master.
    - `EXG-NER-02` : Filtrage déterministe avec score de confiance $\ge 0.85$ et enregistrement de `dkg:nerConfidenceScore`.
    - `EXG-SEC-01` : Strict maintien de l'isolation dans l'ABox CTI Externe (`TLP:CLEAR`).
### B. Instanciation & Use Case Pédagogique (Lisible Humain)

- **Document d'illustration** : [`Human_UseCase_Phase4.md`](https://www.google.com/search?q=./Human_UseCase_Phase4.md)[cite: 5]
    
- **Description** : Démonstration pas-à-pas de l'analyse d'un bulletin textuel décrivant un groupe d'attaque (ex: APT29) et sa transformation automatisée en nœuds DKG exploitables par le SOC[cite: 1].
    

### C. Données & Ontologies (Data / Graph RDF)

- **Artefacts Master** : [`DKG_ABox_CTI_External.ttl`](https://www.google.com/search?q=../../02-Donnees/Master_Transversal/TLP_CLEAR_CTI_External/DKG_ABox_CTI_External.ttl)[cite: 3, 5]
- **Artefacts Sources** : `02-Donnees/03_Unstructured_CTI_Sources/` (Bulletins textuels bruts)
- **Artefacts Snapshot** : [`Snapshot_Phase_4/`](https://www.google.com/search?q=../../02-Donnees/Snapshots_Phases/Phase_4_NER/)
### D. Scripts & Outillage (Automation & CI/CD)

- **Générateur / Extracteur** : [`ner_cti_extractor.py`](https://www.google.com/search?q=../../03-Application/ner_cti_extractor.py)
- **Tests Qualité** : [`test_phase4_ner_validation.py`](https://www.google.com/search?q=../../03-Application/tests/test_phase4_ner_validation.py)

## 🏁 3. Synthèse de Clôture & Ressources
### Résumé Exécutif

_(À compléter à la clôture de la phase après validation Pytest et audit 5S)_

### Matrice Récapitulative des Livrables

|**Brique**|**Composant / Fichier**|**Description**|
|---|---|---|
|**Framework**|[`SPEC-04_Unstructured_CTI_NER.md`](https://www.google.com/search?q=../../01-Principes_Sp%C3%A9cifications/Specifications_Framework/SPEC-04_Unstructured_CTI_NER.md)|Spécification de l'extraction NER et des règles de scoring|
|**Instanciation**|[`Human_UseCase_Phase4.md`](https://www.google.com/search?q=./Human_UseCase_Phase4.md)|Cas d'usage d'ingestion d'un bulletin d'alerte CTI|
|**Data**|[`DKG_ABox_CTI_External.ttl`](https://www.google.com/search?q=../../02-Donnees/Master_Transversal/TLP_CLEAR_CTI_External/DKG_ABox_CTI_External.ttl)|Graphe CTI enrichi des entités textuelles extraites|
|**Script**|[`ner_cti_extractor.py`](https://www.google.com/search?q=../../03-Application/ner_cti_extractor.py)|Pipeline NLP, parsing textuel et injection RDF|

## 📚 4. Pour aller plus loin (Ressources Pédagogiques)

- **[spaCy Cyber NER]** : [spaCy Models](https://www.google.com/search?q=https://spacy.io/usage/models) — _Principes des modèles NLP appliqués à la reconnaissance d'entités._
- **[W3C RDF Mapping]** : [W3C Graph Construction](https://www.google.com/search?q=https://www.w3.org/TR/rdf11-concepts/) — _Bonnes pratiques pour convertir des données non structurées en triplets RDF._