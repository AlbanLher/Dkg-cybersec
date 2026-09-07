# 📋 Phase 5 : [Nom de la Phase]

> **Statut** : [En cours / 🟢 Validée & Close]  
> **Date de début** : [06/009/2026]  
> **Date de clôture** : [JJ/MM/AAAA]  

---

## 🎯 1. Objectifs & Périmètre
* **But principal** : [Description synthétique des ambitions de la phase]
* **Livrables attendus** : [Liste des composants logiciels, schémas ou documents produits]

---

## 🛠️ 2. Traçabilité des Livrables par Brique

### A. Spécification & Gouvernance (SPEC Framework)
* **Spécification associée** : [`SPEC-XX-Titre.md`](../../01-Exigences/SPEC-XX.md)
* **Exigences couvertes** : Explicitation des règles Métier/Framework adressées dans cette phase.

### B. Instanciation & Use Case Pédagogique (Lisible Humain)
* **Document d'illustration** : [`Human_UseCase.md`](./Human_UseCase.md)
* **Description** : Scénario concrétisé démontrant la valeur métier sans jargon brut.

### C. Données & Ontologies (Data / Graph RDF)
* **Artefacts Master** : [`Donnees_Master.ttl`](../../02-Donnees/Master_Transversal/...)
* **Artefacts Snapshot** : [`Snapshot_Phase_X/`](../../02-Donnees/Snapshots_Phases/...)

### D. Scripts & Outillage (Automation & CI/CD)
* **Générateur** : [`generate_phaseX.py`](./generate_phaseX.py)
* **Tests Qualité** : [`test_phaseX_quality.py`](./test_phaseX_quality.py)

---

## 🏁 3. Synthèse de Clôture & Ressources

### Résumé Exécutif
[Synthèse globale de l'atterrissage de la phase, des acquis et de l'état du code/graphe]

### Matrice Récapitulative des Livrables
| Brique | Composant / Fichier | Description |
| :--- | :--- | :--- |
| **Framework** | [`SPEC-XX.md`](../../01-Exigences/...) | Spécification des contraintes & règles |
| **Instanciation** | [`Human_UseCase.md`](./...) | Cas d'usage métier expliqué |
| **Data** | [`Graphe_Master.ttl`](../../02-Donnees/...) | Fichiers RDF / Turtle générés |
| **Script** | [`generate_phaseX.py`](./...) | Script de génération et synchronisation |

---

## 📚 4. Pour aller plus loin (Ressources Pédagogiques)
*(Liens documentaires et tutoriels pour approfondir les concepts de la phase)*
* **[Concept 1]** : [Lien / Référence] — *Brève description du concept.*
* **[Concept 2]** : [Lien / Référence] — *Brève description du concept.*



---



### 🔑 Points clés de l'implémentation

1. **Ancrage SSOT Strict** : Importation directe des constantes et des namespaces RDF de `config.py` (`ABOX_RED_PATH`, `ABOX_CTI_PATH`, `ABOX_INFERED_PATH`, `DKG_TBOX`, `DKG_CTI`).
    
2. **Chaînage Avant (Forward Chaining)** : Les résultats de R-01 (`HighRiskAsset` via CISA KEV) sont réinjectés dans `graph_input` pour alimenter directement R-02 (`exposesToCascade` via propagation transitive `connectsTo+`).
    
3. **Ségrégation TLP (EXG-SE-01)** : Tous les faits déduits du croisement CTI / Interne sont isolés et sauvegardés dans `DKG_ABox_Infered.ttl` (`TLP:RED`).
    
4. **Performance & Traçabilité (EXG-HW-01)** : Mesure du temps de calcul avec avertissement si la durée franchit le seuil des 5 secondes.



couverture des test :

### 📊 Couverture des Critères d'Acceptation (EXG-)

|**Exigence**|**Intitulé**|**Stratégie de Validation Pytest**|
|---|---|---|
|**EXG-HW-01**|Raisonnement Local Économe|Assertion `exec_time < 5.0` sur le temps renvoyé par `run_inference()`.|
|**EXG-INF-01**|Inférence HighRiskAsset|Requête `ASK` validant la création des triplets `?asset a dkg:HighRiskAsset`.|
|**EXG-INF-02**|Matérialisation Cascade|Requête `ASK` vérifiant la présence de la relation `?pivot dkg:exposesToCascade ?target`.|
|**EXG-SE-01**|Ségrégation TLP Inférencée|Validation du chemin d'écriture `TLP_RED_Infered_Graph` et contrôle d'étanchéité sur `ABOX_CTI_PATH`.|

### Exécution des tests

Pour lancer cette suite de tests, il vous suffit d'exécuter la commande suivante depuis la racine du projet :

### 📊 Synthèse de Couverture de la Phase 5

|**Fichier Test Pytest**|**Exigences Validées**|
|---|---|
|`test_phase5_inference.py`|**EXG-INF-01**, **EXG-INF-02**, **EXG-SE-01**, **EXG-HW-01**|
|`test_phase5_mitm.py`|**EXG-MITM-01**, **EXG-MITM-02**, **EXG-SKOS-01**, **EXG-SKOS-02**, **EXG-HW-01**|



### 🛡️ Matrice de Traçabilité des Livrables de la Phase 5

|**Composant**|**Fichier Source**|**Fichier Test Associé**|**Statut EXG**|
|---|---|---|---|
|**Règles d'Inférence & RBox**|`03-Application/Phase5/reasoning_engine.py`|`03-Application/Tests/test_phase5_inference.py`|`EXG-INF-01`, `EXG-INF-02`, `EXG-SE-01`, `EXG-HW-01`|
|**Agent MITM & Embeddings**|`03-Application/Phase5/mitm_agent.py`|`03-Application/Tests/test_phase5_mitm.py`|`EXG-MITM-01`, `EXG-MITM-02`, `EXG-HW-01`|
|**Consolidateur SKOS**|`03-Application/Phase5/skos_consolidator.py`|`03-Application/Tests/test_phase5_mitm.py`|`EXG-SKOS-01`, `EXG-SKOS-02`|
|**Orchestrateur Pipeline**|`03-Application/Phase5/pipeline_phase5.py`|Global Execution Pipeline|Alignment SSOT `config.py`|

Le pipeline de la Phase 5 est entièrement configuré. La suite de tests peut être lancée pour valider l'exécution.