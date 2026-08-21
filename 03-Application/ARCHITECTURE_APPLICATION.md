RepresentationDesPrincipesDKG
# 🏗️ Architecture Applicative & Principes Directeur du DKG Cyber

Ce document présente la vision globale de l'application **Cyber DKG (Dynamic Knowledge Graph)**. Il s'appuie sur quatre diagrammes de principes clés pour rendre l'architecture compréhensible et faciliter l'adoption du système par l'ensemble des parties prenantes (experts métier, RSSI, développeurs et analystes).

## 🎨 Charte Graphique des Schémas

Afin d'éviter la saturation visuelle et de faciliter la lecture rapide (notamment dans Obsidian), tous les schémas respectent la même charte de couleurs :

- **🟧 Orange / Ambre (`#fff3e0`) :** Couche Humain / HITL / RSSI (Arbitrage, validation, décision).
    
- **🟦 Bleu clair (`#e1f5fe`) :** Données publiques & Communs (CVE, MITRE, standards W3C).
    
- **🟪 Violet clair (`#f3e5f5`) :** Données confidentielles & Topologie interne entreprise.
    
- **🟩 Vert clair (`#e8f5e9`) :** Socle de connaissances (Ontologie, Lexiques, Graph Neo4j, Modèles).
    
- **🟥 Rose / Rouge (`#ffebee`) :** Système agentique & Détection dynamique.
    

## 1. Gouvernance du Référentiel & Contrôle Humain (HITL)

### Principe Pédagogique

> **« L'Intelligence Artificielle propose, l'humain valide. »**

L'IA et les agents automatisés ne modifient **jamais** directement le graphe de connaissances en autonomie totale. L'Agent Gardien (_Guard_) intercepte toutes les entrées et dérives de schéma. S'il détecte une incohérence, il émet un rapport d'alerte vers un tableau de bord consulté par l'expert métier. Seule l'action explicite de l'humain valide l'évolution de l'ontologie.

Extrait de code

```mermaid
flowchart TD
    subgraph PUB ["🌐 Communs & Référentiels Publics"]
        NVD["Base CVE / NVD"]
        MITRE["MITRE ATT&CK"]
    end

    subgraph PRIV ["🔒 Périmètre Confidentiel Entreprise"]
        ASSETS["Inventaire Parc & IP"]
        DEPT["Cartographie Métier"]
    end

    subgraph SOCLE ["📐 Socle DKG (Neo4j)"]
        ONTO["Ontologie & Lexiques (.ttl)"]
    end

    subgraph GUARD ["🛡️ Agent Gardien (Guard)"]
        DRIFT["Détecteur d'Incohérences & Dérives"]
    end

    subgraph HITL ["👨‍💻 Expert Métier / RSSI (Human-in-the-Loop)"]
        DASH["Tableau de Bord des Zones à Risques"]
        VAL["Validation & Arbitrage (1-Click)"]
    end

    %% Flux
    PUB -->|Flux Standards| DRIFT
    PRIV -->|Flux Internes| DRIFT
    ONTO -->|Schéma OWL/SKOS| DRIFT

    DRIFT -->|Données Conformes| ONTO
    DRIFT -->|Incohérences & Zones Grises| DASH
    
    DASH --> VAL
    VAL -->|Mise à jour Validée| ONTO

    style PUB fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    style PRIV fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    style SOCLE fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px
    style GUARD fill:#ffebee,stroke:#c62828,stroke-width:2px
    style HITL fill:#fff3e0,stroke:#e65100,stroke-width:2px
```

## 2. Boucle Dynamique d'Apprentissage & Pertinence

### Principe Pédagogique

> **« Le socle formel pilote la précision du LLM et des modèles d'extraction. »**

L'ontologie OWL et les lexiques SKOS servent de référence pour la vectorisation (_embeddings_) et l'extraction d'entités (_NER_). En cas de baisse de pertinence ou d'évolution du vocabulaire de l'entreprise, une ré-indexation ou un ré-apprentissage est déclenché pour maintenir un niveau de précision optimal.

Extrait de code

```mermaid
flowchart TD
    subgraph KNOWLEDGE ["📚 Socle de Connaissances"]
        SKOS["Lexiques SKOS<br/>(Acronymes & Jargon)"]
        OWL["Ontologie OWL<br/>(Relations & Typologie)"]
    end

    subgraph AI_PREP ["⚙️ Alignement IA & Vectorisation"]
        NER["Extraction d'Entités (NER)<br/>Alignée SKOS"]
        EMBED["Embeddings Hybrides<br/>(Graphe + Texte)"]
    end

    subgraph AGENTS ["🧠 Agents en Exécution"]
        RAG["Agent GraphRAG<br/>Compréhension Prompts"]
    end

    subgraph FEEDBACK ["🔄 Boucle de Maintien en Condition Opérationnelle"]
        EVAL["Mesure de Pertinence<br/>(Taux de Réponse Exacte)"]
        RELEARN["Trigger Ré-apprentissage /<br/>Ré-indexation Vectorielle"]
    end

    SKOS -->|Synonymes & Libellés| NER
    OWL -->|Structure & Contextes| EMBED

    NER --> RAG
    EMBED --> RAG

    RAG --> EVAL
    EVAL -->|Chute de Pertinence| RELEARN
    RELEARN -->|Mise à jour Index/Fine-tuning| AI_PREP

    style KNOWLEDGE fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px
    style AI_PREP fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    style AGENTS fill:#ffebee,stroke:#c62828,stroke-width:2px
    style FEEDBACK fill:#fff3e0,stroke:#e65100,stroke-width:2px
```

## 3. Écosystème d'Agents & Traitement des Zones Grises

### Principe Pédagogique

> **« L'autonomie à 90%, l'escalade intelligente sur les 10% d'incertitude. »**

Les agents spécialisés (Alignement, GraphRAG, Gouvernance) traitent automatiquement l'immense majorité des requêtes à forte valeur ajoutée. Dès qu'une "zone grise" est détectée (ex. un serveur sans propriétaire identifié ou un acronyme ambigu), le système génère une alerte qualifiée plutôt que d'émettre une réponse fausse ou incertaine.

Extrait de code

```mermaid
flowchart TD
    subgraph USER ["👤 Utilisateur / RSSI / Analyste"]
        PROMPT["Requête / Ingestion de Données"]
    end

    subgraph ROUTER ["🧠 Agent Orchestrateur / Routeur"]
        DISPATCH["Analyse d'Intention & Aiguillage"]
    end

    subgraph AUTO_AGENTS ["🤖 Agents Autonomes (Valeur Ajoutée 90%)"]
        AG_ALIGN["<b>Agent Lexique</b><br/>Traduction Jargon"]
        AG_RAG["<b>Agent GraphRAG</b><br/>Enquête Multi-Sauts"]
        AG_GOV["<b>Agent Conformité</b><br/>Score de Risque"]
    end

    subgraph GREY_ZONE ["⚠️ Détection des Zones Grises"]
        UNCERTAIN["Incohérence Détectée<br/>(ex: Équipement sans proprio / Vulnérabilité orpheline)"]
    end

    subgraph HITL ["👨‍💻 Expert Métier"]
        ARBITRAGE["Arbitrage & Traitement Incident"]
    end

    PROMPT --> DISPATCH
    DISPATCH --> AG_ALIGN
    DISPATCH --> AG_RAG
    DISPATCH --> AG_GOV

    AG_ALIGN -->|Zone Grise| UNCERTAIN
    AG_RAG -->|Zone Grise| UNCERTAIN
    AG_GOV -->|Zone Grise| UNCERTAIN

    UNCERTAIN -->|Alerte Qualifiée| ARBITRAGE

    style USER fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    style ROUTER fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    style AUTO_AGENTS fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px
    style GREY_ZONE fill:#ffebee,stroke:#c62828,stroke-width:2px
    style HITL fill:#fff3e0,stroke:#e65100,stroke-width:2px
```

## 4. Hybridation Public / Privé & Souveraineté des Données

### Principe Pédagogique

> **« Réutiliser les communs publics sans exposer les secrets internes. »**

Le système enrichit les connaissances internes grâce aux bases publiques (CVE, MITRE ATT&CK, ontologies W3C) à travers une passerelle cloisonnée. Les secrets d'entreprise (IPs internes, criticités des composants, noms de serveurs) restent hébergés dans le domaine privé sans risque de fuite vers l'extérieur.

Extrait de code

```mermaid
flowchart TD
    subgraph EXT ["🌐 MONDE PUBLIC (Référentiels Communs)"]
        W3C["Standards W3C (RDF/SKOS/OWL)"]
        CVE_DB["Base NVD (CVE / CVSS)"]
        ATTACK["MITRE ATT&CK Matrix"]
    end

    subgraph BARRIER ["🛡️ Cloisonnement & Masquage (Passerelle Souveraine)"]
        ENRICH["Module d'Enrichissement Sécurisé"]
    end

    subgraph INT ["🔒 MONDE PRIVÉ (Secret d'Entreprise)"]
        ONTO_PRIV["Ontologie Privée (`entreprise:`)"]
        KG_PRIV[("DKG Interne Neo4j<br/>Topologie, IP, Applicatifs, Criticité")]
    end

    %% Relations
    EXT -->|Importation / Alignment| ENRICH
    ENRICH -->|Hybridation sans fuite de données| KG_PRIV
    ONTO_PRIV -->|Règles de Confidentialité| KG_PRIV

    style EXT fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    style BARRIER fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style INT fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
```