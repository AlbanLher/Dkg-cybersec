_Vue de l'avancement par phases_
Vision plus globale de la [roadmap Produit ici](./Roadmap_Produit.md)
## 1  -  Status de Developement

_des liens vous permettent d'accéder à :_
- Phase_content.md de chaque phase décrivant les étapes et livrables de cette phase
- Exemple de Specification resultant pour le Framework
- Exemple de livrable en version human .md de l'instanciation sur Use Case

| Avancement -> | Vague | Phase | étape |
| :-----------: | :---: | :---: | :---: |
|               |   1   |   2   |   2   |

## 2  -  Phases


| Vague |                     Phase<br>Content                     | Titre                                                                                                                                                                  |      Status      |                                                    Exemple<br>SPEC                                                    |                               Exemple <br>d'instantiation                                |                                          Commentaire                                           |
| :---: | :------------------------------------------------------: | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------: | :-------------------------------------------------------------------------------------------------------------------: | :--------------------------------------------------------------------------------------: | :--------------------------------------------------------------------------------------------: |
|   1   |         [**Phase1**](./Phase1/Phase_Content.md)          | initialisation Socle Modèle Canonique & Qualité<br>- TBox (class Datatype) , <br>- RBox { relations, Inverse)<br>- SHACL (shapes & validation)}<br>dans un cas simple. | Reprise en cours | [SPEC-01](01-Principes_Spécifications/Specifications_Framework/SPEC-01_Socle_Structurel_Framework_TBox_RBox_SHACL.md) |     [TBox_Human](../../02-Donnees/Snapshots_Phases/Phase_1_Socle/DKG_TBox_Master.md)     |   Comprendre les enjeux du socle<br>Ajout manuel des Acronymes T-R-A Box dans lexique du .md   |
|   1   |          [**Phase2**](2-ABox/Phase_Content.md)           | initialisation de l'instanciation interne<br>- - ABox                                                                                                                  |   A reprendre.   |                                                        SPEC-02                                                        | [ABox_Human](../02-Donnees/Master_Transversal/TLP_RED_Instances_ABox/DKG_ABox_Master.md) |                                                                                                |
|   2   | [**Phase3**](./3-EnrichissementExterne/Phase_Content.md) | Enrichissement avec des donnéesExterne<br>+ Gouvernance ( TLP )                                                                                                        |   A Reprendre    |                                                                                                                       |                                                                                          | Comprendre l'articulation de TBox, RBox, ABox ref [lien](Phase3/Articulation_des_T-R-A_Box.md) |
|       |                        **Phase4**                        |                                                                                                                                                                        |                  |                                                                                                                       |                                                                                          |                                                                                                |


## 3  -  Backlog des principes et fonctions  :




# 📋 Backlog Produit & Roadmap Évolutive (DKG-CyberSec / Agent SOC)

## 🎯 Vision Globale
Chaque vague du backlog apporte un niveau de maturité supérieur à l'**Agent IA SOC**, en s'appuyant sur un Knowledge Graph (DKG) hybride, explicable et sécurisé selon le protocole TLP.

---

## 🌊 Vague 1 : Socle Ontologique & Cartographie Interne (MVP Data)
**Focus Vague :** Permettre à l'Agent de lire le SI interne et de cartographier la structure des actifs.

### 📌 Epic 1.1 : Socle Modèle TBox & Valimateur SHACL (`TLP:AMBER`)
- [x] **US-1.1.1 (Ontologie) :** En tant qu'analyste, je veux un schéma TBox standardisé pour unifier la représentation des actifs et menaces.
- [x] **US-1.1.2 (Gouvernance SHACL) :** En tant que Data Engineer, je veux valider les instances sous CWA pour interdire les données orphelines.
- [x] **US-1.1.3 (CI/CD) :** Automatiser les tests Pytest/SHACL via GitHub Actions.

### 📌 Epic 1.2 : Instanciation ABox Master (`TLP:RED`)
- [x] **US-1.2.1 (Instances) :** Instancier la cartographie réelle des Assets et failles internes sous le répertoire `TLP_RED_Instances_ABox/`.
- [x] **US-1.2.2 (Documentation) :** Générer automatiquement le Markdown livrable avec glossaire des acronymes et diagramme Mermaid.
- [x] **US-1.2.3 (Rituel 5S) :** Centralisation stricte des constantes et chemins dans `03-Application/config.py`.

---

## 🌊 Vague 2 : Ingestion CTI Externe & Superposition Cross-TLP (Nouveau)
**Focus Vague :** Permettre à l'Agent de croiser la menace mondiale sans fuite de données confidentielles.

### 📌 Epic 2.1 : Ingestion & Alingement CTI (`TLP:CLEAR`)
- [ ] **US-2.1.1 (Flux Publics) :** Importer les référentiels ouverts (CVE, CWE, CAPEC, CISA KEV) sous `TLP_CLEAR_CTI_External/`.
- [ ] **US-2.1.2 (Superposition Sémantique) :** Rapprocher les instances internes (`TLP:RED`) et la CTI (`TLP:CLEAR`) via les URIs partagées et le schéma commun (`TLP:AMBER`).
- [ ] **US-2.1.3 (Rituel 5S Inter-Vague) :** Mettre à jour `config.py` et vérifier le cloisonnement physique des répertoires TLP.
### 📌 Epic 2.2 : Unstructured CTI & NER Pipeline
- [ ] **US-2.2.1 (NER Cyber) :** Extraire automatiquement les entités (CVE, IP, Malwares) et leurs relations depuis des bulletins de menace textuels via un modèle NER spécialisé.
- [ ] **US-2.2.2 (RDF Mapping) :** Transformer les entités extraites par le NER en triples RDF conformes à la TBox (`TLP:CLEAR` / `TLP:AMBER`).
---

## 🌊 Vague 3 : Moteur de Raisonnement & Déductions (Phase 3)
**Focus Vague :** Permettre à l'Agent de déduire des risques cachés par inférence multi-graphes.

### 📌 Epic 3.1 : Règles métier & Scoring de Risque
- [ ] **US-3.1.1 (Inférence SWRL/SPARQL) :** Écrire les règles d'inférence pour tagger automatiquement les nœuds `HighRiskAsset`.
- [ ] **US-3.1.2 (Recette Inférence) :** Valider que les triples déduits respectent la gouvernance TLP du nœud source.
- [ ] **US-3.1.3 (Export Enrichi) :** Générer la vue synthétique de la ABox déduite sous format Markdown.

---

## 🌊 Vague 4 : Agent IA SOC & GraphRAG (Phase 4)
**Focus Vague :** Fournir une interface conversationnelle explicable pour les analystes L1/L2.

### 📌 Epic 4.1 : Interface NL-to-SPARQL & Auditabilite
- [ ] **US-4.1.1 (GraphRAG) :** Traduire les questions en langage naturel d'un analyste en requêtes SPARQL exécutées sur le DKG.
- [ ] **US-4.1.2 (Explicabilité) :** Rendre obligatoire la restitution de la chaîne de preuves (triples utilisés) dans les réponses de l'Agent.
- [ ] **US-4.1.3 (Évaluation) :** Évaluer la fidélité des réponses de l'Agent via des frameworks type Ragas / LangSmith.
### 📌 Epic 4.2 : Hybrid Retrieval & Fine-Tuning Agent
- [ ] **US-4.2.1 (Vectorization / Embeddings) :** Vectoriser les descriptions textuelles et les sous-graphes du DKG pour permettre une recherche sémantique hybride (Vector + SPARQL).
- [ ] **US-4.2.2 (Fine-Tuning Text-to-SPARQL) :** Entraîner/Fine-tuner un modèle spécialisé (SLM) sur le schéma TBox pour garantir la génération de requêtes SPARQL 100% valides et sécurisées.
- [ ] **US-4.2.3 (Instruction Tuning Agent) :** Fine-tuner le comportement de l'Agent pour respecter l'explicabilité et les contraintes TLP dans la restitution des réponses.
---

## 🌊 Vague 5 : Continuous Improvement (Flux Temps Réel & SOAR)
**Focus Vague :** Passer d'un Agent consultatif à un Agent réactif et proactif.

### 📌 Epic 5.1 : Ingestion SIEM & Autonomie Agentique
- [ ] **US-5.1.1 (Streaming Data) :** Ingestion en continu d'événements/alertes SIEM sous forme de triples RDF temporellement horodatés.
- [ ] **US-5.1.2 (Playbooks SOAR) :** Permettre à l'Agent de proposer des règles de remédiation (YARA/Sigma) validées par un humain (Human-in-the-loop).