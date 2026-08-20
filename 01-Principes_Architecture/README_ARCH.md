


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





##  2 - Publique vs Pseudo-Privée vs Privée

Ce projet utilise **trois niveaux d'ontologies** pour équilibrer **transparence** (POC public) et **confidentialité** (production).
Voici comment les distinguer et les utiliser :
###  1. Ontologie Publique 🌍 (`ontologie-publique.ttl`)

| **Caractéristique** | **Détail**                                                                 |
| ------------------- | -------------------------------------------------------------------------- |
| **Contenu**         | Classes/propriétés **génériques** applicables à tout projet cybersécurité. |
| **Exemples**        | `:Device`, `:Software`, `:Vulnerability`, `:hasSoftware`, `:cvssScore`.    |
| **Accès**           | ✅ **Public** (dans le dépôt GitHub).                                       |
| **Utilisation**     | Base commune pour tous les contributeurs.                                  |
| **Fichier**         | `02-Architecture/ONTOLOGIE/ontologie-publique.ttl`                         |

**→ Pour qui ?** Tous les utilisateurs du dépôt public.

---

###  2. Ontologie Pseudo-Privée  🟡 (`ontologie-pseudo-privee.ttl`)

| **Caractéristique** | **Détail**                                                                                          |
| ------------------- | --------------------------------------------------------------------------------------------------- |
| **Contenu**         | Extensions **spécifiques au POC** (ex: classes/propriétés pour les tests).                          |
| **Exemples**        | `:TestDevice`, `:MockVulnerability`, `:hasMockRule`.                                                |
| **Accès**           | 🔶 **"Pseudo-private"** : Public dans le POC, mais **marqué comme privé** dans la doc.              |
| **Utilisation**     | Permet à **tous les contributeurs** (y compris les agents comme moi) de voir la structure complète. |
| **Fichier**         | `02-Architecture/ONTOLOGIE/ontologie-pseudo-privee.ttl`                                             |
| **Avertissement**   | ⚠️ **Dans un vrai projet, ce fichier serait dans `.private/` et non public.**                       |

**→ Pourquoi cette approche ?**
- **POC** : Tout est public pour faciliter la collaboration.
- **Production** : Ce fichier serait **déplacé dans `.private/`** et **exclu de Git**.
- **Documentation** : On **documente clairement** cette différence pour éviter les malentendus.

**→ Pour qui ?** Contributeurs du POC (y compris les outils d’IA comme moi).

---

###  3. Ontologie Privée 🔒 (`.private/ontologie-privee.ttl`)

| **Caractéristique** | **Détail**                                                                          |
| ------------------- | ----------------------------------------------------------------------------------- |
| **Contenu**         | Extensions **spécifiques à votre entreprise** (ex: règles internes, devices réels). |
| **Exemples**        | `:InternalServer`, `:ComplianceRule`, `:hasEmployee`.                               |
| **Accès**           | ❌ **Privé** (exclu de Git via `.gitignore`).                                        |
| **Utilisation**     | Données **confidentielles** (ex: topologie réseau réelle, règles RGPD/NIS2).        |
| **Fichier**         | `.private/ontologie-privee.ttl` (non versionné dans Git).                           |

**→ Pour qui ?** Uniquement vous et votre équipe interne.

---

### 4. Comment Passer du POC à la Production ?
#### 1 -Déplacez `ontologie-pseudo-privee.ttl` :
```bash
   mv 02-Architecture/ONTOLOGIE/ontologie-pseudo-privee.ttl .private/ontologie-privee.ttl
```
#### 2 - Mettez à jour `.gitignore` : 
**gitignore**
        ```
    .private/
    *.secret
    ```
#### 3 -  Ajoutez l’ontologie privée à `.gitignore` :
```bash
    echo ".private/" >> .gitignore
    git add .gitignore
    git commit -m "chore: Exclure ontologie-privee de Git"
```
    
#### 4 - Documenter le changement
dans `CHANGELOG.md`     
    
```
    ## [v1.0.0] - 2026-08-12
    ### Changed
    - `ontologie-pseudo-privee.ttl` → `.private/ontologie-privee.ttl` (passage en production).
```

---


#    ⚠️   Avertissement pour les Contributeurs

> **⚠️ ATTENTION : L’ontologie "pseudo-privée" (`ontologie-pseudo-privee.ttl`) est publique dans ce POC pour faciliter la collaboration.** **Dans un environnement de production, ce fichier doit être déplacé dans `.private/` et exclu de Git.** **Ne pas utiliser les classes/propriétés de ce fichier pour des données réelles sans les adapter à votre contexte.**



##  3 - Selection d'outils

| Outil                     | Usage                          | Lien                                                      | commentaire          |
| ------------------------- | ------------------------------ | --------------------------------------------------------- | -------------------- |
| **Neo4j**                 | Base de données de graphe      | [neo4j.com](https://neo4j.com/)                           | en local pour le POC |
| **RDFLib**                | Manipulation RDF en Python     | [rdflib.readthedocs.io](https://rdflib.readthedocs.io/)   |                      |
| **Sentence Transformers** | Vectorisation                  | [sbert.net](https://www.sbert.net/) ,  `all-MiniLM-L6-v2` |                      |
| **spaCy**                 | NER (Reconnaissance d’entités) | [spacy.io](https://spacy.io/)                             |                      |
| **Faker**                 | Génération de données fictives | [faker.readthedocs.io](https://faker.readthedocs.io/)     |                      |
| Ontologie                 | OWL/TTL + Protégé              |                                                           |                      |
| NER                       | SpaCy (modèle personalisé)     |                                                           |                      |

