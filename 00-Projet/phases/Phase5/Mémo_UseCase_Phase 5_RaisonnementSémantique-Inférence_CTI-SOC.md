# 📖 Complément Memo_UseCase — Phase 5 : Alignement, Superposition & Raisonnement Sémantique

**Classification :** `TLP:AMBER` (Libre usage interne)

**Public Cible :** Métier, RSSI, Chefs de Projet, Décideurs non-techniques

**Objet :** Explication fonctionnelle des principes de superposition de graphes, de l'alignement IA (MITM) et de la chaîne d'exécution de la Phase 5.

## 🎯 Message Clé pour la Direction & les Métiers

> **Cette présentation constitue la vision fonctionnelle cible de notre application.**
> 
> Elle démontre comment le Knowledge Graph transforme des données fragmentées, hétérogènes et cloisonnées en une **intelligence décisionnelle unifiée, automatisée et explicable**.

## 1. Le Principe de Superposition de Graphes (Graph Overlay)

### 💡 Le Concept Expliqué Simplement

Imaginez que vous superposez des **calques transparents** sur une carte géographique :

1. **Calque 1 (ABox Interne - TLP:RED) :** La carte de vos équipements SI (serveurs, bases de données, liens réseau).
    
2. **Calque 2 (ABox CTI - TLP:CLEAR) :** Les renseignements sur la menace cyber mondiale (vulnérabilités CISA KEV, groupes d'attaquants APT).
    
3. **Calque 3 (TBox Master & SKOS - TLP:AMBER) :** Le dictionnaire des concepts métier, du thésaurus et des règles de sécurité.
    

Pris isolément, chaque calque est incomplet. En les **superposant**, le système fait apparaître des connexions invisibles à l'œil humain et matérialise instantanément de nouveaux risques.

### 🖼️ Illustration Visuelle de la Superposition

Extrait de code

```mermaid
graph TD
    classDef red fill:#ffcccc,stroke:#ff0000,stroke-width:2px;
    classDef clear fill:#e6f2ff,stroke:#0066cc,stroke-width:2px;
    classDef amber fill:#fff2cc,stroke:#d6b656,stroke-width:2px;
    classDef infered fill:#d5e8d4,stroke:#82b366,stroke-width:3px,stroke-dasharray: 5 5;

    subgraph Calque_1 ["🔴 Calque SI Interne (TLP:RED)"]
        SRV["Serveur_Pivot_01"]:::red
        DB[("Database_Critical_01")]:::red
        SRV -->|connectsTo| DB
    end

    subgraph Calque_2 ["🔵 Calque CTI Externe (TLP:CLEAR)"]
        CVE["CVE-2024-21887"]:::clear
        KEV["isCisaKev = True"]:::clear
        CVE --- KEV
    end

    subgraph Calque_3 ["🟡 Calque Modèle & Règles (TLP:AMBER)"]
        R1["Règle R-01 : Alerte KEV"]:::amber
        R2["Règle R-02 : Silent Cascade"]:::amber
    end

    %% Superposition
    SRV -.->|hasVulnerability| CVE

    subgraph Calque_Inference ["🟢 Résultat Déduit (Inférence Sémantique)"]
        HIGH_RISK["dkg:HighRiskAsset"]:::infered
        CASCADE["dkg:exposesToCascade"]:::infered
    end

    SRV ==>|R-01 Déduit| HIGH_RISK
    SRV ==>|R-02 Déduit| CASCADE
    CASCADE ==> DB
```

## 2. Le Rapprochement Sémantique par Modèle IA (Agent MITM)

### 💡 Pourquoi un Modèle IA ?

Dans les systèmes informatiques, une même réalité est souvent nommée de manières différentes par divers outils ou équipes :

- L'équipe Réseau écrit : `"Serveur Controleur de Domaine Active Directory"`
    
- L'équipe CTI / Analystes écrit : `"Serveur Contrôleur AD"`
    

Pour un ordinateur classique, ces deux chaînes de caractères sont **différentes**.

### 🤖 Quel Modèle & Quel Rôle ?

Nous intégrons un modèle de Traitement Automatique du Langage (NLP) local et souverain : **`all-MiniLM-L6-v2`** (via la bibliothèque _SentenceTransformers_).

- **Son Rôle :** Il transforme chaque libellé texte en une **empreinte numérique (vectorisation)**. Il calcule ensuite la **distance sémantique** (similarité cosinus) entre l'entité candidate et l'annuaire existant.
    
- **Le Seuil de Décision (`0.85`) :**
    
    - **Si le score est $\ge 0.85$ :** Le modèle conclut qu'il s'agit du même élément. Le système crée automatiquement une équivalence sémantique officielle (`skos:exactMatch` / `owl:sameAs`).
        
    - **Si le score est $< 0.85$ :** Le système conserve l'entité comme indépendante pour éviter toute fausse fusion.
        

### 🖼️ Fonctionnement de la Réconciliation Sémantique

Extrait de code

```mermaid
flowchart LR
    classDef input fill:#e1d5e7,stroke:#9673a6,stroke-width:2px;
    classDef ai fill:#dae8fc,stroke:#6c8ebf,stroke-width:2px;
    classDef match fill:#d5e8d4,stroke:#82b366,stroke-width:2px;
    classDef reject fill:#f8cecc,stroke:#b85450,stroke-width:2px;

    TXT["Candidat : 'Serveur Contrôleur AD'"]:::input --> VECT["Embedding Vectoriel (MiniLM)"]:::ai
    VECT --> COS{"Similarité Cosinus avec la Base<br/>(ex: 'Serveur Controleur Active Directory')"}:::ai
    
    COS -->|Score >= 0.85<br/>ex: 0.94| MATCH["✅ MATCH VALIDÉ<br/>Génération de :<br/>- skos:exactMatch<br/>- owl:sameAs"]:::match
    COS -->|Score < 0.85<br/>ex: 0.42| REJECT["❌ SEUIL NON ATTEINT<br/>Entité conservée séparée"]:::reject
```

## 3. Le Pipeline d'Exécution Complet

Le pipeline de la Phase 5 s'exécute selon une chaîne industrielle rigoureuse, garantissant la **traçabilité**, la **reproductibilité (Principe de Replay)** et la **non-pollution des données**.

Extrait de code

```mermaid
sequenceDiagram
    autonumber
    actor Admin as 👤 Administrateur / Pipeline
    participant MITM as 🤖 Agent MITM (Phase5/mitm_agent.py)
    participant SKOS as 📐 Consolidateur (Phase5/skos_consolidator.py)
    participant REASON as ⚙️ Reasoning Engine (Phase5/reasoning_engine.py)
    participant INF as 🛡️ Pipeline Global (generate_phase5_inference.py)
    participant TBOX as 🗄️ TBox Master (TLP:AMBER)
    participant ABOX as 🗄️ ABox Infered (TLP:RED)

    Admin->>MITM: 1. Lancer l'interception et l'alignement IA
    MITM->>MITM: Calcul similarité MiniLM (Seuil 0.85)
    MITM-->>SKOS: Produit DKG_MITM_Alignment.ttl

    Admin->>SKOS: 2. Lancer la consolidation SKOS
    SKOS->>TBOX: Injecte skos:exactMatch / owl:sameAs dans DKG_TBox_Master.ttl
    SKOS-->>Admin: Génère la documentation TBox Master (.md)

    Admin->>REASON: 3. Lancer le moteur de règles
    REASON->>REASON: Applique R-01 (CISA KEV) & R-02 (Silent Cascade)
    REASON->>ABOX: Écrit les faits déduits dans DKG_ABox_Infered.ttl
    REASON-->>Admin: Génère la documentation ABox Infered (.md)

    Admin->>INF: 4. Lancer la validation SHACL globale
    INF->>INF: Valide la conformité du graphe unifié
    INF-->>Admin: Rapport SHACL PASS & Livrables finaux
```

## 4. Synthèse des Valeurs Ajoutées Métier

|**Composant**|**Rôle Métier**|**Bénéfice Direct**|
|---|---|---|
|**Superposition**|Fusionner le SI Interne et la CTI Externe.|Détection de vulnérabilités critiques contextuelles sans modifier la base SI source.|
|**Agent MITM (IA)**|Réconcilier les synonymes et variantes de noms.|Suppression des doublons et alignement automatique des vocabulaires inter-équipes.|
|**Thésaurus SKOS**|Structurer le vocabulaire métier unifié.|Garantie que la TBox Master reste la source unique de vérité (`SSOT`).|
|**Reasoning Engine**|Déduire les risques cachés (Cascade).|Identification des chemins d'attaque menaçant les bases de données critiques.|
|**Auto-Documentation**|Générer un miroir Markdown (`.md`) pour chaque `.ttl`.|Auditabilité complète et explicabilité des décisions pour les équipes de direction.|