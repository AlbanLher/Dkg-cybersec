# 🎯 Mémoire / Use Case Phase 5 - Inférence Sémantique & Agent MITM de Gouvernance

**Classification :** `TLP:RED` (Confidentiel SI / Inférences Interne)  
**Domaine :** Reasoning Engine, SHACL Rules & Vector Alignment  
**Environnement :** Air-Gapped / Offline Local IA

---

## 📖 Glossaire & Table des Acronymes Métier

| Acronyme | Nom Complet | Rôle & Définition dans le Knowledge Graph DKG |
| :--- | :--- | :--- |
| **APT** | Advanced Persistent Threat | Groupe d'attaquants qualifiés. Rattaché au concept `dkg:ThreatActor` dans la TBox. |
| **MITM** | Man-In-The-Middle Agent | Composant de contrôle intermédiaire validant l'alignement vectoriel des concepts extraits avant fusion. |
| **RBox** | Relationship Box | Partie de la TBox définissant la logique des relations et règles de déduction. |
| **SHACL** | Shapes Constraint Language | Standard W3C utilisé pour la validation structurelle et l'exécution des règles d'inférence (Advanced Features). |
| **TLP** | Traffic Light Protocol | Séparation stricte des données (`TLP:CLEAR` CTI Externe vs `TLP:RED` Inférences SI). |

---

## 📌 Contextualisation & Objectif Métier

Après l'ingestion des données SI internes (Phase 2) et de la CTI externe (Phases 3 & 4), la **Phase 5** réalise la synthèse globale du Knowledge Graph :

1. **Raisonnement Cross-Domain :** Intersecter les composants internes vulnérables (`TLP:RED`) avec les menaces CTI externes (`TLP:CLEAR`) via des règles SPARQL CONSTRUCT / SHACL Rules.
2. **Gouvernance MITM Air-Gapped :** Intercepter toute tentative d'extension du graphe grâce à un modèle d'embeddings local (`sentence-transformers/all-MiniLM-L6-v2`) afin de prévenir la pollution ontologique.

---

## 🏗️ Architecture du Pipeline d'Inférence & Agent MITM

```mermaid
flowchart TD
    subgraph Inputs [Graphes Unifiés]
        A1[ABox Interne TLP:RED]
        A2[ABox CTI Externe TLP:CLEAR]
        T1[TBox Master TLP:AMBER]
    end

    subgraph MITM [Agent MITM - Alignement Local]
        AGENT[mitm_agent.py]
        EMB[Modèle Embeddings Offline]
        THRES{Similarité >= 0.85?}
    end

    subgraph Engine [Phase 5 - Moteur pySHACL]
        RULES[DKG_Rules_Master.ttl]
        PYSHACL[pySHACL Advanced]
    end

    subgraph Output [Master Inferred]
        OUT_TTL[DKG_ABox_Infered.ttl]
        OUT_MD[DOC_SYNTHESE_ABOX_INFERED.md]
    end

    A1 --> AGENT
    A2 --> AGENT
    T1 --> AGENT
    AGENT --> EMB
    EMB --> THRES
    THRES -->|ACCEPTED| PYSHACL
    THRES -->|PROPOSE_EXTENSION| REJECT[Validation Humaine / Ticket Socle]
    RULES --> PYSHACL
    PYSHACL --> OUT_TTL
    OUT_TTL --> OUT_MD
````

## 🔗 Topology Network Graph (Graphe Enrichi par Inférence)

Exemple de triplet déduit automatiquement par le moteur d'inférence en Phase 5 :

Extrait de code

```
graph LR
    subgraph TLP_RED [Périmètre SI Interne - Confidentialité Haute]
        ASSET[data:Asset-Srv-Prod] -->|dkg:hasInstalledComponent| COMP[data:Comp-Log4j]
    end

    subgraph TLP_CLEAR [Périmètre CTI Externe]
        CVE[cti:CVE-2024-21887] -->|dkg:exploitedBy| APT[cti:ThreatActor-APT29]
    end

    subgraph INFERRED [Triplets Déduits - Phase 5]
        COMP -.->|dkg:hasVulnerability| CVE
        ASSET ==>|dkg:isExposedToThreat| APT
    end

    style INFERRED fill:#ffffcc,stroke:#ff9900,stroke-width:2px
```

## 🔍 Requête SPARQL d'Audit des Inférences Multi-Hop

Cette requête extrait les attaques ou expositions nouvellement déduites lors de la Phase 5 :

Extrait de code

```
PREFIX dkg:  [http://dkg.cybersec.org/tbox#](http://dkg.cybersec.org/tbox#)
PREFIX data: [http://dkg.cybersec.org/data#](http://dkg.cybersec.org/data#)
PREFIX cti:  [http://dkg.cybersec.org/cti#](http://dkg.cybersec.org/cti#)

SELECT ?asset ?component ?cve ?threatActor WHERE {
    ?asset a dkg:Asset ;
           dkg:hasInstalledComponent ?component ;
           dkg:isExposedToThreat ?threatActor .
           
    ?component dkg:hasVulnerability ?cve .
    ?threatActor a dkg:ThreatActor .
}
ORDER BY ?asset
```

## 🛡️ RÈGLES DE GOUVERNANCE & SÉCURITÉ

1. **Confidentialité TLP:RED :** Le graphe résolvant l'exposition réelle du SI (`DKG_ABox_Infered.ttl`) est strictement restreint au périmètre `TLP:RED`.
    
2. **Exécution Air-Gapped :** L'agent MITM et le moteur pySHACL s'exécutent entièrement hors-ligne sans aucun appel API externe.
    
3. **Contrôle d'Extension de Schéma :** Seules les entités obtenant un score de similarité vectorielle $\ge 0.85$ avec les concepts TBox existants sont automatiquement intégrées.