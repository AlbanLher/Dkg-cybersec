
📋 **Phase 5 : Ingestion Advanced CTI, NER Local & Inférence RBox (Vague 3)**

**Statut :** En cours
**Date de début :** 02/09/2026
**Date de clôture :** 16/09/2026

🎯 **1. Objectifs & Périmètre**

- **But principal :** Transformer le graphe statique en un Knowledge Graph dynamique et déductif. 
- La phase englobe :
	- la régularisation du socle IA local (téléchargement et exécution offline des modèles NER et d'embeddings), 
	- l'ingestion des flux CTI complexes (STIX 2.1, OSINT unstructuré), 
	- le contrôle par l'Agent MITM (gouvernance avant écriture), 
	- l'exécution des règles d'inférence (SWRL/SPARQL CONSTRUCT) pour déduire les niveaux de risque (`dkg:HighRiskAsset`) et propager la ségrégation TLP.
    
- **Livrables attendus :** Document SPEC-05, extensions TBox (STIX 2.1), outillage IA local offline, composant Agent MITM d'alignement, fichier de règles d'inférence SWRL/SPARQL, scripts de génération/enrichissement RDF, cas d'usage illustré et pipeline CI/CD SHACL mis à jour.
    

🛠️ **2. Traçabilité des Livrables par Brique**

**A. Spécification & Gouvernance (SPEC Framework)**

- **Spécification associée :** `SPEC-05-Advanced-CTI-RBox-Inference.md`
    
- **Exigences couvertes :**
    
    - Execution 100% offline des composants IA (NER Cyber et Embeddings d'alignement).
        
    - Alignement sémantique strict NLP/RDF avec validation TBox préalable (Agent MITM).
        
    - Déduction automatisée des nœuds critiques (`dkg:HighRiskAsset`) via croisements CISA KEV et vulnérabilités ABox RED.
        
    - Application du principe d'héritage TLP (TLP:RED prévaut sur toute chaîne d'inférence impliquant un actif interne).
        

**B. Instanciation & Use Case Pédagogique (Lisible Humain)**

- **Document d'illustration :** `Human_UseCase_Phase5.md`
    
- **Description :** Scénario métier illustrant le traitement d'une menace unstructurée : extraction NER locale, validation MITM contre la TBox, injection ABox CTI, et levée automatique de niveau de risque sur les équipements internes touchés.
    

**C. Données & Ontologies (Data / Graph RDF)**

- **Artefacts Master :**
    
    - `01-Ontologie/TBox/TBOX_MASTER.ttl` _(enrichi des classes CTI/STIX 2.1)_
        
    - `01-Ontologie/Rules/rules_vague3.ttl` _(règles SPARQL CONSTRUCT / SWRL)_
        
    - `02-Donnees/Master_Transversal/TLP_CLEAR_CTI_External/`
        
- **Artefacts Snapshot :** `Snapshot_Phase_5/` _(instantané des graphes ABox RED et CTI post-inférence)_
    

**D. Scripts & Outillage (Automation & CI/CD)**

- **Générateur :** `03-Application/generate_phase5_inference.py`, `03-Application/mitm_agent.py`, `03-Application/models/fetch_models.py`
    
- **Tests Qualité :** `03-Application/tests/test_phase5_quality.py` _(tests SHACL post-inférence, chargement offline des modèles et non-fuite TLP)_
    

🏁 **3. Synthèse de Clôture & Ressources**

**Résumé Exécutif**

_(A compléter lors de la clôture de la phase)_

**Matrice Récapitulative des Livrables**

|**Brique**|**Composant / Fichier**|**Description**|
|---|---|---|
|**Framework**|`SPEC-05-Advanced-CTI-RBox-Inference.md`|Spécification des règles CTI, IA locale, pipeline MITM et moteur d'inférence|
|**Instanciation**|`Human_UseCase_Phase5.md`|Cas d'usage d'une alerte CTI convertie en levée de risque automatique|
|**Data**|`01-Ontologie/Rules/rules_vague3.ttl`|Ensemble des règles SWRL / SPARQL CONSTRUCT pour les inférences|
|**Data**|`02-Donnees/Snapshot_Phase_5/`|Graphes ABox enrichis des faits déduits post-raisonnement|
|**Script**|`03-Application/models/fetch_models.py`|Bootstrap de téléchargement local des modèles NER et embeddings|
|**Script**|`03-Application/mitm_agent.py`|Agent de gouvernance validant l'alignement NLP/TBox avant écriture|
|**Script**|`03-Application/generate_phase5_inference.py`|Script d'exécution du raisonneur RDF et de synchronisation des ABox|

📚 **4. Pour aller plus loin (Ressources Pédagogiques)**

- **GLiNER (Generalist Model for Named Entity Recognition) :** [GLiNER Paper / GitHub](https://github.com/urchade/GLiNER) — Modèle Zero-Shot/Few-Shot NER compact et exécutable en local.
    
- **STIX 2.1 Cyber Threat Intelligence Representation :** [OASIS STIX Documentation](https://oasis-open.github.io/cti-documentation/) — Standard de modélisation structurée des concepts de la menace.
    
- **SPARQL 1.1 CONSTRUCT Queries :** [W3C SPARQL Query Language](https://www.google.com/search?q=https://www.w3.org/TR/sparql11-query/%23construct) — Mécanisme de création de nouveaux triples RDF basés sur la correspondance de motifs de graphes.







### Caractéristiques du Fichier `DKG_Rules_Master.ttl` :

- **En-têtes Turtle Obligatoires :** Intégration stricte des préfixes `dkg:`, `dkg-data:`, `dkg-cti:`, `sh:`, `xsd:`, `rdfs:`, ainsi que `rdf:` et `owl:`.
    
- **Règle R-01 (`dkg:RuleHighRiskAssetAssessment`) :** Exécution d'une requête `SPARQL CONSTRUCT` au sein d'une règle SHACL (`sh:SPARQLRule`) déduisant la classe `dkg:HighRiskAsset`, le score de risque (`9.5`) et la justification lorsqu'un composant hébergé porte une vulnérabilité CISA KEV (`dkg-cti:isCisaKevListed true`).
    
- **Règle R-02 (`dkg:RuleThreatCampaignPropagation`) :** Propagation sémantique liant directement une campagne de menace (`dkg:ThreatCampaign`) à l'actif hôte (`dkg:Asset`) via la propriété `dkg:targetsAsset`.

### Fonctionnalités Clés du Composant `mitm_agent.py` :

- **Conformité Air-Gapped / Offline :** Charge le modèle Sentence Transformers depuis le cache local (`EMBEDDING_MODEL_DIR = 03-Application/models/cache/embeddings/`) défini dans `config.py`.
    
- **Gouvernance & Indexation TBox Master :**
    
    1. Charge le graphe `TBOX_MASTER_PATH` (`TLP:AMBER`).
        
    2. Indexe et vectorise l'ensemble des concepts et labels de l'ontologie en mémoire.
        
- **Algorithme d'Alignement Sémantique :**
    
    - Calcule la similarité cosinus entre le vecteur de l'entité extraite (issues du NER) et les concepts connus de la TBox.
        
    - **Si $\text{Score} \ge 0.85$ (`MITM_SIMILARITY_THRESHOLD`) :** Reçoit le statut `ACCEPTED` et mappe l'entité vers l'URI canonique existante (`dkg:`).
        
    - **Si $\text{Score} < 0.85$ :** Reçoit le statut `PROPOSE_EXTENSION` pour éviter la pollution de l'ontologie Master en proposant une demande d'extension sous contrôle humain (Human-in-the-Loop).

### Étapes Clés du Pipeline d'Inférence et Validation

- **Agrégation des Graphes RDF :** Charge en mémoire la TBox Master (`TBOX_MASTER_PATH`), l'ABox Interne (`ABOX_RED_PATH`), l'ABox CTI (`ABOX_CTI_PATH`) et le paquet de règles (`RULES_MASTER_PATH`).
    
- **Moteur d'Inférence `pySHACL` :** Exécute le raisonnement sémantique via les règles SHACL/SPARQL (`advanced=True`), enrichissant le graphe avec la classification `HighRiskAsset` et la propagation de cible (`targetsAsset`).
    
- **Persistance ABox Infered :** Sauvegarde le graphe enrichi complet dans `ABOX_INFERED_PATH` (`TLP:RED`).
    
- **Validation SHACL & Documentation :** Contrôle la conformité globale du graphe déduit par rapport aux formes SHACL et exporte automatiquement le rapport sous `DOC_INFERED_MD_PATH` (`02_SYNTHESE_ABOX_INFERED.md`).


### Contenu du Cas d'Usage Métier (Phase 5)

- **Contextualisation SOC / CTI :** Explication du besoin opérationnel de corréler automatiquement des bulletins CTI publics (TLP:CLEAR) avec des actifs internes sensibles (TLP:RED) en environnement Air-Gapped.
    
- **Déroulement Étape par Étape :**
    
    1. _Interception & Alignement MITM_ : Extraction NLP locale et validation sémantique via `mitm_agent.py` ($\ge 0.85$ pour acceptation, sinon proposition d'extension de schéma sous gouvernance Human-in-the-Loop).
        
    2. _Inférence Sémantique_ : Application des règles R-01 (reclassification `HighRiskAsset` sur présence d'une CVE CISA KEV) et R-02 (propagation automatique du ciblage `targetsAsset`).
        
    3. _Validation & Cloisonnement_ : Contrôle SHACL et export du graphe déduit sous marquage TLP:RED.
        
- **Tableau Matrice d'Impact Analyste :** Comparatif clair du gain opérationnel avant/après l'inférence.






La **Phase 5 : Advanced CTI & Inference** du projet **DKG-CyberSec** est désormais complètement opérationnelle et validée sur l'ensemble de ses piliers :

- **Air-Gapped & Cache IA (`test_01`) :** Les modèles NLP/NER et d'embeddings sont bien chargés localement sans appel réseau extérieur.
    
- **Gouvernance & Agent MITM (`test_02`) :** L'alignement sémantique par similarité cosinus (seuil 0.85) fonctionne correctement (acceptation des concepts canoniques et proposition d'extensions sous contrôle).
    
- **Graphe & Cloisonnement TLP (`test_03`) :** L'étanchéité entre la CTI externe (`TLP:CLEAR`) et les inférences sensibles (`TLP:RED`) est strictement respectée.
    

### Résumé des Composants Livrés en Phase 5

- **`DKG_Rules_Master.ttl` :** Règles d'inférence SPARQL CONSTRUCT (`sh:SPARQLRule`) déduisant la classe `HighRiskAsset` (CISA KEV) et la propagation `targetsAsset`.
    
- **`03-Application/Phase5/mitm_agent.py` :** Agent de gouvernance sémantique interceptant et alignant les entités issues du NER.
    
- **`03-Application/Phase5/generate_phase5_inference.py` :** Pipeline complet d'inférence sémantique, d'export de la ABox Infered (`TLP:RED`) et de validation SHACL.
    
- **`Human_UseCase_Phase5.md` :** Documentation métier pédagogique du scénario d'inférence SOC/CTI.
    
- **`03-Application/Test/test_phase5_quality.py` :** Suite de tests de qualité assurant la non-régression.