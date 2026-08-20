## 1 - Architecture & Missions de l'Agent Cyber

L'agent est composé de 4 sous-agents spécialisés (ou outils dédiés) orchestrés autour du Dynamic Knowledge Graph (DKG) :

```
                        [ RSSI / Responsable Cyber ]
                                     │
                                     ▼
                      ┌──────────────────────────────┐
                      │    Orchestrateur Principal   │
                      └──────────────┬───────────────┘
                                     │
 ┌───────────────────┬───────────────┴───────────────┬───────────────────┐
 ▼                   ▼                               ▼                   ▼
[1. Agent           [2. Agent Governance            [3. Agent          [4. Agent Analyste
 Document/NER]       & Ontology Guard]               Vector/RAG]        Rapports & Actions]
 • Extrait entités   • Valide le schéma (SHACL)     • Maintient        • Calcule la conformité
 • Détecte écarts    • Détermine le Cas (1, 2, 3, 4)  les embeddings   • Génère les recommandations
```

### 1.1 - Missions & Fonctionnement des 4 Cas d'Ingestion

Lors de l'arrivée de nouvelles entrées (ex: un nouveau scan, un fichier de conformité NIS2, ou une politique de sécurité) :

#### **Cas 1 : Nouvelles Instances Uniquement (RAS)**

- **Déclencheur :** Le document contient des entités parfaitement mappables sur le schéma Phase 0 (`Device`, `Software`, `Vulnerability`).
    
- **Mécanisme :** Ingestion directe via APOC/n10s dans Neo4j.
    
- **Impact Agent :** Aucun réapprentissage.
    
- **Résultat :** Mise à jour transparente du graphe.
    

#### **Cas 2 : Évolution d'Ontologie Sans Ré-apprentissage Agents**

- **Déclencheur :** Une nouvelle classe ou relation est ajoutée à `ontologie.ttl` (ex: ajout de la classe `ExposureZone` ou d'une propriété `criticality`), mais les primitives d'extraction existantes (LLM / Prompt Few-Shot) suffisent à les capturer.
    
- **Mécanisme :**
    
    1. Mise à jour du fichier `.ttl` et ré-import dans n10s (`CALL n10s.nsprefixes.add...`).
        
    2. Ingestion des nouvelles données.
        
- **Impact Agent :** Les prompts d'extraction sont simplement mis à jour avec le nouveau schéma JSON/RDF sans toucher aux poids du modèle NER ou aux index vectoriels complexes.
    

#### **Cas 3 : Évolution d'Ontologie Exigeant l'Adaptation des Outils / Agents**

- **Déclencheur :** L'ontologie intègre des concepts complexes et abstraits de Phase 1 (ex: `Requirement`, `Policy`, `RiskLevel`) absents de la Phase 0.
    
- **Mécanisme :**
    
    1. Le moteur SHACL / Ontology Guard rejette l'ingestion automatique.
        
    2. Re-parsing complet des documents sources.
        
    3. **Adaptation des outils :** Fine-tuning du modèle NER dédié, ré-indexation vectorielle (Chunking + Embeddings) et ajustement des embeddings d'entités/graphes (Graph Embeddings).
        
    4. Ré-ingestion complète dans Neo4j.
        

#### **Cas 4 : "Je ne sais pas" (Aiguillage Vers l'Expert RSSI)**

- **Déclencheur :** Le document contient des informations ambiguës, contradictoires avec l'ontologie de référence, ou totalement inédites.
    
- **Mécanisme :**
    
    1. L'Agent isole les passages problématiques.
        
    2. Stocke temporairement les nœuds dans Neo4j sous le label `:UnmappedEntity` ou avec un flag `:REQUIRES_HUMAN_REVIEW`.
        
    3. Génère une **Fiche de Doubt** (Ticket d'arbitrage) destinée au RSSI.
        
- **Impact Agent :** Mise en attente jusqu'à l'arbitrage humain (Human-in-the-Loop).
    

### 1.2 - Le Flux Opérationnel "Target" pour le RSSI

Dans ce cadre, voici la boucle de travail standard pour votre cas d'usage de Phase 1 :

```
[Entrées : Inventory.json / CVE.ttl / Rapport_Conformite_NIS2.pdf]
                                 │
                                 ▼
                     [Agent Governance & Guard]
                                 │
        ┌────────────────────────┼────────────────────────┐
        ▼                        ▼                        ▼
     [Cas 1]                 [Cas 2 / 3]               [Cas 4]
(Ingestion Directe)     (Propose Évolution         (Émet Fiche de Doute
                         Ontologie & Agents)         pour Arbitrage RSSI)
        │                        │                        │
        └────────────────────────┼────────────────────────┘
                                 │
                                 ▼
                      [Graphe Neo4j Phase 1]
                                 │
                                 ▼
                   [Agent Analyste & Reporting]
                                 │
    ┌────────────────────────────┴────────────────────────────┐
    ▼                                                         ▼
[Tableau de Bord de Conformité]               [Liste des Actions Recommandées]
(ex: % de devices conformes NIS2)             (ex: Patch OpenSSL prioritaire sur SRV-DMZ)
```



