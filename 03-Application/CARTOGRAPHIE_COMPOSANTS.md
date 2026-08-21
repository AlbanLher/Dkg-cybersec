Ce document fait le lien entre l'architecture conceptuelle des 4 schémas de principes et l'implémentation logicielle réelle dans la chaîne d'outils Python et l'infrastucture Neo4j.

**Cartographie des Composants Logiciels & Services (Python & Neo4j)**

Ce document décrit l'ensemble des modules Python, des extensions et des services Neo4j qui constituent l'application **Cyber DKG**. Chaque composant est cartographié selon son rôle dans la chaîne de valeur, ses entrées/sorties et ses dépendances.

## 0 - Vue d'Ensemble de la Pile Technique (Tech Stack)

```
┌────────────────────────────────────────────────────────────────────────┐
│                        COUCHE INTERACTION & IHM                        │
│             Dashboard Streamlit (HITL)  |  CLI Admin / CI/CD            │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
┌───────────────────────────────────▼────────────────────────────────────┐
│                      COUCHE AGENTIQUE & LLM (Python)                   │
│  LangGraph / LangChain  |  Pydantic  |  SentenceTransformers / OpenAI  │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
┌───────────────────────────────────▼────────────────────────────────────┐
│                    COUCHE COMPILATION & CONFORMITÉ                     │
│                rdflib (RDF/TTL)  |  owlready2 / pyshacl                │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
┌───────────────────────────────────▼────────────────────────────────────┐
│                     COUCHE BASE DE CONNAISSANCES                       │
│        Neo4j Graph Database (v5+)  |  APOC  |  neosemantics (n10s)     │
└────────────────────────────────────────────────────────────────────────┘
```

## 1. Modules Python du Socle de Compilation & Guard (`04-Code/build/`)

Ces composants sont responsables de la transformation des fichiers de connaissances Markdown en artefacts Turtle (`.ttl`) et de la vérification stricte de leur conformité.

### 1.1 `md_to_skos.py`

- **Rôle :** Extrait le vocabulaire, les acronymes et le jargon métier contenus dans `00-Projet/LEXIQUE_*.md` pour générer le fichier SKOS standardisé `LEXIQUE_GLOBAL.ttl`.
    
- **Entrées :** `00-Projet/LEXIQUE_PUBLIC.md`, `00-Projet/LEXIQUE_PRIVEE.md`, `00-Projet/LEXIQUE_TECHNIQUE.md`
    
- **Sorties :** `02-Donnees/Phase0/lexique_skos.ttl`
    
- **Dépendances Python :** `rdflib`, `markdown`, `pydantic`
    

### 1.2 `generate_onto_spec.py`

- **Rôle :** Compile la spécification d'ontologie Markdown en un schéma formel OWL 2 DL.
    
- **Entrées :** `01-Principes_Architecture/ONTOLOGIE/ontologie-schema.md`
    
- **Sorties :** `02-Donnees/Phase0/ontologie_cyber.ttl`
    
- **Dépendances Python :** `rdflib`
    

### 1.3 `ontology_guard.py`

- **Rôle :** Moteur de validation des règles de structure. Il exécute la vérification SHACL/OWL sur les artefacts générés et contrôle tout nouveau flux JSON/CSV d'ingestion avant insertion.
    
- **Entrées :** `02-Donnees/Phase0/*.ttl`, Flux d'ingestion bruts (CVE, Scans)
    
- **Sorties :** Rapport de conformité JSON (`VALID` / `INVALID` + liste des dérives)
    
- **Dépendances Python :** `pyshacl`, `rdflib`
    

## 2. Services & Plugins Neo4j (`02-Donnees/` & `04-Code/db/`)

La base de données Neo4j constitue le cœur du Dynamic Knowledge Graph (DKG). Elle s'appuie sur deux extensions clés pour gérer le sémantique W3C et les traversées complexes.

### 2.1 Extension `neosemantics` (n10s)

- **Rôle :** Permet l'import direct et transparent des fichiers Turtle (`.ttl`) OWL/SKOS dans Neo4j sans perdre la sémantique RDF.
    
- **Configuration n10s :**
    
    - `handleVocabUri: "IGNORE"` (simplification des préfixes pour requêtage Cypher fluide)
        
    - `handleMultival: "ARRAY"`
        
    - `keepLangTag: false`
        

### 2.2 Extension `APOC` (Awesome Procedures on Cypher)

- **Rôle :** Fournit les procédures avancées pour la traversée de graphe, le traitement parallèle et l'export dynamique des données de risques.
    
- **Procédures clés utilisées :** `apoc.path.subgraphAll`, `apoc.export.json.*`, `apoc.meta.graph`
    

### 2.3 `neo4j_loader.py`

- **Rôle :** Orchestre la réinitialisation ou la mise à jour incrémentale de la base Neo4j en appelant les procédures n10s (`n10s.graphconfig.init` et `n10s.rdf.import.fetch`).
    
- **Entrées :** Artefacts `.ttl` validés par `ontology_guard.py`
    
- **Sorties :** Graphe Neo4j mis à jour.
    
- **Dépendances Python :** `neo4j` (Driver officiel)
    

## 3. Système Agentique Cyber (`04-Code/agents/`)

L'architecture agentique repose sur un réseau d'agents spécialisés coordonnés par un superviseur/routeur.

Extrait de code

```
flowchart TD
    SUB["<b>supervising_agent.py</b><br/>(Routeur & Intention)"]
    
    A1["<b>align_agent.py</b><br/>(SKOS Resolver)"]
    A2["<b>guard_agent.py</b><br/>(Detection Drift & RFC)"]
    A3["<b>rag_agent.py</b><br/>(Cypher & Vector Search)"]
    A4["<b>gov_agent.py</b><br/>(Score Risque & Impact)"]

    SUB --> A1
    SUB --> A2
    SUB --> A3
    SUB --> A4

    style SUB fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    style A1 fill:#ffebee,stroke:#c62828,stroke-width:1px
    style A2 fill:#ffebee,stroke:#c62828,stroke-width:1px
    style A3 fill:#ffebee,stroke:#c62828,stroke-width:1px
    style A4 fill:#ffebee,stroke:#c62828,stroke-width:1px
```

### 3.1 `supervising_agent.py` (Superviseur & Routeur)

- **Rôle :** Reçoit le prompt utilisateur ou le payload d'événement, identifie l'intention et délègue l'exécution à l'agent spécialisé approprié.
    

### 3.2 `align_agent.py` (Agent Alignement & SKOS Resolver)

- **Rôle :** Intercepte les termes métier, le jargon et les acronymes de la requête pour les traduire en concepts canoniques de l'ontologie via les requêtes `skos:prefLabel` et `skos:altLabel`.
    
- **Action en Zone Grise :** Si un terme reste inconnu après analyse vectorielle, l'agent ne devine pas : il génère une alerte _Terme Inconnu_.
    

### 3.3 `guard_agent.py` (Agent Knowledge Guard)

- **Rôle :** Exécute en continu des contrôles d'intégrité sur la structure du graphe Neo4j. Il identifie les attributs non documentés, les nœuds orphelins et les dérives de schéma.
    
- **Action en Zone Grise :** Génère un ticket/RFC au format JSON vers le tableau de bord HITL.
    

### 3.4 `rag_agent.py` (Agent GraphRAG & Enquête)

- **Rôle :** Génère et exécute dynamiquement des requêtes Cypher optimisées (traversée multi-sauts : _Équipement $\rightarrow$ Vulnérabilité $\rightarrow$ Correctif $\rightarrow$ Service Métier Impacté_).
    

### 3.5 `gov_agent.py` (Agent Gouvernance & Risk Scoring)

- **Rôle :** Calcule les scores de risque cumulés en croisant le schéma privé (criticité `entreprise:CriticalAsset`) et les données publiques (score CVSS / vecteur de menace MITRE).
    

## 4. Interfaces Human-In-The-Loop (`04-Code/ui/`)

### 4.1 `hitl_dashboard.py` (Tableau de Bord des Zones à Risques)

- **Rôle :** Application Web légère (Streamlit / FastHTML) permettant à l'expert métier / RSSI de :
    
    1. Visualiser les propositions de modification de schéma (RFC) émises par le `guard_agent.py`.
        
    2. Valider ou corriger en 1-click la création d'un nouveau terme ou d'une relation.
        
    3. Déclencher automatiquement le commit Git et la re-compilation du socle `.ttl`.
        
- **Dépendances Python :** `streamlit` (ou `fasthtml`), `requests`, `gitpython`
    

## 📊 Matrice des Flux entre Composants

| **Source**                | **Composant Émetteur** | **Composant Destinataire**  | **Type de Données / Protocole**    |
| ------------------------- | ---------------------- | --------------------------- | ---------------------------------- |
| `00-Projet/LEXIQUE_*.md`  | `md_to_skos.py`        | `lexique_skos.ttl`          | Fichier RDF Turtle                 |
| `02-Donnees/Phase0/*.ttl` | `ontology_guard.py`    | `hitl_dashboard.py` / CI-CD | Rapport de Validation SHACL (JSON) |
| `02-Donnees/Phase0/*.ttl` | `neo4j_loader.py`      | Neo4j (via n10s)            | Import SPARQL / HTTP REST          |
| User / Prompt NL          | `supervising_agent.py` | `align_agent.py`            | Prompt en Langage Naturel          |
| `align_agent.py`          | Neo4j Cypher           | `rag_agent.py`              | Termes canoniques normalisés       |
| `guard_agent.py`          | `hitl_dashboard.py`    | Expert Métier (HITL)        | RFC JSON (Proposition de patch)    |