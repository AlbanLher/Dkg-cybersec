RepresentationDesPrincipesDKG

| **Zone / Couche**                         | **Couleur Mermaid**          | **Signification**                                      |
| ----------------------------------------- | ---------------------------- | ------------------------------------------------------ |
| **0. Humain / HITL / RSSI**               | `#fff3e0` (Orange/Ambre)     | Expertise, validation humaine, arbitrage zones grises. |
| **1. Référentiel Publique / Communs**     | `#e1f5fe` (Bleu clair)       | Données publiques, standards (CVE, MITRE, W3C, SKOS).  |
| **2. Référentiel Confidentiel / Interne** | `#f3e5f5` (Violet clair)     | Données métier, topologie privée, souveraineté.        |
| **3. Socle Modèle & Apprentissage**       | `#e8f5e9` (Vert clair)       | Ontologie, Lexiques, Fine-tuning, Embeddings, Graph.   |
| **4. Système Agentique**                  | `#ffebee` (Rouge/Rose clair) | Agents autonomes, détection, orchestration.            |


### Schéma 1 : Gouvernance du Referentiel (Guard, HITL & Zones à Risques)

**Message clé pour les décideurs :** _"L'IA ne dérive pas seule. L'expert métier conserve le contrôle total sur le socle de connaissances via un tableau de bord des zones à risques."_

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


### Schéma 2 : Boucle Dynamique d'Apprentissage & Pertinence (Embedding / NER)

**Message clé pour les équipe techniques/IA :** _"L'ontologie et les lexiques alimentent en continu les composants IA. Quand le métier évolue, ré-entraîner / ré-indexer garantit la précision."_

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

    subgraph AGENTS ["🧠 Agents en Execution"]
        RAG["Agent GraphRAG<br/>Compréhension Prompts"]
    end

    subgraph FEEDBACK ["🔄 Boucle de Maintien en Condition Operationnelle"]
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



### Schéma 3 : Ecosystème d'Agents & Détection des "Zones Grises"

**Message clé pour le management :** _"Les agents gèrent l'essentiel de la valeur ajoutée en autonomie, mais savent lever la main dès qu'une zone grise (source de futurs incidents) est détectée."_


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

### Schéma 4 : Étancheité & Hybridation (Savoir Public vs. Secret Privé)

**Message clé pour la SSI / Sécurité des données :** _"Nous bénéficions de la puissance des standards publics sans jamais compromettre nos données sensibles."_

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
