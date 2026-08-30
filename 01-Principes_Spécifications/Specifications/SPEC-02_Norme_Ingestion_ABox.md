_(Phase 2 : Instances Infrastructures & SHACL)_


**Périmètre :** Phase 2 — Instanciation des équipements et logiciels depuis les inventaires Markdown/JSON (TLP:RED).

### Système de Numérotation des Exigences : `EXG-ABOX-*`

#### 1. Ingestion et Extraction d'Arborescence

- **`EXG-ABOX-01` (Complétude de l'Extraction)** : Le parser de conversion (Markdown/JSON $\rightarrow$ RDF) doit obligatoirement sérialiser la totalité du graphe d'arborescence (`Asset` $\rightarrow$ `SoftwareComponent` $\rightarrow$ `Vulnerability`). L'extraction partielle limitée aux simples métadonnées d'équipements est interdite.
    
- **`EXG-ABOX-02` (Espace de Nommage ABox)** : Toutes les instances dynamiques d'infrastructure doivent être sérialisées sous le namespace `[http://dkg.cybersec.org/abox#](http://dkg.cybersec.org/abox#)`.
    

#### 2. Intégrité Structurelle (Garde-fou pre-serialization)

- **`EXG-ABOX-03` (Non-Orphelinat des Assets)** : Aucun individu de type `dkg:Asset` ne peut exister dans l'ABox sans au moins un triplet sortant `dkg:hasInstalledComponent` pointant vers un `dkg:SoftwareComponent`.
    
- **`EXG-ABOX-04` (Rattachement des Failles)** : Tout composant logiciel instancié doit être relié à au moins une référence d'instance de vulnérabilité (`dkg:hasVulnerability`).